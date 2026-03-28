"""URL configuration for AwareWallet project."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from apps.users.forms import CustomPasswordResetForm

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

    # ── Password Reset ────────────────────────────────────────
    path('auth/password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html',
             email_template_name='users/password_reset_email.html',
             subject_template_name='users/password_reset_subject.txt',
             success_url='/auth/password-reset/done/',
             form_class=CustomPasswordResetForm,
         ),
         name='password_reset'),
    path('auth/password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('auth/password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html',
             success_url='/auth/password-reset-complete/'
         ),
         name='password_reset_confirm'),
    path('auth/password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
