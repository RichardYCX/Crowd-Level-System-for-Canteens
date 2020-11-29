# Done By Richard

from datetime import *
import calendar
from Data_Func import *

MenuData = Get_Menu()
StoreData = Get_Hour()

#store names eg. 'Western Stall', 'MacDonalds'
#date: 'dd mm yyyy hh min' eg. '23 10 2020 10 00'
#day eg. 'Monday', 'Tuesday'
#period eg. 'Opening Hours', 'Breakfast', 'Lunch', 'Dinner'

def Return_Store_Names(): #returns store names as list of strings
    try:
        store_names = [store_name for store_name in MenuData.keys()]
    except Exception as error:
        print(error)
        store_names = None
    return store_names

def findDay(date_of_interest): #input date. Returns (day,time) as datetime object
    try:
        if date_of_interest == 'now':
            date_time = datetime.now()
        else:
            date_time = datetime.strptime(date_of_interest, '%d %m %Y %H %M')
        day_of_week = calendar.day_name[date_time.weekday()]
        time_of_day = date_time.time()
    except Exception as error:
        print(error)
        day_of_week = None
        time_of_day = None
    return day_of_week,time_of_day

def Return_Store_Hours(store_name,day_of_interest,period_of_interest): #input store name, day, period of operation. Returns (start hour,end hour) as datetime objects
    try:
        time_slot = StoreData[store_name][day_of_interest][period_of_interest]
        if time_slot == []:
            start_time,end_time = float('inf'),float('inf')
        else:
            start_time,end_time = time_slot
    except Exception as error:
        print(error)
        start_time, end_time = None,None
    return start_time, end_time

def Return_Store_Status(store_name,date_of_interest,period_of_interest): #input store name, date, period.
                                                                         #Returns status as Boolean
    try:
        day_of_week, time_of_day = findDay(date_of_interest)
        start_time, end_time = Return_Store_Hours(store_name=store_name,day_of_interest=day_of_week,period_of_interest=period_of_interest)
        if not start_time == float('inf'):
            if start_time <= time_of_day <= end_time:
                status = True
            else:
                status = False
        else:
            status = False
    except Exception as error:
        print(error)
        status = None
    return status

def Return_Store_Menu(store_name,date_of_interest): #input store name and date. Returns menu as list of strings
    try:
        if Return_Store_Status(store_name=store_name,date_of_interest=date_of_interest,period_of_interest='Opening Hours') == False:
            menu = None
        else:
            day_of_week,time_of_day = findDay(date_of_interest)
            periods = [period for period in StoreData[store_name][day_of_week].keys()]
            for period in periods[1:]:
                start_time,end_time = Return_Store_Hours(store_name=store_name,day_of_interest=day_of_week,period_of_interest=period)
                if start_time <= time_of_day <= end_time:
                    menu = MenuData[store_name][day_of_week][period]
                    break
    except Exception as error:
        print(error)
        menu = None
    return menu
