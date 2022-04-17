from django.core.mail import EmailMessage
from datetime import datetime
import pyotp
import base64
import random
import array
from django.conf import settings


class MailUtil:
    @staticmethod
    def send_mail(data):
        email=EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        
        email.content_subtype = "html"

        email.send()
        print("After Mail sent: ",data['to_email'])


# This class returns the string needed to generate the key
class generateKey:
    @staticmethod
    def returnValue(data):
        # print("data for key to be generated : ",data)
        return str(data) + str(datetime.date(datetime.now())) + settings.SECRET_KEY





class GenerateOTP:
    '''
    A Class for generating OTP
    sample data format to take as argument

    data {
        "data": "sample_data"
    }
    '''
    @staticmethod
    def generate_time_based_otp(data):
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(data['data']).encode())  # Key is generated
        OTP = pyotp.TOTP(key,interval = settings.OTP_EXPIRY_TIME)  # TOTP Model for OTP is created

        return {"OTP": OTP.now()}
        

    @staticmethod
    def verify_time_based_top(data):
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(data['email']).encode())  # Generating Key
        OTP = pyotp.TOTP(key,interval = settings.OTP_EXPIRY_TIME) 
        print("at Verify : ",data['otp'])
        if OTP.verify(data['otp']):  # Verifying the OTP
            return True
        return False


class RemoveAllSessionKeys:
    @staticmethod
    def remove_sessions(request):
        try:
            request.session.flush()
        except Exception as e:
            print(e)





class GenerateDefaultPassword:
    '''
    A Class for generating 8 digit password
    '''
    @staticmethod
    def generate_password():
        # declare arrays of the character that we need in out password
        # Represented as chars to enable easy string concatenation
        DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  
        LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 
                            'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                            'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                            'z']
        
        UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 
                            'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
                            'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                            'Z']
        
        SYMBOLS = ['@', '#', '$', '!']

        # combines all the character arrays above to form one array
        COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS

        # randomly select at least one character from each character set above
        rand_digit = random.choice(DIGITS)
        rand_upper = random.choice(UPCASE_CHARACTERS)
        rand_lower = random.choice(LOCASE_CHARACTERS)
        rand_symbol = random.choice(SYMBOLS)
        
        # combine the character randomly selected above
        # at this stage, the password contains only 4 characters but 
        # we want a 8-character password
        temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
        
        
        # now that we are sure we have at least one character from each
        # set of characters, we fill the rest of
        # the password length by selecting randomly from the combined 
        # list of character above.
        for x in range(settings.PASSWORD_DEFAULT_LEN - 4):
            temp_pass = temp_pass + random.choice(COMBINED_LIST)
        
            # convert temporary password into array and shuffle to 
            # prevent it from having a consistent pattern
            # where the beginning of the password is predictable
            temp_pass_list = array.array('u', temp_pass)
            random.shuffle(temp_pass_list)
        
        # traverse the temporary password array and append the chars
        # to form the password
        password = ""
        for x in temp_pass_list:
                password = password + x
                
        return password

