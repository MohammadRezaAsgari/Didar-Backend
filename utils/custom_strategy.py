from django.conf import settings
from django.shortcuts import redirect

def redirect_user(strategy, details, user=None, *args, **kwargs):
    next_url = strategy.session_get('next')
    if next_url:
        strategy.session_pop('next')
        # Redirect to the 'next' URL
        return redirect(next_url)
    # Default fallback redirect
    return redirect(settings.FRONTEND_URL)
