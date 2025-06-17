from rest_framework import permissions

class UserEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.id == request.user.id:
            return True
        return False


class CheckUserOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'Владелец':
            return True
        return False

class CheckUserStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'Студент':
            return True
        return False


class IsLessonOpen(permissions.BasePermission):
    message = "У вас нет доступа к этому уроку — он закрыт."

    def has_object_permission(self, request, view, obj):
        # obj — это экземпляр Lesson
        return obj.status == 'Открытый'

class IsSelfOrCourseOwner(permissions.BasePermission):
    """
    Разрешает доступ, если:
    - request.user — это сам объект UserProfile (просматривает свой профиль), ИЛИ
    - request.user — владелец любого курса, который купил этот студент.
    """

    message = "Доступ разрешён только владельцу профиля или владельцу курса."

    def has_object_permission(self, request, view, obj):
        # 1) Сам себе
        if request.user == obj:
            return True

        # 2) Проверяем, купил ли obj курс у request.user
        #    purchased_courses — related_name модели PurchasedCourse у UserProfile
        for purchase in obj.purchased_courses.all():
            if purchase.course.owner == request.user:
                return True

        return False