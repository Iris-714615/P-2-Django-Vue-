from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register(r'student', views.StudentList)

urlpatterns = [
    path('login/',views.User.as_view()),
    path('status/<int:pk>/',views.StudentStatus.as_view()),
    path('delete/<int:pk>/',views.StudentDelete.as_view()),
    path('delmany/',views.Delmany.as_view()),
    path('export/',views.Export.as_view()),
]
urlpatterns += router.urls