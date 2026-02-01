from django.db import models

# Create your models here.

class Player(models.Model):
    username = models.CharField(max_length=150,null=False,blank=False,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.username


class Score(models.Model):
    player=models.ForeignKey(Player,on_delete=models.CASCADE,related_name="score")
    points = models.IntegerField()
    achieved_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
        # unique_together = ['player', 'points']  
    def __str__(self):
        return f"{self.player.username} - {self.points}"