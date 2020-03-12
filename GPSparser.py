"""
file: GPS_Checkpoint_final_Group_11.py
language: python3.7
author: np9603@cs.rit.edu Nihal Surendra Parchand
author: rk4447@cs.rit.edu Rohit Kunjilikattil
date: 10/18/2019
"""

import re
import GPS_Hazards

def txttokml(filename):
    """
    This function takes a filename and converts into proper latitude longitude format to store it in the kml file.
    :param filename: Name of each txt file
    """

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
""")

    previous_longitude=0
    previous_latitude=0
    previous_speed=0
    ''' Opening the txt file in read mode '''
    with open(filename+".txt", 'r') as file:
        ''' Iterating through the file line by line '''
        for line in file:
            ''' Splitting the line based on commas '''

            # data = line.split(",")

            data = re.split('[$,]',line)
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


                    ''' Opening the kml file in append mode and append the coordinates and speed '''

                    # if abs(latitude-previous_latitude)>0.001 and abs(longitude-previous_longitude)>0.001:
                    if speed_in_knots>0.5:
                        with open(filename+"_group_11.kml", "a") as file:
                            ''' 0.6f and 0.2f are used for rounding off the values to nearest 6 and 2 decimal places respectively'''
                            file.write("""    
    <Placemark><styleUrl>#yellowPoly</styleUrl>
      <LineString>
        <Description>Speed in Knots, instead of altitude.</Description>
      <extrude>1</extrude>
      <tesselate>1</tesselate>
      <altitudeMode>absolute</altitudeMode>
      <coordinates>\n%0.6f,%0.6f,%0.2f\n""" % (longitude, latitude, speed_in_knots))
                            file.write("""</coordinates></LineString></Placemark>""")
                    else:
                        with open(filename+"_group_11.kml", "a") as file:
                            file.write("""
  <Placemark>
  <description>Red PINfor A Stop</description>
  <Style id="normalPlacemark">
  <IconStyle><color>ff0000ff
  </color>
  </IconStyle>
  </Style>
  <Point>
  <coordinates>%0.6f,%0.6f,%0.2f\n"""% (longitude, latitude, speed_in_knots))
                            file.write("""
</coordinates></Point></Placemark>""")

                    previous_latitude = latitude
                    previous_longitude = longitude
                    previous_speed = speed_in_knots

    ''' Opening the kml file in append mode and append the remaining xml text'''
    # with open(filename+"_group_11.kml", "a") as file:
    #
    #     file.write("""     </coordinates>
    #    </LineString>
    #   </Placemark>
    #   <Placemark><description>StopLight</description><Point><coordinates>%0.6f,%0.6f,%0.2f</coordinates></Point></Placemark>"""% (longitude, latitude, speed_in_knots))

    with open(filename + "_group_11.kml", "a") as file:
            file.write("""
     </Document>
    </kml>""")

def main():
    """
    This function is used to pass text files to the txttokml function
    """

    # ''' Storing the txt filenames in a list '''
    # # filename_list = ["2019_10_09__171123_gps_file","2019_10_08__210327_gps_file","2019_10_05__210421_gps_file"]
    # # filename_list = ["2019_03_03__1523_18"]
    #
    # filename_list = ["2019_10_09__171123_gps_file", "2019_10_08__210327_gps_file","2019_10_05__210421_gps_file"]
    # ''' Passing each file in the txttokml function '''
    # for file in filename_list:
    #     txttokml(file)





main()
