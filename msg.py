from twilio.rest import Client

account_sid = 'AC34e7f73a2037c38b8380fcaab0e681cc' 
auth_token = 'b20014398d2891444b0ef8fc10317aac'

client = Client(account_sid, auth_token)

def unlock_one(self):
    users = ['+17079996055', '+16154976489', '+13343249087']
    for number in users:
        client.messages.create(
        body='RFID Scan Successful!',
        from_='+19193360045',
        to=number
        )
        

def unlock_two(self, user):
    users = ['+17079996055', '+16154976489', '+13343249087']
    if user == 'Justin':
        client.messages.create(
        body='Welcome, Justin!',
        from_='+19193360045',
        to=users[0]
        )
    elif user == 'Tanner':
        client.messages.create(
        body='Welcome, Tanner!',
        from_='+19193360045',
        to=users[1]
        )
    elif user == 'Danilo':
        client.messages.create(
        body='Welcome, Danilo!',
        from_='+19193360045',
        to=users[2]
        )

def lock(self):
    users = ['+17079996055', '+16154976489', '+13343249087']
    for number in users:
        client.messages.create(
        body='All Compartments Locked!',
        from_='+19193360045',
        to=number
        )
        
        
    