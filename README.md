# Kubernetes Microservices Platform (EKS-ready)

This repository demonstrates a small **microservices platform** designed for **Amazon EKS** (also runnable on any Kubernetes cluster).
It includes:

- Two containerized microservices (`user-service`, `order-service`)
- Kubernetes manifests (Deployments, Services, ConfigMap)
- Simple service-to-service communication
- Health endpoints for readiness/liveness probes
- Optional guidance for exposing via AWS LoadBalancer / Ingress

## Tech Stack
- Python (Flask)
- Docker
- Kubernetes (EKS)
- GitHub Actions (build & push images to Docker Hub)

## Architecture (high level)
```
Client
  |
  v
K8s Service (LoadBalancer / Ingress)
  |
  +--> user-service (Flask)
  |
  +--> order-service (Flask) ---> calls user-service
```

## Local build
### Build images
```bash
docker build -t <dockerhub-user>/user-service:1.0 services/user-service
docker build -t <dockerhub-user>/order-service:1.0 services/order-service
```

### Run locally (Docker)
```bash
docker network create micro-net || true
docker run -d --name user-service --network micro-net -p 5001:5000 <dockerhub-user>/user-service:1.0
docker run -d --name order-service --network micro-net -e USER_SERVICE_URL=http://user-service:5000 -p 5002:5000 <dockerhub-user>/order-service:1.0
curl http://localhost:5002/order/123
```

## Deploy to Kubernetes (EKS)
1) Update image names in manifests to your Docker Hub namespace.
2) Apply manifests:
```bash
kubectl apply -f k8s/
kubectl get pods -n micro
kubectl get svc  -n micro
```

### Expose externally (simple)
This repo includes a `Service` of type `LoadBalancer` for `order-service`.
On EKS, this will provision an AWS load balancer automatically.

```bash
kubectl get svc order-service -n micro
```

## GitHub Actions
A sample workflow is provided under `.github/workflows/dockerhub-build-push.yml`.
Add these secrets in GitHub:
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

Then push to `main` to build/push both images.

## Notes
For production-grade ingress on EKS, many teams use:
- AWS Load Balancer Controller + Ingress resources
- ExternalDNS
- cert-manager for TLS
Those are optional and not required for this demo.
