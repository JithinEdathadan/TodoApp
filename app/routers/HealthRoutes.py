from fastapi import APIRouter
from starlette import status
router = APIRouter(
    prefix="/healthy",
    tags=['Health Check']
)

@router.get("/",status_code=status.HTTP_200_OK)
async def health_check():
    return {"status":"healthy"}
