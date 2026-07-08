import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
import time

def run_baseline_backtest(data_dir="data/ml-25m", output_file="data/metrics_history.json"):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Bắt đầu đọc dữ liệu ratings.csv...")
    ratings_path = os.path.join(data_dir, "ratings.csv")
    
    if not os.path.exists(ratings_path):
        print(f"LỖI: Không tìm thấy file {ratings_path}")
        return
        
    # Read only required columns to save RAM
    df = pd.read_csv(ratings_path, usecols=['userId', 'movieId', 'rating', 'timestamp'])
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Đã đọc xong {len(df):,} dòng.")
    
    # Convert timestamp to datetime
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Đang xử lý thời gian (timestamp)...")
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    
    # Lấy 2 năm gần nhất để backtest nhanh hơn (2018 - 2019)
    # MovieLens 25M kết thúc vào 21/11/2019
    start_date = pd.to_datetime('2018-01-01')
    end_date = pd.to_datetime('2019-11-21')
    
    df_recent = df[(df['datetime'] >= start_date) & (df['datetime'] <= end_date)].copy()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Số lượng dòng trong chu kỳ Backtest (2018-2019): {len(df_recent):,}")
    
    # Khởi tạo mô hình Baseline
    # Baseline Model: r_ui = mu + b_u + b_i
    # Train trên dữ liệu TRƯỚC 2018
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Đang huấn luyện Baseline Model (Global Avg, User Bias, Item Bias) trên dữ liệu lịch sử...")
    df_train = df[df['datetime'] < start_date]
    mu = df_train['rating'].mean()
    
    # Calculate User Bias
    user_means = df_train.groupby('userId')['rating'].mean()
    b_u = user_means - mu
    
    # Calculate Item Bias
    item_means = df_train.groupby('movieId')['rating'].mean()
    b_i = item_means - mu
    
    # Xoá df_train để giải phóng RAM
    del df_train
    del df
    
    # Tính toán RMSE cho từng tháng trong chu kỳ Backtest
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Bắt đầu đánh giá (Backtesting) theo từng tháng...")
    df_recent['month'] = df_recent['datetime'].dt.to_period('M')
    
    history_data = []
    
    # Sắp xếp các tháng
    months = sorted(df_recent['month'].unique())
    
    for m in months:
        window_df = df_recent[df_recent['month'] == m]
        
        # Predict: r_ui = mu + b_u + b_i
        # Nếu user hoặc item không có trong tập train, bias = 0
        pred_u = window_df['userId'].map(b_u).fillna(0)
        pred_i = window_df['movieId'].map(b_i).fillna(0)
        
        predictions = mu + pred_u + pred_i
        
        # Clip predictions to [0.5, 5.0]
        predictions = np.clip(predictions, 0.5, 5.0)
        
        # Calculate RMSE
        actuals = window_df['rating']
        mse = np.mean((predictions - actuals) ** 2)
        rmse = np.sqrt(mse)
        
        # Calculate Drift Score (Mô phỏng trôi dạt dựa trên độ lệch trung bình so với mu)
        window_avg = actuals.mean()
        drift_score = abs(window_avg - mu) * 5 # Scale lên để dễ nhìn trên biểu đồ
        
        # Mock latency (phụ thuộc vào số lượng request trong tháng)
        # Giả lập tải hệ thống: càng nhiều request thì latency càng cao
        req_count = len(window_df)
        base_latency = 40.0
        latency = base_latency + (req_count / 10000) + np.random.uniform(-5, 5)
        
        month_str = str(m)
        print(f" - {month_str} | Số lượng: {req_count:5d} | RMSE: {rmse:.4f} | Latency: {latency:.1f}ms")
        
        history_data.append({
            "timestamp": month_str,
            "rmse": round(float(rmse), 4),
            "latency": round(float(latency), 1),
            "drift_score": round(float(drift_score), 4)
        })

    # Đóng gói và lưu kết quả
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    with open(output_file, 'w') as f:
        json.dump(history_data, f, indent=4)
        
    print(f"[{datetime.now().strftime('%H:%M:%S')}] HOÀN TẤT! Đã xuất Lịch sử Thực tế ra file: {output_file}")

if __name__ == "__main__":
    run_baseline_backtest()
