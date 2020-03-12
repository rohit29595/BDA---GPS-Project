import pandas as pd
import re

def calculate_noise_floor(filename):
    gps_data = pd.DataFrame([], columns=['Longitude', 'Latitude', 'Speed In Knots'])

    biggest_latitude_difference = 0
    biggest_longitude_difference = 0
    """
    This function takes a filename and converts into proper latitude longitude format to store it in the kml file.
    :param filename: Name of each txt file
    """

    ''' Opening the kml file in write mode and writing the xml template '''
    with open(filename + "_group_11.kml", "w") as file:
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
    with open(filename + ".txt", 'r') as file:
        ''' Iterating through the file line by line '''
        for line in file:
            ''' Splitting the line based on commas '''

            # data = line.split(",")

            data = re.split('[$,]', line)
            # print(data)

            ''' Checking if the starting field is GPRMC '''

            if len(data) > 1 and data[1] == "GPRMC":
                if data[3] == "A":
                    # print("Latitude: ",data[3])
                    # print("Longitude: ",data[5])
                    ''' Parsing and converting gps latitude for kml '''
                    gps_latitude = float(data[4])
                    ''' If the direction is South then multiply latitude by -1 '''
                    if data[5] == "S":
                        gps_latitude *= -1

                    ''' Converting latitude according to the kml format '''
                    latitude_degree = int(gps_latitude / 100)
                    latitude_minute = gps_latitude - latitude_degree * 100
                    latitude = latitude_degree + (latitude_minute / 60)

                    ''' Parsing and converting gps longitude for kml'''
                    gps_longitude = float(data[6])
                    ''' If the direction is West then multiply latitude by -1 '''
                    if data[7] == "W":
                        gps_longitude *= -1

                    ''' Converting longitude according to the kml format '''
                    longitude_degree = int(gps_longitude / 100)
                    longitude_minute = gps_longitude - longitude_degree * 100
                    longitude = longitude_degree + (longitude_minute / 60)

                    ''' Storing the speed '''
                    speed_in_knots = float(data[8])

                    ''' Printing the latitude, longitude, and speed in knots '''
                    # print("Latitude: ",latitude,end=" ")
                    # print("Longitude: ",longitude,end=" ")
                    # print("Speed: ",speed_in_knots)

                    new_row = {'Longitude': longitude, 'Latitude': latitude, 'Speed In Knots': speed_in_knots}
                    gps_data = gps_data.append(new_row, ignore_index=True)

    for i in range(0,len(gps_data)-1):
        # print(data.iloc[0][i])
        # # print(data.iloc[0][i+1])

        #
        long_diff = abs((gps_data['Longitude'][i])-(gps_data['Longitude'][i+1]))
        lat_diff = abs((gps_data['Latitude'][i])-(gps_data['Latitude'][i+1]))
        if long_diff>1 or lat_diff>1:
            print("--------------------------")
            gps_data=gps_data.drop([i])



    highest_long = gps_data['Longitude'].max()
    smallest_long = gps_data['Longitude'].min()

    noise_floor_for_longitude = highest_long - smallest_long

    print(noise_floor_for_longitude)

    highest_lat = gps_data['Latitude'].max()
    smallest_lat = gps_data['Latitude'].min()

    noise_floor_for_latitude = highest_lat - smallest_lat

    # print("Longitude Diff :" , noise_floor_for_longitude)
    # print("Latitude Diff :" , noise_floor_for_latitude)

    return noise_floor_for_longitude,noise_floor_for_latitude



def main():
    """
    This function is used to pass text files to the txttokml function
    """

    ''' Storing the txt filenames in a list '''

    ''' Passing each file in the txttokml function '''

    filename = "Going_NoWhereFast"
    noise_floor_for_long , noise_floor_for_lat = calculate_noise_floor(filename)

    print("Longitude noise floor is : " + str(noise_floor_for_long))
    print("Latitude noise floor is : " + str(noise_floor_for_lat))







main()