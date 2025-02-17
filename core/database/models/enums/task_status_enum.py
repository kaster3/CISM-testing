from enum import Enum


class TaskStatusEnum(Enum):
    NEW = "Новая задача"
    IN_PROGRESS = "В процессе работы"
    COMPLETED = "Завершено успешно"
    ERROR = "Ошибка"
