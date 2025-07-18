from langchain_gigachat import GigaChat

from ..constants import GigaChatModel
from ..settings import settings

gigachat_pro = GigaChat(
    credentials=settings.gigachat.api_key,
    scope=settings.gigachat.scope,
    model=GigaChatModel.PRO,
    verify_ssl_certs=False,
    profanity_check=False
)

gigachat_lite = GigaChat(
    credentials=settings.gigachat.api_key,
    scope=settings.gigachat.scope,
    model=GigaChatModel.LATEST,
    verify_ssl_certs=False,
    profanity_check=False
)
