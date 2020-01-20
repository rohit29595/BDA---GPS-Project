"""
file: GPS_Checkpoint_final_Group_11.py
language: python3.7
author: np9603@cs.rit.edu Nihal Surendra Parchand
author: rk4447@cs.rit.edu Rohit Kunjilikattil
author: vj3470@cs.rit.edu Vaibhav Joshi
date: 10/18/2019
"""


''' Importing libraries '''

import os
import glob
import re
import pandas as pd
from datetime import datetime

from datetime import timedelta as td


noise_floor_for_long =0
noise_floor_for_lat = 0



def store_gps_in_df(filename):
    gps_data = pd.DataFrame([], columns=['Longitude', 'Latitude', 'Speed In Knots'])

    previous_latitude = 0
    previous_longitude = 0
    with open(filename, 'r') as file:
        ''' Iterating through the file line by line '''
        for line in file:
            ''' Splitting the line based on commas '''

            data = re.split(',',line.strip())
            print(data)

            ''' Checking if the starting field is GPRMC '''

            if len(data) == 13 and data[0] == "$GPRMC":
                if data[2] == "A":

                    ''' Parsing and converting gps latitude for kml '''
                    gps_latitude = float(data[3])
                    ''' If the direction is South then multiply latitude by -1 '''
                    if data[4] == "S":
                        gps_latitude *= -1

                    ''' Converting latitude according to the kml format '''
                    latitude_degree = int(gps_latitude / 100)
                    latitude_minute = gps_latitude - latitude_degree * 100
                    latitude = latitude_degree + (latitude_minute / 60)

                    ''' Parsing and converting gps longitude for kml'''
                    gps_longitude = float(data[5])
                    ''' If the direction is West then multiply latitude by -1 '''
                    if data[6] == "W":
                        gps_longitude *= -1

                    ''' Converting longitude according to the kml format '''
                    longitude_degree = int(gps_longitude / 100)
                    longitude_minute = gps_longitude - longitude_degree * 100
                    longitude = longitude_degree + (longitude_minute / 60)
                    # info = pynmea2.parse(line)
                    ''' Storing the speed '''
                    speed_in_knots = float(data[7])

                    ''' Printing the latitude, longitude, and speed in knots '''
                    # print("Latitude: ",latitude,end=" ")
                    # print("Longitude: ",longitude,end=" ")
                    # print("Speed: ",speed_in_knots)

                    if abs(latitude-previous_latitude) > 0.00008333333334 and abs(longitude-previous_longitude) > 0.00010666666667:
                        new_row = {'UTC Time': datetime.strptime(data[1],'%H%M%S.%f'), 'Longitude': longitude, 'Latitude': latitude, 'Speed In Knots': speed_in_knots}
                        gps_data = gps_data.append(new_row, ignore_index=True)
                        previous_latitude = latitude
                        previous_longitude = longitude

    return gps_data


def cleaning_df(data):
    for i in range(0,len(data)-1):
        # print(data.iloc[0][i])
        # # print(data.iloc[0][i+1])

        long_diff = abs((data['Longitude'][i])-(data['Longitude'][i+1]))
        lat_diff = abs((data['Latitude'][i])-(data['Latitude'][i+1]))
        if long_diff>1 or lat_diff>1:
            print("--------------------------")
            data=data.drop([i])

    remove_index_list=[]
    start_index=0
    end_index = 0
    i=0
    j=0
    while i < len(data):
        if j == len(data):
            return remove_index_list

        if data['Speed In Knots'][i] < 0.5:
            print(i)
            start_index = i
            for j in range(start_index,len(data)):

                if data['Speed In Knots'][j] < 0.5:
                    j+=1

                else:
                    end_index = j
                    remove_index_list.append((start_index,end_index))
                    print(remove_index_list)
                    diff=end_index-start_index
                    i += diff
                    break
        else:
            i+=1

    return remove_index_list

def potential_stops(filename,data,index_list):
    print(data)
    with open(filename + "no_of_stops_group_11.kml", "w") as file:
        file.write("""<?xml version="1.0" encoding="UTF-8"?>
        <kml xmlns="http://www.opengis.net/kml/2.2">
        <Document>
        <Style id="yellowPoly">
          <LineStyle>
            <color>Af00ffff</color>
            <width>6</width>
          </LineStyle>
          <PolyStyle>
            <color>7f00ff00</color>
          </PolyStyle>
        </Style>
    """)

    for index in range(len(index_list)):
        with open(filename + ".kml", "a") as file:
            ''' 0.6f and 0.2f are used for rounding off the values to nearest 6 and 2 decimal places respectively'''
            file.write("""    
           <Placemark>
           <description>Red PINfor A Stop</description>
           <Style id="normalPlacemark">
           <IconStyle>
           <color>ff0000ff</color>
           <Icon>
           <href>http://maps.google.com/mapfiles/kml/paddle/1.png</href>
           </Icon>
           </IconStyle>
           </Style>
           <Point>
           <coordinates>\n%0.6f,%0.6f,%0.2f\n""" % ((data.iloc[index_list[index][1]])[0],(data.iloc[index_list[index][1]])[1],(data.iloc[index_list[index][1]])[2]))
            file.write("""</coordinates></Point></Placemark>""")

    with open(filename + ".kml", "a") as file:
            file.write("""
     </Document>
    </kml>""")


def calculate_trip_time(data):
    length = len(data)-1
    start_time = data.iloc[0][3]
    end_time = data.iloc[length][3]
    # start_time = ":".join([start_time[i:i + 3] for i in range(0, len(start_time), 2)])
    # end_time = ":".join([end_time[i:i + 3] for i in range(0, len(end_time), 2)])
    #
    time_diff = end_time - start_time
    # time_diff = datetime.strptime(end_time,'%H:%M:%S')
    return time_diff


def calculate_stop_time(data,list):
    total_stop_time = td(minutes=0)
    for index in list:
        start_time = data.iloc[index[0]][3]
        end_time =  data.iloc[index[1]][3]
        time_diff = end_time-start_time
        total_stop_time+=time_diff
    return total_stop_time


def calculate_speed_time(data):
    """
    This function calculates the time spent when speed is below 20mph and above 60mph
    :param data:
    :return:
    """

    for i in range(0,len(data)-1):
        long_diff = abs((data['Longitude'][i])-(data['Longitude'][i+1]))
        lat_diff = abs((data['Latitude'][i])-(data['Latitude'][i+1]))
        if long_diff>1 or lat_diff>1:
            data=data.drop([i])

    total_time_below_20_above_60_mph_list=[]

    i=0
    j=0
    while i < len(data):
        if j == len(data):
            break

        if (data['Speed In Knots'][i]*1.15) < 20 or (data['Speed In Knots'][i]*1.15) > 60:
            start_index = i
            for j in range(start_index,len(data)):

                if (data['Speed In Knots'][j]*1.15) < 20 or (data['Speed In Knots'][i]*1.15) > 60:
                    j+=1

                else:
                    end_index = j
                    total_time_below_20_above_60_mph_list.append((start_index,end_index))
                    # print(total_time_below_20_above_60_mph_list)
                    diff=end_index-start_index
                    i += diff
                    break
        else:
            i+=1

    total_time_below_20_above_60_mph = td(minutes=0)
    for index in total_time_below_20_above_60_mph_list:
        start_time = data.iloc[index[0]][3]
        end_time = data.iloc[index[1]][3]
        time_diff = end_time - start_time
        total_time_below_20_above_60_mph += time_diff
    print(total_time_below_20_above_60_mph_list)
    return total_time_below_20_above_60_mph

def txttokml(filename):

    """
    This function takes a filename and converts into proper latitude longitude format to store it in the kml file.
    :param filename: Name of each txt file
    """
    gps_data = pd.DataFrame([], columns=['Longitude', 'Latitude', 'Speed In Knots'])

    ''' Opening the kml file in write mode and writing the xml template '''
    with open(filename+"_group_11.kml", "w") as file:
        file.write("""<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
    <Style id="yellowPoly">
      <LineStyle>
        <color>Af00ffff</color>
        <width>6</width>
      </LineStyle>
      <PolyStyle>
        <color>7f00ff00</color>
      </PolyStyle>
    </Style>
    <Placemark><styleUrl>#yellowPoly</styleUrl>
      <LineString>
        <Description>Speed in Knots, instead of altitude.</Description>
      <extrude>1</extrude>
      <tesselate>1</tesselate>
      <altitudeMode>absolute</altitudeMode>
      <coordinates>\n""")

    previous_longitude = 0
    previous_latitude = 0
    previous_speed = 0
    ''' Opening the txt file in read mode '''
    with open(filename+".txt", 'r') as file:
        ''' Iterating through the file line by line '''
        for line in file:
            ''' Splitting the line based on commas '''

            # data = line.split(",")

            data = re.split(',', line.strip())
            print(data)

            ''' Checking if the starting field is GPRMC '''

            if len(data) == 13 and data[0] == "$GPRMC":
                if data[2] == "A":

                    ''' Parsing and converting gps latitude for kml '''
                    gps_latitude = float(data[3])
                    ''' If the direction is South then multiply latitude by -1 '''
                    if data[4] == "S":
                        gps_latitude *= -1

                    ''' Converting latitude according to the kml format '''
                    latitude_degree = int(gps_latitude / 100)
                    latitude_minute = gps_latitude - latitude_degree * 100
                    latitude = latitude_degree + (latitude_minute / 60)

                    ''' Parsing and converting gps longitude for kml'''
                    gps_longitude = float(data[5])
                    ''' If the direction is West then multiply latitude by -1 '''
                    if data[6] == "W":
                        gps_longitude *= -1

                    ''' Converting longitude according to the kml format '''
                    longitude_degree = int(gps_longitude / 100)
                    longitude_minute = gps_longitude - longitude_degree * 100
                    longitude = longitude_degree + (longitude_minute / 60)
                    ''' Storing the speed '''
                    speed_in_knots = float(data[7])

                    new_row = {'Longitude': longitude, 'Latitude': latitude, 'Speed In Knots': speed_in_knots}
                    gps_data = gps_data.append(new_row, ignore_index=True)

                    ''' Opening the kml file in append mode and append the coordinates and speed '''
                    with open(filename+"_group_11.kml", "a") as file:
                        ''' 0.6f and 0.2f are used for rounding off the values to nearest 6 and 2 decimal places respectively'''
                        file.write("""%0.6f,%0.6f,%0.2f\n""" % (longitude, latitude, speed_in_knots))

    ''' Opening the kml file in append mode and append the remaining xml text'''
    with open(filename+"_group_11.kml", "a") as file:
        file.write("""     </coordinates>
       </LineString>
      </Placemark>
     </Document>
    </kml>""")

    return gps_data

def main():
    """
    This function is used to pass text files to the txttokml function
    """

    ''' Storing the txt filenames in a list '''
    filename_list = ["2019_10_05__210421_gps_file","2019_10_08__210327_gps_file","2019_10_09__171123_gps_file"]

    ''' Passing each file in the txttokml function '''
    cost_function_dict = {}

    for filename in glob.glob("*.txt"):
        data = store_gps_in_df(filename)
        trip_time = calculate_trip_time(data)
        print("The trip time was : ", trip_time)

        remove_list = cleaning_df(data)
        stop_time = calculate_stop_time(data, remove_list)
        print("The total stop time was : ",stop_time)

        total_time_below_20_above_60_mph = calculate_speed_time(data)
        print("The total time below 20mph and above 60mph was : ", total_time_below_20_above_60_mph)
        regularization = (stop_time.total_seconds()+total_time_below_20_above_60_mph.total_seconds())
        cost_function = (trip_time.total_seconds()/1800) + regularization

        cost_function_dict[filename] = cost_function

    for key,value in cost_function_dict.items():
        print(key)
        print(value)

    # txttokml(file2)

main()