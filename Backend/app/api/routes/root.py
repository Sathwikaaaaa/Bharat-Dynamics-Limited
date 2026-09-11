from fastapi import APIRouter


router = APIRouter(
    tags=["Root"]
)


@router.get("/")
def root():
    return {
        "message": "Bharat Dynamics Invoice OCR API",
        "status": "running"
    }