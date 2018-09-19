# Python real-time serial plotter for Arduino

This project can be used for prototyping sensors attached to Arduino.
Use this as is or modify to your use case.

![Main window](/img/python_serial_plotter.gif)

## Usage

`python serialplotter.py --port_name='COM3' --baud_rate=9600`

## Requirements

This setup has been tested with Python 3.6 on Windows 10 and this will propably work as well with Python 3.5+ on Linux and Mac.

Install required libraries with Pip
`pip install matplotlib tkinter pyserial`

## Example code for Arduino

The serial plotter expects only measurement values, one float value per line. The transmitting interval is not specified but every 200 ms works well with 9600 bauds.

[Arduino code example](/Arduino_example_PIR_sensor/Arduino_example_PIR_sensor.ino)

