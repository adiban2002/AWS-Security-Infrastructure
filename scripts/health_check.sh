CLUSTER="devsecops-eks"
PROFILE="devsecops-user"

echo "---------------------------------------"
echo "Health Check: $CLUSTER"
echo "---------------------------------------"

echo "[Nodes]"
kubectl get nodes

echo -e "\n[Pods - All Namespaces]"
kubectl get pods -A

echo -e "\n[Services & LoadBalancers]"
kubectl get svc -A
echo "---------------------------------------"