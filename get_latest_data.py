import datetime

def LatestData(api, options_df, candles_limit=3):
    nifty_data = api.get_quotes(exchange="NSE", token="26000")

    timestamp = nifty_data['request_time']
    nifty_price = nifty_data['lp']
    strike_price = round(float(nifty_price) / 50) * 50

    tokens = options_df[options_df['StrikePrice'] == strike_price]['Token'].to_list()
    TradingSymbol = options_df[options_df['StrikePrice'] == strike_price]['TradingSymbol'].to_list()
    put_token, put_symbol = tokens[0], TradingSymbol[0]
    call_token, call_symbol = tokens[1], TradingSymbol[1]

    call_premium = api.get_quotes(exchange="NFO", token=str(call_token))['lp']
    put_premium = api.get_quotes(exchange="NFO", token=str(put_token))['lp']

    lastBusDay = datetime.datetime.today()
    lastBusDay = lastBusDay.replace(hour=0, minute=0, second=0, microsecond=0)
    candles_data = api.get_time_price_series(exchange='NSE', token='26000', starttime=lastBusDay.timestamp(), interval=1)

    MarketData = f"""time: {timestamp}
    nifty: {float(nifty_price)}
    ATM strike: {strike_price}
    Call Premium: {call_premium}
    Put Premium: {put_premium}
    Last {candles_limit} candles:
    """

    for candle in candles_data[:candles_limit]:
        MarketData += f"[{candle['into']}, {candle['inth']}, {candle['intl']}, {candle['intc']}] \n"

    OptionSymbol = {
        'call_symbol': call_symbol,
        'put_symbol': put_symbol,
        'put_token': put_token,
        'call_token': call_token
    }

    return MarketData, OptionSymbol
