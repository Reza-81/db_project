from datetime import datetime


def buy_ticket(user_id, cursor):
    print('\n1.sort by price')
    print('2.sort by rating')
    print('3.sort by origin')
    print('4.sort by destination')
    print('5.sort by date')
    print('6.sort by vehicle type')
    print('7.sort by agency')
    choice = input('enter your input: ')
    agency_id = input('enter agency id: ')

    if choice == '1':
        price = int(input("please enter a price"))
        cursor.execute('''SELECT t.travel_id, t.date, t.origin, t.destination, t.price, t.duration, v.type 
                            FROM travel t INNER JOIN vehicle v ON t.vehicle_id = v.vehicle_id WHERE  t.price <= %s''',
                            (price,))
        travels = cursor.fetchall() 
        print(travels)
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
        for travel in travels:
            print(f'travel id: {travel[0]}')
            print(f'travel date: {travel[1]}')
            print(f'travel origin: {travel[2]}')
            print(f'travel destination: {travel[3]}')
            print(f'travel price: {travel[4]}')
            print(f'travel duration: {travel[5]}')
            print(f'travel type: {travel[6]}')
            print('-----------------------------')
    else:
        travels = cursor.execute('''SELECT tt.*, t.origin, t.destination 
                                    FROM travel_ticket tt 
                                    JOIN travel t ON tt.travel_id = t.travel_id
                                    JOIN agency a ON t.agency_id = a.agency_id 
                                    JOIN vehicle v ON t.vehicle_id = v.vehicle_id
                                    WHERE tt.user_id = %s
                                    AND a.name = %s;''', (user_id, agency_id))
        for travel in travels:
            print(f'travel id: {travel[0]}')
            print(f'travel date: {travel[1]}')
            print(f'travel origin: {travel[2]}')
            print(f'travel destination: {travel[3]}')
            print(f'travel price: {travel[4]}')
            print(f'travel duration: {travel[5]}')
            print(f'travel type: {travel[6]}')
            print('-----------------------------')
    while True:
        print('\n1.buy a ticket:')
        print('2.back')
        choice = input('your input:')

        if choice == '1':
            travel_id = int(input('enter the travel id: '))
            
            cursor.execute('''SELECT percentage
                        FROM discount
                        WHERE deadline > CURRENT_DATE and owner = %s
                        ORDER BY percentage DESC
                        LIMIT 1;''', (user_id, ))
            discount_percentage = cursor.fetchone()
            cursor.execute('select price from travel where travel_id = %s;', (travel_id,))
            price = cursor.fetchone()[0]
            cursor.execute('''SELECT travel_id
                    FROM travel
                    WHERE seats >= 1 and  travel_id = %s''', (travel_id,))
            enoughSeat = cursor.fetchone()
            cursor.execute("""SELECT EXISTS 
                               (SELECT 1 From "user" u , travel t WHERE u.balance >= t.price and t.travel_id = %s and u.user_id = %s)
                                 as balance_check;""", (travel_id, user_id ))
            enoughBalance = cursor.fetchone()
            if (enoughSeat  and enoughBalance ):
                cursor.execute("INSERT INTO travel_ticket (travel_id, user_id, status) VALUES (%s, %s, 'reserved');", (travel_id, user_id))
                cursor.execute("UPDATE travel_ticket SET status = 'paid' WHERE travel_id = %s AND user_id = %s;", (travel_id, user_id))
                cursor.execute('''UPDATE travel SET seats = seats - %s WHERE travel_id = %s''', (1, travel_id))
            else:
                print("you can not buy travel ticket")
        elif choice == '2':
            return
        else:
            print('your input is wrong')


def charge_account(user_id, cursor):
    amount = input('enter the amount: ')
    cursor.execute('UPDATE "user" SET balance = balance + %s WHERE user_id = %s;', (int(amount), user_id))


def add_support_ticket(user_id, cursor):
    #query to db to add ticket
    cursor.execute('''INSERT INTO support_ticket (sender_id) 
VALUES ( %s );''', (user_id,))
    

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


def add_message_to_ticket(user_id, cursor):
    ticket_id = int(input('\nenter the support ticket id: '))
    message = input('enter your message: ')
    # query to add new message to ticket
    cursor.execute("SELECT sender_id FROM support_ticket WHERE sender_id = %s and support_ticket_id = %s;", (user_id, ticket_id))
    ticket_creator = cursor.fetchone()
    print(ticket_creator)
    if ticket_creator:
        cursor.execute('''INSERT INTO message (ticket_id, sender_id, message_text, message_date, status) VALUES (%s, %s, %s, %s, %s);''',
                   ( ticket_id, user_id, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), False))
    else:
        print('this ticket in not your ticket')


def see_your_travels(user_id, cursor):
    travels = []
    query = """
        SELECT travel.*, travel_ticket.rate, travel_ticket.status
        FROM travel
        JOIN travel_ticket ON travel.travel_id = travel_ticket.travel_id
        WHERE travel_ticket.user_id = %s
    """
    cursor.execute(query, (user_id,))
    travels = cursor.fetchall()
    if travels:
        for travel in travels:
            print(f'travel id: {travel[0]}')
            print(f'travel date: {travel[1]}')
            print(f'travel origin: {travel[2]}')
            print(f'travel destination: {travel[3]}')
            print(f'travel price: {travel[4]}')
            print(f'travel duration: {travel[5]}')
            print(f'travel type: {travel[6]}')
            print('-----------------------------')


def rate_for_travel(user_id, cursor):
    travel_id = input('\nenter your travel id: ')
    rate = int(input('enter your rate: '))
    # query for adding rate to travel
    cursor.execute('''UPDATE travel_ticket SET rate = %s, status = %s WHERE user_id = %s AND travel_ticket_id = %s''', 
                   (rate, 'confirmed', user_id, travel_id))


def delete_account(user_id, cursor):
    cursor.execute('''DELETE FROM "user" WHERE user_id = %s''', user_id)
    print('your account hase been deleted.')


def user_page(user_id, cursor):
    while True:
        print('\nchoose an option')
        print('1.buy ticket')
        print('2.charge account')
        print('3.new support ticket')
        print('4.add message to ticket')
        print('5.see your tickets')
        print('6.see your travels')
        print('7.rate for travel')
        print('8.delete account')
        print('9.exit')
        choice = input('your input: ')

        if choice == '1':
            buy_ticket(user_id, cursor)
        elif choice == '2':
            charge_account(user_id, cursor)
        elif choice == '3':
            add_support_ticket(user_id, cursor)
        elif choice == '4':
            add_message_to_ticket(user_id, cursor)
        elif choice == '5':
            see_your_support_tickets(user_id, cursor)
        elif choice == '6':
            see_your_travels(user_id, cursor)
        elif choice == '7':
            rate_for_travel(user_id, cursor)
        elif choice == '8':
            delete_account(user_id, cursor)
            return
        elif choice == '9':
            return
        else:
            print('your input is wrong')



if __name__ == '__main__':
    user_page(0)
