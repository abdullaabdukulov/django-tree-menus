# Django Tree Menus

![python](https://img.shields.io/badge/-python-grey?style=for-the-badge&logo=python&logoColor=white&labelColor=306998)
![django](https://img.shields.io/badge/-django-grey?style=for-the-badge&logo=django&logoColor=white&labelColor=092e20)
![postgresql](https://img.shields.io/badge/postgre-SQL-%23000.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![linux](https://img.shields.io/badge/linux-grey?style=for-the-badge&logo=linux&logoColor=white&labelColor=072c61)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

## Описание проекта

Django приложение для создания древовидных меню с возможностью редактирования через админ-панель. Реализовано с использованием template tags и оптимизировано для минимального количества запросов к БД.

### Особенности

✅ **Template Tag** - Меню реализовано через `{% draw_menu 'menu_name' %}`  
✅ **Умное раскрытие** - Все элементы над активным пунктом развернуты, первый уровень под активным тоже  
✅ **База данных** - Хранение в PostgreSQL с древовидной структурой  
✅ **Админ-панель** - Полное редактирование через стандартную админку Django  
✅ **Активный пункт** - Определяется автоматически по URL текущей страницы  
✅ **Множество меню** - Несколько меню на одной странице по разным названиям  
✅ **Гибкие URL** - Поддержка как явных URL, так и named URL  
✅ **Оптимизация** - Ровно 1 запрос к БД на отрисовку каждого меню  

---

## Содержание

- [Требования](#требования)
- [Установка](#установка)
  - [Разработка](#разработка)
  - [Staging](#staging)
  - [Production](#production)
- [Использование](#использование)
- [Тестирование](#тестирование)
- [Архитектура](#архитектура)

---

## Требования

- **Python**: 3.11+
- **Django**: 5.2.8
- **PostgreSQL**: 15+
- **Deployment**: gunicorn, gitlab ci/cd, system daemons

---

## Установка

### Разработка

#### 1. Клонирование репозитория

```bash
git clone https://github.com/abdullaabdukulov/django-tree-menus.git
cd django-tree-menus/
chmod +x start.sh
./start.sh dev
```

#### 2. Настройка окружения

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/development.txt
```

#### 3. Настройка переменных окружения

Отредактируйте файл `.env` согласно вашим настройкам

#### 4. Активация pre-commit

```bash
pre-commit install && pre-commit autoupdate
```

#### 5. Запуск PostgreSQL

```bash
docker compose up -d --build
```

#### 6. Миграции и создание суперпользователя

```bash
source ./.env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

#### 7. Запуск сервера разработки

```bash
python manage.py runserver
```

Откройте в браузере: http://127.0.0.1:8000

---

## Использование

### 1. Загрузка готового меню (рекомендуется)

Если вы хотите сразу получить готовое меню со структурой (например `main_menu` и пункты до 4-го уровня вложенности),
выполните следующие команды:

```bash
python manage.py loaddata apps/menus/fixtures/menu.json
python manage.py loaddata apps/menus/fixtures/menu_items.json

### 2. Использование в шаблонах

```django
{% load menu_tags %}

<!DOCTYPE html>
<html>
<head>
    <title>Мой сайт</title>
</head>
<body>
    <!-- Главное меню -->
    {% draw_menu 'main_menu' %}
    
    <!-- Боковое меню -->
    {% draw_menu 'sidebar_menu' %}
    
    <div class="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

### 3. Пример структуры меню

```
Главная (/)
О нас (/about/)
  ├── Наша команда (/about/team/)
  └── История (/about/history/)
Услуги (/services/)
  ├── Веб-разработка (/services/web/)
  ├── Мобильные приложения (/services/mobile/)
  └── Дизайн (/services/design/)
      └── UI/UX (/services/design/uiux/)
Контакты (/contacts/)
```

При переходе на `/services/design/uiux/`:
- Развернуты: Услуги → Дизайн → UI/UX
- Свернуты: О нас, Контакты
- Активный: UI/UX

---

## Тестирование

### Запуск всех тестов

```bash
python manage.py test apps.menus
```

### Запуск конкретного теста

```bash
python manage.py test apps.menus.tests.MenuModelTest
python manage.py test apps.menus.tests.MenuManagerTest
python manage.py test apps.menus.tests.DrawMenuTemplateTagTest
```

### Тесты включают:

- ✅ Создание и работа моделей Menu и MenuItem
- ✅ Построение дерева меню (MenuManager)
- ✅ Определение активного пункта и пути
- ✅ Отрисовка template tag
- ✅ Оптимизация запросов к БД
- ✅ Обработка edge cases

---

## Архитектура

```
django-tree-menus/
├── .deployments/
│   ├── development/
│   │   ├── db_configs/
│   │   │   ├── Dockerfile
│   │   │   └── postgres-script.sh
│   │   ├── docker-compose.yml
│   │   └── env_example.txt
│   ├── nginx/
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   ├── staging/
│   │   ├── docker-compose.yml
│   │   ├── Dockerfile
│   │   └── env_example.txt
│   └── production/
│       ├── docker-compose.yml
│       ├── Dockerfile
│       └── env_example.txt
├── apps/
│   └── menus/
│       ├── migrations/
│       ├── templatetags/
│       │   ├── __init__.py
│       │   └── menu_tags.py
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── staging.py
│   │   └── production.py
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py
│   └── wsgi.py
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   ├── staging.txt
│   └── production.txt
├── .dockerignore
├── .env
├── .gitignore
├── .pre-commit-config.yaml
├── docker-compose.yml
├── entrypoint.sh
├── manage.py
├── pyproject.toml
├── README.md
└── start.sh
```

---

## Ключевые компоненты

### Models (apps/menus/models.py)

- **Menu** - Модель для хранения меню
- **MenuItem** - Модель пунктов меню с поддержкой иерархии
- **MenuManager** - Custom manager с методом `get_menu_tree()`
- **MenuQuerySet** - Оптимизированные запросы

### Template Tags (apps/menus/templatetags/menu_tags.py)

- `{% draw_menu 'menu_name' %}` - Отрисовка меню по названию
- Автоматическое определение активного пункта
- Умное раскрытие веток дерева

### Admin (apps/menus/admin.py)

- Полная интеграция с Django Admin
- Inline редактирование пунктов меню
- Сортировка и фильтрация

---

## API моделей

### Menu

```python
Menu.objects.get_menu_tree(menu_name, current_url)
# Возвращает готовое дерево меню с метаданными
```

### MenuItem

```python
item.get_url()  # Возвращает URL (явный или через reverse)
item.should_show_children(parent_is_active)  # Нужно ли показывать детей
item.get_css_classes()  # Возвращает CSS классы для элемента
```

---

## Оптимизация

### Запросы к БД

Приложение использует **ровно 2 SQL запроса** на каждое меню:
1. SELECT для получения объекта Menu
2. SELECT для prefetch всех MenuItem

```python
# В MenuManager.get_menu_tree()
menu = self.with_items().get(name=menu_name)  # 2 queries
```

### Кэширование (опционально)

Для дополнительной оптимизации можно добавить кэширование:

```python
from django.core.cache import cache

def get_menu_tree(self, menu_name, current_url):
    cache_key = f'menu_{menu_name}_{current_url}'
    cached = cache.get(cache_key)
    if cached:
        return cached