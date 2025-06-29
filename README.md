### Запуск проекта
---
#### 1. Создать .env из примера
```bash
cp .env.example .env
```

#### 2. Запустить сервисы через Docker Compose
```bash
docker compose up -d --build
```

#### 3. Готово, приложение доступно по указанным в конфиге портам.
```txt
http://localhost:8000/docs
```
