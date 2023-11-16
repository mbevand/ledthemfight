# LED Them Fight

Official site: https://github.com/mbevand/ledthemfight

*LED Them Fight* is a controller for addressable LED strings. It runs on Raspberry Pi hardware; LED strings are connected directly to GPIO pins. It is easy to use and customize through its built-in web server:
* Small Python codebase, only one dependency: [rpi-ws281x](https://github.com/jgarff/rpi_ws281x) library
* Many pre-defined effects and animations
* Custom effects can be added with as little as 1 or 2 lines of Python (no firmware dev environment needed)
* Various types of LED strings, strips, and arrays are supported: WS2811, WS2812, WS2813, WS2814, WS2815, SK6812, SK6813, SK6822, NeoPixels, etc; specifically anything supported by the underlying rpi-ws281x
* Responsive web interface, ideal for smartphones, tablets, and computers
* Maximum of 2 LED strings, each on a unique GPIO output
* Optional activation of a relay to automatically switch on a power supply when the LEDs are lit

![LED Them Fight](logo.gif)

# Quick Start Guide

1. A [Raspberry Pi](https://www.raspberrypi.com/products/) computer is required. I recommend installing the [Raspberry Pi OS "Lite" version](https://www.raspberrypi.com/software/) without desktop. Or else, with the desktop version you may have to jump through hoops to disable audio device drivers as they [interfere with `rpi-ws281x`](https://github.com/jgarff/rpi_ws281x#limitations)

2. Connect the Pi to the LED string:
   * GPIO18 (pin 12) to the LED data input line
   * GND (eg. pin 14) to the LED ground line

3. I recommend powering the LEDs with a dedicated DC power supply:
   * Power supply positive terminal to the LED VCC
   * Power supply negative terminal to the LED ground line (meaning all the grounds—Pi's, LED's, power supply's—are tied together)

4. On the Pi, install LED Them Fight and its dependencies:

```
$ sudo apt install python3-pip && sudo pip3 install rpi-ws281x
$ git clone https://github.com/mbevand/ledthemfight
$ cd ledthemfight
$ sudo ./ledthemfight.py  # add "-p 1234" to listen on a port other than 80/tcp
```

5. Finally, browse http://x.x.x.x (IP address of the Pi) to control the LEDs. The web interface will prompt for the number of LED strings and LED pixels per string. Accept the defaults, click submit, then you land on the intuitive web interfacee—that is it!

![Screenshot](screenshot.gif)

# Guide to Create Custom Effects

The main reason I created LED Them Fight is to make it *dead simple* to create custom effects that are rendered reliably, ie. without streaming pixel data over unreliable Wifi. Assuming the Pi, LED string, and power supply are wired and turned on, one needs **less than 60 seconds** to install and configure LED Them Fight, from scratch, and create and display a custom effect:

1. Effects are defined in module files written in Python in the `effect_library/` sub-directory. Create one new file named `MyEffect.py`

2. Let's say you want the LED string to display a simple static red color, write this content in `MyEffect.py`:

```
def render(index, frame):
    return "#f00"
```

3. As you save the file, LED Them Fight automatically detects it, and renders it in a simulated LED string, so you can immediately click reload in your browser and the simulated LED string animation is shown in the web interface under the name "MyEffect". Just click on it, and it is rendered on the physical LED string. Done! 60 seconds as promised.

Want to make it blink? Also simple. Write this in `MyEffect.py`:

```
def render(index, frame):
    return red if (frame % 60) < 30 else black
```

Save the file. LED Them Fight automatically detects the edit, and instantly starts rendering this new version on the LED string. It renders at 60 frames per second by default, so this code will make it blink once a second. Notice that instead of specifying the color as `"#rgb"` strings one can use constants like `red` or `black`.

Want to make an animation? Also simple:

```
def render(index, frame):
    return black if ((index + frame) % 30) else red
```

LED Them Fight calls render() for every pixel for every frame, and the function returns
the color of the pixel. The argument index is the index of the pixel in the LED string,
and frame is the number of the frame, starting from 0. It increments by 1 for every frame,
so it increments by 60 every seconds.

The colors that render() returns can be specified as:
* Constants: `red`, `black`, `green`, etc (see the list at top of [worker_led.py](worker_led.py))
* 3-digit hex notation as a string: `"#rgb"`
* 6-digit hex notation as a string: `"#rrggbb"`
* floating point RGB values as a tuple: (1.0, 1.0, 1.0) for white

# Relay Support

When addressable LED strings are "off", displaying pure black, they still draw some power. So if you have them on a dedicated power supply, wire a relay in series on the LED power supply AC input, so LED Them Fight can physically turn it off.

Get a suitable relay that can be controlled from the Pi's 3.3V output level, and connect it to GPIO15 (pin 10) and GND (eg. pin 9). LED Them Fight will drive GPIO15 high—activating the relay—when the LEDs are lit. I like to use this [relay-enabled power strip](https://www.digital-loggers.com/iot2.html) as there is no need to work directly with high AC voltage wires.

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
