import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import Task


@pytest_asyncio.fixture()
async def create_tasks(db_session: AsyncSession):
    async with db_session.begin():
        smtp = text(
            """
            INSERT INTO tasks (name, status)
            VALUES ('task1', 'NEW'),
                   ('task2', 'NEW'),
                   ('task3', 'IN_PROGRESS');
            """
        )
        await db_session.execute(smtp)
        await db_session.commit()


@pytest_asyncio.fixture(params=[1, 2])
async def get_task_by_id(request, db_session: AsyncSession, create_tasks) -> Task | None:
    task_id = request.param
    task = await db_session.get(Task, task_id)
    return task
