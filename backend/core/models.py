from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    '''Manager for users'''

    def create_user(self, email, password=None, **extra_fields):
        '''Create, save and return a new user with the given information'''

        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        '''Create and save a superuser with the given information'''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    '''User in the system'''
    email = models.EmailField(max_length=100, unique=True)
    nickname = models.CharField(max_length=15)
    first_name = models.CharField(max_length=15)
    middle_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to="images/", blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=0)
    # Set false when introducing verification functionalities
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return f'[{self.nickname}] {self.get_full_name}'

    @property
    def get_full_name(self):
        return f'{self.first_name.title()} {self.last_name.title()}'


class Country(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class County(models.Model):
    name = models.CharField(max_length=20)
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE,
                                related_name='counties'
                                )

    class Meta:
        verbose_name_plural = 'Counties'

    def __str__(self):
        return self.name


class City(models.Model):
    class Meta:
        verbose_name_plural = 'Cities'

    county = models.ForeignKey(County,
                               on_delete=models.CASCADE,
                               related_name='cities'
                               )
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Address(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='user_address')
    post_code = models.CharField(max_length=10)
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        related_name='city_address'
    )
    street_address1 = models.CharField(max_length=50)
    street_address2 = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'{self.user.nickname} - {self.name}'

    def get_full_address(self):
        full_address = (self.city.county.country.name,
                        self.post_code,
                        self.city.county.name,
                        self.city.name,
                        self.street_address1,
                        self.street_address2)
        return full_address
