=====================================
ControlProgram Application
=====================================


Requirements:
=====================================
Python 2.7
Python modules:
	PyQt4 (version: 4.11.2)
	PyTango (version: >= 8.1.5)
	Taurus (version: >= 3.3.0)
	Numpy (version: >= 1.8.1)
	CosyWidgets (version: >= 0.1)
	MaxWidgets (version: >= 0.8.3)
	csv, subprocess, argparse, threading, time, os, json, datetime, contextlib, base64, 
	sys, pickle, re, math, signal, traceback, collections, copy, …



Operation:
=====================================
ControlProgram application can be run by executing ControlProgram.py
Application accepts following arguments:
--CSV ${Path to CSV file} (required)
--GCSV ${Path to Group CSV file} (optional)
--GUI ${Path to GUI directory} (required)
--TITLE ${Title of the main window} (optional)
-v (optional)

Moreover, you can run the ControlProgram using the GUIrunner application.
GUIrunner application automatically provides the input arguments to the ControlProgram.
GUIrunner also serves as an update manager and ControlSystem instance manager.

For more information please refer to the provided documentation.