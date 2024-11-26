from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from awesomeUnits.unit import Unit
    from awesomeUnits.measurementSystem import MeasurementSystem


def _representationFromDerivation(derivation: dict[Unit, int]) -> str:
    """Returns the standard expected string from a derivation"""

    pseudoBaseUnits: list[tuple[Unit, int]] = []

    candidates: list[tuple[Unit, int]] = list(derivation.items())

    while len(candidates) > 0:
        candidate = candidates.pop(0)

        if candidate[0].derivation is None or len(candidate[0].derivation.values()) == 1:
            ##"PSEUDO BASE" UNIT
            pseudoBaseUnits.append(candidate)
        
        else:
            for candidateChildrenUnit, candidateChildrenExponent in candidate[0].derivation.items():
                pseudoBaseUnits.append((candidateChildrenUnit, candidate[1] * candidateChildrenExponent))


    upString = "1"
    downString = ""

    for pseudoBaseUnitTup in pseudoBaseUnits:
        unit, exponent = pseudoBaseUnitTup
        if exponent > 0:
            if upString == "1": upString = ""
        
            if exponent == 1: upString += f"{unit.representation}*"
            else: upString += f"{unit.representation}^{exponent}"
        
        elif exponent < 0:
            if downString == "": downString = "/"
            if exponent == -1: downString += f"{unit.representation}*"
            else: downString += f"{unit.representation}^{-exponent}"

        else: raise Exception()

    return f"{upString.rstrip('*')}{downString.rstrip('*')}"




def _derivationFromRepresentation(representation: str, measurementSystem: MeasurementSystem) -> dict[Unit, int]:
    """Gets the derivation from known units from a representation"""


    if representation.count("/") == 0:
        upString = representation
        downString = ""

    elif representation.count("/") == 1:
        upString = representation.split("/")[0]
        downString = representation.split("/")[1]

    else:
        ##hack:
        upString = representation.split("/")[0]
        downString = representation.split("/")[1]
        #raise Exception()
    
    ##clean up string
    if upString == "1": upString = ""
    

    def consume(string: str) -> dict[Unit, int]:
        if string == "1": return {}

        res = {}

        currentUnit = ""
        currentExp = ""

        mode = "unit"

        for char in string:
            if mode == "unit":
                if char.isalpha(): currentUnit += char
                elif char == "^":
                    mode = "exp"
                elif char == "*" and currentUnit != "":
                    res[measurementSystem.get(currentUnit, strict=True)] = 1
                    currentUnit = ""
                elif char == "*":
                    continue
                else:
                    raise Exception()
            
            elif mode == "exp":
                if char.isnumeric() or char == "-":
                    currentExp += char
                elif char.isalpha() or char == "*":
                    mode = "unit"
                    res[measurementSystem.get(currentUnit, strict=True)] = int(currentExp)
                    currentExp = ""
                    currentUnit = char if char.isalpha() else ""
        
        if currentUnit != "":
            res[measurementSystem.get(currentUnit, strict=True)] = int(currentExp) if currentExp != "" else 1

        return res
    
    upBreakdown = consume(upString)
    downBreakdown = consume(downString)
    for unit in downBreakdown:
        downBreakdown[unit] *= -1

    return _sumDerivations(upBreakdown, downBreakdown)




def _sumDerivations(*derivations: dict[Unit, int]) -> dict[Unit, int]:
    
    total: dict[Unit, int] = {}
    for derivation in derivations:
        for unit, exponent in derivation.items():
            if not unit in total: total[unit] = 0
            total[unit] += exponent
    
    return total