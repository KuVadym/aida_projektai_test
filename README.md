# 🗓️ Events API

Це Django REST API для управління подіями та реєстрації користувачів на них. Підтримується авторизація через JWT, створення/редагування подій, перегляд своїх реєстрацій та документація через Swagger.

---

## 🚀 Технології

- Python 3.10  
- Django 4.x  
- Django REST Framework  
- Simple JWT    
- Docker 
- Gunicorn  

---

## ⚙️ Встановлення

### 1. Клонуй репозиторій
git clone https://github.com/yourusername/events-api.git
cd events-api


3. Запуск через Docker
docker build -t events-api .
docker run -p 8000:8000 events-api

🔐 Аутентифікація
Використовується JWT (JSON Web Tokens).

🔑 Отримати токен:

POST /api/token/
{
  "email": "user@example.com",
  "password": "yourpassword"
}
🔄 Оновити токен:

POST /api/token/refresh/
{
  "refresh": "..."
}

📚 API Ендпоінти
POST /api/registration/ — Реєстрація

POST /api/token/ — Логін (отримати токен)

GET /api/events/ — Список подій
POST /api/events/ — Створення події

POST /api/events/<id>/register/ — Зареєструватись на подію

GET /api/events/my/ — Список моїх подій

📖 Документація
Swagger UI доступний за адресою:
GET /api/docs/




