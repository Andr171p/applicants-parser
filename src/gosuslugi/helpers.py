
def extract_direction_code(url: str) -> str:
    """Извлекает код направления подготовки из его URL.

    :param url: URL адрес направления подготовки, например: https://www.gosuslugi.ru/vuznavigator/specialties/2.20.03.01/2/43
    :return Код направления, например: 2.20.03.01
    """
    parts = url.strip("/").split("/")
    index = parts.index("specialties")
    return parts[index + 1]


def extract_university_id(url: str) -> int:
    """Извлекает ID университета из его URL адреса.

    :param url: URL адрес университета на Госуслугах
    :return: ID университета с Госуслуг
    """
    return url.split("/")[-1]


def handle_technical_error() -> ...: ...
