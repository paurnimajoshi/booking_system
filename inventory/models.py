from django.db import models

MAX_BOOKINGS = 2

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    booking_count = models.IntegerField(default=0)  # Added field
    date_joined = models.DateField(null=True, blank=True)  # Added field

    def __str__(self):
        return self.name

class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)  # Added field
    total_count = models.IntegerField()
    remaining_count = models.IntegerField()
    expiration_date = models.DateField(null=True, blank=True)  # Added field

    def __str__(self):
        return f"{self.name} (Remaining: {self.remaining_count})"

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} by {self.member.name}"
