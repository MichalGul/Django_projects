from rest_framework.permissions import BasePermission


class IsEnrolled(BasePermission):
    # check if user performin the reqeust is present int the students relationshi[ pf the Course object
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()
