from abc import ABC, abstractmethod
from typing import Any, Dict

class PipelineStep(ABC):
    @abstractmethod
    def execute(self, context: Any) -> None:
        pass

class BaseMF(ABC):
    @abstractmethod
    def fit(self, data: Any) -> None:
        pass

    @abstractmethod
    def predict(self, user_id: int, item_id: int) -> float:
        pass

class BaseClusterer(ABC):
    @abstractmethod
    def fit(self, embeddings: Any) -> None:
        pass

    @abstractmethod
    def assign(self, user_embedding: Any) -> int:
        pass

class BaseRanker(ABC):
    @abstractmethod
    def fit(self, data: Any) -> None:
        pass

    @abstractmethod
    def predict(self, features: Any) -> float:
        pass

class BaseDriftDetector(ABC):
    @abstractmethod
    def detect(self, actual: Any, expected: Any) -> Dict[str, Any]:
        pass

class BaseDecisionStrategy(ABC):
    @abstractmethod
    def decide(self, impact: Any) -> str:
        pass

class BaseEvaluator(ABC):
    @abstractmethod
    def evaluate(self) -> Dict[str, float]:
        pass
