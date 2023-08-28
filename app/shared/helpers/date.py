import datetime

def calculate_future_time(duration: int):
    expiration_time = datetime.datetime.now() + datetime.timedelta(hours=duration)
    print(expiration_time, int(expiration_time.timestamp()))

    return int(expiration_time.timestamp())