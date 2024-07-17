import datetime

timestamp_ms = 1468507907000

timestamp_seconds = timestamp_ms / 1000.0

dt_object = datetime.datetime.utcfromtimestamp(timestamp_seconds)

print("UTC Date and Time:", dt_object.strftime('%Y-%m-%d %H:%M:%S'))
