from enum import StrEnum


class GigaChatModel(StrEnum):
    """Названия моделей GigaChat"""
    LATEST = "GigaChat:latest"
    PRO = "GigaChat-2-Pro"


# Максимальный лимит рекурсивных вызовов AI агента.
MAX_RECURSION_LIMIT = 50

# Количество университетов.
UNIVERSITIES_COUNT = 1737

TIMEOUT = 5
