
from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from rest_framework import status


import json
from .models import *
from rest_framework.test import APITestCase
from .serializers import MPassSerializer


class TestViews(TestCase):
    def test_list_perevals(self):
        client = Client()

        response = client.get(reverse('perevals-list'))

        self.assertEqual(response.status_code, 200)


class SubmitDataAPITests(APITestCase):
    def setUp(self):
        user1 = MyUser.objects.create(
            email='test1@test.com',
            fam='Ivanov',
            name='Ivan',
            otc='Ivanovich',
            phone='+87979302840'
        )
        user1.full_clean()
        user1.save()
        self.pereval_1 = MPass.objects.create(
            user = user1,
            beauty_title='test BT',
            title='test title',
            other_titles='tests other titles',
            connect='test connect',
            status='new',
            coords=Coord.objects.create(
                latitude=23.123,
                longitude=87.789,
                height=234
            ),
            level=Level.objects.create(
                winter="2B",
                summer="2A",
                autumn="1B",
                spring="1B",
            )
        )
        self.image_1 = Images.objects.create(
            data='',
            title='test-title',
            m_pass=self.pereval_1
        )

        self.pereval_2 = MPass.objects.create(
            user=MyUser.objects.create(
                email='test2@test.com',
                fam='Petrov',
                name='Petr',
                otc='Petrovich',
                phone='+98908039890'
            ),
            beauty_title='test two BT',
            title='test two title',
            other_titles='tests other titles two',
            connect='test connect two',
            add_time='2025-12-25T08:55:32.429115Z',
            status='new',
            coords=Coord.objects.create(
                latitude=23.983,
                longitude=97.789,
                height=224
            ),
            level=Level.objects.create(
                winter="2B",
                summer="1A",
                autumn="2B",
                spring="1A",
            )
        )
        self.image_2 = Images.objects.create(
            data='',
            title='test-title-two',
            m_pass=self.pereval_2
        )

    def test_list(self):
        response = self.client.get(reverse('perevals-list'))
        serializer_data = MPassSerializer([self.pereval_1, self.pereval_2], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MPass.objects.count(), 2)
        self.assertEqual(serializer_data, response.data)
        pereval_object_1 = MPass.objects.filter(beauty_title='test BT').first()
        self.assertEqual(pereval_object_1.beauty_title, 'test BT')
        pereval_object_2 = MPass.objects.filter(beauty_title='test two BT').first()
        self.assertEqual(pereval_object_2.beauty_title, 'test two BT')

    def test_detail(self):
        response = self.client.get(reverse('perevals-detail', kwargs={'pk': self.pereval_1.pk}))
        serializer_data = MPassSerializer(self.pereval_1).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_two(self):
        response = self.client.get(reverse('perevals-detail', kwargs={'pk': self.pereval_2.pk}))
        serializer_data = MPassSerializer(self.pereval_2).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        data = {
            "beauty_title": "перевал",
            "title": "Дятлова",
            "other_titles": "перевал2",
            "connect": "Уральские горы",
            "user": {
                "email": "test@test.ru",
                "fam": "Иванов",
                "name": "Альбер",
                "otc": "Петрович",
                "phone": "+79559708808"
            },
            "level": {
                "winter": "1A",
                "summer": "1B",
                "autumn": "",
                "spring": ""
            },
            "coords": {
            "latitude": 10.1,
            "longitude": 10.2,
            "height": 1000
            },
            "images":[
                {
                    "data": "https://storage.yandexcloud.net/storage.yasno.media/nat-geo/images/2019/5/16/42483f0d38b9408698e3396b0fa1dee2.max-1200x800.jpg",
                    "title": "photo1"
                 }
            ]
        }
        response = self.client.post(reverse('perevals-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MPass.objects.count(), 3)

