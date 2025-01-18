from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=["Home"],
)

# Home
@router.get("/")
async def root():
    return {"msg": "Bem-vindo ao FastAPI!"}