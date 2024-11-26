
from awesomeUnits.magnitude import MagnitudeVector
from awesomeUnits.unit import Unit
from awesomeUnits.variable import Variable
from awesomeUnits.utils import _derivationFromRepresentation

import numpy as np



class MeasurementSystem:


    def __init__(self, name: str, freedomMagnitudes: list[MagnitudeVector], adimensionalMagnitudes: list[MagnitudeVector]) -> None:
        

        self.name: str = name
        self.freedomMagnitudes: list[MagnitudeVector] = freedomMagnitudes
        self.adimensionalMagnitudes: list[MagnitudeVector] = adimensionalMagnitudes

        self.baseUnits: list[Unit] = []##ONE PER FREEDOM MAGNITUDE
        self.derivedUnits: list[Unit] = []
        self._cachedUnits: list[Unit] = []

        self.constants: dict[str, Variable] = {}###CONSTANTS SUCH AS SPEED OF LIGHT AND STUFF


        self.trueAdimensional: Unit = Unit(self, "1", MagnitudeVector(), None, 1.0)




    def get(self, representation: str, strict: bool = False) -> Unit:
        """Returns or creates the unit with the appropiate representation"""

        for unit in self.baseUnits:
            if unit.representation == representation:
                return unit
            
        for unit in self.derivedUnits:
            if unit.representation == representation:
                return unit
            
        if representation == self.trueAdimensional.representation:
            return self.trueAdimensional
        
        
        ##TODO: CREATE THE UNIT IF NEEDED
        if not strict:
            for unit in self._cachedUnits:
                if unit.representation == representation:
                    return unit

            derivation = _derivationFromRepresentation(representation, self)
            unit = Unit.createComposite(representation, derivation)
            return unit

        raise Exception(f"No unit found for representation {representation}")





    def getEingenvalues(self, magnitudes: MagnitudeVector) -> tuple[list[int], list[int]]:

        dependentVariable = np.array(magnitudes.getAsList())
        coeffMatrix = np.array([mag.getAsList() for mag in self.freedomMagnitudes + self.adimensionalMagnitudes]).T
        sol = np.linalg.solve(coeffMatrix, dependentVariable)

        return [int(x) for x in sol[:len(self.freedomMagnitudes)]], [int(x) for x in sol[len(self.freedomMagnitudes):]]
    


    def getConstantOfMagnitudes(self, magnitudes: MagnitudeVector) -> Variable | None:

        for constant in self.constants.values():
            if constant.unit.magnitudes == magnitudes:
                return constant
        
