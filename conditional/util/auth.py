from functools import wraps
from flask import request
from conditional.util.ldap import ldap_is_active, ldap_is_alumni, \
    ldap_is_eboard, ldap_is_eval_director, \
    ldap_is_financial_director, ldap_get_member


def webauth_request(func):
    @wraps(func)
    def wrapped_func(*args, **kwargs):
        user_name = request.headers.get('x-webauth-user')
        account = ldap_get_member(user_name)
        is_active = ldap_is_active(account)
        is_alumni = ldap_is_alumni(account)
        is_eboard = ldap_is_eboard(account)
        is_financial = ldap_is_financial_director(account)
        is_eval = ldap_is_eval_director(account)

        return func({"user_name": user_name,
                     "is_active": is_active,
                     "is_alumni": is_alumni,
                     "is_eboard": is_eboard,
                     "is_financial": is_financial,
                     "is_eval": is_eval}, *args, **kwargs)

    return wrapped_func
