PROFILE="devsecops-user"
CLUSTER="devsecops-eks"
REGION="ap-south-1"

echo "Setting up environment for $CLUSTER..."
aws eks update-kubeconfig --name $CLUSTER --region $REGION --profile $PROFILE
echo "Kubeconfig updated. Current context set to $CLUSTER."