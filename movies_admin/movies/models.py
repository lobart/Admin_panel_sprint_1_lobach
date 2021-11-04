import re
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

class TimeStampedModel(models.Model):
    # В созданных вами таблицах есть поля created_at и updated_at.
    # Чтобы не повторять эти две строки в каждой модели,
    # создадим класс-миксин.
    created_at = models.DateTimeField(_('Создано'),auto_now_add=True)
    updated_at = models.DateTimeField(_('Изменено'), auto_now=True)

    class Meta:
        abstract = True


class Genre(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('Название'), max_length=255)
    # blank=True делает поле необязательным для заполнения.
    description = models.TextField(_('Описание'), blank=True)

    def __str__(self):
        return "%s"%self.name

    class Meta:
        verbose_name = _('Жанр')
        verbose_name_plural = _('Жанры')
        # Ваши таблицы находятся в нестандартной схеме. Это тоже нужно указать в классе модели
        db_table = "content\".\"genre"


class FilmworkGenre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filmwork = models.ForeignKey('Filmwork', on_delete=models.CASCADE, db_column='film_work_id')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, db_column='genre_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"


class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('Кино')
    TV_SHOW = 'tv_show', _('Шоу')


class Filmwork(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    title = models.CharField(_('Название'), max_length=255)
    description = models.TextField(_('Описание'), blank=True)
    creation_date = models.DateField(_('Дата выпуска'), blank=True)
    certificate = models.TextField(_('Сертификат'), blank=True)
    file_path = models.FileField(_('Файл'), upload_to='film_works/', blank=True)
    rating = models.FloatField(_('Рейтинг'), validators=[MinValueValidator(0)], blank=True)
    type = models.CharField(_('Тип'), max_length=20, choices=FilmworkType.choices)
    genres = models.ManyToManyField(Genre, through='FilmworkGenre')

    def get_matchname(self):
        """Returns the match name for a tag"""
        return re.sub("\W+", "", self.title.lower())

    def __str__(self):
        return "%s"%self.title

    class Meta:
        verbose_name = _('фильм')
        verbose_name_plural = _('фильмы')
        db_table = "content\".\"film_work"

class Person(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.TextField(_('Полное имя'), blank=True)
    birth_date = models.DateField(_('Дата рождения'), blank=True)
    filmwork = models.ManyToManyField(Filmwork, through='PersonFilmWork')

    def __str__(self):
        return "%s"%self.full_name

    class Meta:
        verbose_name = _('актер')
        verbose_name_plural = _('актеры')
        db_table = "content\".\"person"

class PersonFilmWork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filmwork = models.ForeignKey('Filmwork', on_delete=models.CASCADE, db_column='film_work_id')
    person = models.ForeignKey('Person', on_delete=models.CASCADE, db_column='person_id')
    role = models.TextField(_('role'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
