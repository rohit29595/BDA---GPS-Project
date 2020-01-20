"""
File Name : GPS_Hazards.py
Authors : Nihal Parchand (np3123@rit.edu),Vaibhav Joshi (vj3470@rit.edu),Rohit Kunjilikattil(rk1111@rit.edu)
Group # : 11
Date : 12/02/2019
Version : 1.0
Revisions :
"""

def generate_kml_header():
    """
    This function generates the initial KML header for the XXX KML file
    """
    # Opening our file that is to be outputted.
    with open('GPS_checkpoint.kml', 'w+') as f:

        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        f.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
        f.write("<Document>\n")
        f.write("<Style id=\"yellowPoly\">\n")
        f.write("  <LineStyle>\n"
                    "    <color>Af00ffff</color>\n"
                    "    <width>6</width>\n"
                "  </LineStyle>\n"
                "  <PolyStyle>\n"
                "    <color>7f00ff00</color>\n"
                "  </PolyStyle>\n")
        f.write("</Style>\n")
        f.close()

def getdecdegree(degmin,sign):
    """
    A helper function to convert degreee-minutes to decimal degree for latitute longitude
    :param degmin: Degree minutes
    :param sign: N,E,W,S (will determine the final sign)
    :return: the decimal degree with the appropriate sign
    """
    deg = degmin // 100 # get degree
    min = degmin % 100 # get minutes

    sign=-1 if sign in ['S', 'W'] else 1 # handling negatives
    return round(sign*(deg+float(min)/60),6)


def find_left_right_turns(gps_data):
    """
    This function determines that the turn is left / right using a sliding window technique.
    It first separates out the GPRMC entries and uses the angle field to determine the turn type.
    :param gps_data: List containing each line of GPS file
    :return: None
    """

    # TO store all the GPRMC angle field of each entry
    angles = []

    # To seprate the GPRMC fields
    GPRMC = []

    # To keep track of the sliding window.
    index = 0

    # this loop populates the angle fields of each of the GPRMC entries
    for idx, data in enumerate(gps_data):
        line = data.split(",")
        if line[0] == "$GPRMC":
            if line[2] == "A": # if valid
                GPRMC.append(data)
                angles.append(float(line[8]))
        else:
            pass
    # This is a sliding window that is used to determine the angle difference which will subsequently determine the
    # type of turn. A difference between angles of 8 entries is taken (the number 8 is decided after manual inspection
    # of GPS files. Once it is determined that the turn is made, the window skips 8 entries to avoid repetitive markings
    while index < len(angles)-8:
        # Thresholds that determine whether the angle is a turn
        if 40 <= abs(angles[index] - angles[index + 8]) <= 95:

            # get corresponding latitute and longitude
            latitude = getdecdegree(float(GPRMC[index].split(",")[3]), GPRMC[index].split(",")[4])
            longitude = getdecdegree(float(GPRMC[index].split(",")[5]), GPRMC[index].split(",")[6])

            # for left turns, the angle at the start is always greater than the final angle. Angle decreases
            if angles[index] > angles[index+8]:

                # add marker
                with open("GPS_checkpoint.kml", "a") as file:
                    file.write("""
                      <Placemark>
                      <description>Left turn</description>
                      <Point>
                      <coordinates>%0.6f,%0.6f\n""" % (longitude, latitude))
                    file.write("""
                    </coordinates></Point></Placemark>""")
                    # slide window
                    index += 8
            # for right turns, the angle at the start is always less than the final angle. Angle increases
            else:
                # add marker
                with open("GPS_checkpoint.kml", "a") as file:
                    file.write("""
                  <Placemark>
                  <description>Right turn</description>
                  <Style id="normalPlacemark">
                  <IconStyle><color>ff00ff00
                  </color>
                  </IconStyle>
                  </Style>
                  <Point>
                  <coordinates>%0.6f,%0.6f\n""" % (longitude, latitude))
                    file.write("""
                </coordinates></Point></Placemark>""")

                # slide window
                index += 8
        else:
            index += 1


def get_lat_lon(gps_data):
    """
    Convert the GPS coordinates into KML format and return all data in a list
    :param gps_data: list of GPS data
    :return: returns the converted coordinates and speed data in a list which will be populated in the kml file.
    """

    lat_lon_speed = []
    for data in gps_data:
        line = data.split(",")
        # only considering GPRMC as it gives us speed
        if line[0] == "$GPRMC":
            if line[2] == "A": # if valid
                lat = getdecdegree(float(line[3]), line[4]) # 3 and 4 is lat
                lon = getdecdegree(float(line[5]), line[6]) # 5 and 6 is long
                speed=float(line[7]) # speed
                lat_lon_speed.append([lon, lat, speed]) # append the data
        else:
            pass

    return lat_lon_speed

def generate_kml(lat_lon) :
    """
    :param lat_lon: list containing the latitude, longitude and speed values for each entry
    """
    # Opening our file that is to be outputted.
    with open('GPS_checkpoint.kml', 'a') as f:

        f.write("<Placemark><styleUrl>#yellowPoly</styleUrl>\n")
        f.write("<LineString>\n")
        f.write("<Description>Speed in Knots, instead of altitude.</Description>\n")
        f.write("  <extrude>l</extrude>\n")
        f.write("  <tesselate>l</tesselate>\n")
        f.write("  <altitudeMode>absolute</altitudeMode>\n")
        f.write("  <coordinates>\n")

        for entry in lat_lon:
            f.write(" "+ str(entry[0]) + "," + str(entry[1]) + "," +str(entry[2]))
            f.write("\n")

        f.write(" </coordinates>\n")
        f.write("   </LineString>\n")
        f.write("  </Placemark>\n")
        f.write(" </Document>\n")
        f.write("</kml>\n")


if __name__== '__main__' :

    with open('2019_05_13__1213_11__Penfield_to_RIT.txt', 'r') as file:

        # filtering out the lines before the actual GPS data
        line = None
        while True:
            line = file.readline()
            if not line.strip():
                pass
            elif line.strip().split(",")[0] == "$GPGGA" or line.strip().split(",")[0] == "$GPRMC":
                break

        # read remaining GPS data.
        gps_data = file.readlines()

        # inserting back the first line
        gps_data.insert(0,line)

        # remove new line chars
        gps_data = [data.strip() for data in gps_data]

        # setup KML file
        generate_kml_header()

        # function call to find the left and right turns.
        find_left_right_turns(gps_data)

        # compute the latitude and longitude coordinates
        lat_lon=get_lat_lon(gps_data)

        # plot the path.
        generate_kml(lat_lon)













