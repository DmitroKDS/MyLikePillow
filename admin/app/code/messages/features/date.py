from datetime import datetime

def format(date: datetime) -> str:
    now = datetime.now()

    if now.date() == date.date():
        return f'Сьогодні {date.strftime("%H:%M")}'
    elif now.month == date.month and now.day-date.day==1:
        return f'Вчора {date.strftime("%H:%M")}'

    return date.strftime("%d.%m.%Y %H:%M")