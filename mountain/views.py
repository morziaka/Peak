from django.db import DatabaseError
from django.forms import model_to_dict
from django.shortcuts import render

from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer


class CoordsViewset(viewsets.ModelViewSet):
    queryset = Coord.objects.all()
    serializer_class = CoordSerializer


class LevelViewset(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImageViewset(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer



class MPassViewSet(viewsets.ModelViewSet):
    queryset = MPass.objects.all()
    serializer_class = MPassSerializer
    filter_backends = [DjangoFilterBackend]


    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=request.data)
        try:
            if not serializer.is_valid():
                return Response(
                    {
                        'status': 400,
                        'message': serializer.errors,
                        'id': None},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save()
            return Response(
                {
                    'status': 200,
                    'message': 'Отправлено успешно',
                    'id': serializer.instance.pk},
                status=status.HTTP_200_OK
            )

        except DatabaseError as e:
            return Response({'status': 500, 'message': str(e), 'id': None},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def partial_update(self, request, *args, **kwargs):
        mpass_obj = self.get_object()
        mpass_data = request.data
        serializer = self.get_serializer(mpass_obj, data=mpass_data, partial=True)

        user_dict = model_to_dict(mpass_obj.user)
        user_dict.pop('id')
        user_data = mpass_data.get('user')

        if mpass_obj.status != 'new':
            return Response({"state": 0, "message": "Можно изменять информацию только в статусе 'new'"})

        if user_data and user_dict != user_data:
            return Response({"state": 0, "message": "Нельзя изменять данные пользователя"})

        if serializer.is_valid():
            serializer.save()
        return Response({"state": 1, "message": "Информация успешно обновлена"})