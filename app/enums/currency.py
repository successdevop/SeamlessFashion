from enum import Enum


class CurrencyEnum(str, Enum):
    NGN = "naira"
    USD = "dollars"
    GBP = "pounds"
    EUR = "euros"