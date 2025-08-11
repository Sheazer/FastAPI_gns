# ESF Microservices (FastAPI + PostgreSQL + Docker)

## Описание
Три микросервиса:
1. **Auth Service** — регистрация, логин, JWT.
2. **ESF Service** — CRUD для ЭСФ, отправка в ГНС.
3. **GNS Proxy** — мок-сервис, эмулирует ГНС.

Все сервисы используют:
- FastAPI (Swagger)
- Tortoise ORM
- PostgreSQL
- Docker Compose

## Запуск
```bash
docker-compose up --build
