#!/usr/bin python
import bme680
import bme680iaq as iaq
from time import sleep

# BME680 initialization
bme680_temp_offset = 0 # may require a different value as sensor heats due to use
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
iaq_tracker = iaq.IAQTracker()

def prompt_data(temp, press, hum, Rgas, AQ):	
	out_string = "{0:.2f}°C, {1:.2f}hPa, {2:.2f}%RH, {3:.1f}kOhm".format(temp,press,hum,R_gas/1000)
	if AQ == None:
		out_string += ", cal."
	else:
		out_string += ", {0:.1f}%aq".format(AQ)
	print(out_string)

if sensor.get_sensor_data():
  if sensor.data.heat_stable:
    r_gas = sensor.data.gas_resistance
    aq = iaq_tracker.getIAQ(sensor.data)
  else:
    r_gas = 0
    aq = None
  prompt_data(sensor.data.temperature, sensor.data.humidity, sensor.data.pressure, r_gas, ac)
