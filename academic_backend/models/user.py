from django.db import models

from academic_backend.helpers.factories import Factory


class User(Factory):
    co_user = models.AutoField(
        primary_key=True, unique=True, 
        db_column='co_usuario'
        )
    no_user = models.CharField(
        max_length=255, blank=False, null=False,
        db_column='no_usuario'
        )
    
    co_registration = models.CharField(
        max_length=100, blank=False, 
        db_column='co_matricula'
        )
    
    co_profile = models.IntegerField(
        blank=False, db_column='co_tipo_perfil'
        )
    
    ds_email = models.CharField(
        max_length=255, blank=False, 
        db_column='ds_email'
        )
    
    ds_password = models.CharField(
        max_length=255, blank=False, 
        db_column='ds_senha'
        )
    
    ds_phone = models.CharField(
        max_length=255, blank=True, 
        db_column='ds_telefone'
        )

    class Meta:
        db_table = 'tb_usuario'
