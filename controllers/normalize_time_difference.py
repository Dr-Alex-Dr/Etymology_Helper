import math

def normalize_time_difference(seconds):
    if seconds < 60:
        return f"{math.ceil(seconds)} секунд" if math.ceil(seconds) != 1 else "1 секунды"
    elif seconds < 3600:
        minutes = math.ceil(seconds / 60)
        return f"{minutes} минут" if minutes != 1 else "1 минуты"
    else:
        hours = math.ceil(seconds / 3600)
        return f"{hours} часов" if hours != 1 else "1 часа"
