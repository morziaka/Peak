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

    # CREATING mpass object
    @action(detail=True, methods=['post'])
    def submitData(self, request):
        data = request.data

        try:
            user_data = data.get('user')
            email = user_data['email']
            email_exist = MPass.objects.filter(user_id__email=email).exist()
            valid_user_fields = [
                user_data['name'] != MPass.objects.filter(user_id__email=email).values('name'),
                user_data['fam'] != MPass.objects.filter(user_id__email=email).values('fam'),
                user_data['otc'] != MPass.objects.filter(user_id__email=email).values('otc'),
                user_data['phone'] != MPass.objects.filter(user_id__email=email).values('phone'),
            ]
            if email_exist and any(valid_user_fields):
                raise serializers.ValidationError({'Этот email уже используется другим пользователем.'})

            phone = user_data['phone']
            phone_exist = MPass.objects.filter(user_id__phone=phone).exist()
            valid_user_fields = [
                user_data['name'] != MPass.objects.filter(user_id__phone=phone).values('name'),
                user_data['fam'] != MPass.objects.filter(user_id__phone=phone).values('fam'),
                user_data['otc'] != MPass.objects.filter(user_id__phone=phone).values('otc'),
                user_data['email'] != MPass.objects.filter(user_id__phone=phone).values('email'),
            ]
            if phone_exist and any(valid_user_fields):
                raise serializers.ValidationError({'Этот телефон уже используется другим пользователем.'})

            coords_data = data.get('coords')
            level_data = data.get('level')
            images_data = data.get('images')

            user_serializer = UserSerializer(data=user_data)
            coords_serializer = CoordSerializer(data=coords_data)
            level_serializer = LevelSerializer(data=level_data)
            images_serializers = [ImagesSerializer(data=image_data) for image_data in images_data]

            if user_serializer.is_valid() and coords_serializer.is_valid() and level_serializer.is_valid() and all(
                    image_serializer.is_valid() for image_serializer in images_serializers):
                user_instance = user_serializer.save()
                coords_instance = coords_serializer.save()
                level_instance = level_serializer.save()

                pereval_data = {
                    'user': user_instance.id,
                    'coords': coords_instance.id,
                    'level': level_instance.id,
                    **data  # Remaining data
                }

                pass_serializer = MPassSerializer(data=pereval_data)
                if pass_serializer.is_valid():
                    pass_instance = pass_serializer.save()

                    for image_serializer in images_serializers:
                        image_serializer.save(mpass=pass_instance)

                    return Response({'status': 200, 'message': 'Отправлено успешно', 'id': pass_instance.id},
                                    status=status.HTTP_200_OK)
            else:
                return Response({'status': 400, 'message': 'Bad Request, недостаточно полей', 'id': None},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'status': 500, 'message': str(e), 'id': None},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)