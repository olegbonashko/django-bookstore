from catalog.models import Book


class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, book, quantity=1):
        book_id = str(book.id)

        if book_id not in self.cart:
            self.cart[book_id] = {
                'quantity': 0
            }

        self.cart[book_id]['quantity'] += quantity

        self.save()

    def remove(self, book):
        book_id = str(book.id)

        if book_id in self.cart:
            del self.cart[book_id]

            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        book_ids = self.cart.keys()

        books = Book.objects.filter(id__in=book_ids)

        for book in books:
            self.cart[str(book.id)]['book'] = book

        for item in self.cart.values():
            item['total_price'] = item['book'].price * item['quantity']

            yield item

    def get_total_price(self):
        return sum(
            item['book'].price * item['quantity']
            for item in self
        )