from datetime import datetime
from itertools import chain

from django.urls import reverse

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Position(models.Model):
    job_id = models.CharField(max_length=10)
    title = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    location = models.CharField(max_length=500)
    description = models.TextField()
    apply_url = models.URLField()
    source = models.CharField(max_length=100)
    position_type = models.CharField(max_length=100)
    updated_at = models.DateTimeField(default=datetime.utcnow)

    class Meta:
        ordering = ('department', 'title',)

    def __str__(self):
        return '{}@{}'.format(self.job_id, self.source)

    @property
    def location_list(self):
        return sorted(self.location.split(','))

    def get_absolute_url(self):
        return reverse('careers.position',
                       kwargs={'source': self.source, 'job_id': self.job_id})

    @classmethod
    def position_types(cls):
        return sorted(set(cls.objects.values_list('position_type', flat=True)))

    @classmethod
    def locations(cls):
        return sorted(set(
            location.strip() for location in chain(
                *[locations.split(',') for locations in
                  cls.objects.values_list('location', flat=True)])))

    @classmethod
    def categories(cls):
        return sorted(set(cls.objects.values_list('department', flat=True)))
