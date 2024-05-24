# Set up Phemex API with API key and secret, enable rate limit to avoid API restrictions
import pprint

import ccxt
from secrets_keys import api_key, secret



phemex = ccxt.phemex({
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
})

def fetch_swap_balance():
    balance = phemex.fetch_balance({'type': 'swap'})
    usdt_balance = balance['total'].get('USDT', 0)
    print(f"USDT Balance: {usdt_balance}")
    return usdt_balance

def fetch_current_price(symbol):
    ticker = phemex.fetch_ticker(symbol)
    current_price = ticker['last']
    print(f"Current price for {symbol}: {current_price}")
    return current_price

def calculate_order_size(trade_percentage, leverage, symbol):
    usdt_balance = fetch_swap_balance()
    trade_capital = usdt_balance * (trade_percentage / 100)
    current_price = fetch_current_price(symbol)
    order_size = (trade_capital * leverage) / current_price
    print(f"Order Size (BTC): {order_size}")
    return order_size

def open_position_with_sl_tp(symbol, position_side, amount, stop_loss_price, take_profit_price):
    order_params = {
        'posSide': position_side.capitalize(),
        'stopLossPrice': stop_loss_price,
        'takeProfitPrice': take_profit_price,
        'reduceOnly': False
    }
    if position_side.lower() == 'long':
        order = phemex.create_order(symbol, 'market', 'buy', amount, None, order_params)
    elif position_side.lower() == 'short':
        order = phemex.create_order(symbol, 'market', 'sell', amount, None, order_params)
    print(f"{position_side.capitalize()} Market Order with SL and TP: {order}")
    return order


# Definition der Funktionen, wie bereits besprochen

def get_positions():
    symbols = ["BTCUSDT"]
    positions = phemex.fetch_positions(symbols=symbols)
    return positions

def print_positions():
    positions = get_positions()
    if positions:  # Überprüfe, ob die Liste der Positionen nicht leer ist
        print("Aktuelle Positionen:")
        for position in positions:
            if float(position['info']['size']) > 0:  # Filtere Positionen mit einer Größe größer als 0
                print(f"Symbol: {position['info']['symbol']}")
                print(f"Größe: {position['info']['size']}")
                print(f"Durchschnittlicher Einstiegspreis: {position['info']['avgEntryPrice']}")
                print(f"Seite: {'Long' if position['info']['side'] == 'buy' else 'Short'}")
                print("---------------")
    else:
        print("Keine aktuellen Positionen.")

import time

def is_position_open():
    positions = get_positions()  # Nutze die zuvor definierte get_positions-Funktion
    for position in positions:
        if float(position['info']['size']) > 0:  # Prüfe, ob die Position offen ist
            return True
    return False


def get_last_closed_position(symbol):
    # Abrufe die Handelshistorie für das spezifizierte Symbol
    trades = phemex.fetch_my_trades(symbol)
    # Überprüfe, ob Trades vorhanden sind und gib den letzten zurück
    if trades:
        last_trade = trades[-3]
        pprint.pprint(last_trade)
    else:
        print("Keine geschlossenen Positionen gefunden.")








