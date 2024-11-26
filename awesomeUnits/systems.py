
from awesomeUnits.measurementSystem import MeasurementSystem
from awesomeUnits.magnitude import MagnitudeVector
from awesomeUnits.unit import Unit
from awesomeUnits.variable import Variable


def initInternationalSystem() -> MeasurementSystem:

    freedomMagnitudes = [
        MagnitudeVector(distance=1),
        MagnitudeVector(time=1),
        MagnitudeVector(mass=1),
        MagnitudeVector(temperature=1),
        MagnitudeVector(current=1)
    ]

    ms = MeasurementSystem("international system", freedomMagnitudes, [])

    ms.baseUnits = [
        Unit.createBase(ms, "m", "distance"),
        Unit.createBase(ms, "s", "time"),
        Unit.createBase(ms, "kg", "mass"),
        Unit.createBase(ms, "K", "temperature"),
        Unit.createBase(ms, "A", "current"),
    ]


    ms.derivedUnits.append(Unit.createFromUnit("km", ms.get("m"), .001))
    ms.derivedUnits.append(Unit.createFromUnit("cm", ms.get("m"), 100))
    ms.derivedUnits.append(Unit.createFromUnit("h", ms.get("s"), 1/3600))


    joule = Unit.createFromUnit("J", "kg*m^2/s^2", 1.0, appendToDerived=True, measuringSystem=ms)
    ev = Unit.createFromUnit("eV", joule,  6.242e18, appendToDerived=True, measuringSystem=ms)
    hertz = Unit.createFromUnit("Hz", "1/s", 1, appendToDerived=True, measuringSystem=ms)
    coulomb = Unit.createFromUnit("C", "A*s", 1.0, appendToDerived=True, measuringSystem=ms)

    ms.constants["speed_of_light"] = Variable(3e8, ms.get("m/s"))
    ms.constants["h_bar"] = Variable(1.06e-34, ms.get("J*s"))
    ms.constants["boltzmann"] = Variable(8.62e-5, ms.get("eV/K"))
    ms.constants["charge"] = Variable(5.28e-19, ms.get("C"))

    return ms




def initCorrectSystem() -> MeasurementSystem:

    freedomMagnitudes = [
        MagnitudeVector(distance=1),
        MagnitudeVector(time=1),
        MagnitudeVector(mass=1),
        MagnitudeVector(temperature=1),
        MagnitudeVector(current=1)
    ]

    ms = MeasurementSystem("imperial system", freedomMagnitudes, [])

    ms.baseUnits = [
        Unit.createBase(ms, "yard", "distance"),
        Unit.createBase(ms, "s", "time"),
        Unit.createBase(ms, "lbs", "mass"),
        Unit.createBase(ms, "K", "temperature"),
        Unit.createBase(ms, "A", "current"),
    ]


    ms.derivedUnits.append(Unit.createFromUnit("m", ms.get("yard"), 1/1760))
    ms.derivedUnits.append(Unit.createFromUnit("'", ms.get("yard"), 3.0))
    ms.derivedUnits.append(Unit.createFromUnit("\"", ms.get("yard"), 36.0))
    ms.derivedUnits.append(Unit.createFromUnit("h", ms.get("s"), 1/3600))


    return ms



def initNaturalUnits() -> MeasurementSystem:

    ###ONLY FREEDOM MAGNITUDE IN HERE IS ENERGY
    freedomMagnitudes = [
        MagnitudeVector(distance=2, mass=1, time=-2),
    ]

    adimensionalMagnitudes = [
        MagnitudeVector(distance=1, time=-1),##speed of light
        MagnitudeVector(distance=2, mass=1, time=-1),##h bar
        MagnitudeVector(distance=2, mass=1, temperature=-1),##boltzmann
        MagnitudeVector(time=1, current=1)##charge
    ]

    ms = MeasurementSystem("natural units", freedomMagnitudes, adimensionalMagnitudes)

    ms.baseUnits.append(Unit(ms, "eV", MagnitudeVector(distance=2, mass=1, time=-2)))

    return ms



def init(name: str = "international system"):
    global _CURRENT_SYSTEM

    if name == "international system":
        _CURRENT_SYSTEM = initInternationalSystem()

    else:
        raise Exception()

