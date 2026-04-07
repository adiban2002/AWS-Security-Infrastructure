from fastapi import APIRouter, Depends, HTTPException, status
import logging

from app.services.aws_service import parameter_store, secrets_manager
from app.services.auth.routes import router as auth_router
from app.services.user.routes import router as user_router
from app.services.payment.routes import router as payment_router
from app.services.notifications.routes import router as notifications_router

logger = logging.getLogger("routes")

router = APIRouter(
    prefix="/api/v1",
    tags=["API"],
)


def verify_request():
    return True


@router.get("/public", status_code=status.HTTP_200_OK)
def public_endpoint():
    logger.info("Public endpoint accessed")

    return {
        "message": "Public endpoint working",
        "status": "success"
    }


@router.get("/secure-data", dependencies=[Depends(verify_request)])
def secure_data():
    logger.info("Secure endpoint accessed")

    try:
        secret = secrets_manager.get_secret()

        return {
            "message": "Secure data fetched",
            "secret": secret,
            "status": "success"
        }

    except Exception as e:
        logger.error(f"Error fetching secret: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Failed to fetch secure data"
        )


@router.get("/config")
def get_config():
    logger.info("Fetching configuration")

    try:
        value = parameter_store.get_parameter("app-config")

        return {
            "config": value,
            "status": "success"
        }

    except Exception as e:
        logger.error(f"Error fetching config: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Failed to fetch configuration"
        )


@router.get("/health")
def route_health():
    return {"route": "healthy"}


router.include_router(auth_router)
router.include_router(user_router)
router.include_router(payment_router)
router.include_router(notifications_router)