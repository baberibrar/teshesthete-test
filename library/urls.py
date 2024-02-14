from rest_framework.routers import SimpleRouter
from .views import *
from django.urls import path, include

router = SimpleRouter(trailing_slash=False)
router.register("api/user", UserViewSet, basename="user")
router.register("api/book", BookViewSet, basename="book")

urlpatterns = [
    path("", include(router.urls)),
    path("api/login", UserViewSet.as_view({"post": "login"}), name="login"),
    path("api/borrow-book/", BorrowBookView.as_view(), name="borrow_book"),
    path("api/return-book/", ReturnBookView.as_view(), name="return_book"),
]
