from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Book


class BookListView(ListView):
    model = Book
    template_name = "catalog/book_list.html"
    context_object_name = "books"
    paginate_by = 5

    def get_queryset(self):
        queryset = Book.objects.select_related("category").all().order_by("id")

        search = self.request.GET.get("search")
        category = self.request.GET.get("category")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(author__icontains=search)
            )

        if category:
            queryset = queryset.filter(category__slug=category)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset


class BookDetailView(DetailView):
    model = Book
    template_name = "catalog/book_detail.html"
    context_object_name = "book"


class BookCreateView(CreateView):
    model = Book
    template_name = "catalog/book_form.html"
    fields = ["category", "title", "author", "price", "description", "stock"]
    success_url = reverse_lazy("catalog:book_list")


class BookUpdateView(UpdateView):
    model = Book
    template_name = "catalog/book_form.html"
    fields = ["category", "title", "author", "price", "description", "stock"]
    success_url = reverse_lazy("catalog:book_list")


class BookDeleteView(DeleteView):
    model = Book
    template_name = "catalog/book_confirm_delete.html"
    success_url = reverse_lazy("catalog:book_list")