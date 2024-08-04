import datetime

month_codes = {
        'F': 'JAN', 'G': 'FEB', 'H': 'MAR', 'J': 'APR',
        'K': 'MAY', 'M': 'JUN', 'N': 'JUL', 'Q': 'AUG',
        'U': 'SEP', 'V': 'OCT', 'X': 'NOV', 'Z': 'DEC'
    }

def convert_tradingview_to_fyers(ticker,exchange):
    
    if len(ticker) > 5 and ticker[-5] in month_codes and ticker[-4:].isdigit():
        symbol_root = ticker[:-5]
        month_code = ticker[-5]
        year = ticker[-4:]
        month_name = month_codes[month_code]
        fyers_symbol = f"{symbol_root}{year[2:]}{month_name}FUT"
    else:
        symbol_root = ticker
        fyers_symbol = f"{symbol_root}-EQ"
    return exchange + ":" + fyers_symbol

def get_root_symbol(ticker):
    
    # Check if the ticker format suggests it's a future symbol
    if len(ticker) > 5 and ticker[-5] in month_codes and ticker[-4:].isdigit():
        symbol_root = ticker[:-5]
    else:
        symbol_root = ticker

    return symbol_root


# def main():
#     print(f"TradingView symbol: BANKNIFTYF2024 -> Fyers symbol: {convert_tradingview_to_fyers("BANKNIFTYF2024")}")
#     print(f"TradingView symbol: BANKNIFTYX2024 -> Fyers symbol: {convert_tradingview_to_fyers("BANKNIFTYX2024")}")
#     print(f"TradingView symbol: BANKNIFTYf2024 -> Fyers symbol: {convert_tradingview_to_fyers("BANKNIFTYf2024")}")
#     print(f"TradingView symbol: NIFTYF2024 -> Fyers symbol: {convert_tradingview_to_fyers("NIFTYF2024")}")
#     print(f"TradingView symbol: NIFTYF2020 -> Fyers symbol: {convert_tradingview_to_fyers("NIFTYF2020")}")
#     print(f"TradingView symbol: NIFTYF2099 -> Fyers symbol: {convert_tradingview_to_fyers("NIFTYF2099")}")
#     print(f"TradingView symbol: MIDCPNIFTYQ2024 -> Fyers symbol: {convert_tradingview_to_fyers("MIDCPNIFTYQ2024")}")

#     print(f"TradingView symbol: NIFTYF2024 -> Fyers symbol: {convert_tradingview_to_fyers("NIFTYF2024")}")
#     print(f"TradingView symbol: TCS -> Fyers symbol: {convert_tradingview_to_fyers("TCS")}")
#     print(f"TradingView symbol: REL123 -> Fyers symbol: {convert_tradingview_to_fyers("REL123")}")
#     print(f"TradingView symbol: COMPLEXZ2030 -> Fyers symbol: {convert_tradingview_to_fyers("COMPLEXZ2030")}")
#     print(f"TradingView symbol: niftyF2024 -> Fyers symbol: {convert_tradingview_to_fyers("niftyF2024")}")
#     print(f"TradingView symbol: ABCF2024 -> Fyers symbol: {convert_tradingview_to_fyers("ABCF2024")}")
#     print(f"TradingView symbol: XYZF -> Fyers symbol: {convert_tradingview_to_fyers("XYZF")}")
#     print(f"TradingView symbol: BULLG9999 -> Fyers symbol: {convert_tradingview_to_fyers("BULLG9999")}")

# if __name__ == '__main__':
#     main()
