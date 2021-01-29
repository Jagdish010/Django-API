from django.urls import path, include
from .views import user_profile
from .views import api_profile
from .views import api_profile_2
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
	path('', user_profile.home, name='home'),
	path('profile/<str:profile_id>/', user_profile.profile, name='profile'),
	path('edit_profile/<str:profile>/<str:target_field>/', user_profile.edit_profile, name='edit_profile'),
	path('api-auth/', include('rest_framework.urls')),
	# path('api_profile', api_profile.profileapi.as_view()),
	path('api_profile', api_profile.profileapi),
	# path('api_profile', api_profile_2.profileapi),
	# path('api/token/', obtain_auth_token, name='obtain_token')
]