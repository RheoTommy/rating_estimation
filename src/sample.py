import time
from datetime import datetime

unix_time = datetime.fromisoformat("2021-11-27T22:40:00+09:00")  # abc229
print(unix_time)
print(unix_time.timestamp())

print(datetime.now().timestamp())