# decorators.py
from django.http import HttpResponseForbidden
from .models import Admin

def admin_instance_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        admin_id = kwargs.get('admin_id')
        if admin_id:
            try:
                admin = Admin.objects.get(id=admin_id)
                if admin.username == request.user.email:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden("You don't have permission to view this Admin instance.")
            except Admin.DoesNotExist:
                return HttpResponseForbidden("Admin instance not found.")
        else:
            return HttpResponseForbidden("Invalid request. Admin ID is missing.")
    return _wrapped_view
