from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, AppraisalRequest
from .serializers import BookSerializer, AppraisalRequestSerializer
from rest_framework import status
from .tasks import add_data
from celery.result import AsyncResult


@api_view(['POST'])
def add_books(request):
    """
    Function responds to website HTTP POST request.
    Serializes data, returns appropriate status depend on validation.

    """
    book = BookSerializer(data=request.data)
    if book.is_valid():
        book.save()
        return Response(status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def book_info(request, book_id):
    """
    Function responds to website HTTP GET or POST request
    Function gets extra param: book_id: str
    Depend on data existence and request method updates or returns serialized data
    """
    try:
        book = Book.objects.get(book_id=book_id)
    except Exception:
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        if request.method == 'GET':
            serializer = BookSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PUT' and book:
            serializer = BookSerializer(book, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def appraisal_request(request):
    """
    Function responds to website HTTP post request
    If requested data valid calls and runs background task
    Redirects to another endpoint that client can track result

    """
    url = AppraisalRequestSerializer(data=request.data)
    url.is_valid(raise_exception=True)
    url.save()
    url = AppraisalRequest.objects.filter(url=url.data['url']).first()
    """
    param -  duration: int - amount of seconds that function sleeps
    before its finishes. (just to show what happens in case background task
    needs more time before its done.
    """
    task = add_data.delay(url.url, duration=10)
    url.request_id = task.id
    url.save()
    return HttpResponseRedirect(reverse('books_api:request_info', kwargs={'request_id': url.id}))
    


@api_view()
def appraisal_request_info(request, request_id):
    """
        Function responds to website HTTP GET request
        Function gets extra param: request_id: int
        Depend on background task results
        updates, saves and returns appraisal_request data
        if success, returns url where client can check requested data

    """
    requested_info = AppraisalRequest.objects.get(id=request_id)
    task = AsyncResult(id=requested_info.request_id)
    requested_info.update_status('IN PROGRESS')
    requested_info.requested_info = 'wait for info'

    while not task.ready():
        serializer = AppraisalRequestSerializer(requested_info)
        return Response(serializer.data)
    else:
        try:
            requested_info.requested_info = task.get()
            requested_info.update_status('SUCCESS')
            requested_info.save()
            serializer = AppraisalRequestSerializer(requested_info)
            return Response(serializer.data)
        except Exception as ex:
            if not requested_info.url.startswith("https://www.goodreads.com/book/show/"):
                requested_info.requested_info = f'Occurred an Error - wrong url! try again'
            else:
                requested_info.requested_info = f'Occurred an Error - {ex}! try again'
            requested_info.update_status('FAILURE')
            requested_info.save()
            serializer = AppraisalRequestSerializer(requested_info)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
