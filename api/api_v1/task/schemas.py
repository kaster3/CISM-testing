from pydantic import BaseModel, ConfigDict

from core.database.models.enums.task_status_enum import TaskStatusEnum


class TaskBaseSchema(BaseModel):
    name: str


class TaskSchema(TaskBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: TaskStatusEnum


class TaskCreate(TaskBaseSchema):
    status: TaskStatusEnum = TaskStatusEnum.NEW


class TaskUpdatePartial(TaskBaseSchema):
    name: str | None = None
    status: TaskStatusEnum | None = None
