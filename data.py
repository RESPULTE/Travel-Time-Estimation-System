from abc import ABC, abstractclassmethod
from utils import *
from typing import List

DATA_MANIPULATION_MENU = "1: add    2: edit    3: delete    4. exit"


class Data(ABC):
    """
    This is a abstract base class for the Transport and Location Data Type that define some common
    function between the 2 class
    """

    # This is used to store all the class object that has been created
    database = []

    @abstractclassmethod
    def new(self):
        ...

    @abstractclassmethod
    def print_database(cls):
        """
        This function is used to print out the database in an orderly manner
        """
        ...

    def update(self):
        """
        This function is used to prompt the user to update the class object's attributes
        """
        ...

    def to_file(self):
        """
        This function is used to provide a standard format to store each data in the file
        """
        ...

    @classmethod
    def handle_data_manipulation(cls, filename: str):
        """
        This function is responsible for all the add/edit/delete that can be done
        to the location's data or the transport's data. It does the selected command
        and then updates the file that stores the data accordingly
        """
        while True:
            cls.print_database()

            cmd = prompt_input(DATA_MANIPULATION_MENU, lambda x: x in ["1", "2", "3", "4", "5"])

            # creates a new data, write it to file and then add it to the database
            if cmd == "1":
                new_data = cls.new()
                with open(filename, "a") as f:
                    f.write(new_data.to_file())
                cls.database.append(new_data)

            elif cmd == "2":
                if len(cls.database) == 0:
                    print("nothing to edit")
                    continue

                # get the data to edit using the index given by the user
                index = cls.get_valid_index(msg="element to edit:   ")
                data = cls.database[index - 1]

                # prompt the user to confirm the decision to change the selected data
                if not prompt_user_to_confirm("edit the selected data:  "):
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
                if len(cls.database) == 0:
                    print("nothing to delete")
                    continue

                # prompt and confirms with the user about the index of the data to delete
                index = cls.get_valid_index(msg="data to delete:    ")
                if not prompt_user_to_confirm("delete the selected data:    "):
                    return

                # remove the deleted data from the database
                data = cls.database.pop(index - 1)

                with open(filename, "r+") as f:
                    loc_data = f.read()
                    # find the deleted data in the file and remove it
                    updated_loc_data = loc_data.replace(data.to_file(), "")
                    f.seek(0)
                    f.write(updated_loc_data)
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
            lambda x: x not in [i.name for i in cls.database] and x != "",
            skip=skip,
        )

    @classmethod
    def get_valid_index(cls, msg: str = ""):
        """
        This function prompts the user to give a valid index of a data that exists in within the database
        """

        return prompt_input(f"Please input the index of the {msg}:  ", lambda x: 1 <= x <= len(cls.database), func=int)


class TransportData(Data):
    database: List["TransportData"] = []

    def __init__(self, name: str, speed: float):
        self.name = name
        self.speed = float(speed)

    @classmethod
    def new(cls):
        return cls(cls.get_new_name(), cls.get_new_speed())

    @classmethod
    def print_database(cls):
        table_len = 5 + 5 + 50 + 15
        print("\n" + "-" * table_len)
        print(f"|{''.center(5)}|{'Name of Transport'.center(50)}|{'Speed'.center(15)}|")
        print("-" * table_len)

        for i, vtrans in enumerate(TransportData.database, 1):
            print(f"|{(str(i) + '.').center(5)}|{vtrans.name.center(50)}|{(str(vtrans.speed) + 'KM/h').center(15)}|")

        print("-" * table_len)

    def to_file(self):
        return f"{self.name},{self.speed}\n"

    def update(self):
        self.name = self.get_new_name(skip=True) or self.name
        self.speed = self.get_new_speed(skip=True) or self.speed

    @staticmethod
    def get_new_speed(skip=False):
        return prompt_input("Please input transport's speed:    ", lambda x: x > 0, func=float, skip=skip)


class LocationData(Data):
    database: List["LocationData"] = []

    def __init__(self, name: str, latitude, longitude):
        self.name = name
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    @classmethod
    def new(cls):
        return cls(
            cls.get_new_name(),
            cls.get_new_coordinate("latitude"),
            cls.get_new_coordinate("longitude"),
        )

    @classmethod
    def print_database(cls):
        table_len = 5 + 5 + 50 + 15 + 15
        print("\n" + "-" * table_len)
        print(f"|{''.center(5)}|{'Name of Location'.center(50)}|{'Latitude'.center(15)}|{'Longitude'.center(15)}|")
        print("-" * table_len)

        for i, vloc in enumerate(LocationData.database, 1):
            print(
                f"|{(str(i) + '.').center(5)}|{vloc.name.center(50)}|{str(vloc.latitude).center(15)}|{str(vloc.longitude).center(15)}|"
            )
        print("-" * table_len)

    def to_file(self):
        return f"{self.name},{self.latitude},{self.longitude}\n"

    def update(self):
        self.name = self.get_new_name(skip=True) or self.name
        self.latitude = self.get_new_coordinate("latitude", skip=True) or self.latitude
        self.longitude = self.get_new_coordinate("longitude", skip=True) or self.longitude

    @staticmethod
    def get_new_coordinate(coodinate_type: str, skip=False):
        return prompt_input(
            f"Please input location's {coodinate_type}: ", lambda x: 0 <= x <= 180, func=float, skip=skip
        )
