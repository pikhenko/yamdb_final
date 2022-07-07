import uuid
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES_LIST = (
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
    ('user', 'Пользователь'),
)


def user_validation(name):
    if name == 'me':
        raise ValidationError(
            ('Требуется изменить имя <me>.'),
            params={'value': name},
        )


class User(AbstractUser):
    username = models.CharField(
        validators=(user_validation,),
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
    )
    role = models.CharField(
        max_length=150,
        choices=ROLES_LIST,
        default='user',
    )
    confirmation_code = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        null=True,
        blank=True

    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        verbose_name='О себе',
        blank=True
    )
    password = models.CharField(
        blank=True,
        max_length=128
    )

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username
