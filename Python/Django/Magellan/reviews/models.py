from django.db import models



class ReviewData(models.Model):
    date = models.DateTimeField()
    product = models.CharField(max_length=255)
    credit_type = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    rating_int = models.IntegerField()
    title = models.CharField(max_length=255)
    verified_customer = models.CharField(max_length=100)
    body = models.TextField()
    helpful = models.IntegerField()
    not_helpful = models.IntegerField()
    comment = models.IntegerField()
    sentiment_category = models.CharField(max_length=100)
    dominant_topic = models.CharField(max_length=100)
    topic1 = models.CharField(max_length=100, blank=True, null=True)
    topic2 = models.CharField(max_length=100, blank=True, null=True)
    topic3 = models.CharField(max_length=100, blank=True, null=True)
    topic4 = models.CharField(max_length=100, blank=True, null=True)
    topic5 = models.CharField(max_length=100, blank=True, null=True)

    # class Meta:
    #     app_label = 'magellan.reviews'

    def __str__(self):
        return f"{self.date} - {self.product}"

