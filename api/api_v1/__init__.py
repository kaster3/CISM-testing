from fastapi import APIRouter

from core import settings

from .task.handlers import router as task_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

for rout in (task_router,):
    router.include_router(
        router=rout,
    )


@router.get("")
async def root():
    return {"message": "this path is http://127.0.0.1:8000/api/v1"}
