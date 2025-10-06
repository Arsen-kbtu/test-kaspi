from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional

class SeedData(BaseModel):
    """Входные данные для парсера."""
    url: HttpUrl


class ProductInfo(BaseModel):
    """Результат парсинга страницы товара."""
    name: str = Field(..., description="Название товара")
    categories: List[str] = Field(default_factory=list, description="Категории товара")
    rating: Optional[float] = Field(None, description="Средний рейтинг товара (0-5)")
    reviews_count: Optional[int] = Field(None, description="Количество отзывов")
    min_price: Optional[int] = Field(None, description="Минимальная цена в тенге")
    max_price: Optional[int] = Field(None, description="Максимальная цена в тенге")
    images: Optional[List[str]] = None