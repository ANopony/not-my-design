import clr
import os

dll_path = r"C:\File\PycharmProjects\not-my-design\LibreHardwareMonitorLib.dll"
clr.AddReference(dll_path)
from LibreHardwareMonitor.Hardware import Computer

computer = Computer(
    IsCpuEnabled = False,
    IsGpuEnabled = True,
    IsMemoryEnabled = False,
    IsMotherboardEnabled = False,
    IsControllerEnabled = False,
    IsNetworkEnabled = False,
    IsStorageEnabled = False
)
computer.IsGpuEnabled = True
computer.Open()

for hardware in computer.Hardware:
    hardware.Update()
    for sensor in hardware.Sensors:
        if sensor.SensorType.ToString() == "Load" and "GPU" in sensor.Name:
            print(f"{sensor.Name}: {sensor.Value}%")