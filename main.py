from math import radians, cos, sin, asin, sqrt
from utils import prompt_user_to_confirm

from settings import *
from DataHandler import *


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
    global TransportDatabase, LocationDatabase

    while True:
        # displaying the table of all locations for the user to choose
        loc_name_list = [loc.name for loc in LocationDatabase]
        print_table(["Location"], loc_name_list)

        # prompting the user to choose the starting and ending location
        starting_loc_num = get_valid_index(LocationDatabase, msg="starting location")
        start_loc = LocationDatabase[starting_loc_num - 1]

        destination_loc_num = get_valid_index(LocationDatabase, msg="destination")
        while destination_loc_num == starting_loc_num:
            print_message("Please choose a different location!")
            destination_loc_num = get_valid_index(LocationDatabase, msg="destination")

        dest_loc = LocationDatabase[destination_loc_num - 1]

        # displaying the table of all transport for the user to choose
        print_database(TransportDatabase)

        # prompting the user to choose the transport
        transport = TransportDatabase[get_valid_index(TransportDatabase, msg="transport of your choice") - 1]

        distance = calculate_distance(start_loc, dest_loc)
        time_hrs = distance / transport.speed

        # using 'time_hrs % 1' to get the decimals
        time_min = time_hrs % 1 * 60

        if time_hrs < 1:
            time_msg = f"{int(time_min)} minutes"

        else:
            time_msg = ""
            if time_hrs > 24:
                time_msg = f"{int(time_hrs / 24)} days "
                time_hrs %= 24

            time_msg += f"{int(time_hrs)} hours {int(time_min)} minutes"

        # displaying the result of calculation
        print_message(
            f"| {start_loc.name} |    ---------- {transport.name} ---------->     | {dest_loc.name} |",
            "",
            f"   distance        : {round(distance, 2)}  KM",
            f"   estimated time  : {time_msg}",
            formatting=str.ljust,
        )

        if prompt_user_to_confirm("Do you want to continue the simulation?", "N"):
            break


def handle_data_manipulation(database, filename):
    """
    This function is responsible for all the add/edit/delete that can be done
    to the location's data or the transport's data. It does the selected command
    and then updates the file that stores the data accordingly
    """
    global TransportDatabase, LocationDatabase

    data_type = TransportData if database is TransportDatabase else LocationData
    data_changed = False
    cmd = ""

    while cmd != "4":
        print_database(database)

        cmd = prompt_input(
            prompt="1: add    2: edit    3: delete    4. exit\n",
            data_type_name="command",
            guide_msg="Please input either 1, 2, 3 or 4 as the command",
            checker=lambda x: x in ["1", "2", "3", "4"],
        )

        # creates a new data, write it to file and then add it to the database
        if cmd == "1":
            new_data = create_data(data_type)
            database.append(new_data)
            data_changed = True

        elif cmd == "2":
            if len(database) == 0:
                print_message("nothing to edit")
                continue

            # get the data to edit using the index given by the user
            index = get_valid_index(database, msg="element to edit")
            data = database[index - 1]

            # prompt the user to confirm the decision to change the selected data
            if not prompt_user_to_confirm(f"Confirm to edit edit '{data.name}' ?"):
                continue

            updated_data = update_data(data)
            database.append(updated_data)
            data_changed = True

        elif cmd == "3":
            if len(database) == 0:
                print_message("nothing to delete")
                continue

            # prompt and confirms with the user about the index of the data to delete
            index = get_valid_index(database, msg="data to delete")
            data = database[index - 1]
            if not prompt_user_to_confirm(f"Confirm to delete '{data.name}' ?"):
                continue

            # remove the deleted data from the database
            database.remove(data)
            data_changed = True

    if data_changed:
        write_database_to_file(database, filename)


def main():
    global TransportDatabase, LocationDatabase

    # loading the data from the file into the database, using extend since i don't want to
    # overwrite the existing object, which will cause some weird errors in the internal code
    LocationDatabase.extend(read_database(LOCATIONDATA_FILENAME, LocationData))
    TransportDatabase.extend(read_database(TRANSPORTDATA_FILENAME, TransportData))

    print_welcome = True

    while True:
        if print_welcome:
            print_message(WELCOME_MSG)
            print_welcome = False

        cmd = prompt_input(
            prompt="1: start simulation   2: location    3. Transport    4. Exit\n",
            data_type_name="command",
            guide_msg="Please input either 1, 2, 3 or 4 as the command",
            checker=lambda x: x in ["1", "2", "3", "4"],
        )

        if cmd == "1":
            # skipping the print welcome message using 'continue'
            if not TransportDatabase:
                print_message("Please add a transport to be used")
                continue

            if len(LocationDatabase) < 2:
                print_message("Please add at least 2 Location to travel to-and-fro")
                continue

            run_simulation()

        elif cmd == "2":
            handle_data_manipulation(LocationDatabase, LOCATIONDATA_FILENAME)
        elif cmd == "3":
            handle_data_manipulation(TransportDatabase, TRANSPORTDATA_FILENAME)
        else:
            break

        print_welcome = True


if __name__ == "__main__":
    main()
