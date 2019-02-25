from django.db import models


class Conso(models.Model):
    client_id = models.IntegerField()
    janvier = models.FloatField()
    fevrier = models.FloatField()
    mars = models.FloatField()
    avril = models.FloatField()
    mai = models.FloatField()
    juin = models.FloatField()
    juillet = models.FloatField()
    aout = models.FloatField()
    septembre = models.FloatField()
    octobre = models.FloatField()
    novembre = models.FloatField()
    decembre = models.FloatField()
    year = models.IntegerField()

    def __str__(self):
        return str(self.client_id)

    def __iter__(self):
        return iter([
            self.janvier, self.fevrier, self.mars, self.avril, self.mai,
            self.juin, self.juillet, self.aout, self.septembre, self.octobre,
            self.novembre, self.decembre
        ])

    class Meta:
        abstract = True


class Conso_eur(Conso):
    pass


class Conso_watt(Conso):
    pass
