# MMM-BME680

This is an extension for the [MagicMirror²](https://github.com/MichMich/MagicMirror). It monitors temperature, humidity, air pressure and gas levels from [BME-680 sensor](https://www.bosch-sensortec.com/products/environmental-sensors/gas-sensors/bme680/). The BME-680 produces data within the following ranges:

- Pressure: 300-1100 hPa
- Humidity: 0-100%
- Temperature: -40-85°C 
- Index for Air Quality (IAQ) targeting breath Volitile Organic Compounds (b-VOC): 0-500 (+/-15% sensor-to-sensor variation)

Bosch provide propriety code for converting to the Index for Air Quality (IAQ), which requires licencing. This project attempts to callibrate the sensor on a "good day" and then provides a relative change in air quality from those good measurements. I suggest selecting open air, shady location where the [air quality is good as can be](https://github.com/gpailler/MMM-aqicn) to provide that calibration. The sensor only provides a rough indication of volitile organic compounds, so the calibration should be sufficient as an indication of indoor air quality. (No responsibility is taken for anyone relying on this in dangerous environments, obviously.)

## Installation
1. Navigate into your MagicMirror's `modules` folder.
2. Clone repository `git clone https://github.com/samwaugh/MMM-BME680.git`.
3. Go to newly created directory (`cd MMM-BME680`).
4. Execute `npm install` to install the node dependencies.
5. Connect the BME680 to your Raspberry Pi.

### Hardware
The particular board that this was tested with is the [Pimoroni breakout](https://learn.pimoroni.com/article/getting-started-with-bme680-breakout), older  than the current [BME-680](https://shop.pimoroni.com/products/bme680-breakout?variant=12491552129107) and the [BME-688](https://shop.pimoroni.com/products/bme688-breakout?variant=39336951709779). This can be connected directly to pins 1-5 on the 40-pin RPi GPIO. This also assumes 2IC is enabled on the RPi.

<img src=".github/bme680-5.webp">
<img src=".github/RXD PWM0.png">

## Using the module

Add it to the modules array in the `config/config.js` file:

````javascript
modules: [
	...
	{
		module: 'MMM-BME680',
		position: 'top_left',
		config: {
			updateInterval: 30 //seconds
			}
	},
	...
]
````

### Configuration options

<img src=".github/example.png">

<table width="100%">
	<thead>
		<tr>
			<th>Property</th>
			<th width="100%">Description</th>
		</tr>
	<thead>
	<tbody>
		<tr>
			<td><code>titleText</code></td>
			<td>Widget title text
				<br><b>Type:</b> <code>string</code>
				<br><b>Default:</b> <code>Home weather</code>
			</td>
		</tr>
		<tr>
			<td><code>iconDisplay</code></td>
			<td>Display icons
				<br><b>Type:</b> <code>int</code>
				<br><b>Default:</b> <code>1</code> display, <code>0</code> do not display
			</td>
		</tr>
		<tr>
			<td><code>updateInterval</code></td>
			<td>Wait interval between readings of BME680 sensor values in seconds
				<br><b>Type:</b> <code>int</code>
				<br><b>Default:</b> <code>100</code>
			</td>
		</tr>
		<tr>
			<td><code>temperatureScaleType</code></td>
			<td>Different temperature scales
				<br><b>Type:</b> <code>int</code>
				<br><b>Default:</b> <code>0</code>
				<br><b>Scale types:</b> <code>0</code> Celsius, <code>1</code> Fahrenheit
			</td>
		</tr>
		<tr>
			<td><code>pressureScaleType</code></td>
			<td>Different pressure scales
				<br><b>Type:</b> <code>int</code>
				<br><b>Default:</b> <code>0</code>
				<br><b>Scale types:</b> <code>0</code> hPa, <code>1</code> inHg
			</td>
		</tr>
	</tbody>
</table>

## Additional Mirror Projects of Interest

The following are MMM projects looking at integrating hardware sensors as opposed to full IOT weather sensor solutions:

- [MMM-BME280](https://github.com/awitwicki/MMM-BME280) for temperature, humidity and pressure (from which this project was forked, many thanks!).
- [MMM-MHZ19](https://github.com/awitwicki/MMM-MHZ19) using [MHZ-19](https://revspace.nl/MHZ19) CO2 sensor.
- Temperature and humidity using Adafruit DHT11, DHT22, or AM2302 sensors: [MMM-DHT-Sensor](https://github.com/bernardpletikosa/MMM-DHT-Sensor) (fork grandparent!), [MMM-LocalTemperature](https://github.com/glitch452/MMM-LocalTemperature), [MMM-DHT22](https://github.com/Bangee44/MMM-DHT22), [MMM-dht22](https://github.com/nebulx29/MMM-dht22), [MMM-loldht22](https://github.com/cslev/MMM-loldht22)
- [MMM-HDC1080](https://github.com/MichaelF1/MMM-HDC1080) temperature and humidity sensor.
- [MMM-ds18b20](https://github.com/Thlb/MMM-temp-ds18b20) temperature sensor.
- [MMM-01ZM](https://github.com/rubinho101/MMM-01ZM) Xiaomi LYWSDCGQ 01ZM Temperature-Humidity sensor AND [Nova PM SDS011](https://microcontrollerslab.com/nova-pm-sds011-dust-sensor-pinout-working-interfacing-datasheet/) particulate matter (dust and smoke) sensor.


## Code Information
### Dependencies
- `python3` (should be installed on Raspberry Pi)
- `smbus` (Python library, install via `pip3 install smbus` )
- `bme680` (Python library, install via `pip3 install bme680` if Pimoroni library needed)

### Developer Notes
- [Pimoroni Python code for BME68x](https://github.com/pimoroni/bme680-python) used for this project
- [Borsch BME68x Sensor API](https://github.com/BoschSensortec/BME68x-Sensor-API) to use this to produce the IAQ calculation, licencing and a compiled binary is required. As this is not easily achievable for the open source nature of MMM, this module is not used.
- [Deprecated Borsch BEM680 Sensor API](https://github.com/BoschSensortec/BME680_driver)

<img src=".github/IAQ.png">

### Test BME680 module
1. Navigate into your `MagicMirror/modules/MMM-BME680` folder
2. Run script `python3 bme.py`
   - If you get `FileNotFoundError: [Errno 2] No such file or directory` you have to enable i2c interface (`raspi-config nonint do_i2c 0`)
3. Script should print sensor values like this `24.7 38.3 996.6` - that means `temperature humidity pressure`
   - If you only see `0 0 0` make sure you are not setting the PINs you are using in another program. 
