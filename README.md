# code_quest_assignment (Django & PostgreSQL)

This repository implements a **smart, high-performance product search** for thousands of items with support for:

- **Partial keywords** (fast `icontains` backed by a GIN-trgm index)
- **Misspellings** (fuzzy matching via `TrigramSimilarity`)
- **Mixed English/Arabic** (Full-Text Search with `english` & `arabic` configs + simple fallback)
- **REST API** (Django REST Framework, paginated, throttle-protected)
- **Web UI** (server-rendered search page, responsive CSS, instant “clear results” on typing)

---

## 📦 Tech Stack

- Python 3.10+
- Django 5.x
- PostgreSQL 14+ (with `pg_trgm` & full-text extensions)
- Django REST Framework

---

## 🚀 Setup Instructions

### 1. Clone & Virtualenv

```bash
git clone git@github.com:saied2035/code_quest_assignment.git
cd code_quest_assignment
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. PostgreSQL Extensions

Connect to your PostgreSQL database:

```py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'database name' # 'product_search_api',
        'USERNAME': 'database username' # root,
        'HOST': 'database port' # '127.0.0.1',
        'PORT': 'port number' # '5432'
        'PASSWORD': 'username password' # remove this line if the username has access without any passwords
    }
}
```

### 3. Migrate

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Populate Dummy products

```bash
python manage.py populate_dummy --count number # py manage.py populate_dummy --count 10000
```
If you have data:

- add a field to your product model:
```py
search_vector = SearchVectorField(null=True)
```
- run this command:
```bash 
python manage.py update_search_vectors 
```

### 5. Run the Dev Server

```bash
python manage.py runserver
```

Now visit:

**Web UI** → http://127.0.0.1:8000/

**API docs** → none by default; see below for examples

#### 🔍 API Documentation

##### Authentication & Throttling

- **No auth required** for anon users

- **Anon throttle:** 20 requests/minute

- **User throttle:** 100 requests/minute

##### Endpoint: Search Products

```sql
GET /api/products/search/
```

| Query-param |  Type   | Required | Default | Description                                           |
| :---------: | :-----: | :------: | :-----: | :---------------------------------------------------- |
|     `q`     | string  |   yes    |    —    | Search term (partial, misspelled, English/Arabic/etc) |
|   `page`    | integer |    no    |    1    | Page number (pagination)                              |

**Response (200 OK)**
```json
{
    "count": 86,
    "next": "http://127.0.0.1:8000/products/api/search?page=2&q=application",
    "previous": null,
    "results": [
        {
            "id": 8801,
            "name": "Secured static application",
            "brands": [
                {
                    "id": 127,
                    "name": "Ramirez and Sons"
                }
            ],
            "categories": [
                {
                    "id": 1,
                    "name": "Beverages"
                },
                {
                    "id": 2,
                    "name": "Snacks"
                },
                {
                    "id": 7,
                    "name": "Meat"
                }
            ]
        },
        {
            "id": 9606,
            "name": "Reduced radical application",
            "brands": [
                {
                    "id": 124,
                    "name": "Cruz LLC"
                },
                {
                    "id": 126,
                    "name": "Tucker LLC"
                },
                {
                    "id": 128,
                    "name": "Cooper, Gallegos and Bailey"
                }
            ],
            "categories": [
                {
                    "id": 1,
                    "name": "Beverages"
                },
                {
                    "id": 4,
                    "name": "Vegetables"
                }
            ]
        },
        //rest of the result in page 1
    ]
} 
```
**Errors**
- **400 Bad Request** if q is missing:
```json
{ "detail": "Provide a search term via ?q=…" }
```

### 🖥 Web UI

**URLs**

- GET /

- GET /search/

**Features**

- Responsive mobile-first layout

- Instant clear of previous results on typing

- Pagination

### Templates & Static

**Templates**

- templates/base.html (layout + CSS include)

- product/templates/product/search.html (search form & results)

**Static**

- product/static/product/style.css

Be sure your settings.py includes:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        # …
    },
]

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'product' / 'static',
]
```

### 🎁 Bonus Ideas

- Redis caching of top-N query results

- DRF browsable API

- Rate-limit caching using a Redis backend

- Autocomplete / search-as-you-type via AJAX

- use the pyspellchecker library to fix missplings before search for more accurate searching.

Feel free to open issues or pull requests—happy searching!
