from django.contrib import admin
from .models import Filmwork, PersonFilmWork, FilmworkGenre, Person, Genre


class PersonRoleInline(admin.TabularInline):
    model = PersonFilmWork
    list_display = ['full_name']
    extra = 0


class GenreFilmWorkInline(admin.TabularInline):
    model = FilmworkGenre
    list_display = ['genre']
    extra = 0

@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    save_on_top = True
    # отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating',)
    # порядок следования полей в форме создания/редактирования
    fields = (
        'title', 'type', 'description', 'creation_date', 'certificate',
        'file_path', 'rating', 'created_at', 'updated_at',
    )

    readonly_fields = ('created_at', 'updated_at',)

    filter_horizontal = ('genres',)
    # фильтрация в списке
    list_filter = ('type',)

    search_fields = ('title', 'description', 'id',)

    inlines = [PersonRoleInline, GenreFilmWorkInline]

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ('full_name','birth_date', 'created_at', 'updated_at',)
    readonly_fields = ('created_at', 'updated_at',)
    search_fields = ('full_name',)

@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ('name','description', 'created_at', 'updated_at',)
    readonly_fields = ('created_at', 'updated_at',)
    search_fields = ('name',)