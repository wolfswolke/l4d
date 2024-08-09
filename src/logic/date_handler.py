from datetime import datetime


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d_%H:%M:%S")