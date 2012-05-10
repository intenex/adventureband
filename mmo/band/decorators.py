import urlparse
try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.decorators import available_attrs

# for redirect_to_login
from django.http import HttpResponseRedirect, QueryDict


# Not a decorator - taken from django.contrib.auth.views so I could take out the 'next' argument - which is an ugly unnecessary querystring added to the redirect URL
def redirect_to_login(login_url=None,
                      redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Redirects the user to the login page, *not* passing the given 'next' page
    """
    if not login_url:
        login_url = settings.LOGIN_URL

    login_url_parts = list(urlparse.urlparse(login_url))
    if redirect_field_name:
        querystring = QueryDict(login_url_parts[4], mutable=True)
        login_url_parts[4] = querystring.urlencode(safe='/')

    return HttpResponseRedirect(urlparse.urlunparse(login_url_parts))

def user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME, login_text=None):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            login_scheme, login_netloc = urlparse.urlparse(login_url or
                                                        settings.LOGIN_URL)[:2]
            request.session['login_text']=login_text
            return redirect_to_login(login_url, redirect_field_name)
        return _wrapped_view
    return decorator

def login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None, login_text=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        login_url=login_url,
        redirect_field_name=redirect_field_name,
        login_text=login_text
    )
    if function:
        return actual_decorator(function)
    return actual_decorator