DEFAULT_FUNCTION_NAME="DevSecOps-Edge-Security"
DEFAULT_REGION="us-east-1"
DEFAULT_PROFILE="default"


FUNCTION_NAME="${1:-$DEFAULT_FUNCTION_NAME}"
PROFILE="${2:-$DEFAULT_PROFILE}"
REGION="$DEFAULT_REGION" 
ROLE_NAME="${FUNCTION_NAME}-Role"

echo "-------------------------------------------------------"
echo " Starting Dynamic Edge Deployment for: $FUNCTION_NAME"
echo " Using AWS Profile: $PROFILE"
echo " Target Region: $REGION"
echo "-------------------------------------------------------"


if ! aws configure list-profiles | grep -q "^$PROFILE$"; then
    echo " Error: AWS Profile '$PROFILE' not found!"
    echo "Available profiles: $(aws configure list-profiles | xargs)"
    exit 1
fi


echo " Checking IAM Role: $ROLE_NAME..."
ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text --profile $PROFILE 2>/dev/null)

if [ -z "$ROLE_ARN" ]; then
    echo "Creating new IAM Role..."
    aws iam create-role --role-name $ROLE_NAME \
        --assume-role-policy-document file://trust_policy.json \
        --profile $PROFILE > /dev/null
    
    aws iam attach-role-policy --role-name $ROLE_NAME \
        --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole \
        --profile $PROFILE
    
    echo " Waiting for IAM propagation (10s)..."
    sleep 10
    ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text --profile $PROFILE)
else
    echo " Role already exists."
fi


echo " Packaging Lambda function..."
zip -q function.zip lambda_handler.py
echo " Zip created: function.zip"


if aws lambda get-function --function-name "$FUNCTION_NAME" --region "$REGION" --profile "$PROFILE" > /dev/null 2>&1; then
    echo " Updating existing Lambda function code..."
    aws lambda update-function-code --function-name "$FUNCTION_NAME" \
        --zip-file fileb://function.zip --region "$REGION" --profile "$PROFILE" > /dev/null
else
    echo " Creating new Lambda function..."
    aws lambda create-function --function-name "$FUNCTION_NAME" \
        --runtime python3.9 --handler lambda_handler.lambda_handler \
        --role "$ROLE_ARN" --zip-file fileb://function.zip \
        --region "$REGION" --profile "$PROFILE" > /dev/null
fi


echo " Publishing new version..."
VERSION_DATA=$(aws lambda publish-version --function-name "$FUNCTION_NAME" --region "$REGION" --profile "$PROFILE")
VERSION=$(echo $VERSION_DATA | grep -oP '(?<="Version": ")[^"]*' || echo $VERSION_DATA | sed -n 's/.*"Version": "\(.*\)".*/\1/p')


ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text --profile $PROFILE)
FINAL_ARN="arn:aws:lambda:$REGION:$ACCOUNT_ID:function:$FUNCTION_NAME:$VERSION"

echo "-------------------------------------------------------"
echo " DEPLOYMENT SUCCESSFUL!"
echo " Function Name: $FUNCTION_NAME"
echo " Version: $VERSION"
echo " Lambda@Edge ARN:"
echo "$FINAL_ARN"
echo "-------------------------------------------------------"
echo "Copy the ARN above and paste it into your CloudFront Trigger settings."

rm function.zip