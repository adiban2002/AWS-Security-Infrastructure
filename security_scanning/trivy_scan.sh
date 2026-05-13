IMAGE_NAME=$1

if [ -z "$IMAGE_NAME" ]; then
    echo "Error: No image name provided."
    exit 1
fi

echo "----------------------------------------"
echo "Starting Trivy Security Scan for: $IMAGE_NAME"
echo "----------------------------------------"

if ! command -v trivy &> /dev/null; then
    echo "Trivy not found. Installing..."
    wget https://github.com/aquasecurity/trivy/releases/download/v0.49.1/trivy_0.49.1_Linux-64bit.tar.gz
    tar zxvf trivy_0.49.1_Linux-64bit.tar.gz
    sudo mv trivy /usr/local/bin/
fi


trivy image --severity HIGH,CRITICAL --format table "$IMAGE_NAME"

echo "----------------------------------------"
echo "Trivy Scan Completed Successfully!"
echo "----------------------------------------"