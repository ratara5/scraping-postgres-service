from datetime import datetime, timedelta
import calendar

from utils.month import Month

MEET_DAY = "tuesday" # tuesday | wednesday | thursday

def belong_to_month(day, month, year):
    try:
        # Get number of month from month name
        month_number = list(calendar.month_name).index(month.capitalize())
        
         # Get month range days
        _, max_days = calendar.monthrange(int(year), month_number)
        
        # Confirm if the date is valid for this month and year
        return 1 <= int(day) <= max_days
    except ValueError:
        return False

def get_date(interval_string, year):
    # Translation month names dictionary
    """
    months_translation = {
        "enero": "January",
        "febrero": "February",
        "marzo": "March",
        "abril": "April",
        "mayo": "May",
        "junio": "June",
        "julio": "July",
        "agosto": "August",
        "septiembre": "September",
        "octubre": "October",
        "noviembre": "November",
        "diciembre": "December"
    }
    """

    # Step 1
    if " a " in interval_string:
        rexp_index = interval_string.find(" a ")
        mes1 = interval_string.split()[2]
        mes2 = interval_string[rexp_index + len(" a ") + 1:].split()[-1]
        number_of_months = 2
        months = [mes1, mes2]
    else:
        number_of_months = 1
        months = [interval_string.split()[-1]]

    # To english months names translation
    ## translated_months = [months_translation[m.lower()] for m in months]
    translated_months = [Month.get_english_name(m) for m in months]

    # Step 2
    days = list(calendar.day_name)
    number_day_of_week = days.index(MEET_DAY.capitalize())

    if number_of_months == 1:
        number_day_of_month = int(interval_string.split('-')[0]) + number_day_of_week
        date_value = datetime.strptime(
            f"{number_day_of_month}-{translated_months[0]}-{year}", "%d-%B-%Y"
        )
    else:
        number_day_of_month = int(interval_string.split()[0]) + number_day_of_week
        if belong_to_month(number_day_of_month, translated_months[0], year):
            date_value = datetime.strptime(
                f"{number_day_of_month}-{translated_months[0]}-{year}", "%d-%B-%Y"
            )
        else:
            date_value = datetime.strptime(
                f"1-{translated_months[1]}-{year}", "%d-%B-%Y"
            )       

    # Step 3
    # date_value = datetime.strptime(pre_date_value, "%d-%B-%Y").date()
    print(date_value)
 
    return date_value.date()

# Sample using
# weekdate = "7-14 de enero"
# date_value_result = wednesday_date(weekdate, '2024')
# print(date_value_result)