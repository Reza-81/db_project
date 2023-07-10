import hashlib

def login(cursor):
    user_name = input('\nenter user name:')
    password = input('enter password:')

    cursor.execute('SELECT username, password FROM "user" WHERE username = %s;', (user_name, ))
    db_password = cursor.fetchone()
    if not db_password:
        print ('there is no such user name.')
    elif hashlib.sha256(password.encode()).hexdigest() == db_password[1]:
        cursor.execute('SELECT role_id, user_id FROM "user" WHERE username = %s;', (user_name, ))
        role, user_id = cursor.fetchone()
        print(role, user_id)
        return role, int(user_id)
    else:
        print('your password is wrong')
        print(hashlib.sha256(password.encode()).hexdigest())
        return None


