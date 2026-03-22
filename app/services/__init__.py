# Makes services a package

from .aws_service import parameter_store, secrets_manager

__all__ = ["parameter_store", "secrets_manager"]