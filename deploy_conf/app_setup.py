from os import environ, getenv
from django import setup
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from redlock import RedLock


setup()  # init Django before we use models


def is_leader():
    print('Acquire Leader role...')
    # Expire the aquired lock after 5 minutes
    expiry_mins = int(getenv('LEADER_EXPIRY_MINS', '5'))
    expiry_millis = expiry_mins * 60 * 1000
    lock_name = 'leader-lock-{}'.format(environ['DB_NAME'])
    lock = RedLock(
        lock_name,
        retry_times=1,
        ttl=expiry_millis,
        connection_details=[{'url': environ['REDIS_URL']}]
    )
    return lock.acquire()


def setup_initial_admin_user():
    # Auto create initial admin user.
    ADMIN_USERNAME = getenv('ADMIN_USERNAME', '')
    ADMIN_PASSWORD = getenv('ADMIN_PASSWORD', '')
    if ADMIN_USERNAME and ADMIN_PASSWORD:
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=ADMIN_USERNAME,
            is_staff=True, is_superuser=True,
            defaults={'password': make_password(ADMIN_PASSWORD)}
        )
        if created:
            print('Admin user created:', ADMIN_USERNAME)
        else:
            print('Admin user exists:', ADMIN_USERNAME)


def migrate_database():
    print('Run database migrations...')
    call_command('migrate', interactive=False)


if __name__ == '__main__':
    # Run some setup tasks (only on leader/primary server)
    if is_leader():
        print('Leader role acquired...')
        migrate_database()
        setup_initial_admin_user()
    else:
        print('Not the leader. Skip.')
