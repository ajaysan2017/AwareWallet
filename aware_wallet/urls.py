from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Auth (login, logout, register)
    path('auth/', include('apps.users.urls')),

    # Core pages
    path('', include('apps.transactions.urls')),
    path('categories/', include('apps.categories.urls')),
    path('budgets/', include('apps.budgets.urls')),
    path('recurring/', include('apps.recurring.urls')),
    path('savings/', include('apps.savings.urls')),
    path('analytics/', include('apps.analytics.urls')),

    # REST API
    path('api/v1/users/',        include('apps.users.api_urls')),
    path('api/v1/categories/',   include('apps.categories.api_urls')),
    path('api/v1/transactions/', include('apps.transactions.api_urls')),
    path('api/v1/budgets/',      include('apps.budgets.api_urls')),
    path('api/v1/recurring/',    include('apps.recurring.api_urls')),
    path('api/v1/savings/',      include('apps.savings.api_urls')),
    path('api/v1/analytics/',    include('apps.analytics.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)