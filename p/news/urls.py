from django.conf.urls import url
from . import views

urlpatterns = {
    url(r'categories', views.categories, name='categories'),
    url(r'details/(\w*)', views.details, name='details'),
}
