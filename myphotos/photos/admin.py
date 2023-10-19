from django.contrib import admin, messages

from .models import MyPhotos, Category


@admin.register(MyPhotos)
class WomenAdmin(admin.ModelAdmin):
    """Админ класс WomenAdmin для модели Women.
    Args:
        admin (class): _description_
    """

    list_display = ("title", "time_create", "is_published", "cat")  # 'get_html_photo'
    list_display_links = ("title",)
    ordering = ["time_create", "title"]
    search_fields = ("title", "content", "cat__name")
    list_editable = ("is_published",)
    list_per_page = 5
    actions = ["set_published", "set_draft"]
    list_filter = ("cat__name", "is_published", "time_create")
    # 'time_create', 'time_update' 'photo','get_html_photo'
    fields = ["title", "slug", "content", "cat", "is_published", "tags"]
    readonly_fields = ("time_create", "time_update")  # 'get_html_photo'
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["tags"]
    # filter_vertical = ['tags']

    @admin.display(description="Краткое описание", ordering="content")
    def brief_info(self, myphotos: MyPhotos):
        return f"Описание {len(myphotos.content)} символов"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=MyPhotos.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=MyPhotos.Status.DRAFT)
        self.message_user(
            request, f"{count} записей снято с публикации!", messages.WARNING
        )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админ класс CategoryAdmin для модели Category.
    Args:
        admin (class): _description_
    """

    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


admin.site.site_header = "Панель администрирования"
admin.site.site_title = "Админка сайта с фото"
admin.site.index_title = "Фото Евгения Закиева"
