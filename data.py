from __future__ import annotations  # This is for type-hinting

from abc import ABC, abstractclassmethod
from typing import List, Union

from utils import *
from settings import *


class Data(ABC):
    """
    This is a abstract base class for the Transport and Location Data Type that define some common
    function between the 2 class
    """

    # This is used to store all the class object that has been created
    database: List[Union[TransportData, LocationData]] = []

    @abstractclassmethod
    def new(self):
        """
        This function is used to create new instance objects by prompting the user to key-in the data
        """
        ...

    @abstractclassmethod
    def print_database(cls):
        """
        This function is used to print out the database in a table-like format
        """
        ...

    def update(self):
        """
        This function is used to update the class object's attributes by
        prompting the user to key-in the data that needs to be edited
        """
        ...

    def to_file(self):
        """
        This function is used to provide a standard format to store each data in the file
        """
        ...

    @classmethod
    def write_to_database(cls, filename):
        """
        Just a simple function to write data into a given file by using the 'to_file()' method of data
        """
        with open(filename, "w") as f:
            for data in cls.database:
                f.write(data.to_file())

    @classmethod
    def handle_data_manipulation(cls, filename: str):
        """
        This function is responsible for all the add/edit/delete that can be done
        to the location's data or the transport's data. It does the selected command
        and then updates the file that stores the data accordingly
        """
        while True:
            cls.print_database()

            cmd = prompt_input(
                "1: add    2: edit    3: delete    4. exit\n",
                "command",
                "Please input either 1, 2, 3 or 4 as the command",
                lambda x: x in ["1", "2", "3", "4"],
            )

            # creates a new data, write it to file and then add it to the database
            if cmd == "1":
                new_data = cls.new()
                with open(filename, "a") as f:
                    f.write(new_data.to_file())
                cls.database.append(new_data)

            elif cmd == "2":
                if len(cls.database) == 0:
                    print_message("nothing to edit")
                    continue

                # get the data to edit using the index given by the user
                index = cls.get_valid_index(msg="element to edit")
                data = cls.database[index - 1]

                # prompt the user to confirm the decision to change the selected data
                if not prompt_user_to_confirm(f"Confirm to edit edit '{data.name}' ?"):
                    continue

                data.update()
                cls.write_to_database(filename)

            elif cmd == "3":
                if len(cls.database) == 0:
                    print_message("nothing to delete")
                    continue

                # prompt and confirms with the user about the index of the data to delete
                index = cls.get_valid_index(msg="data to delete")
                data = cls.database[index - 1]
                if not prompt_user_to_confirm(f"Confirm to delete '{data.name}' ?"):
                    continue

                # remove the deleted data from the database
                cls.database.remove(data)
                cls.write_to_database(filename)

            elif cmd == "4":
                break

    @classmethod
    def get_new_name(cls, skip=False):
        """
        This function prompts the user to give a valid name for the new data that does not exist in the database
        """

        # cls.__name__.removesuffix('Data') is just to get the class's name, which can either be "Location" or "Transport"
        # This is used for clarification when outputting the message to the user
        return prompt_input(
            f"Please input new {cls.__name__.removesuffix('Data')}'s name:  ",
            "name",
            f"Please do not leave the name blank or use the character '{DELIMITER}' in your name of choice",
            lambda x: x not in [i.name for i in cls.database] and x not in (DELIMITER, ""),
            skipable=skip,
        )

    @classmethod
    def get_valid_index(cls, msg: str = ""):
        """
        This function prompts the user to give a valid index of a data that exists in within the database
        """

        return prompt_input(
            f"Please input the index of the {msg}:  ",
            "index",
            "Please input a number that is present in the column 'no' ",
            lambda x: 1 <= x <= len(cls.database),
            func=int,
        )


class TransportData(Data):
    """
    This is the class that stores all transportation data and
    implements methods to update and create new transportation data
    """

    def __init__(self, name: str, speed: float):
        self.name = name
        self.speed = float(speed)

    @classmethod
    def new(cls):
        """
        This function is used to create new instance objects by prompting the user to key-in the data
        """
        return cls(cls.get_new_name(), cls.get_new_speed())

    @classmethod
    def print_database(cls):
        """
        This function is used to print out the database in a table-like format
        """

        # check if there's any data in the database, if not just print 'no data'
        if not TransportData.database:
            print_message(NO_DATA_MSG)
            return

        TransportData.database.sort(key=lambda trans: trans.speed)

        name_list = []
        speed_list = []
        for trans in cls.database:
            name_list.append(f"{trans.name}")
            speed_list.append(f"{trans.speed:>8.2f}")

        print_table(["Transport", "Speed (KM/h)"], name_list, speed_list)

    def to_file(self):
        """
        This is the string representation of the object when it is written into the database (.txt file)
        """
        return f"{self.name}{DELIMITER}{self.speed}\n"

    def update(self):
        """
        This function is used to update the LocationData object's attributes by
        prompting the user to key-in the data that needs to be edited.

        If the user chose to not enter anything (just press enter),
        then the original value will remain unchanged
        """
        self.name = self.get_new_name(skip=True) or self.name
        self.speed = self.get_new_speed(skip=True) or self.speed

    @staticmethod
    def get_new_speed(skip=False):
        """
        Prompts the user to key in the new speed and checks whether it is valid.
        """
        return prompt_input(
            "Please input transport's speed (KM/h): ",
            "speed",
            "Please input a speed that's not negative",
            lambda x: x > 0,
            func=float,
            skipable=skip,
        )


class LocationData(Data):
    """
    This is the class that stores all location's data and
    implements methods to update and create new location's data
    """

    def __init__(self, name: str, latitude, longitude):
        self.name = name
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    @classmethod
    def new(cls):
        """
        This function is used to create new instance objects by prompting the user to key-in the data
        """
        return cls(
            cls.get_new_name(),
            cls.get_new_latitude(),
            cls.get_new_longitude(),
        )

    @classmethod
    def print_database(cls):
        """
        This function is used to print out the database in a table-like format
        """

        # check if there's any data in the database, if not just print 'no data'
        if not LocationData.database:
            print_message(NO_DATA_MSG)
            return

        LocationData.database.sort(key=lambda loc: loc.name)

        # This is looping through all data, and then formatting them and printing out each one
        lon_list = []
        lat_list = []
        name_list = []
        for loc in LocationData.database:
            name_list.append(loc.name)
            if loc.latitude > 0:
                latitude = f"{loc.latitude:>8.4f}  N"
            else:
                # The negative is just to make it positive when it is printed out
                latitude = f"{-loc.latitude:>8.4f}  S"
            lat_list.append(latitude)

            if loc.longitude > 0:
                longitude = f"{loc.longitude:>8.4f}  E"
            else:
                # The negative is just to make it positive when it is printed out
                longitude = f"{-loc.longitude:>8.4f}  W"
            lon_list.append(longitude)

        print_table(["Location", "Latitude", "Longitude"], name_list, lat_list, lon_list)

    def to_file(self):
        """
        This is the string representation of the object when it is written into the database (.txt file)
        """
        return f"{self.name}{DELIMITER}{self.latitude}{DELIMITER}{self.longitude}\n"

    def update(self):
        """
        This function is used to update the LocationData object's attributes by
        prompting the user to key-in the data that needs to be edited.

        If the user chose to not enter anything (just press enter),
        then the original value will remain unchanged
        """
        self.name = self.get_new_name(skip=True) or self.name
        self.latitude = self.get_new_latitude(skip=True) or self.latitude
        self.longitude = self.get_new_longitude(skip=True) or self.longitude

    @staticmethod
    def get_new_latitude(skip=False):
        """
        Prompts the user to key in the new latitude/longitude and checks whether it is valid.
        A valid latitude should be in the form of "101.1202N", the direction can either be
        "N", north or "S" south
        """
        lat_data = prompt_input(
            f"Please input location's latitude (example: 3.1319N) : ",
            "Coordinate (example: 3.1319N)",
            "Please input the latitude of the location, followed by either N(North) or S(South) without any spaces",
            lambda x: x[1] in ["N", "S"],
            func=lambda x: (float(x[:-1]), x[-1]),
            skipable=skip,
        )
        if not lat_data and skip:
            return

        lat, direction = lat_data

        return lat if direction == "N" else -lat

    @staticmethod
    def get_new_longitude(skip=False):
        """
        Prompts the user to key in the new latitude/longitude and checks whether it is valid.
        A valid latitude should be in the form of "101.1202W", the direction can either be
        "W", west or "E" east
        """
        long_data = prompt_input(
            f"Please input location's longitude (example: 101.6841E) : ",
            "Coordinate (example: 101.6841E)",
            "Please input the longitude of the location, followed by either W(West) or E(East) without any spaces",
            checker=lambda x: x[1] in ["W", "E"],
            func=lambda x: (float(x[:-1]), x[-1]),
            skipable=skip,
        )
        if not long_data and skip:
            return

        long, direction = long_data

        return long if direction == "E" else -long
