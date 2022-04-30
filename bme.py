#!/usr/bin python
import bme680
from bme680iaq import *

# BME680 initialization
bme680_temp_offset = 0
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
print('calling IAQ tracker')
iaq_tracker = IAQTracker()

if sensor.get_sensor_data():
    print('sensor data received')
    if sensor.data.heat_stable:
        r_gas_k = sensor.data.gas_resistance/1000
        aq = iaq_tracker.getIAQ(sensor.data)
    else:
        r_gas_k = 0
        aq = -1
    print("{0:.2f} {1:.2f} {2:.2f} {3:.1f} {4:.2f}"
	  .format(sensor.data.temperature, sensor.data.humidity, sensor.data.pressure, r_gas_k, aq)

	  
