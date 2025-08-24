 
# travel-mini

Travel-mini: a small Minikube-ready demo with a Gateway (frontend), Flights service and Hotels service.

Features:
- Flask microservices (gateway, flights, hotels)
- HTML/CSS frontend served by gateway, which proxies to internal services
- Kubernetes manifests: Namespace, ConfigMap, Secret, Deployments, Services, Ingress
- Liveness/readiness probes and resource requests/limits (you can increase the values of both)
- Basic pytest tests for each service


Prereqs:
- minikube
- kubectl
- docker

Quick local steps (Minikube)
1. Start minikube and enable ingress:
   minikube start 
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

# Image names and tag
GATEWAY_IMAGE ?= travel-gateway:dev
FLIGHTS_IMAGE ?= travel-flights:dev
HOTELS_IMAGE ?= travel-hotels:dev
NAMESPACE ?= travel

minikube-docker-env:
	@echo "Run the following in your shell to use minikube's docker daemon:"
	@echo "  eval $$(minikube -p minikube docker-env)"

minikube-build:
	# Build images inside minikube docker daemon
	@echo "Building images inside Minikube's Docker daemon..."
	@eval $$(minikube -p minikube docker-env) && \
	docker build -t $(GATEWAY_IMAGE) ./services/gateway && \
	docker build -t $(FLIGHTS_IMAGE) ./services/flights && \
	docker build -t $(HOTELS_IMAGE) ./services/hotels

deploy:
	kubectl apply -f k8s/namespace.yaml
	kubectl -n $(NAMESPACE) apply -f k8s/configmap.yaml
	kubectl -n $(NAMESPACE) apply -f k8s/secret.yaml
	kubectl -n $(NAMESPACE) apply -f k8s/flights-deployment.yaml 
	kubectl -n $(NAMESPACE) apply -f k8s/hotels-deployment.yaml
	kubectl -n $(NAMESPACE) apply -f k8s/gateway-deployment.yaml
	kubectl -n $(NAMESPACE) apply -f k8s/flights-service.yaml
	kubectl -n $(NAMESPACE) apply -f k8s/hotels-service.yaml
	kubectl -n $(NAMESPACE) apply -f k8s/gateway-service.yaml
	-kubectl -n $(NAMESPACE) apply -f k8s/ingress.yaml

delete:
	kubectl -n $(NAMESPACE) delete -f k8s/ingress.yaml || true
	kubectl -n $(NAMESPACE) delete -f k8s/gateway-service.yaml || true
	kubectl -n $(NAMESPACE) delete -f k8s/hotels-service.yaml || true
	kubectl -n $(NAMESPACE) delete -f k8s/flights-service.yaml || true
	kubectl -n $(NAMESPACE) delete -f k8s/gateway-deployment.yaml || true
	kubectl -n $(NAMESPACE) delete -f k8s/hotels-deployment.yaml || true
	kubectl -n $(NAMESPACE) delete -f k8s/flights-deployment.yaml || true
	kubectl -n $(NAMESPACE) delete -f k8s/secret.yaml || true
	kubectl -n $(NAMESPACE) delete -f k8s/configmap.yaml || true
	kubectl delete ns $(NAMESPACE) || true

test:
	python3 -m pytest -q services/gateway/tests services/flights/tests services/hotels/tests
