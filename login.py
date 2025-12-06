from NorenRestApiPy.NorenApi import NorenApi
from pyotp import TOTP
import logging

# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

def Login():
    user = ''
    pwd = ''
    factor2 = ''
    vc = ''
    app_key = ''
    imei = ""

    class ShoonyaApiPy(NorenApi):
        def __init__(self):
            super().__init__(
                host='https://api.shoonya.com/NorenWClientTP/',
                websocket='wss://api.shoonya.com/NorenWSTP/'
            )

    api = ShoonyaApiPy()
    otp = TOTP(factor2).now().zfill(6)
    login_response = api.login(
        userid=user,
        password=pwd,
        twoFA=otp,
        vendor_code=vc,
        api_secret=app_key,
        imei=imei
    )
    print(login_response)

    return api
