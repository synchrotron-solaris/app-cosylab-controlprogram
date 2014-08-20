=====================================
Facility View Application
=====================================


Requirements:
=====================================

-Python 2.6 or greater
-Python modules:
    -PyQt4
    -PyTango
    -taurus
    -csv
    -subprocess
    -argparse
    -threading




Operation:
=====================================

FacilityView application is run by executing FacilityView.py.
Application accepts following arguments:
--CSV path to the CSV file (required)
--GUI path to GUI directory (required)
--TITLE title of the main window (optional)

------------------------------------------------
CSV file must be a file of the following format:
------------------------------------------------
1*(DEVICE_DESCRIPTION), "\n"

DEVICE_DESCRIPTION = ELEMENT_NAME, ",", TYPE, ",", L, ",", S, ",", X, ",", Y, ",", Z, ",", SECTION,
    ",", SUBSYSTEM, ",", MANAGED_IN_CS, ",", DEVICE_SERVER_NAME, ",", DEVICE_SERVER_INSTANCE, ",",
    DEVICE_CLASS, ",", TANGO_DEVICE_NAME, ",", TRIGGERED_BY_TTL, ",", CUSTOM_GUI, ",", AGGREGATE_GUI, ",", DESCRIPTION, ",", COMMENT

AGGREGATE_GUI = AGGREGATE_SYSTEM, "-", "AGGREGATE_PART"
AGGREGATE_SYSTEM = AGGREGATE_SYSTEM_GROUP, 1*("0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9")

---------------------------------------------------
In the GUI directory, following scripts must exist:
---------------------------------------------------

For every different AGGREGATE_SYSTEM_GROUP, a file AGGREGATE_SYSTEM_GROUP.py must exist.
-When opening an aggregate-system GUI, this script is being executed. Following arguments are passed:
    -For every device with the specified AGGREGATE_SYSTEM_GROUP, two arguments are passed:
        1. --AGGREGATE_PART
        2. TANGO_DEVICE_NAME
	-Additional two arguments
		1. --LAB
		2. AGGREGATE_SYSTEM_GROUP
For every device that has a custom gui (CUSTOM_GUI = SCRIPT_NAME), a file SCRIPT_NAME.py must exist.
-When opening a device GUI that has a custom gui, a SCRIPT_NAME.py will be executed. Following argument are passed:
    1. TANGO_DEVICE_NAME

