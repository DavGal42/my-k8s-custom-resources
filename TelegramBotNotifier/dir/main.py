import kopf
import requests

def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}

    response = requests.post(url, data=data)

    return response.ok


@kopf.on.create('telegram.alert', 'v1', 'telegramnotifiers')
def on_create_fn(spec, name, namespace, logger, **kwargs):
    bot_token = spec.get('botToken')
    chat_id = spec.get('chatID')

    message = f"👋 Привет! TelegramNotifier `{name}` успешно создан в неймспейсе `{namespace}`."

    if bot_token and chat_id:
        success = send_telegram_message(bot_token, chat_id, message)

        if success:
            logger.info("✅ Приветственное сообщение успешно отправлено.")
        else:
            logger.error("❌ Не удалось отправить сообщение.")
    else:
        logger.warning("⚠️ There is no botToken or chatID.")

