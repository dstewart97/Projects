from django.db import models



class Topic(models.Model):
    key = models.CharField(max_length=100)
    values = models.TextField(help_text="Comma-seperated keywords for topics")
    selected = models.BooleanField(default=False, help_text="Use this topic for analysis")

    @property
    def tooltip_text(self):
        return self.values

    def __str__(self):
        return self.key
