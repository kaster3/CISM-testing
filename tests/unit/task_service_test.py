import pytest
from fastapi import HTTPException
from pytest_mock import MockerFixture

from api.api_v1.task.service import TaskService
from core.database.models.enums.task_status_enum import TaskStatusEnum


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "task_status, expected_tasks, expected_call",
    [
        (
            TaskStatusEnum.COMPLETED,
            [{"id": 1, "name": "Task 1", "status": TaskStatusEnum.COMPLETED}],
            ("get_tasks_by_status", {"task_status": TaskStatusEnum.COMPLETED}),
        ),
        (
            None,
            [
                {"id": 1, "name": "Task 1", "status": TaskStatusEnum.COMPLETED},
                {"id": 2, "name": "Task 2", "status": TaskStatusEnum.IN_PROGRESS},
            ],
            ("get_all_tasks", {}),
        ),
        (
            TaskStatusEnum.NEW,
            [],
            ("get_tasks_by_status", {"task_status": TaskStatusEnum.NEW}),
        ),
    ],
)
async def test_get_tasks(
    task_service: TaskService,
    mocker: MockerFixture,
    task_status: TaskStatusEnum | None,
    expected_tasks: list[dict],
    expected_call: tuple[str, dict],
) -> None:
    mock_repo = mocker.AsyncMock()

    if expected_call[0] == "get_tasks_by_status":
        mock_repo.get_tasks_by_status.return_value = expected_tasks
    else:
        mock_repo.get_all_tasks.return_value = expected_tasks

    task_service.repo = mock_repo

    if not expected_tasks:
        with pytest.raises(HTTPException) as exc_info:
            await task_service.get_tasks(task_status=task_status)
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Tasks not found"
    else:
        tasks = await task_service.get_tasks(task_status=task_status)
        assert tasks == expected_tasks

    repo_method = getattr(mock_repo, expected_call[0])
    repo_method.assert_called_once_with(**expected_call[1])
