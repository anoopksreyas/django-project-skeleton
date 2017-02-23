from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from optparse import make_option

class Command(BaseCommand):
    help = "Resets django admin password."
    
    def add_arguments(self, parser): #registering the named arguments
        parser.add_argument('--username',
                            help='Admin username.'
                            )
        parser.add_argument('--password',
                            help='Admin password.'
                            )
        
    def handle(self, *args, **kwargs):
        username = kwargs.get('username')
        new_password = kwargs.get('password')
        try:
            usr = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError("Admin user doesn\'t exists.")
        usr.set_password(new_password)
        usr.save()
        
        self.stdout.write('Successfully updated django admin password.', ending='')