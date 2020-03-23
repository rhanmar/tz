from django.urls import path

from . import views

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(
    'api/get_top_customers',
    views.TopCustomersView,
    basename='top_customers'
    )
# for using this url in template write {% url 'your_basename-list' %}

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/csv', views.upload_csv, name='upload_csv'),
    path('test', views.test),
]

urlpatterns += router.urls
