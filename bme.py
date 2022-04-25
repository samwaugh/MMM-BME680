#!/usr/bin python
import bme680
from bme680iaq import *

# BME680 initialization
bme680_temp_offset = -2
try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)

# These oversampling settings can be tweaked to change the balance between accuracy and noise in the data.
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(150)
sensor.select_gas_heater_profile(0)
sensor.set_temp_offset(bme680_temp_offset)

#Initialize IAQ calculator
iaq_tracker = IAQTracker()

if sensor.get_sensor_data():
    if sensor.data.heat_stable:
        R_gas_k = sensor.data.gas_resistance/1000
        AQ = iaq_tracker.getIAQ(sensor.data)
    else:
        R_gas_k = 0
        AQ = -1
    print("{0:.2f} {1:.2f} {2:.2f} {3:.1f} {4:.2f} {5:.1f}"
	  .format(sensor.data.temperature, sensor.data.humidity, sensor.data.pressure, R_gas_k, AQ)
