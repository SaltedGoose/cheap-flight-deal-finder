from twilio.rest import Client
import smtplib

ACCOUNT_SID = ''#enter account sid here
AUTH_TOKEN = ''#enter auth token here

MY_EMAIL = ''#enter your email here
MY_PASSWORD = ''#enter your passowrd here



class NotificationManager:
    def __init__(self):
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    # def send_message(self, price_to_fly, destination, iata_code):
    #     message = self.client.messages \
    #         .create(
    #             body=f'Low price alert! Only £{price_to_fly} to fly from London-STN to {destination}-{iata_code}, from {TOMORROW_DATE} to {SIX_MONTHS_DATE}',
    #             from_ = '+14012178238',
    #             to = '+44 7376 296236'
    #         )
    #     print(message.status)

    def send_email(self, message, list_of_users):
        for user in list_of_users:
            user_email = user['email']
            with smtplib.SMTP('smtp.gmail.com') as connection:
                connection.starttls()

                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL, 
                    to_addrs=user_email, 
                    msg=message
                    )
            print(f'email sent to {user_email}')