from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_users(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def authorized_users(allowed_roles = []):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            user_groups = None
            access = False
            # Check if the user belongs to any group or not
            if request.user.groups.exists():
                user_groups = request.user.groups.all()
                print(user_groups)
                user_groups_name = []
                for user_group in user_groups:
                    user_groups_name.append(user_group.name)
                    if user_group.name in allowed_roles:
                        access = True
                    print(user_groups_name)
                    print(allowed_roles)
            if access == True:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("Sorry! You are not authorized to view this page!")
        return wrapper_func
    return decorator

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        user_groups = None
        # Check if the user belongs to any group or not
        if request.user.groups.exists():
            user_groups = request.user.groups.all()
            user_groups_name = []
            for user_group in user_groups:
                user_groups_name.append(user_group.name)
            if 'admin' in user_groups_name:
                return view_func(request, *args, **kwargs)
            elif "customer" in user_groups_name:
                return redirect('user')
        else:
            return HttpResponse("Sorry! You are not authorized to view this page!")
    return wrapper_func
