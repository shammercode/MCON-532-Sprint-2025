from datetime import datetime, timedelta
import pytz
from dateutil.parser import parser
from dateutil.relativedelta import relativedelta

def exercise_1():
    #Exercise 1: Parse Dates
    #Use strptime() to parse:
    #"07-05-2025" as dd-mm-yyyy
    date_1 = datetime.strptime("07-05-2025", "%d-%m-%Y")
    print(date_1)
    #"May 7, 2025 2:30 PM" to a datetime object
    date_2 = datetime.strptime("May 7, 2025 2:30 PM", "%B %d, %Y %I:%M %p")
    print(date_2)
    #"2025/05/07 14:30:00" using %Y/%m/%d %H:%M:%S
    date_3 = datetime.strptime("2025/05/07 14:30:00", "%Y/%m/%d %H:%M:%S" )
    print(date_3)

def exercise_2():
    #Exercise 2: Format Dates
    #Use strftime() to format:
    #Today's date in "MM-DD-YYYY"
    today_str = datetime.now().strftime("%m-%d-%Y")
    print("Month-Day-Year:", today_str)

    #Current time as "Hour:Minute AM/PM"
    cur_time_str = datetime.now().strftime("%I:%M %p")
    print("Hour:Minute AM/PM:", cur_time_str)

    #Log-style timestamp like "[07/May/2025:14:30:00]"
    cur_time_stamp =datetime.now().strftime("[%d/%b/%Y:%H:%M:%S]")
    print("Log Timestamp:", cur_time_stamp)

def exercise_3():
    #Exercise 3: Get UTC and Local Time
    #Print the current UTC time using datetime.now(tz=...).
    cur_utc_time = datetime.now(pytz.utc)
    print("UTC Time:", cur_utc_time)
    #Convert it to "America/Los_Angeles" time.
    cur_la_time = cur_utc_time.astimezone(pytz.timezone('America/Los_angeles'))
    print("American/Los_Angeles Time:", cur_la_time)

def exercise_4():
    #Exercise 4: Time Difference
    #Calculate the number of days between "2025-05-07" and "2025-12-25".
    dates_difference = datetime.strptime("2025-05-07", "%Y-%m-%d") - datetime.strptime("2025-12-25", "%Y-%m-%d")
    days_difference = dates_difference.days
    print("Days in between:", abs(days_difference))

def exercise_5():
    #Exercise 5: Timezone Conversion
    #Create a datetime in UTC.
    cur_utc_time = datetime.now(pytz.utc)
    #Convert it to "Asia/Tokyo" and "Europe/Paris".
    cur_tokyo_time = cur_utc_time.astimezone(pytz.timezone('Asia/Tokyo'))
    cur_paris_time = cur_utc_time.astimezone(pytz.timezone('Europe/Paris'))

def exercise_6():
    #Exercise 6: Datetime Comparison
    #Write a function that takes two strings in ISO format and returns the one that represents the later time.
    def max_time(iso_str_1, iso_str_2):
        date_1 = datetime.fromisoformat(iso_str_1)
        date_2 = datetime.fromisoformat(iso_str_2)
        return max(date_1, date_2)
    utc_now = datetime.now(pytz.utc)
    utc_in_30_days =utc_now + timedelta(days=30)
    print("Later time:", max_time(utc_now.isoformat(),utc_in_30_days.isoformat()))

def exercise_7():
    #Exercise 7: Timedelta
    #Find and print in ISO format today's date and a date 3 weeks from now
    cur_date = datetime.now()
    in_3_weeks_date = cur_date + timedelta(weeks=3)
    print("Today's date in ISO format:", cur_date.isoformat())
    print("Date in 3 weeks from now in ISO format:", in_3_weeks_date.isoformat())

    #Find and print in ISO format today's date and a date 3 month ago
    cur_date = datetime.now()
    three_months_ago_date = cur_date - relativedelta(months=3)
    print("Today's date in ISO format:", cur_date.isoformat())
    print("Date 3 months ago in ISO format:", three_months_ago_date.isoformat())

def main():
    exercise_1()
    exercise_2()
    exercise_3()
    exercise_4()
    exercise_5()
    exercise_6()
    exercise_7()

if __name__ == '__main__':
    main()