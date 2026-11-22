# ☁️ Cloud-Based Visitor Counter Using Docker, Kubernetes and Redis

A cloud-native web application that tracks website visitors using **Python Flask and Redis**, containerized with **Docker** and deployed using **Kubernetes**.

## 📌 Project Overview

This project demonstrates how a web application can be containerized and deployed in a Kubernetes environment.

Whenever a user visits the website, the visitor count increases automatically. Redis stores the visitor count centrally, allowing multiple Flask application replicas to share the same counter.

The application is deployed locally using Minikube.

## 🎯 Objectives

- Build a web application using Python Flask.
- Store visitor counts using Redis.
- Containerize the application using Docker.
- Manage multiple application replicas using Kubernetes.
- Implement Kubernetes Services for application communication.
- Configure health checks using readiness and liveness probes.
- Understand container orchestration and self-healing.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| Redis | In-memory database for visitor count |
| Docker | Application containerization |
| Docker Compose | Local multi-container setup |
| Kubernetes | Container orchestration |
| Minikube | Local Kubernetes cluster |
| Gunicorn | Python WSGI application server |

## 🏗️ Project Architecture

```text
                 User / Browser
                       |
                       |
                 NodePort :30080
                       |
                       |
                Kubernetes Service
                       |
                 ----------------
                 |              |
              Flask Pod      Flask Pod
                 |              |
                 ------+-------
                       |
                       |
                Redis Service
                       |
                       |
                  Redis Pod
                       |
                       |
               visitor_count
```

### How It Works

1. A user opens the visitor counter website.
2. Kubernetes Service routes the request to one of the Flask application Pods.
3. Flask receives the request and communicates with Redis.
4. Redis increments the `visitor_count` key.
5. Flask displays the updated visitor count on the webpage.
6. Multiple Flask replicas share the same Redis counter.

## 📁 Project Structure

```text
visitor-counter/
│
├── app.py                # Flask application
├── Dockerfile            # Docker image configuration
├── docker-compose.yml    # Local multi-container setup
├── k8s.yaml              # Kubernetes deployments and services
├── requirements.txt      # Python dependencies
├── .gitignore            # Files excluded from Git
└── README.md             # Project documentation
```

## ⚙️ Prerequisites

Install the following tools before running the project:

- Python 3
- Docker Desktop
- Docker Compose
- kubectl
- Minikube
- Git

## 🚀 Running the Project Using Docker Compose

### Step 1: Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/cloud-visitor-counter.git
```

### Step 2: Navigate to the project directory

```bash
cd cloud-visitor-counter
```

### Step 3: Start the application

```bash
docker compose up --build -d
```

### Step 4: Open the application

Visit:

```text
http://localhost:5000
```

### Step 5: Stop the application

```bash
docker compose down
```

## ☸️ Kubernetes Deployment Using Minikube

### Step 1: Start Minikube

```bash
minikube start
```

### Step 2: Build the Docker image inside Minikube

```bash
minikube image build -t visitor-counter:v1 .
```

### Step 3: Apply Kubernetes configuration

```bash
kubectl apply -f k8s.yaml
```

### Step 4: Check Pods

```bash
kubectl get pods
```

### Step 5: Check Deployments

```bash
kubectl get deployments
```

### Step 6: Check Services

```bash
kubectl get services
```

### Step 7: Access the application

```bash
minikube service visitor-web --url
```

Open the generated URL in your browser.

## 🔍 Testing and Verification

### Check application Pods

```bash
kubectl get pods
```

### Check visitor count in Redis

```bash
kubectl exec deployment/redis-deployment -- redis-cli GET visitor_count
```

### Check Redis keys

```bash
kubectl exec deployment/redis-deployment -- redis-cli KEYS "*"
```

### Check Redis database size

```bash
kubectl exec deployment/redis-deployment -- redis-cli DBSIZE
```

### Check application logs

```bash
kubectl logs deployment/visitor-web
```

### Test Kubernetes self-healing

Delete one application Pod:

```bash
kubectl delete pod POD_NAME
```

Check the Pods again:

```bash
kubectl get pods
```

Kubernetes automatically creates a replacement Pod to maintain the desired replica count.

## ✨ Key Features

- **Real-time Visitor Counting:** Automatically increments the visitor count whenever the homepage is accessed.
- **Centralized Data Storage:** Redis stores a shared visitor count for all Flask replicas.
- **Containerization:** Docker packages the application and its dependencies.
- **Scalability:** Kubernetes manages multiple Flask application replicas.
- **Self-Healing:** Kubernetes replaces deleted or failed Pods to maintain the desired replica count.
- **Health Monitoring:** Readiness and liveness probes check application health through the `/health` endpoint.
- **Service Discovery:** Kubernetes Services enable communication between Flask and Redis.

## 📊 Kubernetes Configuration

| Component | Configuration |
|---|---|
| Redis Deployment | 1 replica |
| Flask Deployment | 2 replicas |
| Redis Service | ClusterIP |
| Flask Service | NodePort |
| NodePort | 30080 |
| Flask Port | 5000 |
| Redis Port | 6379 |
| Application Image | visitor-counter:v1 |

## ⚠️ Limitations

- The application currently runs on a local Minikube cluster rather than a public cloud platform.
- Redis is configured without persistent storage. Visitor data may be lost if the Redis Pod or process restarts.
- The project does not currently include authentication or advanced security features.
- No external monitoring or automated CI/CD pipeline is configured.

## 🔮 Future Improvements

- Deploy the application on AWS, Azure or Google Cloud.
- Add Redis PersistentVolume and PersistentVolumeClaim.
- Implement Horizontal Pod Autoscaling.
- Add monitoring using Prometheus and Grafana.
- Configure CI/CD using GitHub Actions.
- Add a custom domain and HTTPS support.
- Improve frontend design and add visitor analytics.

## 👨‍💻 Learning Outcomes

Through this project, I learned:

- Building web applications using Flask.
- Using Redis for centralized data storage.
- Creating Docker images and containers.
- Managing multi-container applications.
- Deploying applications using Kubernetes.
- Working with Kubernetes Pods, Deployments and Services.
- Implementing health probes and understanding self-healing.

## 📚 References

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Redis Documentation](https://redis.io/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)

---

**Project:** Cloud-Based Visitor Counter Using Docker, Kubernetes and Redis

**Purpose:** Academic Cloud Computing Project