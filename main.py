import json
import time
import datetime
from login import Login
from get_option_data import NiftyOptions
from get_latest_data import LatestData
from place_order import BuyOption, ExitOption
from openai import OpenAI
from keys import openaikey


def wait_for_next():
    now = datetime.datetime.now()
    next_run = (now + datetime.timedelta(minutes=1)).replace(second=2, microsecond=0)
    sleep_seconds = (next_run - now).total_seconds()
    print(f"Sleeping for {sleep_seconds:.2f} seconds until {next_run.time()}")
    time.sleep(sleep_seconds)


def main():
    api = Login()
    df = NiftyOptions()
    position_open = False

    position_token = None
    position_symbol = None
    output = None
    position_detail = None

    client = OpenAI(api_key=openaikey)
    assistant_id = ""
    thread = client.beta.threads.create()

    c = 0
    while True:
        if c == 0:
            MarketData, TradingSymbols = LatestData(api, df, candles_limit=30)
        else:
            MarketData, TradingSymbols = LatestData(api, df)

        c += 1
        print(f"Round {c}")

        call_symbol = TradingSymbols['call_symbol']
        put_symbol = TradingSymbols['put_symbol']
        call_token = TradingSymbols['call_token']
        put_token = TradingSymbols['put_token']

        if position_open is True:
            position_detail['current_premium'] = float(api.get_quotes(exchange="NFO", token=str(position_token))['lp'])
            position_detail['pl'] = (position_detail['current_premium'] - float(position_detail['buying_premium'])) * 75
            MarketData += f"\n Current Position: {position_symbol} | PL: {position_detail['pl']}"

            print(position_detail)

        # Send updated market data to the AI assistant
        message_content = json.dumps(MarketData)
        client.beta.threads.messages.create(thread_id=thread.id, role="user", content=message_content)
        run = client.beta.threads.runs.create_and_poll(thread_id=thread.id, assistant_id=assistant_id)

        if run.status == "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            last_msg = messages.data[0]
            response_text = last_msg.content[0].text.value

            print("Assistant final function call or response:", response_text)

            response_dict = json.loads(response_text)
            fn_name = response_dict.get("name")
            fn_name = fn_name.replace("()", "")

            if fn_name == "buy_call_option":
                if position_open:
                    if position_symbol[12:13] == "C":
                        buying_premium = BuyOption(api, call_symbol, call_token, place=False)
                        print("NOTICE: AI Buying Call Despite Having Call")
                    else:
                        print("NOTICE: AI Exiting Call and Buying Put")
                        ExitOption(api, position_symbol, position_token)
                        buying_premium = BuyOption(api, call_symbol, call_token)
                else:
                    buying_premium = BuyOption(api, call_symbol, call_token)

                position_token = call_token
                position_symbol = call_symbol
                position_open = True
                position_detail = {
                    'type': position_symbol,
                    'buying_premium': buying_premium,
                    'current_premium': buying_premium,
                    'pl': 0
                }
                output = "Call option bought successfully."

            elif fn_name == "buy_put_option":
                if position_open:
                    if position_symbol[12:13] == "P":
                        buying_premium = BuyOption(api, put_symbol, put_token, place=False)
                        print("NOTICE: AI Buying Put Despite Having Put")
                    else:
                        print("NOTICE: AI Exiting Put and Buying Call")
                        ExitOption(api, position_symbol, position_token)
                        buying_premium = BuyOption(api, put_symbol, put_token)
                else:
                    buying_premium = BuyOption(api, put_symbol, put_token)

                position_token = put_token
                position_symbol = put_symbol
                position_open = True
                position_detail = {
                    'type': position_symbol,
                    'buying_premium': buying_premium,
                    'current_premium': buying_premium,
                    'pl': 0
                }
                output = "Put option bought successfully."

            elif fn_name in ("exit_call_option", "exit_put_option"):
                if position_open is not False:
                    ExitOption(api, position_symbol, position_token)
                    position_open = False
                    position_token = None
                    position_detail = None
                    output = "Call option exited." if fn_name == "exit_call_option" else "Put option exited."

            elif fn_name == "wait_and_watch":
                output = "Waiting to get get better opportunity"

            elif fn_name in ("hold_call_option", "hold_put_option"):
                output = "holding the current position"

            else:
                output = f"Function not recognized - {fn_name}."

            print(output)

        wait_for_next()
        print()


if __name__ == "__main__":
    main()
