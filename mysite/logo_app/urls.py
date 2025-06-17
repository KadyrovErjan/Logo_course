from .views import *
from rest_framework import routers
from django.urls import path, include
from django.contrib.auth import views as auth_views



router = routers.SimpleRouter()
# router.register(r'?', ?ViewSet, basename='?')

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('user/edit/<int:pk>', UserProfileEditAPIView.as_view(), name='user_edit'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='login'),

    path('home/', HomeAPIView.as_view(), name='home'),
    path('whycourse/', WhyCourseAPIView.as_view(), name='whycourse'),
    path('aboutus/', AboutUsAPIView.as_view(), name='aboutus'),
    path('title_for_course/', TitleForCourseAPIView.as_view(), name='title_for_course'),
    path('titlereview/', TitleForReviewAPIView.as_view(), name='title_review'),
    path('titlecourse/', TitleCourseAPIView.as_view(), name='title_course'),

    path('courses/', CourseListAPIView.as_view(), name='course_list'),
    path('courses/<int:pk>', CourseDetailAPIView.as_view(), name='course_detail'),
    path('courses/buy/', PurchaseCourseAPIView.as_view(), name='purchase-course'),

    path('courses/create/', CourseCreateAPIView.as_view(), name='course_create'),
    path('courses/create/<int:pk>', CourseEditAPIView.as_view(), name='course_edit'),

    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/create/<int:pk>', LessonEditAPIView.as_view(), name='lesson-edit'),
    path('lesson/<int:pk>', LessonDetailAPIView.as_view(), name='lesson-detail'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson-list'),

    path('favorite/create', FavoriteCreateAPIView.as_view(), name='favorite_create'),
    path('favorite/', FavoriteListAPIView.as_view(), name='favorite_list'),
    path('favorites/remove/<int:course_id>/', FavoriteDeleteAPIView.as_view(), name='remove-favorite'),

    path('course/reviews/create/', CourseReviewCreateAPIView.as_view(), name='create-course-review'),
    path('course/reviews/', CourseReviewListAPIView.as_view(), name='course-review-list'),

    path('lesson/reviews/create/', LessonReviewCreateAPIView.as_view(), name='create-lesson-review'),
    path('lesson/reviews/', LessonReviewListAPIView.as_view(), name='lesson-review-list'),

    path('titleemail/', EmailTitleAPIView.as_view(), name='title_email'),
    path('email/create', EmailCreateAPIView.as_view(), name='email-create'),

    path('change_password/', change_password, name='change_password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('owners-with-students/', OwnersWithStudentsAPIView.as_view(), name='owners-with-students'),
    path('owner/', OwnerListAPIView.as_view(), name='owner_list'),
    path('owner/<int:pk>', OwnerDetailAPIView.as_view(), name='owner_detail'),

]

