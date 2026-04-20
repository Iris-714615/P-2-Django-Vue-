from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register(r'list', views.TeacherList)

urlpatterns = [
    path("delete/<int:pk>/", views.TeacherDelete.as_view()),
    path("delmany/", views.TeacherDelmany.as_view()),
    path("upload/", views.Upload.as_view()),
]
urlpatterns += router.urls