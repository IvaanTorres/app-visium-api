import datetime

def calculate_future_time(duration: int):
    current_time = datetime.datetime.utcnow()
    expiration_time = current_time + datetime.timedelta(minutes=duration)

    return expiration_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')  # Convert to ISO 8601 format