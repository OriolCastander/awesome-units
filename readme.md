## AWESOME UNITS

I am so tired to be writing this right now, just look at thge example to get a grasp of how the thing works. But it should be super useful and stuff.

The measurement systems allow for composite units. I.e. if you divide a distance magnitude by a time magnitude it'll get the units correctly, even if it has not seen them before. For "special" units, like the joule that is equivalent to kg*m^2/s^2 (this last one is understood dynamically), see systems.py

Constants that are used for conversions to systems with adimensional stuff are saved in constants, Check out systems.py for more.

Lots of stuff to do, among them numpy support. Leave a comment and such.

Create a venv and run pip install -r requirements.txt, or simply have numpy available that is the only thing in use.

Better yet, run 'python setup.py bdist_wheel' to build the wheel (will be in dist/) and then run it anywhere you want