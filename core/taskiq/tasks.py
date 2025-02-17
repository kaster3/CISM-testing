import asyncio
import logging
import random
from typing import Annotated

from taskiq import TaskiqDepends

from api.api_v1.task.dependencies import get_task_repository
from api.api_v1.task.repository import TaskRepository
from api.api_v1.task.schemas import TaskUpdatePartial
from core.database.models.enums.task_status_enum import TaskStatusEnum
from .broker import broker


log = logging.getLogger(__name__)


@broker.task
async def task_process(
        task_in: int,
        repo: Annotated[TaskRepository, TaskiqDepends(get_task_repository)],
) -> None:
    log.info("Starting task process")
    task = await repo.get_task(task_id=task_in)
    task = await repo.update_task(
        task=task, task_in=TaskUpdatePartial(status=TaskStatusEnum.IN_PROGRESS)
    )
    log.info("Updated task with status: %s" % task.status.value)
    await asyncio.sleep(random.randint(5, 10))
    finished_status = TaskStatusEnum.COMPLETED if random.random() < 0.5 else TaskStatusEnum.ERROR
    task = await repo.update_task(task=task, task_in=TaskUpdatePartial(status=finished_status))
    log.info("Completed task with status: %s" % task.status.value)
