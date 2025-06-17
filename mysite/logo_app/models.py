from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
USER_ROLE = (
    ('Владелец', 'Владелец'),
    ('Студент', 'Студент')
)



class UserProfile(AbstractUser):
    role = models.CharField(max_length=10, choices=USER_ROLE, default='Студент')
    avatar = models.ImageField(upload_to='user_avatar/', null=True, blank=True)

    def __str__(self):
        return self.username

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(
        reverse('password_reset:reset-password-request'),
        reset_password_token.key
    )

    send_mail(
        # Subject
        "Password Reset for {title}".format(title="Some website title"),
        # Message
        email_plaintext_message,
        # From email
        "noreply@somehost.local",
        # Recipient list
        [reset_password_token.user.email]
    )


class RegisterEmail(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
class Home(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='home_image/')

    def __str__(self):
        return self.title


class Highlight(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='home_highlights')
    title = models.CharField(max_length=54)
    icon = models.ImageField(upload_to='highlight_icon/')
    description = models.TextField()


class WhyCourse(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    title_of_number1 = models.CharField(max_length=5)
    description_of_number1 = models.TextField()
    title_of_number2 = models.CharField(max_length=5)
    description_of_number2 = models.TextField()

    def __str__(self):
        return self.title

class WhyCourseHighlight(models.Model):
    whycourse = models.ForeignKey(WhyCourse, on_delete=models.CASCADE, related_name='whycourse_highlight')
    highlight_title = models.CharField(max_length=54)
    highlight_icon = models.ImageField(upload_to='highlight_icon/')
    highlight_description = models.TextField()

class TitleForCourse(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()

class TitleForReview(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

class EmailTitle(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

class AboutUs(models.Model):
    title = models.CharField(max_length=300)
    title_author = models.CharField(max_length=32)
    author_image = models.ImageField(upload_to='author_image/')
    author_bio = models.TextField()

    def __str__(self):
        return self.title

class AboutUsImage(models.Model):
    about_us = models.ForeignKey(AboutUs, on_delete=models.CASCADE, related_name='aboutus_images')
    image = models.ImageField(upload_to='aboutus_image/')

class TitleCourse(models.Model):
    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to='course_list_image/')
    famous_course = models.CharField(max_length=100)
    famous_course_description = models.TextField()

class Category(models.Model):
    category_name = models.CharField(max_length=32)

    def __str__(self):
        return self.category_name

class Course(models.Model):
    owner = models.ForeignKey(UserProfile, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    brief_description = models.TextField()
    description = models.TextField()
    price = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='course_images/')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    time_image = models.ImageField(upload_to='time_image/')
    lesson_image = models.ImageField(upload_to='lesson_image/')
    progress_image = models.ImageField(upload_to='progress_image/')
    progress = models.CharField(max_length=32)
    status_course = models.CharField(max_length=20, choices=[('Бесплатно', 'Бесплатно'), ('Платно', 'Платно')],
                                         default='Бесплатно')

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_lessons')
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='lesson_video/')
    goal = models.CharField(max_length=100)
    video_time = models.DurationField()
    STATUS_LESSON = (
        ('Открытый', 'Открытый'),
        ('Закрытый', 'Закрытый')
    )
    status = models.CharField(max_length=20, choices=STATUS_LESSON, default='Открытый')
    created_date = models.DateField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)


class CourseReview(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    city = models.CharField(max_length=43)
    region = models.CharField(max_length=43)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'course')

class LessonReview(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user} - {self.course}"

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user.username} - {self.course.title}'

class PurchasedCourse(models.Model):
    user = models.ForeignKey(UserProfile, related_name='purchased_courses', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

