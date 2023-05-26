from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('<id>', PasswordResetView.as_view(), {'post_reset_redirect': reverse_lazy('password_reset_done')}, name='password_reset'),
    path('done/<id>', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('<uidb64>', PasswordResetConfirmView.as_view(),
        {'post_reset_redirect': reverse_lazy('password_reset_complete')}, name='password_reset_confirm'),
    path('complete/<id>', PasswordResetCompleteView.as_view(), name="password_reset_complete")
]
