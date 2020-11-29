# Done By Richard

from collections import OrderedDict
from datetime import datetime

import Basic_Store_Func
import matplotlib.pyplot as plt
#from Data_Func import *

import Data_Func

def Average_People(): #eturns a dictionary in the format of [store_name][day][time slot][average_number of people]
                      #time_slot eg. 0900, 1000
    Queue_data = Data_Func.Get_Average_People_Data()
    Average_People_Data = {}
    for store in Queue_data:
        day_dict = {}
        for day in Queue_data[store]:
            time_dict = []
            for time in Queue_data[store][day]:
                time_dict.append(round(sum(Queue_data[store][day][time])/len(Queue_data[store][day][time])))
            day_dict[day] = time_dict
        Average_People_Data[store] = day_dict
    return Average_People_Data

def Queue_Time(store_name,number_of_people): #returns queue time, while checking if store is open
    Wait_Time_Data = Data_Func.Get_Waiting_Time()
    print("Function/Queue_Time")
    daynow=datetime.now().strftime("%A")
    hournow=int(datetime.now().strftime("%H"))

    Opening_Time, Closing_Time = Basic_Store_Func.Return_Store_Hours(store_name=store_name,day_of_interest=daynow,period_of_interest='Opening Hours')
    Opening_Time, Closing_Time = int(Opening_Time.strftime("%H")), int(Closing_Time.strftime("%H"))
    time_per_person=Wait_Time_Data[store_name][daynow]
    if Opening_Time <= hournow <= Closing_Time:
        return number_of_people*time_per_person[hournow-Opening_Time]
    else:
        return 0

def Barplot(store_name,date_of_interest): #plots the bargraph of how busy the store is on a usual day
    Wait_Time_Data = Data_Func.Get_Waiting_Time()
    People_Queue_Data = Average_People()
    day = date_of_interest
    Opening_Time, Closing_Time = Basic_Store_Func.Return_Store_Hours(store_name=store_name,day_of_interest=day,period_of_interest='Opening Hours')
    if (Opening_Time, Closing_Time) != (float('inf'),float('inf')):
        try:
            Opening_Time, Closing_Time = int(Opening_Time.strftime("%H")), int(Closing_Time.strftime("%H"))
            time_per_person = Wait_Time_Data[store_name][day]
            number_of_people = People_Queue_Data[store_name][day]
            y = [time*number for time, number in zip(time_per_person,number_of_people)]
            plt.bar(x=range(Opening_Time,Closing_Time),height=y,align='edge')
            plt.xlabel('Hours', fontsize=20)
            plt.ylabel('Average Waiting Time', fontsize=20)
            plt.title(day)
            #plt.show()
            print({"x":range(Opening_Time,Closing_Time), "y":y})
            return {"x":range(Opening_Time,Closing_Time), "y":y}
        except:
            return None
    else:
        return None
