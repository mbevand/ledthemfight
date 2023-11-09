# LED Them Fight

Official site: https://github.com/mbevand/ledthemfight

*LED Them Fight* is a controller for addressable LED strings. It runs on Raspberry Pi hardware, with a GPIO pin connected directly to the LEDs, and is easy to use and customize through its built-in webserver:
* Small Python codebase, only one dependency: rpi-ws281x
* Many pre-defined effects and animations
* Code custom effects in just a few lines of Python in a text editor (no firmware dev environment needed)
* Various types of LED strings, strips, and arrays are supported: WS2811, WS2812, WS2813, WS2814, WS2815, SK6812, SK6813, SK6822, NeoPixels, etc; specifically anything supported by the underlying [rpi_ws281x](https://github.com/jgarff/rpi_ws281x) library
* Responsive web interface, ideal for smartphones, tablets, and computers
* Maximum of 2 LED strings, each on a unique GPIO output
* Optional activation of a relay to automatically switch on a power supply when the LEDs are lit

![LED Them Fight](logo.gif)

# Quick Start Guide

1. A [Raspberry Pi](https://www.raspberrypi.com/products/) computer is required

2. I recommend installing the [Raspberry Pi OS](https://www.raspberrypi.com/software/) "Lite" version without desktop. With the desktop version you may have to jump through hoops to disable audio device drivers as they [interfere with `rpi_ws281x`](https://github.com/jgarff/rpi_ws281x#limitations)

3. Connect the Pi to the LEDs:
   * GPIO18 (pin 12) to the LED data input line ("DIN")
   * GND (eg. pin 14) to the LED ground line

4. Either power the LEDs with a dedicated DC power supply, or if the LEDs are 5V and if they do not draw too much power, the Pi may be able to power them itself:
   * 5V (eg. pin 4) to the LED VCC line
   * GND (eg. pin 6) to the LED ground line

5. Optionally: you may connect a relay between the Pi's GPIO15 (pin 10) and GND (eg. pin 9); LED Them Fight will activate the relay when the LEDs are lit; this relay can control the LED power supply

6. On the Pi, install LED Them Fight and its dependencies:

```
$ sudo apt install python3-gpiozero python3-pip
$ sudo pip3 install rpi-ws281x
$ git clone https://github.com/mbevand/ledthemfight
$ cd ledthemfight
$ sudo ./ledthemfight.py  # add "-p 1234" to listen on a port other than 80/tcp
```

7. Finally, browse http://x.x.x.x (IP address of the Pi) to control the LEDs. That's it!

# API

The HTTP API, used by the web interface, can easily be invoked from the
command line or by third-party tools. For example, get the current state of
the server, which includes the list of all implemented effect names:

```
$ curl http://HOST/get/state
{
  "nr_led_strings": 1,
  "brightness": 255,
  "effects": [ "Blink", "Breathe", "Color_Wipe", ... ],
  "rendering": [ null ],
  "fps": 0
}
```

Start an effect:

```
$ curl http://HOST/button --json '{"name":"effect","value":"Sparkles"}'
```

Stop the current effect:

```
$ curl http://HOST/button --json '{"name":"stop"}'
```

Change the brightness level (1-255):

```
$ curl http://HOST/button --json '{"name":"brightness","value":"255"}'
```
