from django.urls import path
from .views import ImageUploadView, ImageRepredectView, SearchUserView

urlpatterns = [
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
    path('repridict/', ImageRepredectView.as_view(), name='image-repredict'),
    path('dataperuser/', SearchUserView.as_view(), name = 'data-filter' )

]
