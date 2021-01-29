from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..serializes.profile_serialize import ProfileSerialize
from ..models import UserProfile

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def profileapi(request, *args, **kwargs):
	if request.method == 'GET':
		name = request.GET.get('name')
		if name:
			profile = UserProfile.objects.filter(name=name)
		else:
			profile = UserProfile.objects.all()
		serializer = ProfileSerialize(profile, many=True)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = ProfileSerialize(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'PUT':
		name = request.GET.get('name')
		if name:
			profile = UserProfile.objects.get(name=name)
			serializer = ProfileSerialize(profile, data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		name = request.GET.get('name')
		profile = profile.objects.filter(name=name)
		if profile:
			profile.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)
