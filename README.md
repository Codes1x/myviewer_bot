# Telegram Viewer Bot

Telegram-бот, позволяющий пользователю авторизоваться через свой Telegram-аккаунт и получить список:

- Чатов (группы и супергруппы)
- Каналов (включая приватные)
- Личных диалогов (пользователей)

> Использует `Telethon` для клиентской авторизации и `aiogram` для управления ботом.

---

## Возможности

- Авторизация по номеру, коду и 2FA
- Вывод чатов, каналов и диалогов с ID
- Инлайн-кнопки и удобное меню
- Пагинация при большом количестве записей
- Выход из аккаунта и удаление сессии
- Просмотр информации о профиле
- Поддержка запуска в Docker-контейнере

---

## Быстрый запуск без Docker

### 1. Клонируй репозиторий

```bash
git clone https://github.com/your-username/telegram-viewer-bot.git
cd telegram-viewer-bot

### 2. Создай `.env` файл

В корне проекта создай файл `.env` и добавь туда следующее:

```env
BOT_TOKEN=your_bot_token
API_ID=your_api_id
API_HASH=your_api_hash

Где взять:

BOT_TOKEN — выдается через @BotFather при создании бота

API_ID и API_HASH — получаются на https://my.telegram.org → API Development Tools

### 3. Установи зависимости и запусти

Создай и активируй виртуальное окружение:

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# или source venv/bin/activate  # Linux/macOS

### Установи зависимости и запусти бота

pip install -r requirements.txt
python main.py

### После запуска бот будет активен. Перейди в Telegram и открой:

https://t.me/your_bot_username

### Запуск через Docker (опционально)

Собери и запусти контейнер:

docker-compose build
docker-compose up -d

Просмотр логов

docker-compose logs -f

### Как пользоваться ботом

1. Отправьте /start

2. Введите номер телефона в формате +79001234567

3. Введите код, отправленный Telegram (приходит в Telegram-чат, не по SMS)

4. При необходимости — введите 2FA-пароль

5. Используйте инлайн-меню:

🔹 Чаты  
🔹 Каналы  
🔹 Личные диалоги  
🧾 Профиль  
🚪 Выйти из аккаунта  

###  Структура проекта

telegram_viewer_bot/
├── main.py
├── .env
├── requirements.txt
├── README.md
├── Dockerfile
├── docker-compose.yml
├── sessions/
└── bot/
    ├── handlers/
    │   ├── __init__.py
    │   ├── start.py
    │   ├── auth.py
    │   ├── chats.py
    │   ├── channels.py
    │   ├── users.py
    │   ├── logout.py
    │   └── profile.py
    ├── keyboards/
    │   ├── __init__.py
    │   └── inline.py
    └── utils/
        ├── __init__.py
        ├── client_manager.py
        ├── pagination.py
        └── errors.py

###  Важно
Код авторизации приходит в Telegram-приложение, не по SMS

Telegram может временно блокировать вход, если вы ранее нажимали "Это не я"

Файлы .session сохраняются в sessions/ — не добавляйте их в GitHub!

