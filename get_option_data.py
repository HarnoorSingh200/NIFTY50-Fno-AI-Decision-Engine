from datetime import datetime
import requests, zipfile
from io import BytesIO
import pandas as pd


def NiftyOptions():
    def NFO_filedata():
        url = "https://api.shoonya.com/NFO_symbols.txt.zip"
        response = requests.get(url)
        if response.status_code == 200:
            with zipfile.ZipFile(BytesIO(response.content)) as z:
                file_name = z.namelist()[0]
                with z.open(file_name) as file:
                    df = pd.read_csv(file)
                    return df
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")

    def weekly_option(df, index):
        current_date = datetime.now()
        df['Expiry'] = pd.to_datetime(df['Expiry'], format='%d-%b-%Y')
        df = df[df['Symbol'] == index]
        exp = list(df['Expiry'].unique())
        cur_exp = min(exp)

        df = df[df['Expiry'] == cur_exp]
        df = df.reset_index(drop=True)
        return df

    print("gotten Option data")
    return weekly_option(NFO_filedata(), 'NIFTY')
