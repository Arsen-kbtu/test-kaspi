import json
from app.db.schema import SeedData, ProductInfo
from app.db.models import Product
from app.parser.parser import KaspiParser
from app.db.database import Base, engine, SessionLocal


def main():
    # Создаём таблицу, если нет
    Base.metadata.create_all(bind=engine)

    with open("app/seed.json", encoding="utf-8") as f:
        data = json.load(f)

    seed = SeedData(**data)
    parser = KaspiParser(headless=True)

    product = parser.parse(seed)

    # Сохраняем в БД
    db = SessionLocal()
    db_product = Product(
        name=product.name,
        categories=product.categories,
        rating=product.rating,
        reviews_count=product.reviews_count,
        min_price=product.min_price,
        max_price=product.max_price,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    db.close()

    # Сохраняем в файл
    with open("app/export/product.json", "w", encoding="utf-8") as f:
        json.dump(product.model_dump(), f, ensure_ascii=False, indent=2)

    print(json.dumps(product.model_dump(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
