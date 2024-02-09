from django.contrib.postgres.fields import ArrayField
from django.db import models

from academic_backend.helpers.factories import Factory


class News(Factory):
    co_news = models.AutoField(
        primary_key=True, unique=True,
        db_column='co_noticia'
    )

    no_news = models.CharField(
        max_length=255, blank=False, null=False,
        db_column='no_titulo_noticia'
    )

    ds_news = models.TextField(
        blank=False, null=False,
        db_column='ds_noticia'
    )

    dt_news = models.DateField(
        blank=False, null=False,
        db_column='dt_noticia'
    )

    class Meta:
        db_table = 'tb_noticia'