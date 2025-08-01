from django.urls import path
from .views import UserCreateAPIView, UserListAPIView, UserProfileAPIView, ReedemPointsAPIView, GrantPointsAPIView, TransactionsHistoryAPIView

urlpatterns = [
    path('auth/register', UserCreateAPIView.as_view(), name='register-user'),
    path('user/profile', UserProfileAPIView.as_view(), name='profile'),
    path('user/redeem', ReedemPointsAPIView.as_view(), name='redeem-points'),
    path('user/history', TransactionsHistoryAPIView.as_view(), name='transactions-history'),
    path('admin/users', UserListAPIView.as_view(), name='list-users'),
    path('admin/grant', GrantPointsAPIView.as_view(), name='grant-points'),
]