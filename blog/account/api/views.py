from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import (RetrieveUpdateAPIView, get_object_or_404, CreateAPIView, )
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.api.permissions import NotAuthenticated
from account.api.serializers import UserSerializer, ChangePasswordSerializer, RegisterSerializer
from account.api.throttles import RegisterThrottle


class ProfileView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset=queryset, id=self.request.user.id)
        return obj

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class UpdatePassword(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = {"old_password": request.data.get('old_password'),
                "new_password": request.data.get('new_password')}

        serializer = ChangePasswordSerializer(data=data)
        if serializer.is_valid():
            print(serializer.data)
            old_password = serializer.data.get('old_password')
            if not self.object.check_password(old_password):
                return Response({"old_password": "Wrong password"}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateUserView(CreateAPIView):
    throttle_classes = [RegisterThrottle]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
