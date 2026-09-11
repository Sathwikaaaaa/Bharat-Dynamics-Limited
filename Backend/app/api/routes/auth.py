from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database.database import get_db
from app.api.dependencies.auth_dependencies import require_role
from app.database.models import User
from app.schemas.auth_schema import (
    UserRegister,
    UserLogin,
    TokenResponse,
    UserResponse
)
from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token
)
from app.utils.logger import get_logger


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

logger = get_logger(__name__)


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    user = User(
        email=user_data.email,
        password_hash=hash_password(
            user_data.password
        ),
        role="user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info(
        "New user registered: %s",
        user.email
    )

    return UserResponse(
        id=user.id,
        email=user.email,
        role=user.role
    )


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    token = create_access_token({
        "sub": user.email,
        "role": user.role
    })

    logger.info("User logged in: %s", user.email)

    return TokenResponse(
        access_token=token,
        token_type="bearer"
    )

@router.get("/admin")
def admin_dashboard(
    current_user: User = Depends(
        require_role("admin")
    )
):
    return {
        "message": "Welcome admin",
        "email": current_user.email,
        "role": current_user.role
    }