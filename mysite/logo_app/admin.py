from django.contrib import admin
from .models import *

class HighlightInline(admin.TabularInline):
    model = Highlight
    extra = 1

class WhyCourseHighlightInline(admin.TabularInline):
    model = WhyCourseHighlight
    extra = 1

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

class AboutUsImageInline(admin.TabularInline):
    model = AboutUsImage
    extra = 1

class HomeAdmin(admin.ModelAdmin):
    inlines = [HighlightInline]

class WhyCourseAdmin(admin.ModelAdmin):
    inlines = [WhyCourseHighlightInline]

class AboutUsAdmin(admin.ModelAdmin):
    inlines = [AboutUsImageInline]

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]

admin.site.register(UserProfile)
admin.site.register(Home, HomeAdmin)
admin.site.register(WhyCourse, WhyCourseAdmin)
admin.site.register(AboutUs, AboutUsAdmin)
admin.site.register(Category)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseReview)
admin.site.register(LessonReview)
admin.site.register(TitleForCourse)
admin.site.register(TitleForReview)
admin.site.register(EmailTitle)
admin.site.register(TitleCourse)

