"""
    application entry point.
"""
import datetime
import getpass

from flask.cli import FlaskGroup

from inner_air import db, app, User
from inner_air.utils.decorators import def_params

cli = FlaskGroup(app)


"""
    admin settings
    
    defaults are:
        firstname = 'admin'
        email = 'admin@inner-air.com'
        password: 'admin'
        confirm_password: 'admin'
"""


@cli.command('create_admin')
@def_params
def create_admin(firstname='admin', email='admin@inner-air.com',
                 password='admin', confirm_password='admin'):
    """
        creates admin user
    """
    firstname = str(input('enter your name: ')) or firstname
    email = str(input('enter your email: ')) or email
    password = getpass.getpass('enter password: ') or password
    confirm_password = getpass.getpass("enter password again: ") or confirm_password

    if password != confirm_password:
        print('Field must be equal to password. ')
    else:
        try:
            db.session.add(User(
                firstname=firstname,
                email=email,
                password=password,
                is_anonymous=True,
                is_admin=True,
                is_confirmed=True,
                confirmed_on=datetime.datetime.now()
            )
            )
            db.session.commit()
            print(f'admin with email {email} was created successfully!')
        except Exception:
            print("couldn't create admin user.")


if __name__ == "__main__":
    cli()
