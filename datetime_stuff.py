import time
import urequests as requests


def time_datetime_to_rtc_datetime(datetime):
    tm = datetime
    return (tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0)


def rtc_datetime_to_time_datetime(datetime):
    tm = datetime
    # RTC : year, month, day, weekday, hour, minutes, seconds, microseconds
    # time: year, month, day, hour, minutes, seconds, weekday, yearday
    return (tm[0], tm[1], tm[2], tm[4], tm[5], tm[6], tm[3], 0)


def set_local_datetime(rtc):
    """ Set local datetime from World Time API on RTC object."""
    r = requests.get("http://worldtimeapi.org/api/ip")
    r_json = r.json()
    r.close()
    unix_time = r_json["unixtime"]
    unix_time += r_json["raw_offset"]  # timezone offset
    unix_time += r_json["dst_offset"]  # daylight savings offset
    epoch_time = unix_time - 946684800  # embedded micropython uses epoch of 2000-01-01 00:00:00 UTC
    datetime = time.localtime(epoch_time)
    # Datetime tuple order is different between time.localtime and rtc.datetime. I don't know why.
    datetime = time_datetime_to_rtc_datetime(datetime)
    rtc.datetime(datetime)


def current_epoch(rtc):
    """ Seconds since 2000-1-1 00:00:00 """
    return time.mktime(rtc_datetime_to_time_datetime(rtc.datetime()))
