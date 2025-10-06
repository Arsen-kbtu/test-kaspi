import re
import json
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from app.db.schema import SeedData, ProductInfo


class KaspiParser:
    def __init__(self, headless: bool = True):
        self.headless = headless

    def parse(self, seed: SeedData) -> ProductInfo:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()
            page.goto(str(seed.url), wait_until="networkidle")

            # Закрытие выбора города
            if page.locator(".dialog__close").count() > 0:
                page.locator(".dialog__close").first.click()
                page.wait_for_timeout(300)

            # Название
            name = page.query_selector(".item__heading")
            name_text = name.inner_text().strip() if name else "Не найдено"

            # Категории
            categories = [
                el.inner_text().strip()
                for el in page.query_selector_all(".breadcrumbs__item")
            ]

            # Рейтинг и отзывы
            rating_value, reviews_count = None, None
            try:
                rating_span = page.locator(".item__rating span.rating")
                if rating_span.count() > 0:
                    cls = rating_span.get_attribute("class") or ""
                    if match := re.search(r"_(\d+)", cls):
                        rating_value = float(match.group(1)) / 10

                reviews_el = page.locator(".item__rating-link span")
                if reviews_el.count() > 0:
                    txt = reviews_el.text_content().strip()
                    if match := re.search(r"(\d+)", txt):
                        reviews_count = int(match.group(1))
            except Exception:
                pass

            # Минимальная цена
            min_price = None
            price_elements = page.locator('.sellers-table__price-cell-text:not(._installments-price)')
            if price_elements.count() > 0:
                text = price_elements.first.text_content().strip()
                min_price = int(re.sub(r"[^\d]", "", text))

            # Максимальная цена
            max_price = min_price
            while True:
                next_button = page.locator('li.pagination__el', has_text="Следующая")
                if next_button.count() == 0:
                    break
                cls = next_button.first.get_attribute("class") or ""
                if "disabled" in cls or "inactive" in cls:
                    break
                try:
                    next_button.scroll_into_view_if_needed()
                    next_button.click()
                except PlaywrightTimeout:
                    page.evaluate("(el) => el.click()", next_button.first)
                # page.wait_for_timeout(1500)
                try:
                    page.wait_for_selector('.sellers-table__price-cell-text:not(._installments-price)', timeout=5000)
                except PlaywrightTimeout:
                    break

            price_elements = page.locator('.sellers-table__price-cell-text:not(._installments-price)')
            if price_elements.count() > 0:
                text = price_elements.last.text_content().strip()
                max_price = int(re.sub(r"[^\d]", "", text))

            images = []
            image_elements = page.locator(".item__slider-thumb-pic")
            count = image_elements.count()

            for i in range(count):
                try:
                    # Получаем src или data-src атрибут изображения
                    img = image_elements.nth(i)
                    src = img.get_attribute("src") or img.get_attribute("data-src")
                    if src:
                        if not src.startswith("http"):
                            src = "https:" + src
                        images.append(src)
                except Exception as e:
                    self.logger.error(f"Ошибка при получении изображения: {e}")
            browser.close()
            # Добавляем изображения в результат
            return ProductInfo(
                name=name_text,
                categories=categories,
                rating=rating_value,
                reviews_count=reviews_count,
                min_price=min_price,
                max_price=max_price,
                images=images
            )