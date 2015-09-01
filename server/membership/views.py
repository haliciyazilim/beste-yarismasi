# -*- coding: utf-8 -*-

from membership.models import User
from membership.serializers import UserSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


class Login(APIView):
    def post(self, request, format=None):

        data = request.data

        if 'username' not in data or 'password' not in data:
            response_detail = {'detail': 'username or password is missing'}
            return Response(response_detail, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            username = data['username']
            password = data['password']

            try:
                user = User.objects.get(username=username)

                is_password_true = user.check_password(password)

                if is_password_true:
                    token = Token.objects.get_or_create(user=user)
                    serializer = UserSerializer(user)

                    return Response({'user': serializer.data, 'token': token[0].key}, status=status.HTTP_200_OK)
                    # return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    response_detail = {'detail': 'username or password is false'}
                    return Response(response_detail, status=status.HTTP_401_UNAUTHORIZED)

            except User.DoesNotExist:
                response_detail = {'detail': 'username or password is false'}
                return Response(response_detail, status=status.HTTP_401_UNAUTHORIZED)


class Logout(APIView):
    # permission_classes = (AllowAny,)

    def post(self, request, format=None):

        print request.user
        print request.auth
        print request.META.get('HTTP_AUTHORIZATION')
        # print request.header

        # user_id=request.data['user']
        request_token = request.auth
        # request_token = request.META.get('HTTP_AUTHORIZATION')

        if request_token:
            try:
                token = Token.objects.get(key=request_token)
                token.delete()
                return Response(status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class Signup(APIView):
    def post(self, request, format=None):
        request.encoding = 'utf-8'
        data = request.data
        print 'signup data %s' % data
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():

            password = serializer.initial_data['password']
            password_validation = serializer.initial_data['password_validation']

            if password == password_validation:
                user = User.objects.create_user(
                    serializer.initial_data['username'],
                    serializer.initial_data['email'],
                    serializer.initial_data['password'],
                )

                user.first_name = serializer.initial_data['first_name']
                user.last_name = serializer.initial_data['last_name']
                user.phone_number = serializer.initial_data['phone_number']
                user.gender = serializer.initial_data['gender']
                user.address = serializer.initial_data['address']
                user.city = serializer.initial_data['city']

                user.save()
                token = Token.objects.get_or_create(user=user)

                serialized_user = UserSerializer(user)
                return Response({'user': serialized_user.data, 'token': token[0].key}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Profile(APIView):
    def post(self, request, format=None):

        request_token = request.META.get('HTTP_AUTHORIZATION')

        if request_token:
            try:
                token = Token.objects.get(key=request_token)

                user = User.objects.get(id=token.user_id)

                print 'Profile %s' % user

                serializer = UserSerializer(user)

                return Response({'user': serializer.data}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
