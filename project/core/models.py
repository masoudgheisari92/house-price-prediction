from django.db import models


class TimeStampedModel(models.Model):
    class Meta:
        abstract = True

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class City(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self) -> str:
        return self.name


class Region(TimeStampedModel):
    city = models.ForeignKey(to=City, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"{self.city}/{self.name}"


class House(TimeStampedModel):
    region = models.ForeignKey(
        to=Region, on_delete=models.CASCADE, blank=True, null=True
    )
    link = models.URLField(max_length=256, unique=True)
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1024, null=True, blank=True)
    price = models.IntegerField()
    year_of_construction = models.IntegerField()
    area = models.IntegerField()
    floor = models.IntegerField()
    room = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.city}/{self.region}"
