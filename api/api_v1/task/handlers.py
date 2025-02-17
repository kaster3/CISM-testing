from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from core.database.models import Task
from core.database.models.enums.task_status_enum import TaskStatusEnum

from .dependencies import get_task_by_id, get_task_service
from .schemas import TaskCreate, TaskSchema
from .service import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["Task"],
)


@router.get(
    "/{task_id}",
    response_model=TaskSchema,
    status_code=status.HTTP_200_OK,
)
async def get_task_by_id(
    task: Annotated[Task, Depends(get_task_by_id)],
):
    return task


@router.get(
    "/",
    response_model=list[TaskSchema],
    status_code=status.HTTP_200_OK,
)
async def get_tasks(
    service: Annotated[TaskService, Depends(get_task_service)],
    task_status: TaskStatusEnum = Query(None),
):
    tasks = await service.get_tasks(task_status=task_status)
    return tasks


@router.post(
    "/",
    response_model=TaskCreate,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_in: TaskCreate,
    service: Annotated[TaskService, Depends(get_task_service)],
):
    task = await service.create_task(task_in=task_in)
    return task
