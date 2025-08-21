from config import ADMINS

#def is_admin(user_id):

#    return user_id in ADMINS


def is_admin(user_id: int) -> bool:
    from config import ADMINS
    # Convert comma-separated string to list of integers
    return user_id in [int(admin_id.strip()) for admin_id in ADMINS.split(',')]
