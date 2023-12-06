from photos.utils import menu


def get_photo_context(request):
    """Получение контекста для меню"""
    return {"mainmenu": menu}
