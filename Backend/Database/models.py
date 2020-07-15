from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    """Lets me modify the base user model"""

    def create_user(self, email, password=None, **extra_fields):
        """Creates a new user"""
        if not email:
            raise ValueError('Email address is required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


def get_sentinel_user():
    """Either gets or creates an account that will be swapped
    with all foreign key references to a user if they delete their
    account """
    return get_user_model().objects.get_or_create(username='Deleted',
                                                  email='deleted@gmail.com')


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Creates a custom user model using email as identifer
    but returns a username for its string representation"""
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=128, unique=True)
    password = models.CharField(max_length=254)
    salt = models.CharField(max_length=128)
    email_verified = models.BooleanField(default=False)
    avatar = models.ImageField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Questions(models.Model):
    """Creates a model for quiz questions"""
    category = models.CharField(max_length=254)
    difficulty = models.CharField(max_length=8)
    question_type = models.CharField(max_length=20)
    text = models.CharField(max_length=254)

    objects = models.Manager()

    def __str__(self):
        return self.text


class Answers(models.Model):
    """Creates a model for answers"""
    question = models.ForeignKey('Questions', models.DO_NOTHING)
    correct_answer = models.CharField(max_length=254)
    incorrect_answer = models.CharField(max_length=254)
    incorrect_answer2 = models.CharField(max_length=254)
    incorrect_answer3 = models.CharField(max_length=254)

    objects = models.Manager()

    def __str__(self):
        return self.question


class UserAnswers(models.Model):
    """Creates a model for a users answers to questions"""
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    question_id = models.ForeignKey(
        Questions,
        on_delete=models.CASCADE,
    )
    result = models.BooleanField(default=False)
    count_correct = models.SmallIntegerField()
    count_incorrect = models.SmallIntegerField(blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.result


class UserRelationships(models.Model):
    """Creates a model for recording relationships between users"""
    RELATIONSHIP_STATUS = (
        ('pending', 'Pending'),
        ('friends', 'Friends'),
        ('blocked', 'Blocked')
    )

    id = models.BigAutoField(primary_key=True)
    user_first_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_first_id',
    )
    user_second_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_second_id',
    )
    relationship_status = models.CharField(
        max_length=7, choices=RELATIONSHIP_STATUS)

    objects = models.Manager()

    def __str__(self):
        return self.relationship_status


class LoginAttempts(models.Model):
    """Creates a model to record a users login activity"""
    LOGIN_STATUS = (
        ('failed', 'Failed'),
        ('success', 'success')
    )

    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    last_login = models.DateTimeField(default=timezone.now)
    login_status = models.CharField(max_length=7, choices=LOGIN_STATUS)

    objects = models.Manager()

    def __str__(self):
        return self.login_status


class Practice(models.Model):
    """Creates a model to record a users practice matches"""
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    score = models.SmallIntegerField()
    start_time = models.DateTimeField(default=timezone.now)
    time_taken = models.TimeField()

    objects = models.Manager()

    def __str__(self):
        return self.score


class Results(models.Model):
    """Creates a model to record results for every match"""
    id = models.BigAutoField(primary_key=True)
    winner_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name='winner_id',
    )
    second_place_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name='second_place_id',
    )
    third_place_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name='third_place_id',
    )
    fourth_place_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name='fourth_place_id',
    )
    fifth_place_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name='fifth_place_id',
    )
    sixth_place_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        related_name='sixth_place_id',
    )
    objects = models.Manager()

    def __str__(self):
        return self.winner_id


class SuddenDeath(models.Model):
    """Creates a model to record the results of any matches that
    make it to sudden death"""
    id = models.BigAutoField(primary_key=True)
    rounds = models.SmallIntegerField()
    objects = models.Manager()

    def __str__(self):
        return self.rounds


class Games(models.Model):
    """Creates a model to record setup details of each game"""
    CATEGORY = (
        ('general knowledge', 'general knowledge'),
        ('science', 'science'),
        ('mythology', 'mythology'),
        ('sports', 'sports'),
        ('geography', 'geography'),
        ('history', 'history'),
        ('politics', 'politics'),
        ('art', 'art'),
        ('celebrities', 'celebrities'),
        ('animals', 'animals'),
        ('vehicles', 'vehicles'),
        ('entertainment', 'entertainment'),
        ('random', 'random')
    )

    id = models.BigAutoField(primary_key=True)
    number_of_questions = models.SmallIntegerField()
    number_of_players = models.SmallIntegerField()
    start_time = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=18, choices=CATEGORY)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
    )
    result_id = models.ForeignKey(
        Results, on_delete=models.CASCADE, null=True, blank=True)
    sudden_death_id = models.ForeignKey(
        SuddenDeath, on_delete=models.CASCADE, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.created_by


class UserScores(models.Model):
    """Creates a model to record the scores for each game"""
    id = models.BigAutoField(primary_key=True)
    game_id = models.ForeignKey(Games, on_delete=models.CASCADE)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    base_score = models.SmallIntegerField()
    bonus_score = models.DecimalField(max_digits=6, decimal_places=3)
    total_score = models.DecimalField(max_digits=6, decimal_places=3)
    time_taken = models.TimeField()

    objects = models.Manager()

    def __str__(self):
        return self.total_score
