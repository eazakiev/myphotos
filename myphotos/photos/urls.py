from django.urls import path, register_converter
from . import converters
from django.views.decorators.cache import cache_page
from . import views

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path("", views.PhotosHome.as_view(), name="home"),
    path("about/", views.about, name="about"),
    path("addpage/", views.AddPage.as_view(), name="add_page"),
    path("contact/", views.ContactFormView.as_view(), name="contact"),
    path("post/<slug:post_slug>/", views.ShowPost.as_view(), name="post"),
    path("category/<slug:cat_slug>/", views.PhotosCategory.as_view(), name="category"),
    path("tag/<slug:tag_slug>/", views.TagPostList.as_view(), name="tag"),
    path("edit/<int:pk>/", views.UpdatePage.as_view(), name="edit_page"),
    path("confidential/", views.confidential, name="confidential"),
    path("terms/", views.terms, name="terms"),
]
