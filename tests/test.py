from .factories import *
from .factories import UserFactory

def test_user_data_output():
    user = UserFactory.build()
    print(f"\n{'='*30}")
    print(f"DEBUG USER GENERATION:")
    print(f"Username:   {user.username:<20} | Length: {len(user.username)}")
    print(f"Email:      {user.email:<20} | Length: {len(user.email)}")
    print(f"First Name: {user.first_name:<20} | Length: {len(user.first_name)}")
    print(f"Last Name:  {user.last_name:<20} | Length: {len(user.last_name)}")
    print(f"{'='*30}")
