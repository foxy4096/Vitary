from django.db import connection
from django.core.management import call_command

def check_database_health():
    try:
        with connection.cursor() as cursor:
            # Execute a simple query to check database connectivity
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            return result == (1,)
    except Exception as e:
        # Log the exception or handle it based on your application's needs
        return False



def check_migrations():
    try:
        call_command('migrate', check=True)
        return True
    except Exception as e:
        # Log the exception or handle it based on your application's needs
        return False
