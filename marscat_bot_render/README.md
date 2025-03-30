# MarsCatEmpire — Telegram Bot для Render

## Как развернуть бота на Render

1. Создай новый репозиторий на GitHub и загрузи туда эти файлы.
2. Перейди на https://render.com → New Web Service.
3. Подключи GitHub, выбери репозиторий.
4. Укажи:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
   - Add Environment Variable: BOT_TOKEN = твой токен от BotFather

5. Нажми Deploy. Готово!

База данных сохраняется локально как `marscat.db`.