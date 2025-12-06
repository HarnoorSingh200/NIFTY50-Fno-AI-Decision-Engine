import time

def BuyOption(api, symbol, token, place=True):
    if place is True:
        api.place_order(buy_or_sell='B', product_type='M', exchange='NFO', tradingsymbol=symbol,
                        quantity=75, discloseqty=0, price_type='MKT', price=0, trigger_price=None,
                        retention='DAY', remarks='my_order_001')
    buying_premium = api.get_quotes(exchange="NFO", token=str(token))['lp']
    print(f"Bought {symbol} at {buying_premium}")
    time.sleep(1)

    return buying_premium


def ExitOption(api, symbol, token, place=True):
    if place is True:
        api.place_order(buy_or_sell='S', product_type='M', exchange='NFO', tradingsymbol=symbol,
                        quantity=75, discloseqty=0, price_type='MKT', price=0, trigger_price=None,
                        retention='DAY', remarks='my_order_001')
    selling_premium = api.get_quotes(exchange="NFO", token=str(token))['lp']
    print(f"Sold {symbol} at {selling_premium}")
    time.sleep(1)

    return selling_premium
