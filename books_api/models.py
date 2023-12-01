from django.db import models


class AppraisalRequest(models.Model):
    STATUS_OF_REQUEST = [
        ('P', 'PENDING'),
        ('I', 'IN PROGRESS'),
        ('S', 'SUCCESS'),
        ('F', 'FAILURE'),
    ]

    url = models.CharField(max_length=128)
    request_id = models.CharField(max_length=64, default='')
    status = models.CharField(max_length=30, choices=STATUS_OF_REQUEST, default='PENDING')
    requested_info = models.CharField(max_length=64, default='')

    def update_status(self, status):
        self.status = status
        self.save()


class Book(models.Model):
    title = models.CharField(max_length=64)
    author = models.CharField(max_length=64)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    total_voters = models.IntegerField()
    book_id = models.CharField(max_length=64)

    def __str__(self):
        return self.title
