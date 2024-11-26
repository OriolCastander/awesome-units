


class Conversion:

    def __init__(self, incomingRepresentation: str, incomingSystem: str, outcomingRepresentation: str, outcomingSystem: str, factor: float) -> None:


        self.incomingRepresentation: str = incomingRepresentation
        self.incomingSystem: str = incomingSystem
        self.outcomingRepresentation: str = outcomingRepresentation
        self.outcomingSystem: str = outcomingSystem
        self.factor: float = factor


    def __repr__(self) -> str:
        return f"{self.incomingRepresentation} ({self.incomingSystem}) -> {self.outcomingRepresentation} ({self.outcomingSystem})"

__CONVERSIONS = [
    Conversion("eV", "international system", "eV", "natural units", 1.0),
    Conversion("yard", "imperial system", "m", "international system", 1.093),
    Conversion("m", "international system", "yard", "imperial system", 1/1.093),
]




def getConversion(representation: str, system: str, isOutcoming: bool = True) -> Conversion | None:

    if not isOutcoming: raise NotImplementedError()

    for conversion in __CONVERSIONS:
        if conversion.outcomingRepresentation == representation and conversion.outcomingSystem == system:
            return conversion