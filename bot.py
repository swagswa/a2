from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import asyncio
from datetime import datetime

# Настройки API
API_ID = '27387168'
API_HASH = 'cca1552d4eadd63fced41a4e8c0f1ef6'
BOT_TOKEN = '7758329175:AAFHeall6y4Z17ObbHroe9jiBW6uvJIp3HY'
TARGET_USER_ID = 6911079735
WEB_APP_URL = 'https://asdasdasd1231asdpoasdiopasd.netlify.app/'

# Инициализация клиента
app = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True
)

# Глобальные переменные
last_api_message = None
user_states = {}

# Константы для текстов на разных языках
messages = {
    'ru': {
        'welcome': '😈Добро пожаловать в 1WIN Signals😈',
        'games': 'В нашем боте есть 4 игры с 1WIN и дальше мы будем добавлять новые игры для заработка.',
        'ai': 'Наш бот основан на нейросети OpenAI с точностью предсказаний 92%',
        'promo': '💥НЕ ЗАБЫВАЙТЕ ПРОМОКОД - WARGOD666',
        'registration': '📱 Регистрация',
        'send_id': 'Пожалуйста, отправьте свой ID для проверки',
        'success': '💚 Вы успешно зарегистрировались! Можете использовать приложение',
        'app_button': '⚡️Приложение',
        'invalid_id': 'Пожалуйста, отправьте корректный ID.'
    },
    'en': {
        'welcome': '😈Welcome to 1WIN Signals😈',
        'games': 'Our bot has 4 games with 1WIN and will add new games for better earnings.',
        'ai': 'Our bot is based on OpenAI neural network with 92% prediction accuracy',
        'promo': "💥DON'T FORGET PROMO CODE - WARGOD666",
        'registration': '📱 Registration',
        'send_id': 'Please send your ID for verification',
        'success': '💚 You have successfully registered! You can use the application',
        'app_button': '⚡️Application',
        'invalid_id': 'Please send a valid ID.'
    },
    'hi': {
        'welcome': '😈1WIN सिग्नल्स में आपका स्वागत है😈',
        'games': 'हमारे बॉट में 1WIN के 4 गेम हैं और कमाई के लिए नए गेम जोड़ते रहेंगे',
        'ai': 'हमारा बॉट OpenAI न्यूरल नेटवर्क पर आधारित है, जो 92% सटीकता से परिणाम बतता है।',
        'promo': '💥प्रोमो कोड न भूलें - WARGOD666',
        'registration': '📱 पंजीकरण',
        'send_id': 'कृपया सत्यापन के लिए अपना आईडी भेजें',
        'success': '💚 आप सफलतापूर्वक पंजीकृत हो गए हैं! आप एप्लिकेशन का उपयोग कर सकते हैं।',
        'app_button': '⚡️एप्लिकेशन',
        'invalid_id': 'कृपया एक वैध आईडी भेजें।'
    }
}

# Обработка команды /start
@app.on_message(filters.command("start"))
async def start_command(client, message):
    try:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
                InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
            ],
            [InlineKeyboardButton("🇮🇳 हिंदी", callback_data="lang_hi")]
        ])
        
        await message.reply_text(
            "Выберите язык\n\nSelect language\n\nभाषा चुने",
            reply_markup=keyboard
        )
    except Exception as e:
        print(f'❌ Ошибка при обработке команды /start: {e}')

# Обработка callback-запросов
@app.on_callback_query()
async def callback_handler(client, callback_query):
    try:
        data = callback_query.data
        user_id = callback_query.from_user.id
        
        if data.startswith('lang_'):
            language = data.split('_')[1]
            msg = messages[language]
            text = f"{msg['welcome']}\n\n{msg['games']}\n\n{msg['ai']}\n\n{msg['promo']}"
            
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton(msg['registration'], callback_data=f"register_{language}")
            ]])
            
            await callback_query.message.edit_text(text, reply_markup=keyboard)
            
        elif data.startswith('register_'):
            language = data.split('_')[1]
            registration_text = """🔷 1. Для начала зарегистрируйтесь по ссылке на сайте 1WIN

ССЫЛКА (https://1wzvro.top/casino/list?open=register&p=vygr)

- При регистрации вводим промокод: WARGOD666

❌ Если вы не введете промокорд, мы не сможем подключить ваш аккаунт к системе

🔷 2. После успешной регистрации cкопируйте ваш айди на сайте (Вкладка "пополнение" и в правом верхнем углу будет ваш ID).

🔷 3. И отправьте его боту в ответ на это сообщение!"""

            photo_url = "https://i.imgur.com/zLtgFRl.jpg"
            
            user_states[user_id] = {
                'language': language,
                'waiting_for_id': True
            }
            
            await callback_query.message.delete()
            await client.send_photo(
                callback_query.message.chat.id,
                photo_url,
                caption=registration_text
            )
            
    except Exception as e:
        print(f'❌ Ошибка при обработке callback: {e}')

# Перехват сообщений от API (от 7758329175 к 6911079735)
@app.on_message(filters.user(7758329175))
async def handle_api_messages(client, message):
    global last_api_message
    try:
        if message.chat.id == TARGET_USER_ID:
            last_api_message = message.text
            
            print('\n')
            print('╔════════════════════════════════════════════════════════════════')
            print('║ 📨 ПЕРЕХВАЧЕНО СООБЩЕНИЕ ОТ API')
            print('╠════════════════════════════════════════════════════════════════')
            print(f'║ От бота ID: 7758329175')
            print(f'║ К пользователю ID: {TARGET_USER_ID}')
            print(f'║ Текст: {message.text}')
            print(f'║ Время: {datetime.now()}')
            print('╚════════════════════════════════════════════════════════════════')
            print('\n')
            
    except Exception as e:
        print(f'❌ Ошибка при перехвате сообщения от API: {e}')

# Обработка текстовых сообщений от пользователя
@app.on_message(filters.text & filters.regex(r'^\d+$'))
async def handle_text(client, message):
    try:
        user_id = message.from_user.id
        
        if user_id in user_states and user_states[user_id].get('waiting_for_id'):
            print('\n')
            print('╔════════════════════════════════════════════════════════════════')
            print('║ 🔍 СРАВНЕНИЕ ID')
            print('╠════════════════════════════════════════════════════════════════')
            print(f'║ ID от пользователя: {message.text}')
            print(f'║ Последнее сообщение от API: {last_api_message}')
            print('╚════════════════════════════════════════════════════════════════')
            print('\n')
            
            if last_api_message and message.text == last_api_message:
                # ID совпадают - отправляем галочку
                check_message = await message.reply_text("✅")
                await asyncio.sleep(3)
                await check_message.delete()
                
                # Отправляем сообщение об успехе с WebApp кнопкой
                lang = user_states[user_id]['language']
                keyboard = InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        text=messages[lang]['app_button'],
                        web_app=WebAppInfo(url=WEB_APP_URL)
                    )
                ]])
                await message.reply_text(messages[lang]['success'], reply_markup=keyboard)
                user_states[user_id]['waiting_for_id'] = False
            else:
                # ID не совпадают - отправляем крестик
                cross_message = await message.reply_text("❌")
                await asyncio.sleep(3)
                await cross_message.delete()
                
                # Сообщение об ошибке
                error_message = await message.reply_text(messages[user_states[user_id]['language']]['invalid_id'])
                await asyncio.sleep(3)
                await error_message.delete()
                
    except Exception as e:
        print(f'❌ Ошибка при обработке текстового сообщения: {e}')

# Запуск бота
print("🚀 Бот запущен")
app.run()
