from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class RealEstate(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='ID')
    # Категориальные признаки
    TYPE_CHOICES = [
        (0, 'Вторичное жильё'),
        (1, 'Новостройка')
    ]

    HOUSE_TYPE_CHOICES = [
        ('Панельный', 'Панельный'),
        ('Монолитно-кирпичный', 'Монолитно-кирпичный'),
        ('Кирпичный', 'Кирпичный'),
        ('Монолитный', 'Монолитный'),
        ('Блочный', 'Блочный'),
        ('Сталинский', 'Сталинский')
    ]

    SALE_TYPE_CHOICES = [
        ('Свободная продажа', 'Свободная продажа'),
        ('Альтернатива', 'Альтернатива'),
        ('Договор уступки права требования', 'Договор уступки права требования'),
        ('214-ФЗ', '214-ФЗ'),
        ('Предварительный договор купли-продажи', 'Предварительный договор купли-продажи')
    ]

    STREET_CHOICES = [
        ('Прочие', 'Прочие'),
        ('улица Промышленная', 'улица Промышленная'),
        ('улица Стасова', 'улица Стасова'),
        ('Кубанская улица', 'Кубанская улица'),
        ('Старокубанская улица', 'Старокубанская улица'),
        ('Красная улица', 'Красная улица'),
        ('улица Коммунаров', 'улица Коммунаров'),
        ('улица Вишняковой', 'улица Вишняковой'),
        ('Колхозная улица', 'Колхозная улица'),
        ('Воронежская улица', 'Воронежская улица'),
        ('Обрывная улица', 'Обрывная улица'),
        ('Ставропольская улица', 'Ставропольская улица'),
        ('улица Железнодорожная', 'улица Железнодорожная'),
        ('Московская улица', 'Московская улица'),
        ('улица Митрофана Седина', 'улица Митрофана Седина'),
        ('Садовая улица', 'Садовая улица')
    ]

    DISTRICT_CHOICES = [
        ('Центральный мкр', 'Центральный мкр'),
        ('Черемушки мкр', 'Черемушки мкр'),
        ('Завод Измерительных Приборов мкр', 'Завод Измерительных Приборов мкр'),
        ('Дубинка мкр', 'Дубинка мкр'),
        ('Табачная Фабрика мкр', 'Табачная Фабрика мкр')
    ]

    ROOM_COUNT_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (0, 'Свободная планировка'),  # Свободная планировка
        (-1, 'Студия'),  # Студия
        (4, '4'),
        (5, '5'),
        (6, '6')
    ]

    # Категориальные поля
    type = models.IntegerField(
        'Тип',
        choices=TYPE_CHOICES,
        default=0
    )

    room_count = models.IntegerField(
        'Количество комнат',
        choices=ROOM_COUNT_CHOICES,
        default=1
    )

    house_type = models.CharField(
        'Тип дома',
        max_length=50,
        choices=HOUSE_TYPE_CHOICES,
        default='Панельный'
    )

    sale_type = models.CharField(
        'Тип продажи',
        max_length=50,
        choices=SALE_TYPE_CHOICES,
        default='Свободная продажа'
    )

    street = models.CharField(
        'Улица',
        max_length=50,
        choices=STREET_CHOICES,
        default='Прочие'
    )

    district = models.CharField(
        'Район',
        max_length=50,
        choices=DISTRICT_CHOICES,
        default='Центральный мкр'
    )

    # Числовые поля
    total_area = models.DecimalField(
        'Общая площадь',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )

    floor = models.PositiveSmallIntegerField(
        'Этаж',
        validators=[MinValueValidator(1)]
    )

    total_floors = models.PositiveSmallIntegerField(
        'Этажность',
        validators=[MinValueValidator(1)]
    )

    latitude = models.DecimalField(
        'Широта',
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90)
        ]
    )

    longitude = models.DecimalField(
        'Долгота',
        max_digits=9,
        decimal_places=6,
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180)
        ]
    )

    distance_to_center = models.DecimalField(
        'Расстояние до центра',
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Расстояние в километрах (рассчитывается автоматически)'
    )

    class Meta:
        verbose_name = 'Недвижимость'
        verbose_name_plural = 'Объекты недвижимости'

    def __str__(self):
        return f"#{self.id} | {self.get_type_display()} ({self.room_count}к.) - {self.total_area}м²"