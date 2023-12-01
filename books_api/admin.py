from django.contrib import admin
from .models import Book, AppraisalRequest

admin.site.register(Book)
admin.site.register(AppraisalRequest)