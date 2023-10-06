from django.apps import AppConfig


class PhotosConfig(AppConfig):
    """Класс конфигурации приложения Photos.
    Args:
        AppConfig (class): _description_
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'photos'
    verbose_name = 'Мои фотографии'
