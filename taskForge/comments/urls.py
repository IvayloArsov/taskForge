from django.urls import path
from .views import CommentCreateView, CommentDeleteView

app_name = 'comments'

urlpatterns = [
    path('create/<int:ticket_id>/', CommentCreateView.as_view(), name='create'),
    path('delete/<int:pk>/', CommentDeleteView.as_view(), name='delete'),
]