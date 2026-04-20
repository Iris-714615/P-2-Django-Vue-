from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register(r'list', views.ArticleList)

urlpatterns = [
    path("delete/<int:pk>/", views.ArticleDelete.as_view()),
    path("delmany/", views.ArticleDelmany.as_view()),
    path("upload/", views.ArticleUpload.as_view()),
    path("people/", views.People.as_view()),

]
urlpatterns += router.urls


