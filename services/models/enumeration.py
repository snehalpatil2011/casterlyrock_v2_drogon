from enum import Enum

class FundBalanceType(Enum):
    TOTAL_BALANCE = "Total Balance"
    UTILIZED_AMOUNT = "Utilized Amount"
    CLEAR_BALANCE = "Clear Balance"
    REALIZED_PROFIT_AND_LOSS = "Realized Profit and Loss"
    COLLATERALS = "Collaterals"
    FUND_TRANSFER = "Fund Transfer"
    RECEIVABLES = "Receivables"
    ADHOC_LIMIT = "Adhoc Limit"
    LIMIT_AT_START_OF_THE_DAY = "Limit at start of the day"
    AVAILABLE_BALANCE = "Available Balance"
