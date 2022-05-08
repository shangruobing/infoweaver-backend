from rest_framework.permissions import BasePermission, SAFE_METHODS

ROLE_CHOICES = [
    ('0', 'Administrator'),
    ('1', 'Student'),
    ('2', 'Teacher')
]

ADMIN = "0"
STUDENT = "1"
TEACHER = "2"


class AdminPermission(BasePermission):
    message = '仅管理员有权限访问'

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user.role == ADMIN:
            return True

        return False


class StudentOnlyReadPermission(BasePermission):
    message = '管理员、教师有权限操作,学生仅可查看'

    def has_permission(self, request, view):
        if request.user.role in (ADMIN, TEACHER):
            return True

        if request.user.role == STUDENT:
            return request.method in SAFE_METHODS

        return False
