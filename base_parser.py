from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any


class BaseParser(ABC):
    """Абстрактный класс для парсинга постов из социальных сетей/мессенджеров."""

    @abstractmethod
    async def connect(self) -> None:
        """Установка соединения с API."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Закрытие соединения."""
        pass

    @abstractmethod
    async def parse(self, channel: str, limit: int = 100, **kwargs) -> List[Dict[str, Any]]:
        """
        Парсинг постов из указанного канала/паблика.
        Возвращает список словарей с полями: text, date, views, forwards, replies.
        """
        pass

    async def parse_and_save(self, channel: str, limit: int = 100, output_dir: str = "data") -> Path:
        """Парсит и сохраняет результат в JSON."""
        posts = await self.parse(channel, limit=limit)
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        filepath = output_dir / f"{channel}_posts.json"
        import json
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(posts)} posts to {filepath}")
        return filepath
