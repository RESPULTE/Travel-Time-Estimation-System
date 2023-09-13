from collections import namedtuple

from utils import *
from settings import *

# NamedTuple functions exactly like tuple
# for regular tuple, indexing needs to be used when retrieving data inside of it
# but for namedtuple, I can set and use the my attribute's name to retrieve the data
# This is just to make things clearer, i hate indexing haha
TransportData = namedtuple("TransportData", ["name", "speed"])
TransportDatabase = []

LocationData = namedtuple("LocationData", ["name", "latitude", "longitude"])
LocationDatabase = []


def write_database_to_file(database: list, filename: str):
    """
    Just a simple function to write all data in a given database into a given file
    """
    if database is LocationDatabase:
        with open(filename, "w") as f:
            for data in database:
                f.write(f"{data.name}{DELIMITER}{data.latitude}{DELIMITER}{data.longitude}\n")
    else:
        with open(filename, "w") as f:
            for data in database:
                f.write(f"{data.name}{DELIMITER}{data.speed}\n")


def get_new_name(database: list, updating=False):
    """
    This function prompts the user to give a valid name for the new data that does not exist in the database
    """

    data_type = "Location" if database is LocationDatabase else "Transport"
    existing_data_name_list = [data.name for data in database]

    return prompt_input(
        prompt=f"Please input new {data_type}'s name:  ",
        data_type_name="name",
        guide_msg=f"Please do not leave the name blank or use the character '{DELIMITER}' in your name of choice",
        checker=lambda x: x not in existing_data_name_list and x not in (DELIMITER, ""),
        skipable=updating,
    )


def get_valid_index(database: list, msg: str = ""):
    """
    This function prompts the user to give a valid index of a data that exists in within the database
    in other words, index of existing data
    """

    return prompt_input(
        prompt=f"Please input the index of the {msg}:  ",
        data_type_name="index",
        guide_msg="Please input a number that is present in the column 'no' ",
        checker=lambda x: 1 <= x <= len(database),
        func=int,
    )


def create_data(data_type):
    """
    This function is used to create new instance objects by prompting the user to key-in the data
    """
    if data_type is LocationData:
        return LocationData(get_new_name(LocationDatabase), get_new_latitude(), get_new_longitude())
    else:
        return TransportData(get_new_name(TransportDatabase), get_new_speed())


def print_as_table(database: list):
    """
    This function is used to print out the database in a table-like format
    """

    # check if there's any data in the database, if not just print 'no data'
    if not database:
        print_message(NO_DATA_MSG)
        return

    if database is TransportDatabase:
        database.sort(key=lambda trans: trans.speed)

        name_list = []
        speed_list = []
        for trans in database:
            name_list.append(trans.name)
            speed_list.append(f"{trans.speed:>8.2f}")

        print_table(["Transport", "Speed (KM/h)"], name_list, speed_list)

    else:
        database.sort(key=lambda loc: loc.name)

        # This is looping through all data, and then formatting them and printing out each one
        lon_list = []
        lat_list = []
        name_list = []
        for loc in database:
            name_list.append(loc.name)
            if loc.latitude > 0:
                latitude = f"{loc.latitude:>8.4f}  N"
            else:
                # Since the data itself is negative, the negative is there to make it positive when it is printed out
                latitude = f"{-loc.latitude:>8.4f}  S"
            lat_list.append(latitude)

            if loc.longitude > 0:
                longitude = f"{loc.longitude:>8.4f}  E"
            else:
                # Since the data itself is negative, the negative is there to make it positive when it is printed out
                longitude = f"{-loc.longitude:>8.4f}  W"
            lon_list.append(longitude)

        print_table(["Location", "Latitude", "Longitude"], name_list, lat_list, lon_list)


def read_database(filename, data_type):
    """
    This function reads from the given file and returns a list of data
    If the file does not exist, then this function will simply create the file and return anempty list
    """
    database = []
    try:
        with open(filename, "r") as f:
            if data_type is TransportData:
                for line in f.readlines():
                    name, speed = line.split(DELIMITER)
                    database.append(data_type(name, float(speed)))
            else:
                for line in f.readlines():
                    name, lat, lon = line.split(DELIMITER)
                    database.append(data_type(name, float(lat), float(lon)))
    except FileNotFoundError:
        with open(filename, "w") as f:
            pass

    return database


def update_data(data: TransportData | LocationData, database: list):
    """
    This function is used to update the data object's attributes by
    prompting the user to key-in the data that needs to be edited.

    If the user chose to not enter anything (just press enter),
    then the original value will remain unchanged
    """

    database.remove(data)
    new_name = get_new_name(database, updating=True) or data.name

    if database is LocationDatabase:
        new_latitude = get_new_latitude(updating=True) or data.latitude
        new_longitude = get_new_longitude(updating=True) or data.longitude
        updated_data = LocationData(new_name, new_latitude, new_longitude)
    else:
        new_speed = get_new_speed(updating=True) or data.speed
        updated_data = TransportData(new_name, new_speed)

    return updated_data


def get_new_speed(updating=False):
    """
    Prompts the user to key in the new speed and checks whether it is valid.
    """
    return prompt_input(
        prompt="Please input transport's speed (KM/h): ",
        data_type_name="speed",
        guide_msg="Please input a speed that's a non-negative number",
        checker=lambda x: x > 0,
        func=float,
        skipable=updating,
    )


def get_new_latitude(updating=False):
    """
    Prompts the user to key in the new latitude/longitude and checks whether it is valid.
    A valid latitude should be in the form of "101.1202N", the direction can either be
    "N", north or "S" south
    """
    lat_data = prompt_input(
        prompt="Please input location's latitude (example: 3.1319N) : ",
        data_type_name="Coordinate (example: 3.1319N)",
        guide_msg="Please input the latitude of the location, which should be between 0 and 90, followed by either N(North) or S(South) without any spaces",
        checker=lambda x: 0 <= x[0] <= 90 and x[1] in ["N", "S"],
        func=lambda x: (float(x[:-1]), x[-1]),
        skipable=updating,
    )

    # This is to check whether or not the user is trying to update the latitude data
    # if "not long_data" is true, then the user hasn't inputted anything and "updating" is true, which means user is updating
    # if both are true, then the user is updating and wishes to keep the original value the same
    if not lat_data and updating:
        return

    lat, direction = lat_data

    return lat if direction == "N" else -lat


def get_new_longitude(updating=False):
    """
    Prompts the user to key in the new latitude/longitude and checks whether it is valid.
    A valid latitude should be in the form of "101.1202W", the direction can either be
    "W", west or "E" east
    """
    long_data = prompt_input(
        prompt=f"Please input location's longitude (example: 101.6841E) : ",
        data_type_name="Coordinate (example: 101.6841E)",
        guide_msg="Please input the longitude of the location, which should be between 0 and 180, followed by either W(West) or E(East) without any spaces",
        checker=lambda x: x[1] in ["W", "E"] and 0 <= x[0] <= 180,
        func=lambda x: (float(x[:-1]), x[-1]),
        skipable=updating,
    )

    # This is to check whether or not the user is trying to update the longitude data
    # if "not long_data" is true, then the user hasn't inputted anything and "updating" is true, which means user is updating
    # if both are true, then the user is updating and wishes to keep the original value the same
    if not long_data and updating:
        return

    long, direction = long_data

    return long if direction == "E" else -long
