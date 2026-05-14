PROFILE="devsecops-user"
KUBE_DIR="../kubernetes"

echo "Deploying manifests from $KUBE_DIR to devsecops-eks..."

if [ -d "$KUBE_DIR" ]; then
    kubectl apply -f "$KUBE_DIR/"
    echo "Kubernetes deployment successful."
else
    echo "Error: '$KUBE_DIR' directory not found!"
    exit 1
fi

echo -e "\n Resource Status:"
kubectl get deployments,services