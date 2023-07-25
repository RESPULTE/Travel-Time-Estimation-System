from math import radians, cos, sin, asin, sqrt

from .utils import prompt_user_to_confirm
from .data import *

WELCOME_MESSAGE = """
-----------------------------------------
 Welcome to Personal Travel Assistance !
-----------------------------------------
"""
DATA_MANIPULATION_MENU = "1: add    2: edit    3: delete    4. exit"
LOCATIONDATA_FILENAME = "LocationData.txt"
TRANSPORTDATA_FILENAME = "TransportData.txt"


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
        for i, vloc in enumerate(LocationData.database, 1):
            print(f"{i}. {vloc.name}")
        start_loc: LocationData = LocationData.database[LocationData.get_valid_index(msg="starting location") - 1]
        dest_loc: LocationData = LocationData.database[LocationData.get_valid_index(msg="destination") - 1]

        for i, vtrans in enumerate(TransportData.database, 1):
            print(f"{i}. {vtrans.name}, {vtrans.speed}")
        transport: TransportData = TransportData.database[
            TransportData.get_valid_index(msg="transport of your choice") - 1
        ]

        distance = calculate_distance(start_loc, dest_loc)
        print(f"distance: {distance}")
        time = distance / transport.speed
        print(f"estimated time: {time}")

        if prompt_user_to_confirm("exit the simulation"):
            break


def handle_data_manipulation(filename: str, data_type: LocationData | TransportData):
    """
    This function is responsible for all the add/edit/delete that can be done
    to the location's data or the transport's data. It does the selected command
    and then updates the file that stores the data accordingly
    """
    while True:
        data_type.print_database()

        cmd = prompt_input(DATA_MANIPULATION_MENU, lambda x: x in ["1", "2", "3", "4", "5"])

        # creates a new data, write it to file and then add it to the database
        if cmd == "1":
            new_data = data_type.new()
            with open(filename, "a") as f:
                f.write(new_data.to_file())
            data_type.database.append(new_data)

        elif cmd == "2":
            if len(data_type.database) == 0:
                print("nothing to edit")
                continue

            # get the data to edit using the index given by the user
            index = data_type.get_valid_index(msg="element to edit")
            data = data_type.database[index - 1]

            # prompt the user to confirm the decision to change the selected data
            if not prompt_user_to_confirm("edit the selected data"):
                continue

            data.update()

            old_loc_data = data.to_file()
            with open(filename, "r+") as f:
                loc_data = f.read()
                # look for the old data in the file and replace it with the new data
                updated_loc_data = loc_data.replace(old_loc_data, data.to_file())

                # This reset's the file reader's pointer so that it starts from the beginning of
                # the file instead of where it had left off
                f.seek(0)
                f.write(updated_loc_data)

        elif cmd == "3":
            if len(data_type.database) == 0:
                print("nothing to delete")
                continue

            # prompt and confirms with the user about the index of the data to delete
            index = data_type.get_valid_index(msg="data to delete")
            if not prompt_user_to_confirm("delete the selected data"):
                return

            # remove the deleted data from the database
            data = data_type.database.pop(index - 1)

            with open(filename, "r+") as f:
                loc_data = f.read()
                # find the deleted data in the file and remove it
                updated_loc_data = loc_data.replace(data.to_file(), "")
                f.seek(0)
                f.write(updated_loc_data)
        elif cmd == "4":
            break

    ...


def main():
    # loading the data from the file into the database
    with open(LOCATIONDATA_FILENAME, "r") as f:
        LocationData.database = [LocationData(*line.split(",")) for line in f.read().split("\n")[:-1]]

    with open(TRANSPORTDATA_FILENAME, "r") as f:
        TransportData.database = [TransportData(*line.split(",")) for line in f.read().split("\n")[:-1]]

    while True:
        print(WELCOME_MESSAGE)

        cmd = prompt_input(
            "1: start simulation   2: location    3. Transport    4. Exit", lambda x: x in ["1", "2", "3", "4"]
        )

        if cmd == "1":
            if not TransportData.database:
                print("Please add a transport to be used")
                continue

            if len(LocationData.database) < 2:
                print("Please add at least 2 Location to travel to-and-fro")
                continue

            run_simulation()
        elif cmd == "2":
            handle_data_manipulation(LOCATIONDATA_FILENAME, LocationData)
        elif cmd == "3":
            handle_data_manipulation(TRANSPORTDATA_FILENAME, TransportData)
        else:
            break

    pass


if __name__ == "__main__":
    main()
