from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from awesomeUnits.unit import Unit
    from awesomeUnits.measurementSystem import MeasurementSystem
    from awesomeUnits.magnitude import MagnitudeVector

from awesomeUnits.conversions import __CONVERSIONS, Conversion, getConversion
from awesomeUnits.utils import _representationFromDerivation

import decimal



class Variable:
    

    def __init__(self, value: float, unit: Unit) -> None:

        if type(unit) == str:
            import awesomeUnits.systems
            unit = awesomeUnits.systems._CURRENT_SYSTEM.get(unit)

        self.value: float = value
        self.unit: Unit = unit


    def __repr__(self) -> str:
        return f"{decimal.Decimal(self.value):.3E} {self.unit}"
    
    
    
    def convertTo(self, unit: Unit | str, inplace: bool = False) -> "Variable":
        """Converts to the specified unit. Inplace if specified"""

        if type(unit) == str:
            unit = self.unit.measurementSystem.get(unit)

        ##TODO: ASSERT EQUIVALENCE
        
        factor = unit.factorFromBase / self.unit.factorFromBase

        if inplace:
            self.value *= factor
            self.unit = unit
            return self
        
        else:
            return Variable(self.value * factor, unit)

    def __add__(self, other: "Variable") -> "Variable":

        if type(other) != Variable:
            raise Exception(f"{other} must be a variable")
        
        ##TODO: ASSERT SAME SYSTEM

        ##TODO: ASSERT EQUIVALENCE
        
        other = other.convertTo(self.unit)

        return Variable(self.value + other.value, self.unit)
    

    def __sub__(self, other: "Variable") -> "Variable":

        other = Variable(-other.value, other.unit)
        return self + other
    


    def __mul__(self, other: "Variable") -> "Variable":

        if type(other) == Variable:
            
            ##TODO: ASSET MEASUREMENT SYSTEM
            derivation = {self.unit: 2} if self.unit == other.unit else {self.unit: 1, other.unit: 1}
            representation = _representationFromDerivation(derivation)
            resultingUnit = self.unit.measurementSystem.get(representation)
            return Variable(self.value * other.value, resultingUnit)
        
        elif isinstance(other, (float, int)):
            return self * Variable(other, "1")
    

    def __truediv__(self, other: "Variable") -> "Variable":
        
        if type(other) == Variable:
            
            ##TODO: ASSET MEASUREMENT SYSTEM
            derivation = {} if self.unit == other.unit else {self.unit: 1, other.unit: -1}
            representation = _representationFromDerivation(derivation)
            resultingUnit = self.unit.measurementSystem.get(representation)
            return Variable(self.value / other.value, resultingUnit)
        
        elif isinstance(other, (float, int)):
            return self / Variable(other, "1")
        
    

    def __rtruediv__(self, other: float | int) -> "Variable":

        if not isinstance(other, (int, float)):
            raise NotImplementedError()
        
        derivation = {self.unit: -1}
        representation = _representationFromDerivation(derivation)
        resultingUnit = self.unit.measurementSystem.get(representation)

        return Variable(1 / self.value, resultingUnit)


    def toSystem(self, measurementSystem: MeasurementSystem) -> "Variable":

        eigenvaluesFreedom, eigenvaluesAdimensionals = measurementSystem.getEingenvalues(self.unit.magnitudes)

        #print(f"eigen {eigenvaluesFreedom}, {eigenvaluesAdimensionals}")

        factor = 1.0
        derivation: dict[Unit, int] = {}

        for i, exponent in enumerate(eigenvaluesFreedom):
            if exponent == 0: continue
            conversion = getConversion(measurementSystem.baseUnits[i].representation, measurementSystem.name)
            

            ###TODO: MAKE THIS FLEXIBLE SO THAT WE CAN CONVERT FROM UNITS NOT STRICTLY IN THE CONVERSION
            if conversion.incomingRepresentation != self.unit.representation or conversion.incomingSystem != self.unit.measurementSystem.name:
                factor *= self.unit.measurementSystem.get(conversion.incomingRepresentation).factorFromBase
            
            factor *= conversion.factor ** exponent

            derivation[measurementSystem.get(conversion.outcomingRepresentation)] = exponent



        for i, exponent in enumerate(eigenvaluesAdimensionals):
            if exponent == 0: continue

            constant = self.unit.measurementSystem.getConstantOfMagnitudes(measurementSystem.adimensionalMagnitudes[i])
            if constant is None: raise Exception()

            factor *= constant.value ** exponent


        return Variable(self.value / factor, measurementSystem.get(_representationFromDerivation(derivation)))