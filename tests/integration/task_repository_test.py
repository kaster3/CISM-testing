import pytest
from syrupy import SnapshotAssertion, snapshot  # noqa: F401

from api.api_v1.task.repository import TaskRepository
from api.api_v1.task.schemas import TaskCreate, TaskUpdatePartial
from core.database.models import Task
from core.database.models.enums.task_status_enum import TaskStatusEnum


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "task_id, expected",
    [
        (1, True),
        (2, True),
        (3, True),
        (4, False),
    ],
)
async def test_get_task_by_id(
    init_models: None,
    create_tasks: None,
    task_id: int,
    expected: bool,
    task_repository: TaskRepository,
    snapshot: SnapshotAssertion,  # noqa: 811
):
    task = await task_repository.get_task(task_id=task_id)

    if expected:
        assert task is not None
        snapshot.assert_match(task)
    else:
        assert task is None


@pytest.mark.asyncio
async def test_get_all_tasks(
    init_models: None,
    create_tasks: None,
    task_repository: TaskRepository,
    snapshot: SnapshotAssertion,  # noqa: 811
):
    tasks = await task_repository.get_all_tasks()
    snapshot.assert_match(tasks)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status, quantity",
    [
        (TaskStatusEnum.NEW, 2),
        (TaskStatusEnum.IN_PROGRESS, 1),
        (TaskStatusEnum.COMPLETED, 0),
        (TaskStatusEnum.ERROR, 0),
    ],
)
async def test_get_tasks_by_status(
    init_models: None,
    create_tasks: None,
    status: TaskStatusEnum,
    quantity: int,
    task_repository: TaskRepository,
    snapshot: SnapshotAssertion,  # noqa: 811
):
    tasks = await task_repository.get_tasks_by_status(task_status=status)
    assert len(tasks) == quantity
    snapshot.assert_match(tasks)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "task_id, task_data",
    [
        (1, TaskCreate(name="Test 1")),
        (2, TaskCreate(name="Test 2")),
    ],
)
async def test_create_task(
    init_models: None,
    task_id: int,
    task_data: TaskCreate,
    task_repository: TaskRepository,
    snapshot: SnapshotAssertion,  # noqa: 811
):

    await task_repository.create_task(task_data)
    task = await task_repository.get_task(task_id=task_id)
    snapshot.assert_match(task)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "task_data",
    [
        TaskUpdatePartial(name="Test 1", status=TaskStatusEnum.IN_PROGRESS),
        TaskUpdatePartial(name="Test 2", status=TaskStatusEnum.ERROR),
    ],
)
async def test_update_task(
    init_models: None,
    get_task_by_id: Task,
    task_data: TaskUpdatePartial,
    task_repository: TaskRepository,
    snapshot: SnapshotAssertion,  # noqa: 811
):

    updated_task = await task_repository.update_task(
        task=get_task_by_id,
        task_in=task_data,
    )

    task = await task_repository.get_task(task_id=updated_task.id)
    snapshot.assert_match(task)
