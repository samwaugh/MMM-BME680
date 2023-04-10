Module.register("MMM-BME680", {
    // Default module config.
    defaults: {
        titleText: "MIRROR SENSOR",
        iconDisplay: 1, // display icons
        updateInterval: 30, // Seconds
        tempScaleType: 0, // Celsius
        pressureScaleType: 0, // hPa
        tempOffset: 1.5 // degrees
    },

    // Define start sequence.
    start: function () {
        Log.info("Starting module: " + this.name);

        this.temperature = 'Loading...';
        this.humidity = 'Loading...';
        this.pressure = 'Loading...';
        this.iaq = 'Loading...';
        this.r = "Loading...";

        this.update();
        setInterval(
            this.update.bind(this),
            this.config.updateInterval * 1000);
    },

    update: function () {
        this.sendSocketNotification('REQUEST', this.config);
    },

    getStyles: function () {
        return ['MMM-BME680.css'];
    },

    // Override dom generator.
    getDom: function () {
        var wrapper = document.createElement("div");

        var header = document.createElement("div");
        var label = document.createTextNode(this.config.titleText);
        header.className = 'bme-header';
        header.appendChild(label)
        wrapper.appendChild(header);

        var table = document.createElement("table");
        var tbdy = document.createElement('tbody');
        for (var i = 0; i < 5; i++) {
            var val = "";
            var suffix = "";
            var icon_img = "";

            switch (i) {
                case 0:
                    switch (this.config.tempScaleType) {
                        case 0: // Celsius
                            val = this.temperature - this.config.tempOffset;
                            suffix = "°C";
                            break;
                        case 1: // Fahrenheit
                            val = Math.round(this.temperature * 9.0 / 5.0 + 32.0) - this.config.tempOffset;
                            suffix = "°F";
                            break;
                    }
                    icon_img = "temperature-high";
                    break;
                case 1:
                    val = this.humidity;
                    icon_img = "tint";
                    suffix = "%";
                    break;
                case 2:
                    switch (this.config.pressureScaleType) {
                        case 0: // hPa
                            val = this.pressure;
                            suffix = " hPa";
                            break;
                        case 1: // inHg
                            val = Math.round(this.pressure * 100 / 33.864) / 100;
                            suffix = " inHg";
                            break;
                    }
                    icon_img = "tachometer-alt"; // maybe "wind"
                    break;
                 case 3:
                    val = this.r;
                    suffix = " Ohms";
                    icon_img = "fan" // maybe "fan";
                    break;
                 case 4:
                    val = this.iaq;
                    suffix = " %";
                    icon_img = "house-chimney-medical" // maybe "fan";
                    break;
           }

            var tr = document.createElement('tr');
            var icon = document.createElement("i");

            switch (this.config.iconDisplay) {
                case 0: // don't display icons
                    icon.className = ' bme-icon';
                    break;
                case 1: // display icons
                    icon.className = 'fa fa-' + icon_img + ' bme-icon';
                    break;
            }

            var text_div = document.createElement("div");
            var text = document.createTextNode(" " + val + suffix);
            text_div.className = 'bme-text';
            text_div.appendChild(text);

            var td = document.createElement('td');
            td.className = 'bme-td-icon';
            td.appendChild(icon)
            tr.appendChild(td)

            var td = document.createElement('td');
            td.appendChild(text_div)
            tr.appendChild(td)

            tbdy.appendChild(tr);
        }
        table.appendChild(tbdy);
        wrapper.appendChild(table);

        return wrapper;
    },

    socketNotificationReceived: function (notification, payload) {
        if (notification === 'DATA') {
            this.temperature = payload.temp;
            this.humidity = payload.humidity;
            this.pressure = payload.press;
            this.r = payload.r;
            this.iaq = payload.iaq;
            this.updateDom();
        }
    },
});
