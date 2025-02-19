from django.apps import \
    AppConfig  # Импортируем класс AppConfig из модуля django.apps, который используется для конфигурации приложения.


class PortfolioAppConfig(
    AppConfig):  # Определяем класс конфигурации приложения PortfolioAppConfig, наследующий от AppConfig.
    default_auto_field = 'django.db.models.BigAutoField'  # Устанавливаем тип поля автоинкрементного идентификатора
    # по умолчанию на BigAutoField.
    name = 'portfolio_app'  # Указываем имя приложения, как оно будет называться в проекте Django.
