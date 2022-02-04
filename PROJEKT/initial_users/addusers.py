"""ITT LÁTNI, HOGY HOGYAN KELL PROGRAMOZOTTAN USEREKET HOZZÁADNI A RENDSZERHEZ"""

from django.contrib.auth.models import User

# Create user and save to the database
user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')

# Update fields and then save again
user.first_name = 'John'
user.last_name = 'Citizen'
user.save()

with open('PROJEKT/initial_users/users.csv')as f:
    pass

