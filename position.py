import time
import ccxt
from secrets_keys import api_key, secret

phemex = ccxt.phemex({
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
})


# Saldo für Swap-Konto abrufen
def fetch_swap_balance():
    balance = phemex.fetch_balance({'type': 'swap'})
    usdt_balance = balance['total'].get('USDT', 0)
    return usdt_balance


def fetch_current_price(symbol):
    ticker = phemex.fetch_ticker(symbol)
    return ticker['last']


def calculate_sl_tp_prices(symbol, sl_percentage, tp_percentage, position_side):
    current_price = fetch_current_price(symbol)

    if position_side.lower() == 'long':
        stop_loss_price = current_price * (1 - sl_percentage / 100)
        take_profit_price = current_price * (1 + tp_percentage / 100)
    elif position_side.lower() == 'short':
        stop_loss_price = current_price * (1 + sl_percentage / 100)
        take_profit_price = current_price * (1 - tp_percentage / 100)
    else:
        raise ValueError("Invalid position side. Use 'long' or 'short'.")

    print(f"Stop Loss Price: {stop_loss_price}, Take Profit Price: {take_profit_price}")
    return stop_loss_price, take_profit_price


def open_position_with_sl_tp(symbol, position_side, amount):
    # Position eröffnen
    if position_side.lower() == 'long':
        order = phemex.create_order(symbol, 'market', 'buy', amount, params={'posSide': 'Long'})
        sl_side = 'sell'
        tp_side = 'sell'
    elif position_side.lower() == 'short':
        order = phemex.create_order(symbol, 'market', 'sell', amount, params={'posSide': 'Short'})
        sl_side = 'buy'
        tp_side = 'buy'
    else:
        raise ValueError("Invalid position side. Use 'long' or 'short'.")

    print(f"{position_side.capitalize()} Market Order:", order)



    return order


def calculate_sl_tp_prices(symbol, sl_percentage, tp_percentage, position_side):
    """
    Berechnet die Stop-Loss- und Take-Profit-Preise basierend auf dem aktuellen Preis und den Prozentwerten.

    :param symbol: Das Handelspaar, z.B. "BTCUSDT".
    :param sl_percentage: Der Prozentsatz für den Stop-Loss.
    :param tp_percentage: Der Prozentsatz für den Take-Profit.
    :param position_side: Die Richtung der Position ("long" oder "short").
    :return: Ein Tuple mit den Stop-Loss- und Take-Profit-Preisen.
    """
    current_price = fetch_current_price(symbol)
    print(f"Aktueller Preis für {symbol}: {current_price}")

    if position_side.lower() == 'long':
        stop_loss_price = current_price * (1 - sl_percentage / 100)
        take_profit_price = current_price * (1 + tp_percentage / 100)
    elif position_side.lower() == 'short':
        stop_loss_price = current_price * (1 + sl_percentage / 100)
        take_profit_price = current_price * (1 - tp_percentage / 100)
    else:
        raise ValueError("Invalid position side. Use 'long' or 'short'.")

    return stop_loss_price, take_profit_price



def calculate_order_size(trade_percentage, leverage, symbol):
    usdt_balance = fetch_swap_balance()
    trade_capital = usdt_balance * (trade_percentage / 100)
    print("Trade Capital:", trade_capital)
    current_price = fetch_current_price(symbol)
    order_size = (trade_capital * leverage) / current_price
    return order_size





# Beispielverwendung
symbol = "BTCUSDT"
sl_percentage = 0.3
tp_percentage = 0.3
position_side = "long"  # oder "short"
trade_percentage = 20
leverage = 15

stop_loss_price, take_profit_price = calculate_sl_tp_prices(symbol, sl_percentage, tp_percentage, position_side)
print(f"Stop Loss Price: {stop_loss_price}, Take Profit Price: {take_profit_price}")
amount = calculate_order_size(trade_percentage, leverage, symbol)
print(amount)



open_position_with_sl_tp(symbol, position_side, amount)