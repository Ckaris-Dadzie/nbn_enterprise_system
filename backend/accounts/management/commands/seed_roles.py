# accounts/management/commands/seed_roles.py
from django.core.management.base import BaseCommand
from accounts.models import Role


ROLES = [
    ('Admin',             'Full system access'),
    ('Manager',           'High-level operational control'),
    ('FrontDeskOfficer',  'Customer registration and order creation'),
    ('Cashier',           'Payment confirmation and receipt printing'),
    ('FinanceOfficer',    'Financial management and reporting'),
    ('InventoryManager',  'Raw material stock management'),
    ('ProductManager',    'Finished goods catalog management'),
    ('ProductionManager', 'Production monitoring and batch recording'),
]


class Command(BaseCommand):
    help = 'Seed the eight default system roles into the database.'


    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding roles...')
        created_count = 0


        for name, description in ROLES:
            role, created = Role.objects.get_or_create(
                name=name,
                defaults={'description': description},
            )
            if created:
                created_count += 1
                self.stdout.write(f'  Created : {name}')
            else:
                self.stdout.write(f'  Exists  : {name}')


        self.stdout.write(self.style.SUCCESS(
            f'Done. {created_count} new role(s) created.'
        ))


 
