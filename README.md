# ☁️ Cloud-Based Visitor Counter Using Flask, Redis, Docker and Kubernetes

A cloud computing project that demonstrates containerization, Kubernetes deployment, horizontal pod autoscaling, hybrid-cloud simulation with failover, and resource optimization.

## 📌 Project Overview

This project implements a visitor counter web application using Python Flask and Redis.

Whenever a user visits the application, the visitor count is incremented and stored in Redis. Docker is used to containerize the application, while Kubernetes manages deployment, scaling, service discovery, and self-healing.

The project also demonstrates Horizontal Pod Autoscaling (HPA) and hybrid-cloud failover using two independent local Minikube clusters connected through an NGINX reverse proxy.

## 🎯 Project Objectives

1. Containerize the Flask application using Docker.
2. Deploy Flask and Redis using Kubernetes.
3. Implement Horizontal Pod Autoscaling (HPA).
4. Simulate hybrid-cloud deployment with primary and backup clusters.
5. Configure NGINX for automatic failover.
6. Apply cost optimization techniques and measure resource usage.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| Redis | Visitor count storage |
| Docker | Containerization |
| Docker Compose | Local multi-container deployment |
| Kubernetes | Container orchestration |
| Minikube | Local Kubernetes clusters |
| kubectl | Kubernetes management |
| NGINX | Reverse proxy and failover |
| HPA | Automatic pod scaling |
| Gunicorn | Python application server |

## 🏗️ Architecture

### Normal Kubernetes Deployment

User Browser → Kubernetes NodePort Service → Flask Pods → Redis Service → Redis Pod

### Hybrid-Cloud Simulation

User → NGINX Reverse Proxy
- Primary: Private Minikube Cluster
- Backup: Public Minikube Cluster

Both clusters contain Flask application replicas and an independent Redis deployment.

**Note:** The private and public cloud environments are simulated using two separate local Minikube clusters. They are not actual deployments on commercial cloud providers.

## 📁 Project Structure

```text
cloud_project/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── k8s.yaml
├── hpa.yaml
├── nginx.conf
├── .gitignore
└── README.md
```

## 🚀 Task 1: Docker Containerization

The Flask application is containerized using a Dockerfile based on `python:3.12-slim`.

Dependencies are installed using pip with `--no-cache-dir` to avoid retaining unnecessary package cache files.

### Run using Docker Compose

Clone the repository:

```bash
git clone https://github.com/shikharawasthi3500/cloud_project.git
cd cloud_project
```

Build and start the application:

```bash
docker compose up --build -d
```

Open:

```text
http://localhost:5000
```

Stop the application:

```bash
docker compose down
```

## ☸️ Task 2: Kubernetes Deployment

The application is deployed using Kubernetes Deployments and Services.

### Components

- Redis Deployment: 1 replica
- Flask Deployment: 2 initial replicas
- Redis Service: ClusterIP
- Flask Service: NodePort
- NodePort: 30080
- Readiness and liveness probes: `/health`

### Deployment Commands

Start Minikube:

```bash
minikube start
```

Build the application image:

```bash
minikube image build -t visitor-counter:v1 .
```

Apply Kubernetes configuration:

```bash
kubectl apply -f k8s.yaml
```

Check Pods:

```bash
kubectl get pods
```

Check Services:

```bash
kubectl get services
```

Access the application:

```bash
minikube service visitor-web --url
```

### Self-Healing Verification

Delete one Flask Pod:

```bash
kubectl delete pod POD_NAME
```

Check Pods again:

```bash
kubectl get pods
```

Kubernetes automatically creates a replacement Pod to maintain the desired replica count.

## 📈 Task 3: Horizontal Pod Autoscaling

HPA automatically adjusts the number of Flask application replicas based on CPU utilization.

### HPA Configuration

- Minimum replicas: 2
- Maximum replicas: 6
- CPU utilization target: 50%

Apply HPA:

```bash
kubectl apply -f hpa.yaml
```

Check autoscaling:

```bash
kubectl get hpa
```

Monitor scaling:

```bash
kubectl get hpa -w
```

### Load Testing

A BusyBox deployment was used to generate HTTP requests:

```bash
kubectl create deployment load-generator --image=busybox:1.36 --replicas=5 -- /bin/sh -c "while true; do wget -q -O- http://visitor-web:5000/ > /dev/null; done"
```

Remove the load generator after testing:

```bash
kubectl delete deployment load-generator
```

**Observed result:** The application scaled from 2 replicas to 6 replicas under heavy load. After load generation stopped, the HPA could scale back toward its minimum replica count.

## 🌐 Task 4: Hybrid Cloud with Failover

Hybrid-cloud behavior was simulated using two separate Minikube clusters.

| Cluster | Role |
|---|---|
| minikube | Private cluster (Primary) |
| public-cluster | Public cluster (Backup) |

Both clusters run the Flask application and Redis.

### NGINX Reverse Proxy

NGINX is configured to send requests to the private cluster first. The public cluster is configured as a backup upstream.

The application endpoints were exposed locally through Kubernetes port forwarding.

Private cluster:

```bash
kubectl --context=minikube port-forward service/visitor-web 5001:5000 --address=0.0.0.0
```

Public cluster:

```bash
kubectl --context=public-cluster port-forward service/visitor-web 5002:5000 --address=0.0.0.0
```

Start the NGINX container:

```bash
docker run -d --name visitor-nginx -p 8080:80 -v "${PWD}/nginx.conf:/etc/nginx/nginx.conf:ro" nginx:alpine
```

Access the application through NGINX:

```text
http://localhost:8080
```

### Failover Testing

1. Start both Minikube clusters.
2. Verify that both application endpoints are healthy.
3. Access the application through NGINX.
4. Stop the primary cluster:

```bash
minikube stop -p minikube
```

5. Test the NGINX endpoint again:

```bash
curl http://localhost:8080/health
```

**Observed result:** After the primary cluster was stopped, NGINX continued returning HTTP 200 OK with Redis connected through the backup cluster.

**Important limitation:** Each cluster uses its own Redis instance. Visitor counts are therefore not synchronized between clusters, and this setup does not guarantee zero data loss.

## 💰 Task 5: Cost Optimization

Three optimization approaches were demonstrated.

### 1. Docker Image Optimization

- Used the lightweight `python:3.12-slim` base image.
- Used `pip install --no-cache-dir`.
- Avoided unnecessary application files in the image.

Measured Docker image disk usage: **204 MB**.

### 2. Kubernetes Resource Right-Sizing

Flask resource requests were reduced based on observed usage.

| Resource | Before | After |
|---|---:|---:|
| CPU request per Pod | 100m | 50m |
| Memory request per Pod | 128Mi | 96Mi |
| CPU limit per Pod | 500m | 300m |
| Memory limit per Pod | 256Mi | 192Mi |

This reduced requested CPU by 50% and requested memory by 25% per Flask Pod.

### 3. Horizontal Pod Autoscaling

Instead of maintaining a fixed number of application replicas, HPA adjusts replicas according to demand.

- Idle configuration: 2 replicas
- Maximum configured replicas: 6
- CPU target: 50%

This avoids reserving the maximum number of application replicas when traffic is low.

**Note:** These are measured local resource optimizations. Monetary cloud savings have not been calculated because the project runs on local Minikube clusters.

## 🔍 Application Health Check

The application provides a health endpoint:

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{
  "redis": "connected",
  "status": "healthy"
}
```

## ⚠️ Limitations

- Hybrid-cloud deployment is simulated locally using Minikube.
- Redis does not currently use persistent volumes.
- Redis data is independent between the two clusters.
- No actual cloud-provider billing comparison is available.
- NGINX failover depends on the local port-forwarding processes remaining active.

## 🔮 Future Improvements

- Deploy on AWS, Microsoft Azure or Google Cloud.
- Configure Redis persistent storage and replication.
- Synchronize application data between clusters.
- Implement Prometheus and Grafana monitoring.
- Configure CI/CD using GitHub Actions.
- Add HTTPS and a custom domain.

## 📚 Learning Outcomes

Through this project, I learned:

- Docker image creation and containerization.
- Multi-container deployment using Docker Compose.
- Kubernetes Deployments, Pods and Services.
- Kubernetes self-healing and health probes.
- Horizontal Pod Autoscaling.
- Hybrid-cloud architecture and failover simulation.
- NGINX reverse proxy configuration.
- Resource monitoring and optimization.

## 🔗 Project Repository

GitHub: https://github.com/shikharawasthi3500/cloud_project

**Project:** Cloud-Based Visitor Counter Using Flask, Redis, Docker and Kubernetes

**Purpose:** Academic Cloud Computing Project
