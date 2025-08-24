
# travel-mini

Travel-mini: a small Minikube-ready demo with a Gateway (frontend), Flights service and Hotels service.

Features:
- Flask microservices (gateway, flights, hotels)
- HTML/CSS frontend served by gateway, which proxies to internal services
- Kubernetes manifests: Namespace, ConfigMap, Secret, Deployments, Services, Ingress
- Liveness/readiness probes and resource requests/limits
- Makefile helpers to build images in Minikube and deploy
- Basic pytest tests for each service
- Jenkinsfile example for CI/CD (build/push/deploy)

Prereqs:
- minikube
- kubectl
- docker
- (optional) Jenkins for CI/CD

Quick local steps (Minikube)
1. Start minikube and enable ingress:
   minikube start --memory=4096 --cpus=2
   minikube addons enable ingress

2. Build Docker images inside Minikube:
   make minikube-build

3. Deploy manifests:
   make deploy

4. Access the app via Ingress host:
   - Get Minikube IP: minikube ip
   - Add an entry to /etc/hosts: <MINIKUBE_IP> travel.local
   - Open: http://travel.local

Alternatively, port-forward:
   kubectl -n travel port-forward svc/gateway 8080:80
   Open: http://localhost:8080

Makefile targets
- minikube-build : builds and tags images inside Minikube
- deploy : applies k8s manifests
- delete : removes resources
- test : run pytest for all services

Security note:
- This demo stores a simple SECRET in k8s Secret for demo purposes. Do not store production secrets in plain YAML.

If you want CI/CD tips for Jenkins (credentials, kubeconfig), see Jenkinsfile.
