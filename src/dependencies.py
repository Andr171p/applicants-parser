from dishka import Provider, Scope, provide, from_context, make_async_container

from faststream.rabbit import RabbitBroker

from .settings import Settings, settings


class AppProvider(Provider):
    app_settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_broker(self, app_settings: Settings) -> RabbitBroker:
        return RabbitBroker(url=app_settings.rabbit_settings.get_rabbit_url)


container = make_async_container(AppProvider(), context={Settings: settings})
