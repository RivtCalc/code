"""Unum units for rivt

    Add new units at end of this file
"""

import os
import importlib.util
from pathlib import Path, PurePath
import unum

# load unum from rivt directory
spec1 = importlib.util.find_spec("rivtcalc")
rivpath = Path(spec1.origin).parent
unum_path = Path(rivpath / 'unum' / '__init__.py')
spec2 = importlib.util.spec_from_file_location("unum", unum_path)
unum = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(unum)
unum.Unum.UNIT_FORMAT = "%s"
unum.Unum.UNIT_INDENT = " "
unum.Unum.VALUE_FORMAT = "%.3f"
unit = unum.Unum.unit

# =============== standard SI units - do not modify ===============
M = unit("m", 0, "meter")
NM = unit("nm", 10**-9 * M, "nanometer")
UM = unit("um", 10**-6 * M, "micrometer")
MM = unit("mm", 10**-3 * M, "millimeter")
CM = unit("cm", 10**-2 * M, "centimeter")
DM = unit("dm", 10**-1 * M, "decimeter")
S = unit("s", 0, "second")
SEC = S
A = unit("A", 0, "ampere")
MA = unit("mA", 10**-3 * A, "milliampere")
K = unit("K", 0, "kelvin")
MOL = unit("mol", 0, "mole")
KG = unit("kg", 0, "kilogram")
GRAM = unit("gram", 10**-3 * KG, "gram")
RAD         = unit( 'rad'   , M / M          , 'radian'   )
SR          = unit( 'sr'    , M**2 / M**2    , 'steradian')
HZ      = unit( 'Hz'    , 1 / S          , 'hertz'      )
N       = unit( 'N'     , M*KG / S**2    , 'newton'     )
J       = unit( 'J'     , N*M            , 'joule'      )
W       = unit( 'W'     , J / S          , 'watt'       )
C       = unit( 'C'     , S * A          , 'coulomb'    )
V       = unit( 'V'     , W / A          , 'volt'       )
F       = unit( 'F'     , C / V          , 'farad'      )
OHM     = unit( 'ohm'   , V / A          , 'ohm'        )
SIEMENS = unit( 'siemens'     , A / V          , 'siemens'    )
WB      = unit( 'Wb'    , V * SIEMENS          , 'weber'      )
T       = unit( 'T'     , WB / M**2      , 'tesla'      )
HENRY   = unit( 'H'     , WB / A         , 'henry'      )
CD      = unit("cd", 0, "candela")
LM      = unit( 'lm'    , CD * SR   , 'lumen'          )
LX      = unit( 'lx'    , LM / M**2 , 'lux'            )
celsius = CELSIUS = unit( 'deg C' , K         , 'degree Celsius' )
FAHR    = unit('degF', K*9./5 , 'degree Fahrenheit')
# ================ do not modify above =================================

# note that temperature conversion is for relative degree size, not offset

# =========== define engineering units below ===========================
# metric------------------------------------------
G   = unit('G', 9.80665 * M/S**2, 'gravity acceleration')
PA  = unit('Pa', N / M**2, 'pascal')
MPA = unit('MPa', PA*(10**6), 'megapascals')
KPA = unit('KPa', PA*(10**3), 'kilopascals')
KN  = unit('KN', N*(10**3), 'kilonewton')
MN  = unit('MN', N*(10**6), 'meganewton')
KM  = unit('M', M*(10**3), 'kilometer')
# imperial---------------------------------------
# length
IN      = unit('in', M / 39.370079, 'inch')
FT      = unit('ft', M / 3.2808399, 'foot')
MILES   = unit('miles', FT * 5280, 'miles')
# mass
LBM     = unit('lbm', KG / 2.2046226, 'pound-mass')
# force
LBF     = unit('lbs', 4.4482216 * N, 'pound-force')
KIPS    = unit('kips', LBF * 1000., 'kilopounds')
KIP     = unit('kip', LBF * 1000., 'kilopound')
# moment
FT_KIPS = unit('ft-kips', FT*LBF*1000., 'foot-kips')
IN_KIPS = unit('in-kips', IN*LBF*1000., 'inch-kips')
# area
SF      = unit('sf', FT**2, 'square feet')
# pressure
PSF     = unit('psf', LBF/FT**2, 'pounds per square foot')
PSI     = unit('psi', LBF/IN**2, 'pounds per square inch')
KSF     = unit('ksf', KIPS/FT**2, 'kips per square foot')
KSI     = unit('ksi', KIPS/IN**2, 'kips per square inch')
# density
PCI     = unit('pci', LBF/IN**3, 'pounds per cubic inch')
PCF     = unit('pcf', LBF/FT**3, 'pounds per cubic ft')
# line loads
KLI     = unit('kips/in', KIPS/IN, 'kips per inch')
PLI     = unit('lbf/in', LBF/IN, 'pounds per inch')
PLF     = unit('lbf/ft', LBF/FT, 'pounds per foot')
KLF     = unit('kips/ft', KIPS/FT, 'kips per foot')
# time
HR      = unit('hr', 60*60*S, 'hours')
# velocity
MPH     = unit('mph', MILES / HR, 'miles per hour')
FPS     = unit('fps', FT / SEC, 'feet per second')