import pytest
from pytest_mock import MockerFixture

from core.database.models.enums.task_status_enum import TaskStatusEnum
from core.taskiq.tasks import TaskUpdatePartial, task_process


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "random_value, expected_status",
    [
        (0.4, TaskStatusEnum.COMPLETED),
        (0.6, TaskStatusEnum.ERROR),
    ],
)
async def test_task_process(
    mocker: MockerFixture,
    random_value: float,
    expected_status: TaskStatusEnum,
    task_id: int = 1,
):
    mock_repo = mocker.AsyncMock()

    mock_task = mocker.AsyncMock()
    mock_task.id = 1
    mock_task.name = "Test Task"
    mock_task.status = TaskStatusEnum.NEW

    mock_repo.get_task.return_value = mock_task
    mock_repo.update_task.return_value = mock_task

    mocker.patch("asyncio.sleep", return_value=None)
    mocker.patch("random.random", return_value=random_value)

    await task_process(task_in=task_id, repo=mock_repo)

    mock_repo.get_task.assert_called_once_with(task_id=task_id)

    expected_calls = [
        mocker.call(task=mock_task, task_in=TaskUpdatePartial(status=TaskStatusEnum.IN_PROGRESS)),
        mocker.call(task=mock_task, task_in=TaskUpdatePartial(status=expected_status)),
    ]
    mock_repo.update_task.assert_has_calls(expected_calls, any_order=False)
