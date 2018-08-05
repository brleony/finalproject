from django.db import models

# Create your models here.
class Wallet(models.Model):
    name = models.CharField(max_length = 64)
    #currency
    date_created = models.DateTimeField(
        'Date Created',
        auto_now_add = True,
    )
    last_used = models.DateTimeField(
        'Last Used',
        auto_now = True,
    )
    user = models.ForeignKey(
        'auth.User',
        on_delete = models.CASCADE,
    )

    def __str__(self):
        return f"{self.id}"

class Category(models.Model):
    name = models.CharField(max_length = 64)
    BLUE = 'blue'
    INDIGO = 'indigo'
    PURPLE = 'purple'
    PINK = 'pink'
    RED = 'red'
    ORANGE = 'orange'
    YELLOW = 'yellow'
    GREEN = 'green'
    TEAL = 'teal'
    CYAN = 'cyan'
    COLOR_CHOICES = (
        (BLUE),
        (INDIGO),
        (PURPLE),
        (PINK),
        (RED),
        (ORANGE),
        (YELLOW),
        (GREEN),
        (TEAL),
        (CYAN),
    )
    color = models.CharField(
        max_length = 64,
        choices = COLOR_CHOICES,
        default = 'cyan',
    )
    icon = models.CharField(
        max_length = 64,
        default = 'fa-asterisk',
    )
    date_created = models.DateTimeField(
        'Date Created',
        auto_now_add = True,
    )
    last_edited = models.DateTimeField(
        'Last Edited',
        auto_now = True,
    )
    wallet = models.ForeignKey(
        'Wallet',
        on_delete = models.CASCADE,
    )

    def __str__(self):
        return f"{self.id}"

class Expense(models.Model):
    amount = models.DecimalField( ###
        "What does it cost?",
        max_digits = 20,
        decimal_places = 2,
    )
    comment = models.CharField(max_length = 255)
    date_spent = models.DateTimeField(
        'Date Spent',
    )
    date_created = models.DateTimeField(
        'Date Created',
        auto_now_add = True,
    )
    last_edited = models.DateTimeField(
        'Last Edited',
        auto_now = True,
    )
    category = models.ForeignKey(
        'Category',
        on_delete = models.CASCADE, #TODO
    )
    wallet = models.ForeignKey(
        'Wallet',
        on_delete = models.CASCADE,
    )

    def __str__(self):
        return f"{self.id}"