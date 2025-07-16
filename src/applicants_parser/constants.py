from enum import StrEnum


class GigaChatModel(StrEnum):
    """Названия моделей GigaChat"""
    LATEST = "GigaChat:latest"
    PRO = "GigaChat-2-Pro"


MAX_RECURSION_LIMIT = 50  # Максимальный лимит рекурсивных вызовов AI агента
