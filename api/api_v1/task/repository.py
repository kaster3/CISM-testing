from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.task.schemas import TaskCreate, TaskUpdatePartial
from core.database.models import Task
from core.database.models.enums.task_status_enum import TaskStatusEnum


class TaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_task(self, task_id: int) -> Task | None:
        task = await self.session.get(Task, task_id)
        return task

    async def get_all_tasks(self) -> list[Task]:
        stmt = select(Task)
        tasks = await self.session.scalars(stmt)
        return list(tasks)

    async def get_tasks_by_status(self, task_status: TaskStatusEnum) -> list[Task]:
        stmt = select(Task).where(Task.status == task_status)
        tasks = await self.session.scalars(stmt)
        return list(tasks)

    async def create_task(self, task_in: TaskCreate) -> Task:
        task = Task(**task_in.model_dump())
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def update_task(
        self,
        task: Task,
        task_in: TaskUpdatePartial,
    ) -> Task:
        for name, value in task_in.model_dump(exclude_unset=True).items():
            setattr(task, name, value)
        await self.session.commit()
        return task
