import boto3
from botocore.exceptions import ClientError

class ParameterStore:
    def __init__(self, region_name="ap-south-1"):
        self.client = boto3.client('ssm', region_name=region_name)

    def get_parameter(self, parameter_name, decrypt=False):
        try:
            response = self.client.get_parameter(
                Name=parameter_name, 
                WithDecryption=decrypt
            )
            return response['Parameter']['Value']
        except ClientError as e:
            print(f"Error fetching parameter {parameter_name}: {e.response['Error']['Code']}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
        
ssm_manager = ParameterStore()