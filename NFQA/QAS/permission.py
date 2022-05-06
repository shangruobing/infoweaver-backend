from rest_framework.permissions import BasePermission, SAFE_METHODS


class TeacherPermission(BasePermission):
    message = '学生没有权限访问'

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user.role == "0":
            """0 代表老师"""
            return True

        return False


class StudentOnlyReadPermission(BasePermission):
    message = '学生只能查看 没有权限更改信息'

    def has_permission(self, request, view):
        if request.user.role == "0":
            """0 代表老师"""
            return True
        if request.user.role == "1":
            # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
            return request.method in SAFE_METHODS

        return False
