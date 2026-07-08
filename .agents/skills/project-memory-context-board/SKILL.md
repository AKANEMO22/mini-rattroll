---
name: project-memory-context-board
description: Duy trì hiểu biết sâu và nhất quán về một codebase lớn xuyên suốt phiên làm việc dài, đồng thời giữ context nạp vào LLM luôn dưới ngưỡng an toàn. PHẢI dùng skill này ngay khi agent bắt đầu làm việc trên một project nhiều file/nhiều hàm phụ thuộc lẫn nhau, khi cuộc hội thoại vượt quá vài lượt sửa code, khi có dấu hiệu agent sắp phải đọc lại nhiều file cùng lúc, hoặc khi agent chuẩn bị sửa một hàm/module đã từng được fix trước đó trong phiên. Dùng skill này cho MỌI hành động: bắt đầu task, sau mỗi lần sửa file thành công, sau mỗi lần sửa thất bại, trước khi đọc file mới, và khi ngữ cảnh hội thoại bắt đầu dài (nhiều lượt, nhiều file đã đọc). Không đợi người dùng nhắc mới áp dụng.
---

# Project Memory & Context Board

## 1. Vấn đề skill này giải quyết

Một AI coding agent chạy trong IDE trên một project lớn gặp hai lỗi đối nghịch nhau nếu không có kiến trúc bộ nhớ đúng:

- **Nạp quá tải (context overflow):** càng chat lâu, càng đọc nhiều file, cửa sổ ngữ cảnh càng đầy → agent buộc phải cắt bớt lịch sử, và thường cắt nhầm phần quan trọng (mục tiêu gốc, các ràng buộc đã thống nhất).
- **Hiểu nông dần theo thời gian (context rot):** thay vì "càng chat càng hiểu sâu project", agent thực chất càng chat càng quên — vì hiểu biết bị lưu trong lịch sử hội thoại thô, một dạng bộ nhớ không có cấu trúc, dễ bị nén/cắt mất.

Nguyên tắc cốt lõi của skill: **không lưu hiểu biết trong lịch sử chat. Lưu hiểu biết trong một trạng thái có cấu trúc, bên ngoài hội thoại, được cập nhật bởi hệ thống (không phải do LLM "nhớ" phải cập nhật).** Lịch sử hội thoại chỉ là log tạm thời, có thể bỏ gần hết bất cứ lúc nào mà không mất thông tin quan trọng, vì thông tin quan trọng đã được chuyển hoá thành state.

Nếu tại bất kỳ thời điểm nào một hành động "giữ hiểu biết" chỉ tồn tại dưới dạng "LLM nhớ phải làm việc đó" — đó là một lỗ hổng thiết kế. Trách nhiệm ghi nhớ phải thuộc về code/harness của IDE, không thuộc về suy luận của model.

## 2. Bốn tầng bộ nhớ (Memory Tiers)

Đừng đối xử với toàn bộ hiểu biết về project như một khối đồng nhất. Chia thành 4 tầng theo tần suất cần dùng và mức độ nén:

| Tầng | Nội dung | Luôn nạp? | Cập nhật bởi |
|---|---|---|---|
| **Tier 0 — Context Board** | Mục tiêu, trạng thái hiện tại, hàm bị khoá, bài học lỗi đã đúc kết | Luôn luôn, mọi lượt | Harness (deterministic), sau mỗi tool-call |
| **Tier 1 — Symbol Map** | Bản đồ hàm/class/module: chữ ký, mục đích 1 dòng, trạng thái, file chứa | Chỉ phần liên quan đến task hiện tại | Harness, cập nhật tăng dần khi agent đọc/sửa code |
| **Tier 2 — Nội dung file đầy đủ** | Source code thật | Chỉ khi đang thao tác trực tiếp trên file đó | Tool `read_file` theo yêu cầu của agent |
| **Tier 3 — Lịch sử hội thoại thô** | Toàn bộ diễn biến chat | Chỉ vài lượt gần nhất | Rolling summarization đẩy phần cũ ra ngoài |

Quy tắc vàng: **Tier 0 không bao giờ bị nén hay page-out. Tier 1 phình dần theo thời gian nhưng chỉ phần liên quan mới được nạp. Tier 2 luôn tạm thời. Tier 3 luôn bị nén sau N lượt.**

Đây chính là cơ chế khiến "chat càng dài thì agent càng hiểu sâu": Tier 1 (Symbol Map) chỉ tăng chứ không mất — mỗi lần agent đọc một file mới, project map dày thêm một chút, nhưng vì nó là bản đồ nén (chữ ký + mục đích, không phải full code) nên dung lượng tăng rất chậm so với việc đọc lại toàn văn.

## 3. Context Board — trạng thái tĩnh luôn ở đầu context

### 3.1 Schema

```json
{
  "original_goal": "Mô tả mục tiêu gốc của cả phiên làm việc, viết 1 lần, hiếm khi đổi",
  "current_status": {
    "active_task": "Việc đang làm ngay bây giờ",
    "last_completed_step": "Bước vừa hoàn thành thành công",
    "next_step": "Bước tiếp theo dự kiến"
  },
  "locked_functions": [
    {
      "symbol": "calculateInvoiceTotal",
      "file": "src/billing/invoice.ts",
      "reason": "Đã fix bug rounding, có test pass, KHÔNG sửa lại trừ khi được yêu cầu tường minh",
      "locked_at_turn": 14
    }
  ],
  "failed_attempts": [
    {
      "id": "fa-003",
      "pattern": "Sửa async/await trong middleware auth gây race condition",
      "lesson": "Middleware auth phải chạy tuần tự, không được Promise.all",
      "occurrences": 2,
      "last_seen_turn": 21
    }
  ],
  "open_questions": [
    "Chưa rõ có cần hỗ trợ multi-tenant cho module billing hay không"
  ]
}
```

### 3.2 Nguyên tắc cập nhật (bắt buộc, không tuỳ chọn)

- **Không giao việc cập nhật JSON này cho LLM quyết định "khi nào nên gọi tool update".** Thay vào đó, hook trực tiếp vào các sự kiện tool-call của IDE:
  - Sau khi `edit_file`/`apply_patch` chạy **thành công** và test/build pass → tự động thêm/refresh entry vào `locked_functions`, cập nhật `current_status`.
  - Sau khi một lần sửa **thất bại** (test fail, lỗi runtime, agent tự revert) → tự động ghi vào `failed_attempts`.
  - `original_goal` chỉ được sửa khi người dùng tường minh đổi yêu cầu — không bao giờ để agent tự diễn giải lại mục tiêu.
- Agent (LLM) chỉ có quyền **đề xuất nội dung** (ví dụ: tóm tắt bài học từ lỗi thành 1 câu ngắn), còn **việc entry đó có được ghi vào Context Board hay không** là do harness quyết định dựa trên tín hiệu deterministic (test pass/fail, diff có đụng vào locked_functions hay không).

### 3.3 Khử trùng lặp & hết hạn cho `failed_attempts`

Nếu không dedupe, ledger phình to và tự nó trở thành nguồn nhiễu:
- Trước khi thêm entry mới, so khớp `pattern` với các entry cũ (theo symbol/file liên quan). Nếu trùng → tăng `occurrences`, cập nhật `last_seen_turn`, không tạo entry mới.
- Một entry hết hạn (loại khỏi Context Board, có thể chuyển xuống Tier 1 dưới dạng ghi chú trong Symbol Map) khi function liên quan đã bị refactor hoàn toàn khác so với lúc lỗi xảy ra.
- Giới hạn cứng: tối đa ~15 entries trong `failed_attempts` được nạp mỗi lượt. Nếu vượt, ưu tiên theo `occurrences` giảm dần rồi tới `last_seen_turn` gần nhất.

## 4. Symbol Map — thay thế cho "đọc lại toàn bộ file"

Với project lớn, đừng chunk theo heading Markdown cho *code* (chỉ dùng cách đó cho tài liệu .md thực sự). Với code, xây bản đồ ký hiệu (symbol-level index), cập nhật dần bằng AST parser của IDE (không phải LLM tự đọc rồi tóm tắt bằng tay):

```json
{
  "file": "src/billing/invoice.ts",
  "symbols": [
    {
      "name": "calculateInvoiceTotal",
      "kind": "function",
      "signature": "(items: InvoiceItem[], taxRate: number) => number",
      "purpose": "Tính tổng hoá đơn có làm tròn theo quy tắc kế toán VN",
      "status": "locked",
      "depends_on": ["roundToVND"],
      "used_by": ["generateInvoicePdf", "InvoiceSummaryCard"]
    }
  ]
}
```

Quy trình nạp khi agent cần làm việc trên một vùng code:
1. Tra `used_by` / `depends_on` để biết những symbol nào **liên quan trực tiếp** — chỉ nạp full code của các symbol đó, không nạp cả file nếu file dài.
2. Với symbol không liên quan trực tiếp task hiện tại, chỉ giữ dòng `purpose` 1 câu trong context — đủ để agent không "phát minh lại" hoặc phá vỡ logic đã có, mà không tốn token đọc toàn văn.
3. Mỗi lần agent đọc/sửa một file chưa có trong Symbol Map, harness tự chạy parser AST để thêm entry — đây là cách "hiểu biết" tích luỹ dần và không bao giờ mất, kể cả khi lịch sử chat bị nén.

## 5. Rolling Summarization cho lịch sử hội thoại (Tier 3)

Chỉ áp dụng nén cho phần *diễn biến hội thoại*, không bao giờ dùng để nén Context Board hay Symbol Map.

- Sau mỗi N lượt (gợi ý N=6–10 tuỳ độ dài trung bình mỗi lượt), gộp các lượt cũ nhất thành một entry "decision log":
  ```json
  {
    "turn_range": "8-14",
    "decision": "Chuyển validate input sang middleware riêng thay vì validate trong controller",
    "rationale": "Controller đang bị trùng logic validate ở 3 route khác nhau",
    "files_touched": ["src/middleware/validate.ts", "src/routes/billing.ts"]
  }
  ```
- **Luôn giữ cặp `decision + rationale`, không chỉ `decision`.** Nếu chỉ tóm tắt "đã sửa lỗi X" mà mất lý do tại sao sửa như vậy, ở lượt sau agent rất dễ sửa lại theo hướng phá vỡ chính fix đó.
- Nếu một quyết định trong decision log liên quan trực tiếp đến một `locked_function`, giữ nguyên văn (không nén) phần rationale đó — vì đây chính là lý do function bị khoá.
- 3–5 lượt gần nhất luôn giữ nguyên văn, không tóm tắt — để agent không mất sắc thái của yêu cầu vừa rồi từ người dùng.

## 6. Ngân sách context (Context Budget) — ví dụ phân bổ

Đặt ngưỡng cứng cho mỗi tầng theo % cửa sổ ngữ cảnh khả dụng, để không bao giờ vượt giới hạn IDE agent:

| Thành phần | Ngân sách gợi ý |
|---|---|
| Context Board (Tier 0) | ~3–5% |
| Symbol Map liên quan đến task | ~10–15% |
| Decision log đã nén (Tier 3 cũ) | ~10% |
| 3–5 lượt hội thoại gần nhất (nguyên văn) | ~15–20% |
| Full code đang thao tác (Tier 2) | phần còn lại, ưu tiên cao nhất |

Khi tổng vượt ngưỡng: **cắt Tier 3 trước tiên (nén mạnh hơn hoặc bỏ decision log cũ ít liên quan), không bao giờ cắt Tier 0.** Nếu Tier 1 (Symbol Map) quá lớn do project khổng lồ, chỉ nạp symbol thuộc module đang chạm tới (dùng `depends_on`/`used_by` để giới hạn phạm vi truy vấn — giống RAG nhưng trên đồ thị ký hiệu thay vì vector similarity của Markdown heading).

## 7. Ràng buộc cứng chống sửa lại code đã fix (bổ trợ Context Board)

Context Board đánh dấu `locked_functions` chỉ là **tín hiệu ở tầng ngữ nghĩa** — vẫn nên có một lớp chặn ở tầng công cụ:

- IDE parse AST của diff mà agent định áp dụng. Nếu diff đụng vào node đã đánh dấu `locked`, chặn việc apply và trả lỗi rõ ràng cho agent kèm `reason` lấy từ Context Board.
- Agent có quyền "xin mở khoá": nếu agent giải thích lý do cần sửa (ví dụ refactor hợp lệ ảnh hưởng dây chuyền), harness cho phép mở khoá tường minh cho đúng symbol đó, ghi log lại quyết định mở khoá vào decision log — không mở khoá ngầm định.
- Giới hạn số lần agent được retry khi bị chặn (gợi ý: 2 lần) để tránh vòng lặp vô hạn cố sửa node bị khoá.

## 8. Quy trình mỗi lượt (tóm tắt vận hành)

1. Harness build context cho lượt mới: Context Board (đầy đủ) + Symbol Map (lọc theo phạm vi liên quan) + decision log gần đây + N lượt hội thoại nguyên văn + file đang mở (nếu có).
2. Agent thực hiện hành động (đọc file / sửa code / hỏi lại).
3. Harness bắt sự kiện kết quả (test pass/fail, diff có đụng locked node không, có file mới nào lần đầu được đọc không).
4. Harness tự động cập nhật Context Board và Symbol Map dựa trên sự kiện ở bước 3 — **không hỏi ý agent có muốn cập nhật hay không.**
5. Nếu tổng dung lượng context cho lượt kế tiếp vượt ngân sách (mục 6), chạy rolling summarization để nén Tier 3 trước khi build context cho lượt sau.

## 9. Những điều cần tránh

- Đừng để "cập nhật trạng thái" là một tool mà LLM có thể quên gọi — nó phải được ép chạy tự động bởi harness sau mỗi tool-call quan trọng.
- Đừng nén `locked_functions` hay `original_goal` trong bất kỳ vòng rolling summarization nào.
- Đừng dùng RAG theo heading Markdown cho code — code cần đồ thị phụ thuộc (symbol graph), không phải chunk theo đoạn văn.
- Đừng để `failed_attempts` phình vô hạn — luôn dedupe theo symbol/pattern trước khi thêm entry mới.
- Đừng khoá cứng tuyệt đối `locked_functions` — luôn có đường "xin mở khoá có lý do", nếu không agent sẽ bị kẹt ở những refactor hợp lệ.
