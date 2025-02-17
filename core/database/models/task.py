from sqlalchemy import Enum as SqlAlchemyEnum
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.database.models.base import Base
from core.database.models.enums.task_status_enum import TaskStatusEnum
from core.database.models.mixins.pk_id_mixin import IntIdPkMixin


class Task(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(String(20))
    status: Mapped[TaskStatusEnum] = mapped_column(
        SqlAlchemyEnum(TaskStatusEnum),
        default=TaskStatusEnum.NEW,
    )

    def __repr__(self) -> str:
        return f"Task(id={self.id}, name={self.name!r}, status={self.status})"
