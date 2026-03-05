from django.contrib import admin
from .models import Book, Category


class BookInline(admin.TabularInline):
    model = Book
    extra = 1
    fields = ("title", "author", "price", "stock")
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name", "slug")
    list_filter = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [BookInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "category", "price", "stock")
    list_select_related = ("category",)
    search_fields = ("title", "author", "category__name")
    list_filter = ("category", "author")
    list_editable = ("price", "stock")