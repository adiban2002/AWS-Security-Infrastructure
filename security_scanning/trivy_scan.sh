IMAGE_NAME=$1

if [ -z "$IMAGE_NAME" ]; then
    echo "Error: No image name provided."
    exit 1
fi

echo "----------------------------------------"
echo "Starting Trivy Security Scan for: $IMAGE_NAME"
echo "----------------------------------------"

if [[ -f "./trivy" ]]; then
    TRIVY_BIN="./trivy"
elif command -v trivy &> /dev/null; then
    TRIVY_BIN="trivy"
else
    echo "Trivy not found. Installing locally..."
    wget https://github.com/aquasecurity/trivy/releases/download/v0.51.1/trivy_0.51.1_Linux-64bit.tar.gz
    tar zxvf trivy_0.51.1_Linux-64bit.tar.gz
    chmod +x trivy
    TRIVY_BIN="./trivy"
fi

$TRIVY_BIN image --severity HIGH,CRITICAL --format table "$IMAGE_NAME"

echo "----------------------------------------"
echo "Trivy Scan Completed Successfully!"
echo "----------------------------------------"