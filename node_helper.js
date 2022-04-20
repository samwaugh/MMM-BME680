'use strict';

/* Magic Mirror
 * Module: MMM-BME680
 *
 * By Sam Waugh
 * MIT Licensed.
 */

const NodeHelper = require('node_helper');
const exec = require('child_process').exec;

module.exports = NodeHelper.create({
	start: function () {
		console.log('BME680 helper started ...');
	},

	// Subclass socketNotificationReceived received.
	socketNotificationReceived: function (notification, payload) {
		const self = this;
		if (notification === 'REQUEST') {
			const self = this
			this.config = payload
			var deviceAddr = this.config.deviceAddress;

			// execute external DHT Script
			exec(`python3 ./modules/MMM-BME680/bme680.py ${deviceAddr}`, (error, stdout) => {
				if (error) {
					console.error(`exec error: ${error}`);
					return;
				}
				var arr = stdout.split(" ");
				// Send data
				self.sendSocketNotification('DATA', {
					temp: arr[0],
					humidity: arr[1],
					press: arr[2],
				});
			});
		}
	}
});
