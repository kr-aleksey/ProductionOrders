from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('orders.urls', namespace='orders')),
    path('users/', include('users.urls', namespace='users')),
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
]
