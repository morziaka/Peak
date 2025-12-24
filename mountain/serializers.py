from .models import *
from rest_framework import serializers


class CoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coord
        fields = ['latitude', 'longitude', 'height']


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['winter', 'summer', 'autumn', 'spring']


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['data', 'title']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['email', 'fam', 'name', 'otc', 'phone']


class MPassSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    coords_id = CoordSerializer()
    level_diff = LevelSerializer(allow_null=True)
    images = ImagesSerializer(many=True)

    class Meta:
        model = MPass
        fields = ['id', 'user_id', 'coords_id', 'level_diff', 'beauty_title', 'title', 'other_titles', 'connect',
                  'add_time', 'images']

        # restricts altering user's data while updating pereval
        def validate(self, data):
            if self.instance is not None:
                user_instance = self.instance.user_id
                user_data = data.get('user_id')
                valid_user_fields = [
                    user_instance.email != user_data['email'],
                    user_instance.full_name != user_data['full_name'],
                    user_instance.phone != user_data['phone']
                ]
                if user_data and any(valid_user_fields):
                    raise serializers.ValidationError({'Данные нельзя изменить'})
            return data