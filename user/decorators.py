from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def customer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='customer:login'):
    """
    Decorator for views that checks that the logged in user is customer,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_customer and not u.is_archived and u.is_verified and u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def manager_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='manager:login'):
    """
    Decorator for views that checks that the logged in user is a manager,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda
            u: u.is_active and u.is_manager and not u.is_archived and u.is_verified and u.is_approved and u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def salonist_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='salonist:login'):
    """
    Decorator for views that checks that the logged in user is salonist,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_salonist and not u.is_archived and u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def finance_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='finance:login'):
    """
    Decorator for views that checks that the logged in user is finance,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_finance and not u.is_archived,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def agent_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='shipment:login'):
    """
    Decorator for views that checks that the logged in user is Agent,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_agent and not u.is_archived,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def trainee_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='trainee:login'):
    """
    Decorator for views that checks that the logged in user is trainee,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_trainee and not u.is_archived,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def stock_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='stock:login'):
    """
    Decorator for views that checks that the logged in user is stock,
    redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_stock and not u.is_archived,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
