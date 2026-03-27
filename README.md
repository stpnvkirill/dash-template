# Plotly Dash app template

Starter template for a **Plotly Dash** web app with authentication, user profile, and session management. Use it as a base to build dashboards and data apps without wiring auth and DB from scratch.

**Goals:**

- Ready-made auth (login, registration, sessions)
- Profile page with session management (view/terminate sessions)
- Clear split: Flask backend + Dash frontend (Mantine UI)
- Runs locally or in Docker

## Run locally

You need a PostgreSQL instance: local install, cloud (e.g. managed DB), or run only the database in Docker (`docker compose up db -d`). The app runs on your machine; only the DB can be in Docker or elsewhere.

1. **Requirements:** Python 3.14+, [uv](https://docs.astral.sh/uv/).

2. **Install deps and create `.env`:**

   ```bash
   uv sync
   ```

   Create a `.env` file in the project root (see variables below).

3. **Set in `.env`:**

   ```env
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_USER=your_user
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=dash
   SECRET_KEY=your_secret_key
   
   # Optional: Disable rate limiting for internal tools
   ENABLE_RATE_LIMITING=false
   ```

4. **Apply migrations and start:**

   ```bash
   uv run alembic upgrade head
   uv run main.py
   ```

   App: <http://localhost:8080>

## Run with Docker

When you run the full stack with Docker Compose, the **database starts automatically** (no separate Postgres setup).

```bash
# Create .env with POSTGRES_* and SECRET_KEY (see above)
docker compose up --build
```

App: <http://localhost:8080> · DB port: 6432 (mapped from 5432).

## Feature Development Workflow

### General Principles

The project follows **Domain-Driven Design (DDD)** architecture with clear separation of concerns:

- **Backend**: Flask + SQLAlchemy + PostgreSQL
- **Frontend**: Plotly Dash + Mantine UI
- **Testing**: pytest with fixtures for integration tests

### Backend Feature Development

#### 1. Database Model
Create a model in `app/backend/database/models/`.

```python
# app/backend/database/models/your_entity.py
from sqlalchemy import Column, UUID, String, DateTime, text
from app.backend.database.models.shared import Base

class YourEntity(Base):
    __tablename__ = "your_entities"

    id = Column(UUID, primary_key=True, server_default=text("uuidv7()"))
    name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=text("now()"))
```

#### 2. Database Migration
Create migration using Alembic:

```bash
# Create migration
uv run alembic revision --autogenerate -m  "add your_entity"

# Apply migration
uv run alembic upgrade head
```

#### 3. DTO (Data Transfer Object)
Add DTO in `app/backend/domain/` for data transfer:

```python
# app/backend/domain/your_entity.py
from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class YourEntityDto:
    id: UUID
    name: str
    created_at: datetime
```

#### 4. Converter
Create converter in `app/backend/converters/` for model-DTO transformation:

```python
# app/backend/converters/your_entity_converter.py
from app.backend.database.models import YourEntity
from app.backend.domain import YourEntityDto
from .base_converter import BaseConverter

class YourEntityConverter(BaseConverter):
    @staticmethod
    def to_dto(entity: YourEntity) -> YourEntityDto | None:
        if not entity:
            return None
        return YourEntityDto(
            id=entity.id,
            name=entity.name,
            created_at=entity.created_at,
        )
```

#### 5. Queries (Optional)
If complex queries are needed, create query class in `app/backend/queries/`:

```python
# app/backend/queries/your_entity_queries.py
import sqlalchemy as sa
from app.backend.database.models import YourEntity

class YourEntityQueries:
    @staticmethod
    def get_active_entities_query() -> sa.Select:
        return sa.select(YourEntity).where(YourEntity.is_active == True)
```

#### 6. Repository
Create repository in `app/backend/repositories/` for data operations:

```python
# app/backend/repositories/your_entity_repository.py
from app.backend.database.models import YourEntity
from app.backend.infrastructure.database import SqlService
from .base_repository import BaseRepository

class YourEntityRepository(BaseRepository[YourEntity]):
    def __init__(self, sql_service: SqlService):
        super().__init__(sql_service)

    def get_active_entities(self) -> list[YourEntity]:
        return self.sql_service.select(YourEntity.is_active == True)
```

#### 7. Service
Create service in `app/backend/services/your_entity/` with business logic:

```python
# app/backend/services/your_entity/your_entity_service.py
from app.backend.database.models import YourEntity
from app.backend.domain import YourEntityDto
from app.backend.infrastructure.database import SqlService
from app.backend.repositories.your_entity_repository import YourEntityRepository
from app.backend.services.base import BaseService
from app.backend.converters.your_entity_converter import YourEntityConverter

class YourEntityService(BaseService):
    def __init__(self):
        self.repo = YourEntityRepository(SqlService(model=YourEntity))

    def get_all_active(self) -> list[YourEntityDto]:
        entities = self.repo.get_active_entities()
        return [YourEntityConverter.to_dto(e) for e in entities]
```

#### 8. Backend Registration
New code should use `ServiceFactory`. Legacy code can use `back` for compatibility:

```python
# app/backend/__init__.py
from app.backend.services.factory import get_service_factory

# New way (recommended)
factory = get_service_factory()
entities = factory.your_entity_service.get_all_active()

# Legacy way (for compatibility)
from app.backend import back
entities = back.user.your_entity_service.get_all_active()
```

### Frontend Feature Development

#### 1. Component
Create component in appropriate `app/frontend/components/` folder:

```python
# app/frontend/components/your_entity/your_entity_list.py
import dash_mantine_components as dmc
from app.backend.services.factory import get_service_factory

def YourEntityList():
    factory = get_service_factory()
    entities = factory.your_entity_service.get_all_active()
    return dmc.Stack([
        dmc.Title("Your Entities", order=3),
        dmc.List([
            dmc.ListItem(e.name) for e in entities
        ])
    ])
```

#### 2. Page
If new page is needed, create it in `app/frontend/pages/`:

```python
# app/frontend/pages/your_entity.py
from dash import html
import dash_mantine_components as dmc

from app.frontend.components.your_entity.your_entity_list import YourEntityList
from app.frontend.layout import Layout

def layout():
    return Layout(
        html.Div([
            YourEntityList()
        ])
    )
```

#### 3. Navigation (Optional)
If menu item is needed, update `app/frontend/layout/navbar.py`:

```python
# app/frontend/layout/navbar.py
nav_items = [
    # ... existing items ...
    dmc.NavLink(label="Your Entities", href="/your-entity"),
]
```

### Testing

#### 1. Backend Tests
Create tests in `test/backend/test_your_entity_service.py`:

```python
# test/backend/test_your_entity_service.py
import pytest
from app.backend.services.your_entity.your_entity_service import YourEntityService

class TestYourEntityService:
    @pytest.fixture
    def service_factory(self):
        from app.backend.services.factory import ServiceFactory, reset_service_factory
        factory = ServiceFactory()
        yield factory
        reset_service_factory()

    def test_get_all_active(self, service_factory):
        entities = service_factory.your_entity_service.get_all_active()
        assert isinstance(entities, list)
```

---

## Additional Services

### Password Validator

Validate password strength:

```python
from app.backend.domain.validators import PasswordValidator

result = PasswordValidator.validate("StrongP@ss123")
if result.is_valid:
    # Password meets requirements
    ...
else:
    print(f"Error: {result.error_message}")
```

**Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character

### Rate Limiter

Protect against brute-force attacks:

```python
from app.backend.services.rate_limiter import get_auth_rate_limiter

limiter = get_auth_rate_limiter()

# Check if blocked
if limiter.is_blocked("user@example.com"):
    retry_after = limiter.get_retry_after("user@example.com")
    print(f"Blocked for {retry_after} seconds")

# Record attempt
limiter.record_attempt("user@example.com")

# Reset after successful login
limiter.reset("user@example.com")
```

**Default limits:**
- 5 attempts per 5 minutes
- 15 minutes block after exceeding

**Disable rate limiting** (for internal tools or development):

```env
# .env
ENABLE_RATE_LIMITING=false
```

> **Note:** Rate limiting is enabled by default (`true`) for security. Only disable it for trusted internal tools.

### I18n Service

Load translations:

```python
from app.backend.services.i18n import get_i18n_service

i18n = get_i18n_service()

# Load all translations
translations = i18n.get_translation("ru")

# Get specific text
text = i18n.get_text("btn_login", "ru")
```

**Supported locales:** `en`, `ru`
