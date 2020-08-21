from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    """Тема, которую изучает пользователь"""
    text = models.CharField("Title", max_length=200)
    image = models.ImageField("Image", upload_to="images_topics/", default='default.png')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")

    def __str__(self):
        """Возвращает строковое представление модели."""
        return self.text


class Entry(models.Model):
    """Информация, изученная пользователем по теме"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name="Topic")
    image = models.ImageField("Image", upload_to="images_entries/", default='default.png')
    text = models.TextField(verbose_name="Content")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Date")

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        """Возвращает строковое представление модели."""
        if len(self.text) <= 100:
            return self.text
        return f"{self.text[:100]}..."
