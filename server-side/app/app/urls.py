"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path('api/', include('core.urls._user_urls')),
    path('api/', include('core.urls._tour_urls')),
    path('api/', include('core.urls._advisor_urls')),
    path('api/', include('core.urls._guide_urls')),
    path('api/', include('core.urls._visitor_urls')),
    path('api/', include('core.urls._review_urls')),  
    path('api/', include('core.urls._tour_request_urls')),
    path('api/', include('core.urls._fair_urls')),
    path('api/', include('core.urls._tour_request_batch_urls')),
    path('api/', include('core.urls._reg_request_urls')),
    path('api/', include('core.urls._tour_report_urls')),
    path('api/', include('core.messaging.urls')),
    path('api/auth/', include('core.auth.urls')),
    
]
