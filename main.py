import signup
import login
import user_view
import admin_view
import manager_view
import psycopg2


def main(cursor):
    while True:
        connection.commit()

        print('\nchoose an option:')
        print('1.login')
        print('2.signup')
        choice = input('your input: ')

        if choice == '1': #login
            role, user_id = None, None
            result = login.login(cursor)
            if result:
                role, user_id = result
            if role == 3:
                user_view.user_page(user_id, cursor)
            elif role == 2:
                admin_view.admin_page(user_id, cursor)
            elif role == 1:
                manager_view.manager_page(user_id, cursor)
        elif choice == '2': #sign up
            role, user_id = signup.signup(cursor)
            connection.commit()

            if role == 3:
                user_view.user_page(user_id, cursor)
            elif role == 2:
                admin_view.admin_page(user_id, cursor)
            elif role == 1:
                manager_view.manager_page(user_id, cursor)
        else:
            print ('your input is wrong.')
        
        

    


if __name__ == '__main__':
    # connection to the database
    connection = psycopg2.connect(host='host', dbname='dbname', 
                                user='user', password='password', 
                                port=0)
    cursor = connection.cursor()

    # database initialization
    cursor.execute('''
CREATE TABLE IF NOT EXISTS role (
    role_id SERIAL PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS agency (
    agency_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS vehicle (
    vehicle_id SERIAL PRIMARY KEY,
    type VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS "user" (
    user_id SERIAL PRIMARY KEY,
    role_id int,
    agency_id int,

    FOREIGN KEY (role_id) REFERENCES role (role_id),
    FOREIGN KEY (agency_id) REFERENCES agency (agency_id),


    username VARCHAR(50),
    password VARCHAR(255),
    email VARCHAR(100),
    phone_number VARCHAR(20),
    balance int
);

CREATE TABLE IF NOT EXISTS discount (
    discount_id SERIAL PRIMARY key,
    creator int,
    owner int,

    FOREIGN KEY (creator) REFERENCES "user" (user_id),
    FOREIGN KEY (owner) REFERENCES "user" (user_id),

    percentage int,
    deadline TIMESTAMP
);

CREATE TABLE IF NOT EXISTS support_ticket (
    support_ticket_id SERIAL PRIMARY KEY,
    sender_id int,
    FOREIGN KEY (sender_id) REFERENCES "user" (user_id)
);

CREATE TABLE IF NOT EXISTS message (
    message_id SERIAL PRIMARY KEY,
    message_text varchar(1000),
    message_date TIMESTAMP,
    status varchar(50),
    ticket_id int,
    sender_id int,
    FOREIGN KEY (ticket_id) REFERENCES support_ticket (support_ticket_id),
    FOREIGN KEY (sender_id) REFERENCES "user" (user_id)
    
);

CREATE TABLE IF NOT EXISTS travel (
    travel_id SERIAL PRIMARY KEY,
    agency_id int,
    vehicle_id int,

    FOREIGN KEY (agency_id) REFERENCES agency (agency_id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicle (vehicle_id),
    

    origin varchar(50),
    destination varchar(50),
    seats Int,
    domestic boolean,
    price int,
    date TIMESTAMP,
    duration int
);

CREATE TABLE IF NOT EXISTS travel_ticket (
    travel_ticket_id SERIAL PRIMARY KEY,
    travel_id int,
    user_id int,
    FOREIGN KEY (travel_id) REFERENCES travel (travel_id),
    FOREIGN KEY (user_id) REFERENCES "user" (user_id),
    rate int,
    status varchar(50)
);''')
    
    connection.commit()
    connection.autocommit = True
    main(cursor)

    connection.commit()
    cursor.close()
    connection.close()