import boto3
import json
from botocore.exceptions import ClientError

class SecretsManager:
    def __init__(self, region_name="ap-south-1"):
        self.client = boto3.client('secretsmanager', region_name=region_name)

    def get_secret(self, secret_id):
        try:
            response = self.client.get_secret_value(SecretId=secret_id)
            
            if 'SecretString' in response:
                return json.loads(response['SecretString'])
            else:
                print(f"Secret {secret_id} does not contain a string value.")
                return None
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            print(f"Error fetching secret {secret_id}: {error_code}")
            return None
        except json.JSONDecodeError:
            print(f"Failed to decode JSON from secret: {secret_id}")
            return None

secrets_provider = SecretsManager()