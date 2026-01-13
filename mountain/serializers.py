from .models import *
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer


class CoordSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Coord
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']


class ImagesSerializer(WritableNestedModelSerializer):
    data = serializers.CharField()

    class Meta:
        model = Images
        fields = ['data', 'title']


class UserSerializer(WritableNestedModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'fam', 'name', 'otc', 'phone']


class MPassSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    coords = CoordSerializer()
    level = LevelSerializer(allow_null=True)
    images = ImagesSerializer(many=True)
    status = serializers.CharField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = MPass
        fields = ['beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'status', 'user', 'level', 'coords',
                  'images']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        level_data = validated_data.pop('level')
        images_data = validated_data.pop('images')

        user, _ = MyUser.objects.get_or_create(**user_data)
        coords = Coord.objects.create(**coords_data)
        level = Level.objects.create(**level_data)

        mpass = MPass.objects.create(user=user, coords=coords, level=level, **validated_data)

        for image_data in images_data:
            data = image_data.get('data')
            title = image_data.get('title')
            Images.objects.create(data=data, title=title, m_pass=mpass)

        return mpass

