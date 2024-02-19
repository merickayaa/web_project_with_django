from django.urls import path
from .views import ListThread, ThreadView,CreateMessage
from . import views
urlpatterns = [
    path('', ListThread.as_view(), name='messages'),    
    # path('create-thread/', CreateThread.as_view(), name='create-thread'),
    path('<int:pk>/', ThreadView.as_view(), name='thread'),
    path('<int:pk>/create-message/', CreateMessage.as_view(), name='create-message'),
]