import boto3
import logging
from botocore.exceptions import ClientError, NoCredentialsError

from app.utils.config import settings

logger = logging.getLogger("aws_service")

class AWSClientFactory:

    @staticmethod
    def get_ssm_client():
        return boto3.client("ssm", region_name=settings.AWS_REGION)

    @staticmethod
    def get_secrets_client():
        return boto3.client("secretsmanager", region_name=settings.AWS_REGION)


class ParameterStoreService:
    def __init__(self):
        self.client = AWSClientFactory.get_ssm_client()

    def get_parameter(self, name: str, decrypt: bool = True) -> str:
        try:
            full_name = f"{settings.PARAMETER_PREFIX}/{name}"

            response = self.client.get_parameter(
                Name=full_name,
                WithDecryption=decrypt
            )

            value = response["Parameter"]["Value"]
            logger.info(f"Fetched parameter: {full_name}")

            return value

        except NoCredentialsError:
            logger.warning("AWS credentials not configured")
            return "mock-value"

        except ClientError as e:
            logger.error(f"SSM error: {str(e)}")
            raise

class SecretsManagerService:
    def __init__(self):
        self.client = AWSClientFactory.get_secrets_client()

    def get_secret(self, secret_name: str = None) -> str:
        try:
            secret_name = secret_name or settings.SECRET_NAME

            response = self.client.get_secret_value(
                SecretId=secret_name
            )

            secret = response.get("SecretString", "")
            logger.info(f"Fetched secret: {secret_name}")

            return secret

        except NoCredentialsError:
            logger.warning("AWS credentials not configured")
            return "mock-secret"

        except ClientError as e:
            logger.error(f"Secrets Manager error: {str(e)}")
            raise

parameter_store = ParameterStoreService()
secrets_manager = SecretsManagerService()