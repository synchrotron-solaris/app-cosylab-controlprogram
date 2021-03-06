"""CsvManager.py: File containing a class for managing specific data that is read from a CSV file and structured
into multiple data structures. The file also contains various classes that are a part of the data structures.
CsvManager also updates the state of every device from the CSV file."""

import csv
import taurus
from PyTango import DevState, DevFailed
from taurus.core import TaurusListener
from cosywidgets.panel import TaurusDevicePanel
from PyQt4 import Qt, QtGui, QtCore
import subprocess, os, threading, time, copy, sys, re

__author__ = "Cosylab"


DEFAULT_POLLING_PERIOD = 1000
STATE_CHECK_PERIOD_S = 10
STATE_CHECK_DIFF_S = 10



class CsvManager():
    """Manager CLass, that manages data acquired from the CSV file."""


    # The following constants define the properties containing the columns from CSV
    #------------------------------------------------------------------------------
    CONST_PROPERTY_ELEMENT_NAME = "import_element_name"
    CONST_PROPERTY_TYPE = "import_type"
    CONST_PROPERTY_L = "import_l"
    CONST_PROPERTY_S = "import_s"
    CONST_PROPERTY_X = "import_x"
    CONST_PROPERTY_Y = "import_y"
    CONST_PROPERTY_Z = "import_z"
    CONST_PROPERTY_SECTION = "import_section"
    CONST_PROPERTY_SUBSYSTEM = "import_subsystem"
    CONST_PROPERTY_MANAGED_BY_CS = "import_managed_cs"
    CONST_PROPERTY_EXECUTABLE = "import_executable"
    CONST_PROPERTY_INSTANCE_NAME = "import_instance_name"
    CONST_PROPERTY_DS_CLASS_NAME = "import_ds_class_name"
    CONST_PROPERTY_TANGO_DEVICE_NAME = "import_tango_device_name"
    CONST_PROPERTY_DEVICE_ALIAS = "import_device_alias"
    CONST_PROPERTY_TRIGGERED_BY_TTL = "import_triggered_by_ttl"
    CONST_PROPERTY_CUSTOM_GUI = "import_custom_gui"
    CONST_PROPERTY_AGGREGATE_GUI = "import_aggregate_gui"
    CONST_PROPERTY_COMMENT = "import_comment"
    CONST_PROPERTY_TEST_UNITS = "import_test_units"
    CONST_PROPERTY_DEPENDS_ON_TTL = "depends_on_ttl"
    CONST_PROPERTY_DESCRIPTION = "device description"

    # Order of the properties in the CSV file
    #----------------------------------------
    CONST_CSV_COLUMNS = [
        CONST_PROPERTY_ELEMENT_NAME,
        CONST_PROPERTY_TYPE,
        CONST_PROPERTY_L,
        CONST_PROPERTY_S,
        CONST_PROPERTY_X,
        CONST_PROPERTY_Y,
        CONST_PROPERTY_Z,
        CONST_PROPERTY_SECTION,
        CONST_PROPERTY_SUBSYSTEM,
        CONST_PROPERTY_MANAGED_BY_CS,
        CONST_PROPERTY_EXECUTABLE,
        CONST_PROPERTY_INSTANCE_NAME,
        CONST_PROPERTY_DS_CLASS_NAME,
        CONST_PROPERTY_TANGO_DEVICE_NAME,
        CONST_PROPERTY_DEVICE_ALIAS,
        CONST_PROPERTY_TRIGGERED_BY_TTL,
        CONST_PROPERTY_CUSTOM_GUI,
        CONST_PROPERTY_AGGREGATE_GUI,
        CONST_PROPERTY_DESCRIPTION,
        CONST_PROPERTY_COMMENT
    ]

    # List of columns that don't need to be imported as properties because they
    #  are already present in the Tango database
    #--------------------------------------------------------------------------
    CONST_DONT_IMPORT_CSV_COLUMNS = [
        CONST_PROPERTY_MANAGED_BY_CS,
        CONST_PROPERTY_EXECUTABLE,
        CONST_PROPERTY_INSTANCE_NAME,
        CONST_PROPERTY_DS_CLASS_NAME,
        CONST_PROPERTY_TANGO_DEVICE_NAME,
    ]

    # Specifies which property prefix identify a Timing dependency
    #-------------------------------------------------------------
    CONST_TTL_PREFIX = 'TTL-'



    csv_file_path = None
    gcsv_file_path = None
    gui_dir_path = None
    csvSections = {}
    csvDevices = {}
    csvAggSystems = {}
    csvSectionNames = []
    csvSubsystemNames = []
    csvClassNames = []
    groupConfiguration = {}

    stateThread = None
    stateThreadAlive = None
    stateThreadAliveMutex = None

    def __init__(self, csv, gcsv, guiDir, ui, create_log_file=False):
        self.gui_dir_path = guiDir
        self.csv_file_path = csv
        self.gcsv_file_path = gcsv
        self._create_log_file = create_log_file
        self.initialize(ui)


    def getCsvDevices(self):
        """Getter for CsvDevice instances."""
        return self.csvDevices.values()

    def getCsvDevice(self, device_name):
        """Getter for a CsvDevice instance with a specified name.
        :param device_name: name of the device"""
        if device_name in self.csvDevices.keys():
            return self.csvDevices[device_name]
        return None

    def getCsvDeviceNames(self):
        """Getter for CsvDevice names."""
        return self.csvDevices.keys()

    def getCsvSections(self):
        """Getter for CsvSection instances."""
        return self.csvSections

    def getCsvAggSystems(self):
        """Getter for CsvAggSystem instances."""
        return self.csvAggSystems

    def getCsvAggSystem(self, agg_name):
        """Getter for a CsvAggSystem instance with a specified name.
        :param agg_name: name of the aggregate"""
        if agg_name in self.csvAggSystems.keys():
            return self.csvAggSystems[agg_name]
        return None

    def getCsvSectionNames(self):
        """Getter for CsvSection names."""
        return self.csvSectionNames

    def getCsvSubsystemNames(self):
        """Getter for CsvSubsystem names."""
        return self.csvSubsystemNames

    def getCsvClassNames(self):
        """Getter for CsvClass names."""
        return self.csvClassNames

    def getAttributeNames(self):
        """Returns attribute names of all CsvDevices."""
        attributeNames = []
        for csvDevice in self.csvDevices.values():
            attributeNames = attributeNames + list(set(csvDevice.getAttributesNames()) - set(attributeNames))
        return attributeNames

    def getDeviceNamesGuiOn(self):
        """Returns names of all CsvDevice instances that have their GUIs opened."""
        csvDeviceNames = []
        for csvDevice in self.csvDevices.values():
            if csvDevice.isGuiRunning():
                csvDeviceNames.append(csvDevice.getDeviceName())
        return csvDeviceNames

    def getAggSystemNamesGuiOn(self):
        """Returns names of all CsvAggSystem instances that have their GUIs opened."""
        csvAggSystemNames = []
        for csvAggSystem in self.csvAggSystems.values():
            if csvAggSystem.isGuiRunning():
                csvAggSystemNames.append(csvAggSystem.agg_system_name)
        return csvAggSystemNames




    def initialize(self, ui):
        """Method reads from the given CSV file and initializes all data structures."""

        # Precalculate the indexes of the CSV columns
        #--------------------------------------------
        indexCustomGui = self.CONST_CSV_COLUMNS.index(self.CONST_PROPERTY_CUSTOM_GUI)
        indexAggregate = self.CONST_CSV_COLUMNS.index(self.CONST_PROPERTY_AGGREGATE_GUI)
        indexSection = self.CONST_CSV_COLUMNS.index(self.CONST_PROPERTY_SECTION)
        indexSubsystem = self.CONST_CSV_COLUMNS.index(self.CONST_PROPERTY_SUBSYSTEM)
        indexTangoDeviceName = self.CONST_CSV_COLUMNS.index(self.CONST_PROPERTY_TANGO_DEVICE_NAME)
        indexDeviceAlias = self.CONST_CSV_COLUMNS.index(self.CONST_PROPERTY_DEVICE_ALIAS)
        indexExecutable = self.CONST_CSV_COLUMNS.index(self.CONST_PROPERTY_EXECUTABLE)
        indexInstanceName = self.CONST_CSV_COLUMNS.index(self.CONST_PROPERTY_INSTANCE_NAME)
        indexDSClassName = self.CONST_CSV_COLUMNS.index(self.CONST_PROPERTY_DS_CLASS_NAME)
        indexDescription = self.CONST_CSV_COLUMNS.index(self.CONST_PROPERTY_DESCRIPTION)
        indexManagedByCS = self.CONST_CSV_COLUMNS.index(self.CONST_PROPERTY_MANAGED_BY_CS)


        # Group GUI configuration
        if self.gcsv_file_path:
            with open(self.gcsv_file_path, 'rb') as gcsvFile:
                #dialect = csv.Sniffer().sniff(gcsvFile.read(4096), "\t,;")
                #gcsvFile.seek(0)
                csvReader = csv.reader(gcsvFile, delimiter=";", quotechar='"')
                counter = 1
                for row in csvReader:
                    if len(row) == 4 and not row[0].startswith("#"):
                        data = row[1:]
                        data.append(counter)
                        print data
                        self.groupConfiguration[row[0]] = data
                        counter += 1


        rowCounter = 0
        with open(self.csv_file_path, 'rb') as csvFile:
            dialect = csv.Sniffer().sniff(csvFile.read(4096), "\t,;")
            csvFile.seek(0)
            csvReader = csv.reader(csvFile, dialect)

            for row in csvReader:
                rowCounter += 1

                # If the row does not contain valid data then skip it
                #----------------------------------------------------
                if len(row) < len(self.CONST_CSV_COLUMNS):
                    print "Skipped row " + str(rowCounter) + " because it contains too little columns"
                    continue

                if row[0].startswith("#"):
                    print "Skipped row " + str(rowCounter) + " because it is commented out"
                    continue

                tangoDeviceNameParts = row[indexTangoDeviceName].split('/')
                if len(tangoDeviceNameParts) < 3:
                    print "Skipped row " + str(rowCounter) + " because the device name is in the wrong format (device name = " + row[indexTangoDeviceName] + ")"
                    continue

                if not row[indexExecutable] or not row[indexInstanceName] or not row[indexDSClassName]:
                    print "Skipped row " + str(rowCounter) + " because one of the column is empty (executable name, instance name, class name)"
                    continue

                if not row[indexSection] or not row[indexSubsystem]:
                    print "Skipped row " + str(rowCounter) + " because one of the column is empty (section name, subsystem name)"
                    continue

                if row[indexManagedByCS] != "Y":
                    print "Skipped row " + str(rowCounter) + " because the device is not managed by ControlProgram"
                    continue





                multiAgg = row[indexAggregate].split("|")
                if len(multiAgg) > 1:

                    if row[indexTangoDeviceName] in self.csvDevices.keys():
                        # PROCESS MOCK DEVICE
                        self.processMockDevice(row[indexTangoDeviceName], multiAgg[0])
                        continue

                    else:
                        # PROCESS DEVICE
                        print "Processing device " + row[indexTangoDeviceName] + " ************"
                        self.processDevice(ui, rowCounter, row[indexTangoDeviceName], row[indexExecutable],
                                              row[indexInstanceName], row[indexDSClassName],
                                              row[indexSubsystem], row[indexSection], multiAgg[0],
                                              row[indexCustomGui], self.gui_dir_path, row[indexDeviceAlias],
                                              row[indexDescription],
                                              self._create_log_file)

                    for i in range(1,len(multiAgg)):
                        # PROCESS MOCK DEVICE
                        self.processMockDevice(row[indexTangoDeviceName], multiAgg[i], row[indexDescription])





                else:
                    if row[indexTangoDeviceName] in self.csvDevices.keys():
                        # PROCESS MOCK DEVICE
                        self.processMockDevice(row[indexTangoDeviceName], row[indexAggregate], row[indexDescription])
                    else:
                        # PROCESS DEVICE
                        print "Processing device " + row[indexTangoDeviceName] + " ************"
                        self.processDevice(ui, rowCounter, row[indexTangoDeviceName], row[indexExecutable],
                                              row[indexInstanceName], row[indexDSClassName],
                                              row[indexSubsystem], row[indexSection], row[indexAggregate],
                                              row[indexCustomGui], self.gui_dir_path, row[indexDeviceAlias],
                                              row[indexDescription],
                                              self._create_log_file)


        for key in self.groupConfiguration.keys():
            if key in self.csvAggSystems:
                nextAggs = []
                for nextAggKey in self.groupConfiguration[key][1].split("|"):
                    if nextAggKey in self.csvAggSystems.keys():
                        nextAggs.append(self.csvAggSystems[nextAggKey])
                self.csvAggSystems[key].nextAggs = nextAggs

                prevAggs = []
                for prevAggKey in self.groupConfiguration[key][0].split("|"):
                    if prevAggKey in self.csvAggSystems.keys():
                        prevAggs.append(self.csvAggSystems[prevAggKey])
                self.csvAggSystems[key].prevAggs = prevAggs

                self.csvAggSystems[key].additional_arg = self.groupConfiguration[key][2]
                self.csvAggSystems[key].order_index = self.groupConfiguration[key][3]


    def startStateThread(self):
        self.stateThreadAliveMutex = threading.Lock()
        self.stateThreadAlive = True
        self.stateThread = threading.Thread(target=self.StateCheckerRun)
        self.stateThread.start()


    def processDevice(self, mainUi, order_index, device_name, server_name, instance_name, class_name, subsystem_name, section_name, agg_name, custom_gui, gui_dir, device_alias, description, create_log_file):
        csvDevice = CsvDevice(mainUi, order_index, device_name, server_name, instance_name, class_name, subsystem_name, section_name, agg_name, custom_gui, gui_dir, device_alias, description, create_log_file)
        self.csvDevices[device_name] = csvDevice

        #Create csv AggSystem data model
        #
        #AggSystem
        #   |
        #   -> Device
        #------------------------------------------------
        if csvDevice.has_agg:
            if not csvDevice.agg_system_name in self.csvAggSystems.keys():
                newCsvAggSystem = CsvAggSystem(csvDevice.agg_system_name, self.gui_dir_path, self)
                self.csvAggSystems[csvDevice.agg_system_name] = newCsvAggSystem

                agg_num = re.search(r'\d+$', csvDevice.agg_system_name)

                if agg_num:
                    agg_num = int(agg_num.group())
                    if agg_num == 10:
                        prev_agg_name = csvDevice.agg_system_name.replace(str(agg_num), "0" + str(agg_num-1))
                    else:
                        prev_agg_name = csvDevice.agg_system_name.replace(str(agg_num), str(agg_num-1))
                    if agg_num == 9:
                        next_agg_name = csvDevice.agg_system_name.replace("0" + str(agg_num), str(agg_num+1))
                    else:
                        next_agg_name = csvDevice.agg_system_name.replace(str(agg_num), str(agg_num+1))

                    if prev_agg_name in self.csvAggSystems.keys():
                        self.csvAggSystems[prev_agg_name].nextAggs = [newCsvAggSystem]
                        newCsvAggSystem.prevAggs = [self.csvAggSystems[prev_agg_name]]
                    if next_agg_name in self.csvAggSystems.keys():
                        self.csvAggSystems[next_agg_name].prevAggs = [newCsvAggSystem]
                        newCsvAggSystem.nextAggs = [self.csvAggSystems[next_agg_name]]
            self.csvAggSystems[csvDevice.agg_system_name].appendCsvDevice(csvDevice)


        #Create csv Device data model
        #
        #Section
        #   |
        #   -> Subsystem
        #       |
        #       -> Device
        #------------------------------------------------
        if not csvDevice.getSectionName() in self.csvSections.keys():
            self.csvSections[csvDevice.getSectionName()] = CsvSection(csvDevice.getSectionName())
            self.csvSectionNames.append(csvDevice.getSectionName())
        self.csvSections[csvDevice.getSectionName()].appendCsvDevice(csvDevice)


        if not csvDevice.getSubsystemName() in self.csvSubsystemNames:
            self.csvSubsystemNames.append(csvDevice.getSubsystemName())
        if not csvDevice.getClassName() in self.csvClassNames:
            self.csvClassNames.append(csvDevice.getClassName())


    def processMockDevice(self, device_name, aggregate_gui, description):
        csvDevice = MockCsvDevice(device_name, aggregate_gui, description)
        if csvDevice.has_agg:
            if not csvDevice.agg_system_name in self.csvAggSystems.keys():
                newCsvAggSystem = CsvAggSystem(csvDevice.agg_system_name, self.gui_dir_path, self)
                self.csvAggSystems[csvDevice.agg_system_name] = newCsvAggSystem

                agg_num = re.search(r'\d+$', csvDevice.agg_system_name)
                if agg_num:
                    agg_num = int(agg_num.group())
                    prev_agg_name = csvDevice.agg_system_name.replace(str(agg_num), str(agg_num-1))
                    next_agg_name = csvDevice.agg_system_name.replace(str(agg_num), str(agg_num+1))

                    if prev_agg_name in self.csvAggSystems.keys():
                        self.csvAggSystems[prev_agg_name].nextAggs = [newCsvAggSystem]
                        newCsvAggSystem.prevAggs = [self.csvAggSystems[prev_agg_name]]
                    if next_agg_name in self.csvAggSystems.keys():
                        self.csvAggSystems[next_agg_name].prevAggs = [newCsvAggSystem]
                        newCsvAggSystem.nextAggs = [self.csvAggSystems[next_agg_name]]

            self.csvAggSystems[csvDevice.agg_system_name].appendCsvDevice(csvDevice)



    def StateCheckerRun(self):
        """Target of a StateChecker thread, used for updating the state of every device that was not updated for
        a significant amount of time."""
        alive = True
        while alive:
            for device in self.csvDevices.values():
                if (time.time() - device.state_time_stamp) > STATE_CHECK_DIFF_S:
                    device.pollState()

            for i in range(0,STATE_CHECK_PERIOD_S):
                self.stateThreadAliveMutex.acquire()
                alive = copy.copy(self.stateThreadAlive)
                self.stateThreadAliveMutex.release()
                if not alive:
                    break
                time.sleep(1)

            self.stateThreadAliveMutex.acquire()
            alive = copy.copy(self.stateThreadAlive)
            self.stateThreadAliveMutex.release()






    def printInfo(self):
        """Print Info - structure of the data models"""
        for csvSection in self.csvSections.values():
            csvSection.printInfo()
        for csvAggSystem in self.csvAggSystems.values():
            csvAggSystem.printInfo()

    def destroy(self):
        """Destructor of the CsvManager class. Must be called before the application is closed.
        It unsubscribes the devices from all events."""
        if self.stateThread:
            self.stateThreadAliveMutex.acquire()
            self.stateThreadAlive = False
            self.stateThreadAliveMutex.release()

        for device in self.csvDevices.values():
            device.destroy()

        if self.stateThread:
            self.stateThread.join()

        print "END"



class CsvDevice():
    """Node, representing Tango Device, used as a node in multiple data structures as the most bottom node."""
    order_index = None

    device_name = None
    server_name = None
    instance_name = None
    class_name = None
    subsystem_name = None
    section_name = None

    domain_name = None
    family_name = None
    member_name = None

    has_agg = None
    agg_name = None
    agg_system_name = None
    agg_instance_name = None

    display_name = None

    custom_gui_script = None
    gui_dir = None
    default_gui = None
    custom_gui = None

    state = None
    stateMutex = None

    description = None

    state_listener = None
    state_attribute = None

    state_time_stamp = None

    mainUi = None

    taurus_device = None


    def __init__(self, mainUi, order_index, device_name, server_name, instance_name, class_name, subsystem_name, section_name, agg_name, custom_gui, gui_dir, device_alias, description, create_log_file=False):
        self.order_index = order_index
        self.device_name = device_name
        self.server_name = server_name
        self.instance_name = instance_name
        self.class_name = class_name
        self.subsystem_name = subsystem_name
        self.section_name = section_name
        self.description = description
        self.mainUi = mainUi
        self._create_log_file = create_log_file

        split = self.device_name.split("/")
        self.domain_name = split[0]
        self.family_name = split[1]
        self.member_name = split[2]


        agg_split = agg_name.split("-", 1)
        if len(agg_split) == 2:
            self.has_agg = True
            self.agg_name = agg_name
            self.agg_system_name = agg_split[0]
            self.agg_instance_name = agg_split[1]
        else:
            self.has_agg = False

        if device_alias:
            self.display_name = device_alias
        else:
            self.display_name = self.device_name

        self.custom_gui_script = custom_gui
        self.gui_dir = gui_dir

        real_gui_dir = os.path.realpath(os.path.abspath(self.gui_dir))
        if real_gui_dir not in sys.path:
            sys.path.insert(0, real_gui_dir)

        self.stateMutex = threading.Lock()
        self.state_time_stamp = time.time()


    def subscribeState(self):

        if self.state_listener:
            return

        try:
            self.state_attribute = taurus.core.TaurusManager().getAttribute(self.device_name + "/State")
            self.state_attribute.activatePolling(DEFAULT_POLLING_PERIOD)
            self.state_listener = StateAttributeHandler(self.device_name + "/State", self)
            self.state_attribute.addListener(self.state_listener)
        except:
            self.setState(DevState.UNKNOWN)



    def destroy(self):
        """Unsubscribes the subscribed events."""
        return

    def printInfo(self):
        """Prints information of the device in the console"""
        print "    -------DEVICE-----------"
        print "    ", self.device_name, self.server_name, self.instance_name, self.class_name
        print "    ", self.subsystem_name, self.section_name
        print "    ", self.agg_name, self.agg_system_name, self.agg_instance_name

    def getDeviceName(self):
        """Getter for device name."""
        return self.device_name

    def getServerName(self):
        """Getter for server name."""
        return self.server_name

    def getInstanceName(self):
        """Getter for instance name."""
        return self.instance_name

    def getClassName(self):
        """Getter for class name."""
        return self.class_name

    def getSubsystemName(self):
        """Getter for subsystem name."""
        return self.subsystem_name

    def getSectionName(self):
        """Getter for section name."""
        return self.section_name

    def getDomainName(self):
        """Getter for domain name."""
        return self.domain_name

    def getFamilyName(self):
        """Getter for family name."""
        return self.family_name

    def getMemberName(self):
        """Getter for member name."""
        return self.member_name

    def member(self):
        """Getter for display name."""
        return self.display_name

    def getDescription(self):
        """Getter for device description"""
        return self.description

    def pollState(self):
        """Tries to acquire the state of the device by polling.
        If successful, the state attribute will be set to a new value.
        If not successful, the state attribute will be set to UNKNOWN."""
        #print "POLLING ", self.device_name
        try:
            if self.state_attribute:
                state = self.state_attribute.read().value
                self.setState(state)
        except DevFailed:
            self.setState(DevState.UNKNOWN)

    def getState(self):
        """Getter for device state attribute.
        State attribute is multi-thread proof."""
        self.stateMutex.acquire()
        ret = copy.copy(self.state)
        self.stateMutex.release()
        return ret

    def setState(self, state):
        """Sets the state attribute to a new value.
        The time stamp, used for holding the time of the last state update, is set.
        State attribute is multi-thread proof."""

        if self.state == state:
            self.state_time_stamp = time.time()
            return

        self.stateMutex.acquire()
        self.state = state
        self.state_time_stamp = time.time()
        self.stateMutex.release()
        self.mainUi.refreshRow()

    def getAttributesNames(self):
        """Returns names of all attributes of this device.
        If the device is not accessible, it returns an empty list."""
        attributeNames = []
        try:
            if not self.taurus_device:
                self.taurus_device = taurus.core.TaurusManager().getDevice(self.device_name)

            attributeInfos = self.taurus_device.attribute_list_query()
            for attributeInfo in attributeInfos:
                attributeNames.append(attributeInfo.name)
                #print attributeInfo
        except DevFailed:
            self.taurus_device = None
            return []
        return attributeNames

    def getAttributeInfo(self, att_name):
        """Returns information about attribute of this device with a specified name.
        If the device is not accessible or the attribute does not exist, it returns None.
        :param att_name: attribute name"""
        try:
            if not self.taurus_device:
                self.taurus_device = taurus.core.TaurusManager().getDevice(self.device_name)

            attributeInfos = self.taurus_device.attribute_list_query()
            for attributeInfo in attributeInfos:
                if attributeInfo.name == att_name:
                    return attributeInfo
            return None
        except DevFailed:
            self.taurus_device = None
            return None

    def runGUI(self):
        """Method for running a GUI of this device.
        Returns a success code:
        0  - GUI already running
        1  - Default GUI success
        2  - Custom GUI success
        -1 - Device not accessible/responsive
        -2 - Custom GUI script not found
        -3 - Error whilst running script"""
        if self.isGuiRunning():
            if self.default_gui:
                try:
                    self.default_gui.raise_()
                    self.default_gui.activateWindow()
                except:
                    pass
            elif isinstance(self.custom_gui, QtGui.QDialog):
                try:
                    self.custom_gui.raise_()
                    self.custom_gui.activateWindow()
                except:
                    pass
            return 0
        if not self.isDeviceAccessible():
            return -1
        if not self.isDeviceResponsive():
            return -1
        if self.custom_gui_script:
            return self._runCustomGui()
        else:
            return self._runDefaultGui()

    def _runDefaultGui(self):
        self.default_gui = QtGui.QDialog()
        self.default_gui.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        taurus_panel = TaurusDevicePanel()
        taurus_panel.setModel(self.device_name)
        self.default_gui.setLayout(Qt.QVBoxLayout())
        self.default_gui.layout().addWidget(taurus_panel)
        self.default_gui.setWindowTitle(self.device_name)
        self.default_gui.setResult(2)
        self.default_gui.show()
        return 1

    def _runCustomGui(self):
        file_path = self.gui_dir + "/" + self.custom_gui_script + ".py"
        if not os.path.isfile(file_path):
            return -2


        try:
            command_module = __import__(self.custom_gui_script)
            if not hasattr(command_module, "getGuiWidget"):
                redirect_output = (" &> ~/.ControlProgram/%s.log" % self.custom_gui_script) if self._create_log_file else ""
                self.custom_gui = subprocess.Popen("python2.7 %s %s %s" % (file_path, self.device_name, redirect_output), shell=True)
                return 2

            self.custom_gui = command_module.getGuiWidget([self.device_name])
            if self.custom_gui is None:
                return 2
            self.custom_gui.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
            self.custom_gui.setResult(2)
            self.custom_gui.show()
            return 2
        except ImportError:
            return -3
        except OSError:
            return -3


    def isGuiRunning(self):
        """Method returns True, if a GUI of this device is running, False otherwise."""
        if self.custom_gui_script:
            if self.custom_gui:
                if isinstance(self.custom_gui, QtGui.QDialog):
                    if self.custom_gui.result() == 2:
                        return True
                elif self.custom_gui.poll() is None:
                    return True
            return False
        else:
            if self.default_gui:
                if self.default_gui.result() == 2:
                    return True
            return False

    def getGuiPos(self):
        if self.custom_gui_script:
            return [0,0]
        else:
            if self.default_gui:
                return [self.default_gui.pos().x(), self.default_gui.pos().y()]
            else:
                return [0,0]

    def setGuiPos(self, x,y):
        if self.custom_gui_script:
            return
        else:
            if self.default_gui:
                self.default_gui.move(x,y)
            else:
                return


    def isDeviceAccessible(self):
        """Method checks, if the device is accessible.
        Returns True if so, False otherwise."""
        try:
            if not self.taurus_device:
                self.taurus_device = taurus.core.TaurusManager().getDevice(self.device_name)

            self.taurus_device.ping()
            return True
        except DevFailed:
            self.taurus_device = None
            return False

    def isDeviceResponsive(self):
        """Method checks, if the device is responsive.
        Returns True if so, False otherwise."""
        try:
            state_attribute = taurus.core.TaurusManager().getAttribute(self.device_name + "/State")
            state_attribute.read()
            return True
        except DevFailed:
            return False


class MockCsvDevice(CsvDevice):

    def __init__(self, device_name, agg_name, description):
        self.device_name = device_name
        self.description = description
        agg_split = agg_name.split("-", 1)
        if len(agg_split) == 2:
            self.has_agg = True
            self.agg_name = agg_name
            self.agg_system_name = agg_split[0]
            self.agg_instance_name = agg_split[1]
        else:
            self.has_agg = False


class CsvSection():
    """Top Node of the Section-Subsystem-Device data structure."""
    order_index = None

    section_name = None
    csvSubsystems = None

    def __init__(self, section_name):
        self.section_name = section_name
        self.csvSubsystems = {}
        self.order_index = -1


    def printInfo(self):
        print "----------SECTION----------------- ", self.section_name
        for csvSubsystem in self.csvSubsystems.values():
            csvSubsystem.printInfo()


    def appendCsvDevice(self, csvDevice):
        """Appends the CsvDevice instance to the list and adds it as a child within this node.
        Nodes between this instance and the given device instance are automatically inserted.
        Only used upon construction of the data models
        :param csvDevice: CsvDevice instance"""
        if isinstance(csvDevice, CsvDevice):
            subsystem = self._getCsvSubsystem(csvDevice.getSubsystemName())
            subsystem.appendCsvDevice(csvDevice)
            if csvDevice.order_index < self.order_index or self.order_index < 0:
                self.order_index = csvDevice.order_index


    def _getCsvSubsystem(self, csvSubsystemName):
        """Returns a CsvSubsystem instance with a specified name.
        If it does not exist under this node, it is created an appended."""
        if isinstance(csvSubsystemName, basestring):
            if not csvSubsystemName in self.csvSubsystems.keys():
                self.csvSubsystems[csvSubsystemName] = CsvSubsystem(csvSubsystemName)
        return self.csvSubsystems[csvSubsystemName]


    def getCsvSubsystems(self):
        """Getter for CsvSubsystem instances under this node."""
        return self.csvSubsystems


class CsvSubsystem():
    """Node of the Section-Subsystem-Device data structure.
    Instances of this class are automatically created when creating data structure through CsvSection instances."""
    order_index = None

    subsystem_name = None
    csvDevices = None

    def __init__(self, subsystem_name):
        self.subsystem_name = subsystem_name
        self.csvDevices = {}
        self.order_index = -1

    def printInfo(self):
        print "  ----------SUBSYSTEM------------ ", self.subsystem_name
        for csvDevice in self.csvDevices.values():
            csvDevice.printInfo()

    def appendCsvDevice(self, csvDevice):
        """Appends the CsvDevice instance as a child of this node.
        :param csvDevice: CsvDevice instance"""
        if isinstance(csvDevice, CsvDevice):
            if not csvDevice.device_name in self.csvDevices.keys():
                self.csvDevices[csvDevice.device_name] = csvDevice
                if csvDevice.order_index < self.order_index or self.order_index < 0:
                    self.order_index = csvDevice.order_index
            else:
                return
        else:
            return False

    def getCsvDevices(self):
        """Getter for CsvDevice instances under this node"""
        return self.csvDevices


class CsvAggSystem():
    """Top Node of the AggSystem-Device data structure."""

    csvDevices = None

    agg_system_name = None
    executable_name = None

    gui_widget = None
    gui_dir = None

    order_index = None

    nextAggs = None
    prevAggs = None

    manager = None

    additional_arg = None

    def __init__(self, agg_system_name, gui_dir, manager):
        self.agg_system_name = agg_system_name
        self.executable_name = self.agg_system_name.rstrip('0123456789 ')
        self.csvDevices = []
        self.prevAggs = []
        self.nextAggs = []
        self.gui_dir = gui_dir
        self.manager = manager
        self.order_index = -1


    def appendCsvDevice(self, csvDevice):
        """Appends the CsvDevice instance as a child of this node.
        :param csvDevice: CsvDevice instance"""
        if isinstance(csvDevice, CsvDevice):
            self.csvDevices.append(csvDevice)
        else:
            return False

    def printInfo(self):
        print "----------AGGSYSTEM------------ ", self.agg_system_name
        for csvDevice in self.csvDevices:
            csvDevice.printInfo()


    def runGUI(self):
        """Method for running a GUI of this aggregate
        Returns success code:
        0  - GUI already running
        1  - success
        2  - External GUI, no control
        -1 - GUI script not found
        -2 - Error whilst running script"""
        if self.isGuiRunning():
            try:
                self.gui_widget.raise_()
                self.gui_widget.activateWindow()
            except:
                pass
            return 0

        file_path = self.gui_dir + "/" + self.executable_name + ".py"
        if not os.path.isfile(file_path):
            return -1
        line = ["--LAB ", self.agg_system_name]
        for csvDevice in self.csvDevices:
            line.append("--" + csvDevice.agg_instance_name)
            line.append(csvDevice.getDeviceName())
            if csvDevice.getDescription():
                line.append(csvDevice.getDescription())
            else:
                line.append("No description available")
        if self.additional_arg:
            line.append("--ADD")
            line.append(self.additional_arg)

        try:
            command_module = __import__(self.executable_name)
            if not hasattr(command_module, "getGuiWidget"):
                self.custom_gui = subprocess.Popen("python2.7 %s %s" % (file_path, " ".join(line)), shell=True)
                return 2
            self.gui_widget = command_module.getGuiWidget(line)
            if self.gui_widget is None:
                return 2
            self.gui_widget.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint)
            self.gui_widget.setResult(2)

            if len(self.nextAggs) > 0 and hasattr(self.gui_widget, "addNext"):
                try:
                    index = 0
                    for nextAgg in self.nextAggs:
                        self.gui_widget.addNext(self.runNextGui, index, nextAgg.agg_system_name)
                        index += 1
                except TypeError:
                    self.gui_widget.addNext(self.runNextGui)

            if len(self.prevAggs) > 0 and hasattr(self.gui_widget, "addPrev"):
                try:
                    index = 0
                    for prevAgg in self.prevAggs:
                        self.gui_widget.addPrev(self.runPrevGui, index, prevAgg.agg_system_name)
                        index += 1
                except TypeError:
                    self.gui_widget.addPrev(self.runPrevGui)

            if hasattr(self.gui_widget, "setManagerInstance"):
                self.gui_widget.setManagerInstance(self.manager)

            self.gui_widget.show()
            return 1
        except ImportError:
            return -2

    def runNextGui(self, index=0):
        self.gui_widget.close()
        self.nextAggs[index].runGUI()

    def runPrevGui(self, index=0):
        self.gui_widget.close()
        self.prevAggs[index].runGUI()

    def isGuiRunning(self):
        """Method returns True, if a GUI of this aggregate is running, False otherwise"""
        if self.gui_widget:
            if self.gui_widget.result() == 2:
                return True
        return False

    def getGuiPos(self):
        if self.gui_widget:
            return [self.gui_widget.pos().x(), self.gui_widget.pos().y()]
        else:
            return [0,0]

    def setGuiPos(self, x,y):
        if self.gui_widget:
            self.gui_widget.move(x,y)



class StateAttributeHandler(TaurusListener):

    csvDevice = None

    def __init__(self, name, csvDevice):
        super(StateAttributeHandler, self).__init__(name)
        self.csvDevice = csvDevice

    def eventReceived(self, src, type, evt_value):
        if type == 3:
            #ERROR
            self.csvDevice.setState(DevState.UNKNOWN)
        elif type == 2 or type == 0:
            #NORMAL
            self.csvDevice.setState(evt_value.value)
