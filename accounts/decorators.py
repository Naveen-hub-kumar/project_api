from django.shortcuts import redirect


def admin_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.is_superuser:

            return view_func(

                request,

                *args,

                **kwargs

            )

        return redirect('/attendance/')

    return wrapper