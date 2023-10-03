from flet_core.dropdown import Option


def is_leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def is_big_month(month):
    if month == "01" \
            or month == "03" \
            or month == "05" \
            or month == "07" \
            or month == "08" \
            or month == "10" \
            or month == "12":
        return True
    elif month == "02" \
            or month == "04" \
            or month == "06" \
            or month == "09" \
            or month == "11":
        return False


def generate_months():
    months = []
    for num in range(1, 13):
        if num < 10:
            months.append(Option(key=f"0{num}", text=f"{num} 月"))
        else:
            months.append(Option(key=f"{num}", text=f"{num} 月"))
    return months


def generate_days(num):
    days = []
    for num in range(1, num + 1):
        if num < 10:
            days.append(Option(key=f"0{num}", text=f"{num} 日"))
        else:
            days.append(Option(key=f"{num}", text=f"{num} 日"))
    return days
