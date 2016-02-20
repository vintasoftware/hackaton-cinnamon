from django.conf.urls import url

from .endpoints import BikewayListAPIView, BikewayCategoryListAPIView


urlpatterns = [
    url(r'^bikeways/$', BikewayListAPIView.as_view(), name='bikeway-list'),
    url(r'^bikeways-categories/$', BikewayCategoryListAPIView.as_view(), name='category-list')
]
