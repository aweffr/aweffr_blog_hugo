from django.db import models


class EventHealth(models.Model):
    STRENGTH = '力量'
    AEROBICS = '健身操'
    ELLIPTICAL = '椭圆机'
    WALK = '散步'

    HEALTH_TYPE_CHOICE = (
        (STRENGTH, STRENGTH),
        (AEROBICS, AEROBICS),
        (ELLIPTICAL, ELLIPTICAL),
        (WALK, WALK),
    )

    type = models.CharField(max_length=100, choices=HEALTH_TYPE_CHOICE)
    heart_rate = models.IntegerField(verbose_name='心率', null=True, blank=True)
    calories = models.IntegerField(verbose_name='卡路里', null=True, blank=True)


class Event(models.Model):
    WORK = '工作'
    STUDY = '学习'
    ENTERTAINMENT = '娱乐'
    HEALTH = '健康'

    CHOICES_TYPE = (
        (WORK, WORK),
        (STUDY, STUDY),
        (ENTERTAINMENT, ENTERTAINMENT),
        (HEALTH, HEALTH),
    )

    type = models.CharField(choices=CHOICES_TYPE, max_length=100)

    create_at = models.DateTimeField(auto_now_add=True)
    start_at = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)  # 持续时间, 秒

    modified_at = models.DateTimeField(auto_now=True)

    health = models.OneToOneField(EventHealth, on_delete=models.CASCADE, related_name='event', null=True, blank=True)
