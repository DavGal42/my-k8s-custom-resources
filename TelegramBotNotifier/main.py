import kopf
import requests
from kubernetes import client, config

# Locally - config.load_kube_config()
# In Cluster - config.load_incluster_config()
config.load_incluster_config()

notifier_config = {}


def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    response = requests.post(url, data=data)
    return response.ok


@kopf.on.create('telegram.alert', 'v1', 'telegramnotifiers')
def on_create_fn(spec, name, namespace, logger, **kwargs):
    bot_token = spec.get('botToken')
    chat_id = spec.get('chatID')
    events = spec.get('events', [])
    namespaces = spec.get('namespaces', [])

    if bot_token and chat_id and events and namespaces:
        notifier_config[name] = {
            "bot_token": bot_token,
            "chat_id": chat_id,
            "events": events,
            "namespaces": namespaces,
        }

        message = f"👋 Hi! TelegramNotifier {name} has been created successfully."
        success = send_telegram_message(bot_token, chat_id, message)

        if success:
            logger.info("✅ Message had been sent.")
        else:
            logger.error("❌ Failed to send message.")
    else:
        logger.warning("⚠️ There is no some information.")


@kopf.timer('pods', interval=30.0)
def periodic_pod_checker(logger, **kwargs):
    api = client.CoreV1Api()
    pods = api.list_pod_for_all_namespaces(watch=False)

    for pod in pods.items:
        pod_name = pod.metadata.name
        namespace = pod.metadata.namespace

        for container in pod.status.container_statuses or []:
            state = container.state
            waiting = state.waiting
            if waiting:
                reason = waiting.reason
                for notifier_name, cfg in notifier_config.items():
                    if cfg["namespaces"] and namespace not in cfg["namespaces"]:
                        continue
                    if cfg["events"] and reason not in cfg["events"]:
                        continue

                    message = (
                        f"🔥 Pod {pod_name} in namespace {namespace} has been broken. Reason: *{reason}*"
                    )
                    send_telegram_message(cfg["bot_token"], cfg["chat_id"], message)
                    logger.info(f"📬 Had been sended a message {notifier_name} about pod {pod_name}")


@kopf.on.update('v1', 'pods')
def pod_error_handler(body, logger, **kwargs):
    pod_name = body['metadata']['name']
    namespace = body['metadata']['namespace']

    for container in body.get('status', {}).get('containerStatuses', []):
        state = container.get('state', {})
        waiting = state.get('waiting')
        if waiting:
            reason = waiting.get('reason')
            for notifier_name, cfg in notifier_config.items():
                if cfg.get("namespaces") and namespace not in cfg["namespaces"]:
                    continue
                if cfg.get("events") and reason not in cfg["events"]:
                    continue

                message = f"🔥 Pod {pod_name} in namespace {namespace} has been broken. Reason: *{reason}*"
                send_telegram_message(cfg["bot_token"], cfg["chat_id"], message)
                logger.info(f"📬 Had been sended a message from {notifier_name} for reason {reason}.")
