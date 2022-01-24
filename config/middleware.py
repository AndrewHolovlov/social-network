from datetime import timedelta, datetime

from rest_framework_simplejwt import authentication

from django.conf import settings

from accounts.models import User


class LastActivityMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = authentication.JWTAuthentication().authenticate(request)[0]  # Manually authenticate the token
        if request.user.is_authenticated:
            last_activity = request.session.get('last-activity', None)

            too_old_time = datetime.now() - timedelta(seconds=settings.LAST_ACTIVITY_INTERVAL)
            if not last_activity or datetime.strptime(last_activity, "%Y%m%d %H:%M:%S") < too_old_time:
                User.objects.filter(id=request.user.id).update(
                    last_activity=datetime.now())

            request.session['last-activity'] = datetime.now().strftime("%Y%m%d %H:%M:%S")

        response = self.get_response(request)
        return response
