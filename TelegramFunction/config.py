# Request Link and Long Polling Use
TELEGRAM_TOKEN = '1766250463:AAH3CYEuEgEgJo8uxvosyLq9_dAjzhae6C0'
#WEBHOOK_URL = 'https://9g1cme995k.execute-api.us-east-1.amazonaws.com/default/Hexplode_bot'
WEBHOOK_URL = 'https://9537-2001-b400-e230-3bf9-b012-e2ca-4a21-c476.ngrok.io/bot'
TELEGRAM_BASE = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}'
TELEGRAM_WEBHOOK_URL = TELEGRAM_BASE + f'/setWebhook?url={WEBHOOK_URL}'