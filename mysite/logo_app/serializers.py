from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден")

        if not user.check_password(password):
            raise serializers.ValidationError("Неверный пароль")

        if not user.is_active:
            raise serializers.ValidationError("Пользователь не активен")

        self.context['user'] = user
        return data

    def to_representation(self, instance):
        user = self.context['user']
        refresh = RefreshToken.for_user(user)

        return {
            'user': {
                'username': user.username,
                'email': user.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    model = UserProfile
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'avatar']

class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'avatar', 'email']

class HighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Highlight
        fields = ['id', 'home', 'icon', 'description']

class HomeSerializers(serializers.ModelSerializer):
    highlight = HighlightSerializer(many=True, read_only=True)
    class Meta:
        model = Home
        fields = ['id', 'title', 'description', 'image', 'highlight']

class WhyCourseHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyCourseHighlight
        fields = ['id', 'highlight_title', 'highlight_icon', 'highlight_description']

class WhyCourseSerializer(serializers.ModelSerializer):
    whycourse_highlight = WhyCourseHighlightSerializer(many=True, read_only=True)
    class Meta:
        model = WhyCourse
        fields = ['id', 'title', 'description',  'title_of_number1', 'description_of_number1', 'title_of_number2', 'description_of_number2', 'whycourse_highlight']

class TitleForCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleForCourse
        fields = '__all__'


class TitleForReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleForReview
        fields = '__all__'


class EmailTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTitle
        fields = '__all__'

class AboutUsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUsImage
        fields = ['id', 'image']

class AboutUsSerializer(serializers.ModelSerializer):
    aboutus_images = AboutUsImageSerializer(many=True, read_only=True)
    class Meta:
        model = AboutUs
        fields = ['id', 'title', 'title_author', 'author_image', 'author_bio', 'aboutus_images']



class TitleCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleCourse
        fields = '__all__'


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video', 'goal', 'video_time', 'status']

class LessonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video', 'goal', 'video_time', 'status', 'created_date', 'views']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']

class CourseDetailSerializer(serializers.ModelSerializer):
    course_lessons = LessonListSerializer(many=True, read_only=True)
    category = CategorySerializer()
    class Meta:
         model = Course
         fields = ['id', 'category', 'title', 'description', 'course_lessons']

class CourseListSerializer(serializers.ModelSerializer):
    total_duration = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'brief_description', 'image', 'price', 'status_course', 'time_image', 'total_duration', 'lesson_image', 'lessons_count', 'progress_image', 'progress', 'is_favorite']

    def get_total_duration(self, obj):
        total = sum((lesson.video_time for lesson in obj.course_lessons.all()), timedelta())
        return str(total)

    def get_lessons_count(self, obj):
        return f'{obj.course_lessons.count()} уроков'

    def get_is_favorite(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, course=obj).exists()
        return False

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'course']
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)

class FavoriteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'course']

class PurchaseCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchasedCourse
        fields = ['course']

    def validate(self, data):
        user = self.context['request'].user
        course = data['course']
        if PurchasedCourse.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError("Курс уже куплен")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        return PurchasedCourse.objects.create(user=user, **validated_data)

class UserProfileListSerializer(serializers.ModelSerializer):
    favorites = FavoriteSerializer(many=True, read_only=True)
    purchased_courses = PurchaseCourseSerializer(many=True, read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'avatar', 'role', 'favorites', 'purchased_courses']

    def get_queryset(self):
        user = self.request.user
        # Если текущий пользователь — студент, возвращаем его профиль,
        # иначе — пустой список
        if user.role == 'Студент':
            return UserProfile.objects.filter(id=user.id)
        return UserProfile.objects.none()

class CourseReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseReview
        fields = ['id', 'course', 'city', 'region', 'rating', 'comment']
        extra_kwargs = {'user': {'read_only': True}}

class LessonReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonReview
        fields = ['id', 'lesson', 'comment', 'created_date']
        extra_kwargs = {'user': {'read_only': True}}

class CourseReviewListSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    class Meta:
        model = CourseReview
        fields = ['id', 'user', 'course', 'city', 'region', 'rating', 'comment']

class LessonReviewListSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    class Meta:
        model = LessonReview
        fields = ['id', 'user', 'lesson', 'comment', 'created_date']

class EmailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterEmail
        fields = '__all__'


class StudentWithCategoriesSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'avatar', 'categories']

    def get_categories(self, obj):
        owner = self.context.get('owner')
        purchased_courses = obj.purchased_courses.filter(course__owner=owner).select_related('course__category')
        categories = set(purchase.course.category for purchase in purchased_courses)
        return CategorySerializer(categories, many=True).data


# class OwnerWithStudentsSerializer(serializers.ModelSerializer):
#     students = serializers.SerializerMethodField()
#
#     class Meta:
#         model = UserProfile
#         fields = ['id', 'username', 'avatar', 'students']
#
#     def get_students(self, obj):
#         students_qs = UserProfile.objects.filter(
#             role='Студент',
#             purchased_courses__course__owner=obj
#         ).distinct()
#         return StudentWithCategoriesSerializer(
#             students_qs,
#             many=True,
#             context={'owner': obj}
#         ).data


class OwnerWithStudentsFullSerializer(serializers.ModelSerializer):
    students_paid = serializers.SerializerMethodField()
    students_free = serializers.SerializerMethodField()
    students_both = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'avatar', 'students_paid', 'students_free', 'students_both']

    def _get_students_by_course_status(self, obj, status):
        return UserProfile.objects.filter(
            role='Студент',
            purchased_courses__course__owner=obj,
            purchased_courses__course__status_course=status
        ).distinct()

    def get_students_paid(self, obj):
        qs = self._get_students_by_course_status(obj, 'Платно')
        return StudentWithCategoriesSerializer(qs, many=True, context={'owner': obj}).data

    def get_students_free(self, obj):
        qs = self._get_students_by_course_status(obj, 'Бесплатно')
        return StudentWithCategoriesSerializer(qs, many=True, context={'owner': obj}).data

    def get_students_both(self, obj):
        paid = self._get_students_by_course_status(obj, 'Платно')
        free = self._get_students_by_course_status(obj, 'Бесплатно')
        both = paid & free  # пересечение QuerySet'ов
        return StudentWithCategoriesSerializer(both, many=True, context={'owner': obj}).data

class OwnerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'avatar', 'role']

class CourseCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class LessonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
