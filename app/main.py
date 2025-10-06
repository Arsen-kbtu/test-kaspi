import json
import os
import logging
from app.db.schema import SeedData, ProductInfo
from app.db.models import Product
from app.parser.parser import KaspiParser
from app.db.database import Base, engine, SessionLocal


def setup_logger():
    # Создаем директорию export, если отсутствует
    os.makedirs("app/export", exist_ok=True)

    # Настраиваем логгер
    logger = logging.getLogger("kaspi_parser")
    logger.setLevel(logging.INFO)

    # Форматирование лога
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Запись в файл
    file_handler = logging.FileHandler("app/export/parser.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Вывод в консоль
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Добавляем обработчики
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def main():
    # Инициализация логгера
    logger = setup_logger()
    logger.info("Запуск парсера Kaspi")

    try:
        # Создаём таблицу, если нет
        logger.info("Инициализация базы данных")
        Base.metadata.create_all(bind=engine)

        logger.info("Чтение seed.json файла")
        with open("app/seed.json", encoding="utf-8") as f:
            data = json.load(f)

        seed = SeedData(**data)
        logger.info(f"Парсинг URL: {seed.url}")
        parser = KaspiParser(headless=True)

        logger.info("Запуск процесса парсинга")
        product = parser.parse(seed)
        logger.info(f"Получены данные о товаре: {product.name}")

        # Сохраняем в БД
        logger.info("Сохранение в базу данных")
        db = SessionLocal()
        db_product = Product(
            name=product.name,
            categories=product.categories,
            rating=product.rating,
            reviews_count=product.reviews_count,
            offers_count=product.offers_count,
            min_price=product.min_price,
            max_price=product.max_price,
            images=product.images,
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        db.close()
        logger.info("Данные успешно сохранены в БД")

        # Сохраняем в файл
        logger.info("Сохранение данных в JSON")
        with open("app/export/product.json", "w", encoding="utf-8") as f:
            json.dump(product.model_dump(), f, ensure_ascii=False, indent=2)
        logger.info("Данные сохранены в файл app/export/product.json")

        print(json.dumps(product.model_dump(), indent=2, ensure_ascii=False))
        logger.info("Работа парсера завершена успешно")

    except Exception as e:
        logger.error(f"Ошибка выполнения: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()