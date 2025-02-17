from typing import Annotated

from fastapi import Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.task.repository import TaskRepository
from api.api_v1.task.service import TaskService
from core.database.db_helper import db_helper
from core.database.models import Task


async def get_task_repository(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> TaskRepository:
    return TaskRepository(session=session)


async def get_task_service(
    repo: Annotated[TaskRepository, Depends(get_task_repository)],
) -> TaskService:
    return TaskService(repo=repo)


async def get_task_by_id(
    repo: Annotated[TaskRepository, Depends(get_task_repository)],
    task_id: Annotated[int, Path],
) -> Task:
    task = await repo.get_task(task_id=task_id)
    if task is not None:
        return task
    raise HTTPException(status_code=404, detail="Task not found")
