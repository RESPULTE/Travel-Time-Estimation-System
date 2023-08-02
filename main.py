from math import radians, cos, sin, asin, sqrt
from utils import prompt_user_to_confirm

from settings import *
from data import *


def calculate_distance(start: LocationData, dest: LocationData):
    """
    This function calculates the straight-line distance between 2 coordinates using the Haversine Formula
    """
    lon1, lat1 = radians(start.longitude), radians(start.latitude)
    lon2, lat2 = radians(dest.longitude), radians(dest.latitude)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = pow(sin(dlat / 2), 2) + cos(lat1) * cos(lat2) * pow(sin(dlon / 2), 2)
    c = 2 * asin(sqrt(a))

    earth_radius = 6371
    distance = earth_radius * c

    return distance


def run_simulation():
    """
    This function prompts the user to choose from available
    locations and transports uses the "calculate_distance()" function
    to get the distance between 2 selected location and then calculates
    the time to get there with the selected transport
    """
    while True:
        # displaying the table of all locations for the user to choose
        table_len = 3 + 5 + 50
        print("-" * table_len)
        print(f"|{'no.'.center(5)}|{'Location'.center(50)}|")
        print("-" * table_len)
        for i, vloc in enumerate(LocationData.database, 1):
            print(f"|{(str(i) + '.').center(5)}|{vloc.name.center(50)}|")
            print("-" * table_len)

        # prompting the user to choose the starting and ending location
        start_loc: LocationData = LocationData.database[LocationData.get_valid_index(msg="starting location") - 1]
        dest_loc: LocationData = LocationData.database[LocationData.get_valid_index(msg="destination") - 1]

        # displaying the table of all transport for the user to choose
        table_len = 4 + 5 + 50 + 15
        print("-" * table_len)
        print(f"|{'no.'.center(5)}|{'Transport'.center(50)}|{'Speed (KM/h)'.center(15)}|")
        print("-" * table_len)
        for i, vtrans in enumerate(TransportData.database, 1):
            print(f"|{(str(i) + '.').center(5)}|{str(vtrans.name).center(50)}|{str(vtrans.speed).center(15)}|")
        print("-" * table_len)

        # prompting the user to choose the transport
        transport: TransportData = TransportData.database[
            TransportData.get_valid_index(msg="transport of your choice") - 1
        ]

        distance = calculate_distance(start_loc, dest_loc)
        time = distance / transport.speed

        # displaying the result of calculation
        print("\n")
        print("-" * 40)
        print(f"distance        : {round(distance, 2)}  KM")
        print(f"estimated time  : {round(time, 2)}  hours")
        print("-" * 40)
        print("\n")

        if prompt_user_to_confirm("exit the simulation"):
            break


def main():
    # loading the data from the file into the database
    LocationData.database = read_database(LOCATIONDATA_FILENAME, LocationData)
    TransportData.database = read_database(TRANSPORTDATA_FILENAME, TransportData)

    print_welcome = True

    while True:
        if print_welcome:
            print_message(WELCOME_MSG)
            print_welcome = False

        cmd = prompt_input(
            "1: start simulation   2: location    3. Transport    4. Exit\n",
            "command",
            lambda x: x in ["1", "2", "3", "4"],
        )

        if cmd == "1":
            # skipping the print welcome message using 'continue'
            if not TransportData.database:
                print_message("Please add a transport to be used")
                continue

            if len(LocationData.database) < 2:
                print_message("Please add at least 2 Location to travel to-and-fro")
                continue

            run_simulation()

        elif cmd == "2":
            LocationData.handle_data_manipulation(LOCATIONDATA_FILENAME)
        elif cmd == "3":
            TransportData.handle_data_manipulation(TRANSPORTDATA_FILENAME)
        else:
            break

        print_welcome = True


if __name__ == "__main__":
    main()
