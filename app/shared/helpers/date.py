import datetime

def calculate_future_time(duration: int):
    current_time = datetime.datetime.utcnow()
    expiration_time = current_time + datetime.timedelta(hours=duration)

    return int(expiration_time.timestamp())