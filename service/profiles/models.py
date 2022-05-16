import uuid
from django.db import models
from users.models import User

class Profile(models.Model):

    ROLES = (
        (0, 'None'),
        (1, 'Dev-Backend'),
        (2, 'Dev-Frontend'),
        (3, 'Devops'),
        (3, 'QA'),
    )

    state = models.BooleanField('Estado', default=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateField('Fecha de Creacion', auto_now=False, auto_now_add=True)
    modified_date = models.DateField('Fecha de Modificacion', auto_now=True, auto_now_add=False)
    delete_date = models.DateField('Fecha de Eliminacion', auto_now=True, auto_now_add=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rol = models.IntegerField('Roles',choices=ROLES, default=0)
    first_name = models.CharField('Nombres', max_length=255, blank=False, null=False)
    last_name = models.CharField('Apellidos', max_length=255, blank=True, null=True)
    description = models.CharField('Description de Usuario', max_length=50, blank=False, null=False)
    email = models.EmailField('Correo Electrónico', max_length=255, unique=True )
    phone = models.CharField('Telefono', max_length=255, blank=True)
    git = models.CharField('github',max_length=255, blank=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class CategorySkill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateField('Fecha de Creacion', auto_now=False, auto_now_add=True)
    modified_date = models.DateField('Fecha de Modificacion', auto_now=True, auto_now_add=False)
    delete_date = models.DateField('Fecha de Eliminacion', auto_now=True, auto_now_add=False)
    name_category = models.CharField('Nombre de Categoria de Habilidades', max_length=255, blank=False, null=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_category + " - " + self.profile.first_name

    class Meta:
        ordering = ['name_category']

class Skill(models.Model):
    LEVELS = (
        (0, 'None'),
        (1, 'Basic'),
        (2, 'Intermedium'),
        (3, 'Advanced'),
        (4, 'Native'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_date = models.DateField('Fecha de Creacion', auto_now=False, auto_now_add=True)
    modified_date = models.DateField('Fecha de Modificacion', auto_now=True, auto_now_add=False)
    delete_date = models.DateField('Fecha de Eliminacion', auto_now=True, auto_now_add=False)
    name  = models.CharField('Nombre de Habilidad', max_length=255, blank=False, null=False)
    level = models.IntegerField('Nivel de Habilidad',choices=LEVELS, default=0)
    category_skill = models.ManyToManyField(CategorySkill)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
