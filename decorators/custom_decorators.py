from django.shortcuts import redirect


def active_session_required(f):
    def wrapper(request, *args, **kwargs):
        if 'access_token' in request.session and 'user_id' in request.session:
            return f(request, *args, **kwargs)
        else:
            return redirect('interface:login')
    return wrapper
