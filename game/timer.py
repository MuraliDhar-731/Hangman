import time

def start_timer():
    return time.time()

def stop_timer(start_time):
    end = time.time()
    duration_sec = end - start_time
    return duration_sec / 60
