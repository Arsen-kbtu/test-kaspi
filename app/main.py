import json
from app.db.models import SeedData
from app.parser.parser import KaspiParser

def main():
    with open("app/seed.json", encoding="utf-8") as f:
        data = json.load(f)

    seed = SeedData(**data)
    parser = KaspiParser(headless=True)

    product = parser.parse(seed)
    with open("app/export/product.json", "w", encoding="utf-8") as f:
        json.dump(product.model_dump(), f, ensure_ascii=False, indent=2)
    print(json.dumps(product.model_dump(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()