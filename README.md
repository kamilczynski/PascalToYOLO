📄 Pascal2YOLO - Pascal VOC to YOLO Annotation Converter, Perfect for Preparing Training Datasets

Project Description
Pascal2YOLO is a Python GUI application designed to convert object annotations from the Pascal VOC format (XML) to the YOLO format (TXT). Users can select a folder containing XML files, choose an output directory, and specify a list of classes to include. The application parses each XML file to extract image dimensions and bounding box coordinates, then converts and normalizes these coordinates to the YOLO format. This tool streamlines the preparation of annotation data for training object detection models.

Key Features

✅ Automated Annotation Conversion – Processes multiple XML files and generates corresponding TXT files in YOLO format.

✅ Class Filtering – Allows users to define a list of classes, ensuring that only specified objects are converted.

✅ User-Friendly GUI – Provides an intuitive interface for selecting input and output directories and entering class information.

✅ Robust Error Handling – Informs users of parsing issues or missing required XML tags to avoid conversion errors.

✅ Batch Processing – Efficiently converts all annotation files within a selected folder in one go.

Technologies Used

Python 3.x – The primary programming language.

Tkinter – Used for building the graphical user interface.

xml.etree.ElementTree – For parsing and processing XML files containing Pascal VOC annotations.

OS Module – For file system operations like directory traversal and file path manipulation.
