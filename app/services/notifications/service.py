import os
import json
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Any

def send_notification(user_id: str, message: str) -> Dict[str, Any]:
    aws_region = os.getenv("AWS_REGION", "ap-south-1")
    sns_topic_arn = os.getenv("SNS_TOPIC_ARN")
    
    payload = {
        "user_id": user_id,
        "message": message,
        "metadata": {
            "source": "devsecops-notification-service",
            "engine": "FastAPI"
        }
    }
    
    if not sns_topic_arn:
        print("[ERROR] SNS_TOPIC_ARN environment variable is missing.")
        return {
            "status": "failed",
            "error_context": "SNS_TOPIC_ARN environment variable is missing."
        }

    try:
        
        sns_client = boto3.client("sns", region_name=aws_region)
        
        sns_response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=json.dumps(payload),
            Subject=f"DevSecOps Alert: System Event for User {user_id}"
        )
        
        return {
            "user_id": user_id,
            "message": message,
            "status": "sent",
            "delivery_telemetry": {
                "sns_published": True,
                "sns_message_id": sns_response.get("MessageId")
            }
        }
        
    except ClientError as e:
        print(f"[ERROR] Failed to publish event trace to SNS: {str(e)}")
        return {
            "user_id": user_id,
            "message": message,
            "status": "failed",
            "error_context": str(e)
        }