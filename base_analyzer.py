from abc import ABC, abstractmethod
import pandas as pd


class BaseAnalyzer(ABC):
    """Абстрактный класс для анализа социальной значимости постов."""

    @abstractmethod
    def __init__(self, json_file: str):
        self.posts = None
        self.df = None

    @abstractmethod
    def analyze(self, confidence_threshold: float = 0.5) -> pd.DataFrame:
        """Запускает классификацию/анализ постов."""
        pass

    @abstractmethod
    def get_socially_significant(self) -> pd.DataFrame:
        """Возвращает только социально значимые посты."""
        pass

    @abstractmethod
    def print_stats(self):
        """Вывод базовой статистики."""
        pass
