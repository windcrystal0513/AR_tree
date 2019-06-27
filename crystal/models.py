from django.db import models

class Topic(models.Model):
    """出版社"""
    topic_name = models.CharField(max_length=30)
    topic_id=models.IntegerField(max_length=10)
    domain_id=models.IntegerField(max_length=5)
    def __unicode__(self):
        return self.topic_name

