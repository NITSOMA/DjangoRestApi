from django.urls import path
from . import views

app_name = 'books_api'

urlpatterns = [

    path('api/books/', views.add_books, name='add_book'),
    path('api/books/<str:book_id>/', views.book_info, name='book_info'),
    path('api/appraisal_request/', views.appraisal_request, name='appraisal_request'),
    path('api/appraisal_request/<int:request_id>/', views.appraisal_request_info, name='request_info'),

]