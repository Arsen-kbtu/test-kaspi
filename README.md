# Тестовое задание: Парсер Kaspi магазина  
## 📌 Описание проекта 
- Программа парсит данные товара с сайта Kaspi, а именно название товара, его категорию, рейтинг, количество отзывов, минимальную и максимальную цены
- Данные о товаре сохраняются в виде Json, а также в PostgreSQL
- Дополнительно разработана возможность парсинга предложений по товару и сохранению данных в offers.jsonl, парсинг характеристик товара, количества продавцов и ссылок на фотографии
- ## 🚀 Установка и запуск  

### 1. Клонирование репозитория  
git clone https://github.com/Arsen-kbtu/test-kaspi.git  
cd test-kaspi  

### 2. Установка зависимостей  
pip install -r reqs.txt  

### 3. Настройка окружения  
Создайте файл `.env` и укажите:  
DB_HOST=localhost  
DB_PORT=5432  
DB_NAME=kaspi  
DB_USER=postgres  
DB_PASSWORD=postgres  

### 4. Запуск парсера 
python -m app.main

## 🗄️ PostgreSQL 
**products**  
- id  
- name  
- categories  
- rating  
- reviews_count  
- min_price  
- max_price
- images
- specifications

Для offers таблица отсутствует

## 🗄️ Docker
Есть возможность запустить Postgre внутри контейнера

docker-compose up

После чего замените порт в .env на 5433

## 📝 Пример логов  
Логи можно увидеть в app/export/parser.log

## ✅ Что сделано  
- [x] Парсинг товара  
- [x] Сохранение в PostgreSQL  
- [x] Экспорт в JSON  
- [x] Логирование  
- [x] Docker  
- [x] Расширенный сбор
- [x] Pydantic

## 📄 Дополнительно  
Python 3.11

Решил не создавать Докерфайл, будет занимать много времени для тестирования ссылок
