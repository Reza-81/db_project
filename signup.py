import hashlib
import random
from datetime import datetime
import json
import os
import smtplib



def two_factore_authentication(email):
    # create random code
    code = str(random.randint(100, 999))
    # send code
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login("your@email.com", "password")
    # sending the mail
    s.sendmail("your@email.com", email, code)
    # terminating the session
    s.quit()
    # save code
    new_record = {'code': code, 'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    if os.path.exists('record.json'):
        with open('record.json','r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data[email] = new_record
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
    else:
        with open('record.json', 'w') as file:
            records = {email: new_record}
            file.write(json.dumps(records, indent=4))



def check_verification_code(code, email):
    with open('record.json', 'r+') as file:
        records = json.load(file)
        if (code == records[email]['code'] and (datetime.now() - 
            datetime.strptime(records[email]['time'], "%Y-%m-%d %H:%M:%S")).seconds < 180):
            del records[email]
            file.seek(0)
            json.dump(records, file, indent=4)
            file.truncate()
            return True
        del records[email]
        file.seek(0)
        json.dump(records, file, indent=4)
        file.truncate()
        return False



def signup(cursor):
    while True:
        user_name = input('\nenter your user name: ')
        duplicate_flag = False #check if this user name is already in db
        if duplicate_flag:
            print('this user name is already used.')
        else:
            break
    password = hashlib.sha256(input('enter your password: ').encode()).hexdigest()
    email = input('enter your email: ')
    phone_number = input('enter your phone number: ')
    role = input('enter your role (manager: 1, admin: 2, user: 3):')
    if role == '1':
        agency_id = input('enter the agency id: ')
    else:
        agency_id = 0
    while True:
        two_factore_authentication(email)
        user_verification_code = input('enter your verification code: ')
        if check_verification_code(user_verification_code, email):
            
            sql_query = '''INSERT INTO "user" (role_id, username, password, email, phone_number)
              VALUES (%s, %s, %s, %s, %s) RETURNING user_id;'''

            values = (int(role), user_name, password, email, phone_number)

            cursor.execute(sql_query, values)


            print ('your account hase been created.')
            
            user_id = cursor.fetchone()[0]
            print("yout id is : " , user_id)
            return role, user_id
        else:
            print('the code is wrong or the time is expired.')
            print('we send new code to your email.')
        


if __name__ == '__main__':
    signup()
