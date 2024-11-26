



class MagnitudeVector:

    def __init__(self, distance: int = 0, time: int = 0, mass: int = 0, temperature: int = 0, current: int = 0) -> None:
        
        self.DISTANCE: int = distance
        self.TIME: int = time
        self.MASS: int = mass
        self.TEMPERATURE: int = temperature
        self.CURRENT: int = current


    def __eq__(self, other: "MagnitudeVector") -> bool:
        
        if not isinstance(other, MagnitudeVector):
            raise Exception()
        
        for key, value in self.__dict__.items():
            if value != other.__dict__[key]: return False
        
        return True
    

    def __add__(self, other: "MagnitudeVector") -> "MagnitudeVector":
        
        if not isinstance(other, MagnitudeVector):
            raise Exception()
        
        tally = {}
        for key in self.__dict__:
            tally[key.lower()] = self.__dict__[key] + other.__dict__[key]

        return MagnitudeVector(**tally)
    

    def __mul__(self, other: int) -> "MagnitudeVector":

        if not isinstance(other, int):
            raise Exception()
        
        tally = {}
        for key in self.__dict__:
            tally[key.lower()] = self.__dict__[key] * other

        return MagnitudeVector(**tally)
    

    def getAsList(self) -> list[int]:

        return [self.DISTANCE, self.TIME, self.MASS, self.TEMPERATURE, self.CURRENT]


    def __repr__(self) -> str:
        string = f""
        for key, value in self.__dict__.items():
            string += f"{key}: {value} "

        return string