AWS_REGION="ap-south-1"
ACCOUNT_ID="800557028391"
REPO_NAME="devsecops-app"
IMAGE_NAME="devsecops-app"
TAG="latest"

ECR_URI="$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME"

echo "Starting ECR Push Process..."

echo "Logging into ECR..."
aws ecr get-login-password --region $AWS_REGION | \
docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

echo "Building Docker image..."
docker build -t $IMAGE_NAME -f docker/Dockerfile .

echo "Tagging image..."
docker tag $IMAGE_NAME:$TAG $ECR_URI:$TAG


echo "Pushing image to ECR..."
docker push $ECR_URI:$TAG

echo "Successfully pushed to ECR: $ECR_URI:$TAG"