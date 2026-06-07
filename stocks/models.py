from django.db import models
from django.contrib.auth.models import User

# 1. Profile Model:
class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=10000.00) # Default 10k balance

    def __str__(self):
        return f"{self.user.username}'s Wallet - {self.balance}"

# 2. Stock Model: 
class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True) # e.g., AAPL, RELIANCE
    name = models.CharField(max_length=100)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    initial_price = models.DecimalField(max_digits=10, decimal_places=2) # P&L calculate karne ke liye

    # Admin  profit/loss  
    @property
    def admin_stock_pnl(self):
        return self.current_price - self.initial_price

    def __str__(self):
        return f"{self.name} ({self.ticker}) - ₹{self.current_price}"

# 3. User Portfolio: User ne kaunsa stock kitna kharida
class UserPortfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    @property
    def current_investment_value(self):
        return self.quantity * self.stock.current_price

    def __str__(self):
        return f"{self.user.username} holds {self.quantity} shares of {self.stock.ticker}"

# 4. Transaction Model:
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True , blank=True)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    quantity = models.PositiveIntegerField()
    price_at_transaction = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2) # User ka Expense
    admin_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) # Admin ka direct profit
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.stock.ticker}"
