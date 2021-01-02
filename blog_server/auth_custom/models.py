from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import requests

from datetime import timedelta
from django.utils import timezone


class MyUser(AbstractUser):
    baidu_access_token = models.CharField(max_length=255, null=True, blank=True)
    baidu_access_token_expire_at = models.DateTimeField(null=True, blank=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    @classmethod
    def get_access_token(cls):
        url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (
            settings.BAIDU_APP_KEY,
            settings.BAIDU_APP_SECRET,
        )
        resp = requests.get(url)

        rj = resp.json()
        access_token = rj['access_token']
        expires = rj['expires_in']

        return {'access_token': access_token, 'expires': expires}

    def refresh_access_token(self):
        now = timezone.now()
        ret = self.get_access_token()

        self.baidu_access_token = ret['access_token']
        self.baidu_access_token_expire_at = (now + timedelta(seconds=ret['expires']))
        self.save()

        return self.baidu_access_token
