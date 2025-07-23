# <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Objects/Incoming%20Envelope.webp" alt="Incoming Envelope" width="50" height="50" /> Telegram Bot Notifier During Pod Crash

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Objects/Card%20Index%20Dividers.webp" alt="Card Index Dividers" width="30" height="30" /> Project Structure

```bash
PodCrashNotifier
├── crash-pod-example-1.yml
├── crash-pod-example-2.yml
├── deploy.yml
├── Dockerfile
├── main.py
├── my-notifier.yml
├── rbac.yml
├── requirements.txt
├── sa.yml
└── telegram-notifier-crd.yml
```

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Travel%20and%20Places/Rocket.webp" alt="Rocket" width="30" height="30" /> Installation Guide

### 1. Build the Docker image

```
docker build -t your-dockerhub-username/telegram-notifier:latest .
```

### 2. Log in to Docker Hub

```docker login```

### 3. Push the image to Docker Hub

```
docker push your-dockerhub-username/telegram-notifier:latest
```

### 4. Apply the Custom Resource Definition (CRD)

```
kubectl apply -f telegram-notifier-crd.yml
```

### 5. Create the ServiceAccount and RBAC roles

```
kubectl apply -f sa.yml
kubectl apply -f rbac.yml
```

### 6. Deploy the controller

First you need to edit deploy.yml

```
kubectl apply -f deploy.yml
```
### 7. Create you Telegram Bot and get it's Token and your ChatID

### 8. Create your Notifier CR (custom resource)

You need to edit my-notifier.yml

```
kubectl apply -f my-notifier.yml
```

### 9. Trigger it with a crashing pod

```
kubectl apply -f crash-pod-example-1.yml
# or
kubectl apply -f crash-pod-example-2.yml
```
