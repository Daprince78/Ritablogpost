from django.db import models

# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        """{return self.search} (this is also the simplest way of doing this"""
        return '{}'.format(self.search)

    class Meta:
        verbose_name_plural = 'Searches'