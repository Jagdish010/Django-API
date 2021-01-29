from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializes.profile_serialize import ProfileSerialize
from ..models import UserProfile

class profileapi(APIView):
	# permission_classes = (IsAuthenticated)

	def get(self, request, *args, **kwargs):
		name = request.GET.get('name')
		if name:
			many=True
			profile = UserProfile.objects.get(name=name)
		else:
			many=False
			profile = UserProfile.objects.all()

		serializers = ProfileSerialize(profile, many=many)

		if profile:
			return Response(serializers.data)
		else:
			return Response(status=status.HTTP_404_NOT_FOUND)

	def put(self, request, *args, **kwargs):
		name = request.GET.get('name')
		profile = UserProfile.objects.get(name=name)
		if profile:
			serializer = ProfileSerialize(profile, data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data, status=status.HTTP_200_OK)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		return Response(status=status.HTTP_404_NOT_FOUND)

	def post(self, request, *args, **kwargs):
		serializer = ProfileSerialize(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, *args, **kwargs):
		name = request.GET.get('name')
		profile = UserProfile.objects.get(name=name)
		if profile:
			profile.delete()
			return Response(status=status.HTTP_204_NO_CONTENT)
		return Response(status=status.HTTP_400_BAD_REQUEST)