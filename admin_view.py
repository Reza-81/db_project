def add_travel(cursor):
    date = input('\nEnter the date (YYYY-MM-DD HH:MM:SS): ')
    origin = input('Enter origin: ')
    destination = input('Enter destination: ')
    vehicle_id = input('Enter vehicle id: ')
    seats = input('Enter number of seats: ')
    domestic = input('Is the travel domestic (1, 0): ')
    price = input('Enter the price of travel: ')
    duration = input('Enter the duration of the travel: ')
    agency_id = input('Enter agency id: ')

    # Query to insert the new travel
    params = (date, origin, destination, vehicle_id, seats, domestic, price, duration, agency_id)
    cursor.execute('''INSERT INTO travel 
                   (date, origin, destination, vehicle_id, seats, domestic, price, duration, agency_id) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', params)

    # Commit the changes to the database
    cursor.connection.commit()


    

def show_ticket_messages(cursor):
    ticket_id = int(input('enter ticket id: '))
    cursor.execute('''SELECT *
                            FROM message
                            WHERE ticket_id = %s  ;''', (ticket_id, )) 
    messages = cursor.fetchall()
    if messages:
        for message in messages:
            print("message is", message)
    else:
        print('there is no such ticket.')


def answer_to_ticket( cursor):
    ticket_id = int(input('enter ticket id: '))
    cursor.execute(''' 
                            SELECT 1
                            FROM support_ticket
                            WHERE support_ticket_id = %s
                            ;''', (ticket_id, ))
    flag_ticket_exist = cursor.fetchall()
    if flag_ticket_exist:
        message = input('enter your message: ')
        cursor.execute('''INSERT INTO message (ticket_id, message_text)
        VALUES (%s, %s);''', (ticket_id, message))
    else:
        print('there is no such ticket.')


def see_support_tickets(user_id, cursor):
    #query to the db to get the all tickets
    cursor.execute('''SELECT *
                            FROM support_ticket
                            ''')
    tickets = cursor.fetchall()
    print(tickets)
    if tickets:
        for ticket in tickets:
            print("ticket id is : " , ticket[0])
        while True:
            print('\nchoose an option: ')
            print('1.show ticket messages')
            print('2.answer to ticket')
            print('3.back')
            choice = input('your input: ')

            if choice == '1':
                show_ticket_messages(cursor)
            elif choice == '2':
                answer_to_ticket(cursor)
            elif choice == '3':
                return
            else:
                print('your input is wrong.')
    else:
        print("no ticket found")


def admin_page(user_id, cursor):
    while True:
        print('\nchoose an option')
        print('1.add travel')
        print('2.see tickets')
        print('3.exit')
        choice = input('your input: ')

        if choice == '1':
            add_travel(cursor)
        elif choice == '2':
            see_support_tickets(user_id, cursor)
        elif choice == '3':
            return
        else:
            print('your input is wrong')


if __name__ == '__main__':
    admin_page(0)