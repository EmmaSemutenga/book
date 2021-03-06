from django.db import models


from django.urls import reverse


class Book(models.Model):
    name = models.CharField(max_length=200)
    pages = models.IntegerField()

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('book_view', kwargs={'pk': self.pk})

    def get_book_name(self):
        return self.name