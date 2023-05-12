from django.db import models


class TimeStampedModel(models.Model):
    class Meta:
        abstract = True

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class City(TimeStampedModel):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.name


class House(TimeStampedModel):
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, blank=True, null=True)
    link = models.URLField(max_length=256, unique=True)
    region = models.CharField(max_length=64)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024, null=True, blank=True)
    price = models.IntegerField()
    year_of_construction = models.IntegerField()
    area = models.IntegerField()
    floor = models.IntegerField()
    room = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.city}/{self.region}"
