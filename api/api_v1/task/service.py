import logging

from fastapi import HTTPException

from api.api_v1.task.repository import TaskRepository
from api.api_v1.task.schemas import TaskCreate
from core.database.models import Task
from core.database.models.enums.task_status_enum import TaskStatusEnum

log = logging.getLogger(__name__)


class TaskService:
    def __init__(self, repo: TaskRepository) -> None:
        self.repo = repo


    async def get_tasks(self, task_status: TaskStatusEnum | None) -> list[Task]:
        if task_status is None:
            tasks = await self.repo.get_all_tasks()
        else:
            tasks = await self.repo.get_tasks_by_status(task_status=task_status)
        if not tasks:
            raise HTTPException(status_code=404, detail="Tasks not found")
        return tasks

    async def create_task(self, task_in: TaskCreate) -> Task:
        from core.taskiq.tasks import task_process # :)
        task = await self.repo.create_task(task_in=task_in)
        await task_process.kiq(task.id)
        log.info("Task sent to RabbitMQ")
        return task
