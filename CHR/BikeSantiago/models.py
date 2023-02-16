from django.db import models

class Address(models.Model):
    id = models.IntegerField(primary_key=True)
    slots = models.IntegerField(null=True, blank=True)
    address = models.CharField(verbose_name='Dirección', max_length=100, null=True, blank=True)
    payment = models.CharField(verbose_name='Método de pagos', max_length=100, null=True, blank=True)
    has_ebikes = models.BooleanField(verbose_name='¿Tiene ebikes?')
    payment_terminal = models.BooleanField(verbose_name='Terminal de pagos')
    last_updated = models.CharField(verbose_name='Ultima actualización', max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.id}'


class Station(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    name = models.CharField(max_length=100, null=True, blank=True)
    free_bikes = models.IntegerField(verbose_name='Disponibles', null=True, blank=True)
    empty_slots = models.IntegerField(verbose_name='Ranuras vacias', null=True, blank=True)
    timestamp = models.DateTimeField(verbose_name='Fecha')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    extra = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


