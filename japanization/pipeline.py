from django.contrib.auth.models import Permission

from .utils import privileged_members


def check_group_status(backend, user, response, *args, **kwargs):
    moderator_perms = [
        Permission.objects.get(codename='add_review'),
        Permission.objects.get(codename='change_review')
    ]

    owner_perms = moderator_perms + [
        Permission.objects.get(codename='delete_review')
    ]

    uid = kwargs['uid']
    members = privileged_members('japanization')

    if uid in members:
        user.is_staff = True
        if members[uid] == 'Group Owner':
            user.user_permissions.add(*owner_perms)
        else:
            user.user_permissions.add(*moderator_perms)
    else:
        user.is_staff = False
        user.user_permissions.remove(*owner_perms)

    user.save()
