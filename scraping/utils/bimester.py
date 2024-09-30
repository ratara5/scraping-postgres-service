import calendar
from utils.month import Month


def get_next_bimester(current_month):
    """Calculate the next bimester and return the Spanish names of the two months."""
    next_month_number = (current_month % 12) + 1  # Next month
    following_month_number = (next_month_number % 12) + 1  # Month after next month

    # Get the names in English using the calendar module
    next_month_name_english = calendar.month_name[next_month_number]
    following_month_name_english = calendar.month_name[following_month_number]

    # Map English names to Spanish using the Meses Enum
    next_month_spanish = Month.get_spanish_name(next_month_name_english)
    following_month_spanish = Month.get_spanish_name(following_month_name_english)

    return [next_month_spanish, following_month_spanish]