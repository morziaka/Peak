
from django.db import models
from django.core.validators import RegexValidator
from .utils import get_path_upload_photo

# Create your models here.
check_phone = RegexValidator(regex=r'^\+\d{11}$',
                              message="Введите номер телефона в корректном формате: +7(111)222-33-44")


class MyUser(models.Model):
    name = models.CharField(max_length=150)
    fam = models.CharField(max_length=150)
    otc = models.CharField(max_length=150)
    phone = models.CharField(validators=[check_phone], max_length=15, blank=True)
    email = models.EmailField(max_length=200)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'fam', 'otc', 'phone']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Coord(models.Model):
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    height = models.IntegerField(default=0)

    def __str__(self):
        return str(self.height)

    class Meta:
        verbose_name = "Координаты"
        verbose_name_plural = "Координаты"


class Level(models.Model):
    LEVEL_1 = '1A'
    LEVEL_2 = '1B'
    LEVEL_3 = '2A'
    LEVEL_4 = '2B'
    LEVEL_5 = '3A'
    LEVEL_6 = '3B'
    LEVEL_CHOICES = (
        ('1A', '1A'),
        ('1B', '1B'),
        ('2A', '2A'),
        ('2B', '2B'),
        ('3A', '3A'),
        ('3B', '3B')
    )

    winter = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=LEVEL_1)
    summer = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=LEVEL_1)
    autumn = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=LEVEL_1)
    spring = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=LEVEL_1)

    def __str__(self):
        return f' winter: {self.winter}, summer: {self.summer}, autumn: {self.autumn}, spring: {self.spring}'

    class Meta:
        verbose_name = "Уровень сложности"
        verbose_name_plural = "Уровни сложности"


class MPass(models.Model):
    CHOICE_STATUS = (
        ("new", 'новый'),
        ("pending", 'модератор взял в работу'),
        ("accepted", 'модерация прошла успешно'),
        ("rejected", 'модерация прошла, информация не принята'),
    )

    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=CHOICE_STATUS, default="new")
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user')
    coords = models.OneToOneField(Coord, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk}:  {self.beauty_title}'

    class Meta:
        verbose_name = "Перевал"
        verbose_name_plural = "Перевалы"


class Images(models.Model):
    title = models.CharField(max_length=255)
    data = models.ImageField(upload_to=get_path_upload_photo, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    m_pass = models.ForeignKey(MPass, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"