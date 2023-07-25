from abc import ABC, abstractclassmethod
from .utils import prompt_input


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
    def get_new_name(cls, skip=False):
        """
        This function prompts the user to give a valid name for the new data that does not exist in the database
        """

        # cls.__name__.removesuffix('Data') is just to get the class's name, which can either be "Location" or "Transport"
        # This is used for clarification when outputting the message to the user
        return prompt_input(
            f"Please input new {cls.__name__.removesuffix('Data')}'s name",
            lambda x: x not in [i.name for i in cls.database],
            skip=skip,
        )

    @classmethod
    def get_valid_index(cls, msg: str = ""):
        """
        This function prompts the user to give a valid index of a data that exists in within the database
        """

        return prompt_input(f"Please input the index of the {msg}:  ", lambda x: 1 <= x <= len(cls.database), func=int)


class TransportData(Data):
    database = []

    def __init__(self, name, speed):
        self.name = name
        self.speed = float(speed)

    @classmethod
    def new(cls):
        return cls(cls.get_new_name(), cls.get_new_speed())

    @classmethod
    def print_database(cls):
        for i, vtrans in enumerate(TransportData.database, 1):
            print(f"{i}. {vtrans.name}  |  speed:{vtrans.speed}")

    def to_file(self):
        return f"{self.name},{self.speed}\n"

    def update(self):
        self.name = self.get_new_name(skip=True) or self.name
        self.speed = self.get_new_speed(skip=True) or self.speed

    @staticmethod
    def get_new_speed(skip=False):
        return prompt_input("Please input transport's speed", lambda x: x > 0, func=float, skip=skip)


class LocationData(Data):
    database = []

    def __init__(self, name, latitude, longitude):
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
        for i, vloc in enumerate(LocationData.database, 1):
            print(f"{i}. {vloc.name}  |  latitude:{vloc.latitude}  |  longitude: {vloc.longitude}")

    def to_file(self):
        return f"{self.name},{self.latitude},{self.longitude}\n"

    def update(self):
        self.name = self.get_new_name(skip=True) or self.name
        self.latitude = self.get_new_coordinate("latitude", skip=True) or self.latitude
        self.longitude = self.get_new_coordinate("longitude", skip=True) or self.longitude

    @staticmethod
    def get_new_coordinate(coodinate_type: str, skip=False):
        return prompt_input(f"Please input location's {coodinate_type}", lambda x: 0 <= x <= 180, func=float, skip=skip)
