# Satellite Receiver

<img src="docs/art/beegnd_icon_tongue.png" alt="BEEGND IMG" height="100"/>

Student project: custom rotor design for portable ground station. \
Members of this group:
- Conrad Klaus (code and electronics)
- Prabhpreet S. Data (mechanics, prototype)
- Nasser Mazraani (final design build)

<img src="docs/art/finalProduct.jpeg" alt="Satellite Receiver img" width="700"/>

## PCB design
The pcb is designed as a raspberry pi hat to drive the motors and sensors.\
<img src="docs/art/pcbSchematic.png" alt="Pcb Schematic" width="700"/>\
<img src="docs/art/PCB.png" alt="Pcb Image" width="700"/>

## Code
Main features:
- Rotctl
- Multithreading
- Sensors: magnetic encoder, quadrature
encoder, switches
- Separate driver modules: h-bridge, i2c
multiplexer etc.
- Position monitoring

For further information: ./src/README.md or ./documentation

Code structure: \
<img src="./docs/art/SatelliteReceiver.png" alt="Code structure" width="700"/>
