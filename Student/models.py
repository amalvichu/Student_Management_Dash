from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100) # [cite: 30]
    description = models.TextField(blank=True, null=True) # [cite: 31]
    created_at = models.DateTimeField(auto_now_add=True) # [cite: 32]

    def __str__(self):
        return self.name

class Student(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ] # [cite: 26]
    
    name = models.CharField(max_length=150) # [cite: 14]
    email = models.EmailField(unique=True) # [cite: 16]
    register_number = models.CharField(max_length=50, unique=True) # [cite: 18]
    course = models.CharField(max_length=100) # [cite: 20]
    batch = models.CharField(max_length=20) # [cite: 22]
    department = models.CharField(max_length=100) # [cite: 24]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active') # [cite: 26]
    created_at = models.DateTimeField(auto_now_add=True) # [cite: 25]

    def __str__(self):
        return f"{self.name} ({self.register_number})"

class Achievement(models.Model):
    STATUS_CHOICES = [
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending'),
    ] # [cite: 27]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='achievements')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True) # [cite: 21]
    title = models.CharField(max_length=200) # [cite: 15]
    description = models.TextField() # [cite: 17]
    proof = models.FileField(upload_to='achievement_proofs/', blank=True, null=True) # [cite: 19]
    date = models.DateField() # [cite: 23]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending') # [cite: 27]
    created_at = models.DateTimeField(auto_now_add=True) # [cite: 28]

    def __str__(self):
        return self.title