from .utils import privileged_members
from django.contrib.auth.models import Permission


def check_group_status(backend, user, response, *args, **kwargs):
    editor_perms = [
        Permission.objects.get(codename='add_review'),
        Permission.objects.get(codename='change_review')
    ]

    if kwargs['uid'] in privileged_members('japanization'):
        user.is_staff = True
        user.user_permissions.add(*editor_perms)
        user.save()
    else:
        user.is_staff = False
        user.user_permissions.remove(*editor_perms)
        user.save()
