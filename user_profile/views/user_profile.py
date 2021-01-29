from django.shortcuts import render
from django.http import HttpResponse
from ..models import *
from ..forms.field_edit import UserProfileForm
from django.core.cache import cache
from django.views.decorators.cache import cache_page, cache_control

# Create your views here.
@cache_page(60 * 15, key_prefix="home")
@cache_control(max_age=3600)
def home(request):
	profile = UserProfile.objects.first()
	cache_profile = load_from_cache(name=profile.name)
	context = {'profile': cache_profile}

	return render(request, 'user_profile/profile.html', context)

@cache_page(60 * 15, key_prefix="profile")
@cache_control(max_age=3600)
def profile(request, profile_id):
	cache_profile = load_from_cache(name=profile_id)

	context = {'profile': cache_profile}
	
	return render(request, 'user_profile/profile.html', context)


@cache_page(60 * 15, key_prefix="edit_profile")
@cache_control(max_age=3600)
def edit_profile(request, profile, target_field):
	profile = load_from_cache(name=profile)

	form = UserProfileForm(instance=profile)
	
	# context = {'value': getattr(profile, target_field)}

	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES, instance=profile)

		if form.is_valid():
			form.save()

	context = {'form': form}

	return render(request, 'user_profile/field_edit.html', context)


def load_from_cache(name):
	cache_profile = cache.get('userprofile-%s' % (name), None)

	if not cache_profile:
		cache_profile = UserProfile.objects.get(name=name)
		cache.set('userprofile-%s' % (name), cache_profile)
	
	return cache_profile


# class CacheProfile(UserProfile):
# 	def get_queryset(self):
# 		return super(CacheProfile, self).local_from_cache().select_related()

# 	def load_from_cache(self, queryset):
# 		cache_obj = cache.get('%s-%s' % (self.model.__name__.lower(), self.kwargs['namee']), None)

# 		if not cache_obj:
# 			cache_obj = super(CacheProfile, self).get_object(queryset)
# 			cache.set('%s-%s' % (self.model.__name__.lower(), self.kwargs['name']), cache_obj)
		
# 		return cache_obj