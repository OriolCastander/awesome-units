from __future__ import annotations
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from awesomeUnits.measurementSystem import MeasurementSystem


from awesomeUnits.magnitude import MagnitudeVector



class Unit:

    def __init__(self, measurementSystem: MeasurementSystem, representation: str, magnitudes: MagnitudeVector,
                 derivation: dict["Unit", int] | None = None, factorFromBase: float = 1.0) -> None:
        
        self.measurementSystem: MeasurementSystem = measurementSystem
        self.representation: str = representation
        self.magnitudes: MagnitudeVector = magnitudes
        self.derivation: dict[Unit, int] | None = derivation
        self.factorFromBase: float = factorFromBase



    @staticmethod
    def createBase(measurementSystem: MeasurementSystem, representation: str, magnitude: str) -> "Unit":
        """Creates a fundamental unit to represent a magnitude (i.e, meters (m) in SI)"""

        return Unit(measurementSystem, representation, MagnitudeVector(**{magnitude: 1}), None)
    
    @staticmethod
    def createFromUnit(representation: str, unit: Union["Unit", str], factor: float, appendToDerived: bool = False, measuringSystem: Union["MeasurementSystem",None] = None) -> "Unit":
        """Creates a unit from a existing one, i.e. kilometers from meters"""

        if type(unit) == str:
            if measuringSystem is None:
                import awesomeUnits.systems
                unit = awesomeUnits.systems._CURRENT_SYSTEM.get(unit)
            else:
                unit = measuringSystem.get(unit)

        newUnit = Unit(unit.measurementSystem, representation, unit.magnitudes, {unit: 1}, factor)
        if appendToDerived:
            unit.measurementSystem.derivedUnits.append(newUnit)
        
        return newUnit

    @staticmethod
    def createComposite(representation: str, derivation: dict["Unit", int]) -> "Unit":
        """Create a composite unit. I.e., m/s from meters and seconds"""

        factorFromBase = 1.0
        measurementSystem = None

        magnitudeTally = MagnitudeVector()

        for unit, exponent in derivation.items():
            
            ##magnitude tally
            magnitudeTally = magnitudeTally + (unit.magnitudes * exponent)

            ###factor tally
            factorFromBase *= unit.factorFromBase ** exponent

            ##check consistency in system
            if measurementSystem is None: measurementSystem = unit.measurementSystem
            else:
                if measurementSystem != unit.measurementSystem:
                    raise Exception("")
        
        unit = Unit(measurementSystem, representation, magnitudeTally, derivation, factorFromBase)
        measurementSystem._cachedUnits.append(unit)
        return unit

    

    def __repr__(self) -> str:
        return f"{self.representation}"