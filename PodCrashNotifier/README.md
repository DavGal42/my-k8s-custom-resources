# Telegram Bot Notifier During Pod Crash

## Project Structure

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

## Installation Guide

### 1. Build the Docker image

```bash
docker build -t your-dockerhub-username/telegram-notifier:latest .
```

### 2. Log in to Docker Hub

```bash
docker login
```

### 3. Push the image to Docker Hub

```bash
docker push your-dockerhub-username/telegram-notifier:latest
```

### 4. Apply the Custom Resource Definition (CRD)

```bash
kubectl apply -f telegram-notifier-crd.yml
```

### 5. Create the ServiceAccount and RBAC roles

```bash
kubectl apply -f sa.yml
kubectl apply -f rbac.yml
```

### 6. Deploy the controller

First you need to edit deploy.yml

```bash
kubectl apply -f deploy.yml
```
### 7. Create you Telegram Bot and get it's Token and your ChatID

### 8. Create your Notifier CR (custom resource)

You need to edit my-notifier.yml

```bash
kubectl apply -f my-notifier.yml
```

### 9. Trigger it with a crashing pod

```bash
kubectl apply -f crash-pod-example-1.yml
# or
kubectl apply -f crash-pod-example-2.yml
```
