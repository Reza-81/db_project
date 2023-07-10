import datetime


def add_support_ticket(user_id, cursor):
    #query to db to add ticket
    cursor.execute('''INSERT INTO support_ticket (sender_id) 
VALUES ( %s );''', (user_id,))

def add_message_to_ticket(user_id, cursor):
    ticket_id = int(input('\nenter the support ticket id: '))
    message = input('enter your message: ')
    # query to add new message to ticket
    # check if the ticket id and user id is related
    cursor.execute("SELECT sender_id FROM support_ticket WHERE sender_id = %s and support_ticket_id = %s;", (user_id, ticket_id))
    ticket_creator = cursor.fetchone()
    print(ticket_creator)
    if ticket_creator:
        cursor.execute('''INSERT INTO message (ticket_id, sender_id, message_text, message_date, status) VALUES (%s, %s, %s, %s, %s);''',
                   ( ticket_id, user_id, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), False))
    else:
        print('this ticket in not your ticket')


def show_ticket_messages(user_id, ticket_id, cursor):
    cursor.execute('''SELECT *
FROM message
WHERE ticket_id = %s AND sender_id = %s;''', (ticket_id, user_id))
    messages = cursor.fetchall()
    # query to db to get messages
    if not messages:
        print('there is no message')
        return
    for message in messages:
        print(message)

def see_your_support_tickets(user_id, cursor):
    # query to get user tickets
    cursor.execute("SELECT support_ticket_id FROM support_ticket WHERE sender_id = %s;", (user_id, ))
    tickets = cursor.fetchall()
    if tickets:
        print("yout supports tickets id")
        for ticket in tickets:
            print(ticket)
    else:
        print("No support tickets")
    while True:
        print('\nchoose an option: ')
        print('1.show ticket messages')
        print('2.back')
        choice = input('your input: ')

        if choice == '1':
            ticket_id = int(input('enter ticket id: '))
            cursor.execute("SELECT sender_id FROM support_ticket WHERE sender_id = %s and support_ticket_id = %s;", (user_id, ticket_id ))
            ticket_creator = cursor.fetchall()
            if ticket_creator:
                show_ticket_messages(user_id, ticket_id, cursor)
            else:
                print("you dont have permission")
        elif choice == '2':
            return
        else:
            print('your input is wrong.')

def see_travels(user_id, cursor):
    #get agency id from db
    agency_id = 1
    while True:
        # show sort optins
        print('\n1.sort by price')
        print('2.sort by rating')
        print('3.sort by origin')
        print('4.sort by destination')
        print('5.sort by date')
        print('6.sort by vehicle type')
        print('7.back')
        choice = input('enter your input: ')

        if choice == '1':
            cursor.execute('''SELECT t.travel_id, t.date, t.origin, t.destination, t.price, t.duration, v.type 
                              FROM travel t INNER JOIN vehicle v ON t.vehicle_id = v.vehicle_id WHERE t.agency_id = %s AND t.price <= %s''',
                              (agency_id, 100.00))
            travels = cursor.fetchall()
            for travel in travels:
                print(f'travel id: {travel[0]}')
                print(f'travel date: {travel[1]}')
                print(f'travel origin: {travel[2]}')
                print(f'travel destination: {travel[3]}')
                print(f'travel price: {travel[4]}')
                print(f'travel duration: {travel[5]}')
                print(f'travel type: {travel[6]}')
                print('-----------------------------')
                
        elif choice == '2':
            travels = cursor.execute('''SELECT t.travel_id, t.date, t.origin, t.destination, t.price, t.duration,
                                        v.type, AVG(tt.rate) AS rating FROM travel t INNER JOIN vehicle v 
                                        ON t.vehicle_id = v.vehicle_id INNER JOIN travel_ticket tt 
                                        ON t.travel_id = tt.travel_id WHERE t.agency_id = %s GROUP BY t.travel_id, t.date, t.origin, t.destination, t.price, t.duration, v.type  HAVING AVG(tt.rate) >= %s''',
                                        (agency_id, 1))
            travels = cursor.fetchall()
            
            for travel in travels:
                print(f'travel id: {travel[0]}')
                print(f'travel date: {travel[1]}')
                print(f'travel origin: {travel[2]}')
                print(f'travel destination: {travel[3]}')
                print(f'travel price: {travel[4]}')
                print(f'travel duration: {travel[5]}')
                print(f'travel type: {travel[6]}')
                print('-----------------------------')
        elif choice == '3':
            origin = input('enter the origin: ')
            travels = cursor.execute('''SELECT t.travel_id, t.date, t.origin, t.destination, t.price, t.duration, v.type 
                                        FROM travel t INNER JOIN vehicle v ON t.vehicle_id = v.vehicle_id WHERE t.agency_id = %s AND t.origin = %s''',
                                        (agency_id, origin))
            travels = cursor.fetchall()
            
            for travel in travels:
                print(f'travel id: {travel[0]}')
                print(f'travel date: {travel[1]}')
                print(f'travel origin: {travel[2]}')
                print(f'travel destination: {travel[3]}')
                print(f'travel price: {travel[4]}')
                print(f'travel duration: {travel[5]}')
                print(f'travel type: {travel[6]}')
                print('-----------------------------')
        elif choice == '4':
            destination = input('enter the destination: ')
            travels = cursor.execute('''SELECT t.travel_id, t.date, t.origin, t.destination, t.price, t.duration, v.type 
                                        FROM travel t INNER JOIN vehicle v ON t.vehicle_id = v.vehicle_id WHERE t.agency_id = %s AND t.destination = %s''',
                                        (agency_id, destination))
            travels = cursor.fetchall()
            
            for travel in travels:
                print(f'travel id: {travel[0]}')
                print(f'travel date: {travel[1]}')
                print(f'travel origin: {travel[2]}')
                print(f'travel destination: {travel[3]}')
                print(f'travel price: {travel[4]}')
                print(f'travel duration: {travel[5]}')
                print(f'travel type: {travel[6]}')
                print('-----------------------------')
        elif choice == '5':
            start_date = input('enter the start date: ')
            end_date = input('enter the end date: ')
            travels = cursor.execute('''SELECT t.travel_id, t.date, t.origin, t.destination, t.price, t.duration, v.type 
                                        FROM travel t INNER JOIN vehicle v ON t.vehicle_id = v.vehicle_id 
                                        WHERE t.agency_id = %s AND t.date >= %s AND t.date <= %s''',
                                        (agency_id, start_date, end_date))
            travels = cursor.fetchall()
            
            for travel in travels:
                print(f'travel id: {travel[0]}')
                print(f'travel date: {travel[1]}')
                print(f'travel origin: {travel[2]}')
                print(f'travel destination: {travel[3]}')
                print(f'travel price: {travel[4]}')
                print(f'travel duration: {travel[5]}')
                print(f'travel type: {travel[6]}')
                print('-----------------------------')
        elif choice == '6':
            vehicle = input('enter the vehicle type: ')
            travels = cursor.execute('''SELECT t.travel_id, t.date, t.origin, t.destination, t.price, t.duration, v.type 
                                        FROM travel t INNER JOIN vehicle v ON t.vehicle_id = v.vehicle_id WHERE t.agency_id = %s AND v.type = %s''',
                                        (agency_id, vehicle))
            travels = cursor.fetchall()
            
            for travel in travels:
                print(f'travel id: {travel[0]}')
                print(f'travel date: {travel[1]}')
                print(f'travel origin: {travel[2]}')
                print(f'travel destination: {travel[3]}')
                print(f'travel price: {travel[4]}')
                print(f'travel duration: {travel[5]}')
                print(f'travel type: {travel[6]}')
                print('-----------------------------')
        elif choice == '7':
            return
        # if choice is sort option, show travels again
        else:
            print('your input is wrong')


def see_five_best_costumer(user_id, cursor):
    agency_id = int(input('Enter agency_id please : '))

    cursor.execute('''SELECT u.username, u.email, u.phone_number, SUM(tl.price) AS total_paid_price, COUNT(DISTINCT tl.destination) AS num_destinations
    FROM "user" u
    INNER JOIN travel_ticket tt ON u.user_id = tt.user_id
    INNER JOIN travel tl ON tt.travel_id = tl.travel_id
    WHERE tl.agency_id = %s 
    GROUP BY u.user_id
    ORDER BY total_paid_price DESC
    LIMIT 5;''', (agency_id, ))

    results = cursor.fetchall()
    if results:
        for travel in results:
            print(f'costumer name: {travel[0]}')
            print(f'costumer email: {travel[1]}')
            print(f'costumer phone_number: {travel[2]}')
            print(f'costumer total_paid_price: {travel[3]}')
            print(f'costumer num_destination: {travel[4]}')
            print('-----------------------------')
    else:
        print("no destination")

def see_best_selling_travel(user_id, cursor):
    agency_id = int(input('Enter agency_id please : '))
    cursor.execute('''SELECT t.travel_id, t.origin, t.destination, COUNT(*) AS num_tickets_sold
        FROM travel t
        INNER JOIN travel_ticket tt ON t.travel_id = tt.travel_id
        WHERE t.agency_id = %s
        GROUP BY t.travel_id
        ORDER BY num_tickets_sold DESC
        LIMIT 10;''', (agency_id, )) 
    results = cursor.fetchall()
    if results:
        for travel in results:
            print(f'travel id: {travel[0]}')
            print(f'travel origin: {travel[1]}')
            print(f'travel destination: {travel[2]}')
            print(f'travel num_tickets_sold: {travel[3]}')
            print('-----------------------------')
    else:
        print("no destination")


def see_highest_income(user_id, cursor):
    agency_id = int(input('Enter agency_id please : '))
    cursor.execute('''SELECT DATE_PART('year', t.date) AS year, DATE_PART('month', t.date) AS month, SUM(t.price) AS income
    FROM travel t
    INNER JOIN travel_ticket tt ON t.travel_id = tt.travel_id
    WHERE t.agency_id = %s
    GROUP BY DATE_PART('year', t.date), DATE_PART('month', t.date)
    ORDER BY year DESC, month DESC;''', (agency_id,))
    results = cursor.fetchall()
    if results:
        for travel in results:
            print(f'travel year: {travel[0]}')
            print(f'travel month: {travel[1]}')
            print(f'travel income: {travel[2]}')
            print('-----------------------------')
    else:
        print("no destination")

def see_most_popular_destination(user_id, cursor):
    agency_id = int(input('Enter agency_id please : '))

    cursor.execute('''SELECT t.destination, COUNT(*) AS num_tickets_sold
    FROM travel t
    INNER JOIN travel_ticket tt ON t.travel_id = tt.travel_id
    WHERE t.agency_id = 1
    GROUP BY t.destination
    ORDER BY num_tickets_sold DESC
    LIMIT 10;''', (agency_id, ))
    results = cursor.fetchall()
    if results:
        for travel in results:
            print(f'travel destination: {travel[0]}')
            print(f'travel num_tickets_sold: {travel[1]}')
            print('-----------------------------')
    else:
        print("no destination")


def manager_page(user_id, cursor):
    while True:
        print('\nchoose an option')
        print('1.add ticket support ticket')
        print('2.add message to support ticket')
        print('3.see_your_support_tickets')
        print('4.see travels')
        print('5.5 best costumer')
        print('6.best selling travel')
        print('7.highest income through the year based on time')
        print('8.most polular destination')
        print('9.exit')
        choice = input('your input: ')
        if choice == '1':
            add_support_ticket(user_id, cursor)
        elif choice == '2':
            add_message_to_ticket(user_id, cursor)
        elif choice == '3':
            see_your_support_tickets(user_id, cursor)
        elif choice == '4':
            see_travels(user_id, cursor)
        elif choice == '5':
            see_five_best_costumer(user_id, cursor)
        elif choice == '6':
            see_best_selling_travel(user_id, cursor)
        elif choice == '7':
            see_highest_income(user_id, cursor)
        elif choice == '8':
            see_most_popular_destination(user_id, cursor)
        elif choice == '9':
            return
        else:
            print('your input is wrong')


if __name__ == '__main__':
    manager_page(0)