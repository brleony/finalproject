from django.db import models

# Create your models here.
class Wallet(models.Model):
    name = models.CharField(max_length = 64)
    currency = models.ForeignKey(
        'Currency',
        on_delete = models.PROTECT,
    )
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
        return f"Wallet {self.id} from {self.user}. Uses {self.currency}. Created on {self.date_created}, last used on {self.last_used}."

class Currency(models.Model):
    name = models.CharField(max_length = 64)
    code = models.CharField(max_length = 4)
    unicode_html = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.id} - {self.code} {self.name} Unicode html: {self.unicode_html}."

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
        (BLUE, 'Blue'),
        (INDIGO, 'Indigo'),
        (PURPLE, 'Purple'),
        (PINK, 'Pink'),
        (RED, 'Red'),
        (ORANGE, 'Orange'),
        (YELLOW, 'Yellow'),
        (GREEN, 'Green'),
        (TEAL, 'Teal'),
        (CYAN, 'Cyan'),
    )
    color = models.CharField(
        max_length = 8,
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
        return f"{self.id} - Category {self.name} from wallet {self.wallet}." \
                f"Color: {self.color}. Icon: {self.icon}. Created on {self.date_created}, last edited on {self.last_edited}."

class Expense(models.Model):
    amount = models.DecimalField(
        "What does it cost?",
        max_digits = 32,
        decimal_places = 2,
    )
    DEBIT = 'Debit'
    CREDIT = 'Credit'
    CASH = 'Cash'
    ONLINE = 'Online'
    PAYPAL = 'Paypal'
    MOBILE = 'Mobile'
    BANKTRANSFER = 'Transfer'
    CHEQUE = 'Cheque'
    OTHER = 'Other'
    METHOD_CHOICES = (
        (DEBIT, 'Debit Card'),
        (CREDIT, 'Credit Card'),
        (CASH, 'Cash'),
        (ONLINE, 'Online'),
        (PAYPAL, 'PayPal'),
        (MOBILE, 'Mobile'),
        (BANKTRANSFER, 'Bank Transfer'),
        (CHEQUE, 'Cheque'),
        (OTHER, 'Other'),
    )
    method = models.CharField(
        'Payment Method',
        choices = METHOD_CHOICES,
        max_length = 8,
    )
    comment = models.CharField(
        max_length = 255,
        blank = True,
    )
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
        on_delete = models.SET_NULL,
        blank = True,
        null = True,
    )
    wallet = models.ForeignKey(
        'Wallet',
        on_delete = models.CASCADE,
    )

    def __str__(self):
        return f"{self.id} - {self.amount} spent from wallet {self.wallet} in category {self.category}." \
                f"Paid with {self.method}. Comment: {self.comment}." \
                f"Spent on {self.date_spent}, created on {self.date_created}, last used on {self.last_edited}."