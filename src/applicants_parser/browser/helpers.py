import re

from bs4 import BeautifulSoup, Comment, Doctype

MAX_LENGTH = 20_000

UNUSEFUL_TAGS: list[str] = ["script", "style", "noscript", "meta", "link", "head"]
TABLE_TAGS: list[str] = ["table", "tr", "td", "th"]


def clean_text(text: str) -> str:
    """Отчищает текст от лишних пробелов и отступов."""
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_html(html: str, max_length: int = MAX_LENGTH) -> str:  # noqa: C901
    """
    Отчищает HTML код от лишних тегов, скриптов и прочего ненужного контента

    :param html: HTML код страницы
    :param max_length: Максимальная длина отчищенного кода
    """
    soup = BeautifulSoup(html, "html.parser")
    for element in soup(UNUSEFUL_TAGS):
        element.decompose()
    for comment in soup.find_all(
        string=lambda text: isinstance(text, (Comment, Doctype))
    ):
        comment.extract()
    for tag in soup.find_all(True):
        if not tag.get_text(strip=True) and not tag.attrs:
            tag.decompose()
            continue

        attrs_to_keep: dict[str, str] = {}
        if tag.name == "a":
            if "href" in tag.attrs:
                attrs_to_keep["href"] = tag["href"]
        elif tag.name == "img":
            attrs_to_keep["src"] = tag.get("src", "")
            if "alt" in tag.attrs:
                attrs_to_keep["alt"] = tag["alt"]
        elif tag.name in TABLE_TAGS:
            pass
        else:
            if "class" in tag.attrs:
                attrs_to_keep["class"] = tag["class"]
            if "id" in tag.attrs:
                attrs_to_keep["id"] = tag["id"]

        tag.attrs = attrs_to_keep

        if tag.string:
            cleaned = clean_text(tag.string)
            if cleaned:
                tag.string = cleaned
            else:
                tag.decompose()

    compact_html: list[str] = []
    for line in soup.prettify().split("\n"):
        line = line.strip()  # noqa: PLW2901
        if line:
            line = re.sub(r'^\s{2,}', '  ', line)  # noqa: PLW2901
            compact_html.append(line)

    result = "\n".join(compact_html)
    result = re.sub(r">\s+<", "><", result)
    result = re.sub(r"\n{3,}", "\n\n", result)

    if len(result) > max_length:
        result = result[:max_length]
        last_tag_pos = result.rfind(">")
        if last_tag_pos != -1:
            result = result[:last_tag_pos + 1]
        result += "\n<!-- CONTENT TRUNCATED -->"

    return result
