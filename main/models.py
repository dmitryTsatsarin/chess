from django.db import models

# Create your models here.
class Member(models.Model):
    name=models.CharField(max_length=100)
    elo=models.IntegerField(verbose_name="ELO")
    elo_new=models.IntegerField(verbose_name="ELO after tournament", null=True)

    def __unicode__(self):
        return "%s %s"% (self.name,self.elo)

class Tournament(models.Model):
    start=models.BooleanField()
    tour_closed=models.IntegerField(null=True)
    tour_last=models.IntegerField(null=True)

    def __unicode__(self):
        return "Tournament start=%s" %self.start

class Tour(models.Model):
    tour=models.IntegerField(verbose_name="Tour number")
    player1=models.ForeignKey(Member,related_name='player1')
    player2=models.ForeignKey(Member,related_name='player2',null=True)
    points=models.FloatField(null=True)


