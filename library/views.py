from rest_framework import viewsets, status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Book, BorrowedBook
from .serializers import UserSignupSerializer, UserSerializer, UserLoginSerializer, AddBookSerializer, BookSerializer
import datetime


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            error = {"statusCode": 400, "error": True, "data": "", "message": "Bad Request, Please   check request",
                     "errors": e.args[0]}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        data = UserSerializer(user).data
        response = {"statusCode": 200, "error": False, "message": "User created successfully", "data": data}
        return Response(response, status=status.HTTP_200_OK)

    def login(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            error = {"statusCode": 400, "error": True, "data": "", "message": "Bad Request, Please   check request",
                     "errors": e.args[0]}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)
        user_data = UserSerializer(user).data
        data = {"user": user_data, "refresh": str(refresh), "access": str(access)}
        response = {"statusCode": 200, "error": False, "message": "Login successful", "data": data}
        return Response(response, status=status.HTTP_200_OK)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = AddBookSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.is_staff:
            serializer = AddBookSerializer(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
            except Exception as e:
                error = {"statusCode": 400, "error": True, "data": "", "message": "Bad Request, Please   check request",
                         "errors": e.args[0]}
                return Response(error, status=status.HTTP_400_BAD_REQUEST)
            book = serializer.save()
            book.available = True
            book.save()
            data = AddBookSerializer(book).data
            response = {"statusCode": 200, "error": False, "message": "Book added successfully", "data": data}
            return Response(response, status=status.HTTP_200_OK)
        else:
            error = {"statusCode": 403, "error": True, "data": "",
                     "message": "Forbidden, You are not allowed to add book"}
            return Response(error, status=status.HTTP_403_FORBIDDEN)

    def list(self, request, *args, **kwargs):
        search = request.query_params.get('search', None)
        if search:
            books = Book.objects.filter(title__icontains=search) | Book.objects.filter(author__icontains=search)
        else:
            books = Book.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(books, request)
        serializer = BookSerializer(result_page, many=True)
        data = serializer.data
        response = {"statusCode": 200, "error": False, "message": "Books retrieved successfully", "data": data}
        return paginator.get_paginated_response(response)


class BorrowBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        if not book_id:
            error = {"statusCode": 400, "error": True, "data": "", "message": "Bad Request, Please provide book_id"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        book = Book.objects.filter(id=book_id).first()
        if book and book.available:
            borrowed_book = BorrowedBook.objects.create(user=request.user, book=book,
                                                        borrowed_date=datetime.date.today(),
                                                        return_date=datetime.date.today() + datetime.timedelta(days=14))
            borrowed_book.save()
            book.available = False
            book.save()
            data = {"user": request.user.id, "book": book.id, "borrowed_date": borrowed_book.borrowed_date,
                    "return_date": borrowed_book.return_date}
            response = {"statusCode": 200, "error": False, "message": "Book borrowed successfully", "data": data}
            return Response(response, status=status.HTTP_200_OK)
        elif book and not book.available:
            error = {"statusCode": 400, "error": True, "data": "", "message": "Book not available for borrowing"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        else:
            error = {"statusCode": 404, "error": True, "data": "", "message": "Book not found"}
            return Response(error, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, *args, **kwargs):
        borrowed_books = BorrowedBook.objects.filter(user=request.user, is_returned=False)
        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(borrowed_books, request)
        data = []
        for book in result_page:
            book_data = {"id": book.id, "book": book.book.title, "author": book.book.author,
                         "borrowed_date": book.borrowed_date, "return_date": book.return_date}
            data.append(book_data)
        response = {"statusCode": 200, "error": False, "message": "Borrowed books retrieved successfully", "data": data}
        return paginator.get_paginated_response(response)


class ReturnBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        book = Book.objects.filter(id=book_id).first()
        borrowed_book = BorrowedBook.objects.filter(user=request.user, book=book).first()
        if borrowed_book:
            borrowed_book.return_date = datetime.date.today()
            borrowed_book.is_returned = True
            borrowed_book.save()
            book.available = True
            book.save()
            data = {"user": request.user.id, "book": book.id, "borrowed_date": borrowed_book.borrowed_date,
                    "return_date": borrowed_book.return_date}
            response = {"statusCode": 200, "error": False, "message": "Book returned successfully", "data": data}
            return Response(response, status=status.HTTP_200_OK)
        else:
            error = {"statusCode": 404, "error": True, "data": "", "message": "Book not found in borrowed list"}
            return Response(error, status=status.HTTP_404_NOT_FOUND)
