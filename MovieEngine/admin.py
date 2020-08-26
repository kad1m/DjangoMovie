from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Movie, MovieShots, Actor, Rating, RatingStar, Reviews, Genre

from modeltranslation.admin import TranslationAdmin

# Register your models here.

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description_ru = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label='Description', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ('name', 'url', 'id')
    list_display_links = ('name',)


class ReviewInline(admin.StackedInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"> ')

    get_image.short_description = 'Изображение'


@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name', )
    inlines = [MovieShotsInline, ReviewInline,]
    save_on_top = True
    save_as = True
    actions = ['unpublish', 'publish']
    form = MovieAdminForm
    list_editable = ('draft',)
    readonly_fields = ('get_image',)
    fieldsets = (
        ('Название и слоган', {
            'fields': (('title', 'tagline'),)
        }),
        (None, {
            'fields': ('description', ('poster', 'get_image'))
        }),
        (None, {
            'fields': (('year', 'world_premiere', 'country'),)
        }),
        ('Actors', {
            'classes': ('collapse',),
            'fields': (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
            'fields': (('budget', 'feels_in_usa', 'feels_in_world'),)
        }),
        (None, {
            'fields': (('url', 'draft'),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"> ')

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей было обновлено'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей было обновлено'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    publish.allowed_permission = ('change',)

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permission = ('change',)

    get_image.short_description = 'Постер'

@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    list_display = ('name', 'url')


@admin.register(Actor)
class ActorAdmin(TranslationAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.images.url} width="50" height="60"> ')

    get_image.short_description = 'Изображение'



@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('star', 'ip', 'movie')


@admin.register(MovieShots)
class MovieShotAdmin(TranslationAdmin):
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"> ')

    get_image.short_description = 'Изображение'


admin.site.register(RatingStar)
admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'

