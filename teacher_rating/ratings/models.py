from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

class Teacher(models.Model):
    name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)  # Текущий рейтинг преподавателя
    image = models.ImageField(upload_to='teacher_images/', null=True, blank=True)  # Поле для изображения
    created_at = models.DateTimeField(auto_now_add=True)

    def update_rating(self):
        # Обновляем рейтинг на основе всех одобренных поступков
        approved_actions = self.actions.filter(status='approved')
        self.rating = approved_actions.aggregate(Sum('points'))['points__sum'] or 0
        self.save()

    def get_rank(self):
        all_teachers = Teacher.objects.all().order_by('-rating')
        rank = list(all_teachers).index(self) + 1
        return rank

    def __str__(self):
        return self.name

class Action(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    teacher = models.ForeignKey(Teacher, related_name='actions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    points = models.IntegerField() 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} by {self.user.username}"

@receiver(post_save, sender=Action)
def update_teacher_rating(sender, instance, **kwargs):
    if instance.status in ['approved', 'rejected']:
        instance.teacher.update_rating()

class Review(models.Model):
    teacher = models.ForeignKey(Teacher, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.teacher.name}"
