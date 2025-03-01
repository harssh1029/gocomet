from django.db import models
import random

class Destination(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    clues = models.JSONField()  # Stores list of clues
    fun_fact = models.JSONField()  # Stores list of fun facts
    trivia = models.JSONField()  # Stores list of trivia

    def get_random_clues(self):
        return random.sample(self.clues, 2) if len(self.clues) > 1 else self.clues

    def get_random_fact(self):
        return random.choice(self.fun_fact)