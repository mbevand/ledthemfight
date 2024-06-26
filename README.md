# LED Them Fight

Official site: https://github.com/mbevand/ledthemfight

*LED Them Fight* is a controller for addressable LED strings. It runs on Raspberry Pi hardware; LED strings are connected directly to GPIO pins. It is easy to use and customize through its built-in web server:
* Very small Python codebase (less than 1k lines of code), only one dependency: [rpi-ws281x](https://github.com/jgarff/rpi_ws281x) library
* In-browser preview of effects using animated `<canvas>` elements
* 20+ built-in effects
* Custom effect modules can be coded in as few as 1 or 2 lines of Python—unleash your creativity!
* Responsive web interface, ideal for smartphones, tablets, and computers
* Various types of LED strings, strips, and arrays are supported: WS2811, WS2812, WS2813, WS2814, WS2815, SK6812, SK6813, SK6822, NeoPixels, etc; specifically anything supported by the underlying rpi-ws281x library
* Currently 1 LED string supported (WIP to support two, each on a unique GPIO output)
* Optional activation of a relay to automatically switch on a power supply when the LEDs are lit
* Global brightness setting
* Automatic gamma correction (ɣ=2.2)
* Simple HTTP API that can be used for example from `curl`

![LED Them Fight Logo](https://github.com/mbevand/ledthemfight/assets/2995228/1ccc80b9-c7e0-4138-a4c1-9b336cebd001)

# Motivation

The main reason I created LED Them Fight is that I wanted to make it *dead simple* to create completely original, custom effects rendered live and reliably. No streaming real-time pixel data over unreliable Wi-Fi. No downloading hundreds of megabytes of firmware development packages. No reflashing microcontrollers. No recompiling anything. Just write simple Python code which is instantly rendered on a locally-attached LED string, and on an in-browser preview. From a factory-reset Raspberry Pi **it takes less than 60 seconds to install & configure LED Them Fight and code your first custom effect!**

Compare this to current solutions: for example if you are using the popular [WLED](https://kno.wled.ge/) controller, there are two options to create a custom effect that is not part of its list of built-in effects:

1. Either you stream real-time pixel data from a computer [over UDP to WLED](https://kno.wled.ge/interfaces/udp-realtime/), but WLED runs on ESP32 which is typically Wi-Fi-connected, and Wi-Fi may not be available or reliable where you need it, such as an outdoor location where holiday lights are set up. Pulling an Ethernet cable may not be convenient. Overall, the requirement to have two systems (computer + ESP32) and reliable networking adds complexity and cost.

2. Or you download and install [hundreds of megabytes of Visual Studio Code / PlatformIO packages](https://kno.wled.ge/advanced/compiling-wled/) just to compile WLED, then edit its source to code your effect in C++, then compile and reflash your ESP32, then figure out your effect has some bugs so you re-compile, re-flash, re-test, etc. Slow testing iterations. Annoying.

But with LED Them Fight, all you need is a text editor to write effects in as few as 1 or 2 lines of Python code, and when you edit a `red` to `blue`, it **instantly and automatically** notices the edit and renders blue on the LED string. The browser also shows a preview of the effect. You have basically a live view and live preview of your code as you are typing it! This allows to very, very quickly iterate and experiment with animations and colors.

# Quick Start Guide

1. A [Raspberry Pi](https://www.raspberrypi.com/products/) computer is required. **(2023-12-05: the Pi 5 is [currently](https://github.com/jgarff/rpi_ws281x/issues/528) unsupported.)** I recommend installing the [Raspberry Pi OS "Lite" version](https://www.raspberrypi.com/software/) without desktop. Or else, with the desktop version you may have to jump through hoops to disable audio device drivers as they [interfere with the rpi-ws281x library](https://github.com/jgarff/rpi_ws281x#limitations)

2. Connect the Pi to the LED string:
   * GPIO18 (pin 12) to the LED data input line
   * GND (eg. pin 14) to the LED ground line

3. I recommend powering the LEDs with a dedicated DC power supply:
   * Power supply positive terminal to the LED VCC
   * Power supply negative terminal to the LED ground line (meaning all the grounds—Pi's, LED's, power supply's—are tied together)

That is it for the hardware side. Now, for the software side, you need less than 60 seconds to install & configure LED Them Fight and code your first custom effect:

4. On the Pi, install LED Them Fight and its dependencies:

```
$ sudo apt install git python3-pip
$ git clone https://github.com/mbevand/ledthemfight
$ cd ledthemfight
$ pip3 install -t . rpi-ws281x
$ sudo ./ledthemfight.py
```

5. Browse http://x.x.x.x (IP address of the Pi). The web interface will prompt for the number of LED strings and LED pixels per string. Accept the defaults, click submit. The browser redirects to the main page which shows a preview of all the effects:

https://github.com/mbevand/ledthemfight/assets/2995228/471bbf01-dcc2-4adc-a49d-0d2e6833c509

6. Now, the fun part. You are going to write your own effect. They are defined in
the [effect_library/](effect_library/) directory:

```
$ ls effect_library/
Blink.py    Fireworks.py  Rainbow.py
Breathe.py  Flag_FR.py    Random.py
...
```

7. Create a new effect file in this directory with the `.py` extension, for example `MyEffect.py`. Let's say you want the LED string to display a static red color, so write this in `MyEffect.py`:

```
def render(index, frame):
    return red
```

As you save the file, LED Them Fight automatically detects it and renders it in
a simulated LED string, which you can preview by reloading your browser page.
The preview will be in the web interface under the name "MyEffect". Then click
on it to render it on the physical LED string, showing your nice red color.
Done. 60 seconds, as promised!

8. With more than 60 seconds we can do more fun things. Let's make it flash red and blue. Edit `MyEffect.py` to this:

```
def render(index, frame):
    return red if (frame % 60) < 30 else blue
```

As soon as you save the file, because it was already being rendered on the
physical LED string, the edit is automatically detected and without any user
interaction the string flashes red and blue. Now you might understand the
simple architecture that LED Them Fight implements: for every frame, for every
pixel, it calls your `render()` function which returns the color for that
pixel. The `index` argument is the index of the pixel in the string. The
`frame` argument is the frame counter. By default rendering is done at 60
frames per second. So `(frame % 60) < 30` is `True` only in the first half of
every second. So all pixels will flash red in the first half of every second,
and will flash blue in the other half.

9. Let's display a rainbow:

```
def render(index, frame):
    return hsv((index % num_pixels) / num_pixels, 1, 1)
```

Again, as soon as you save the file, you see the rainbow. Notice how the code
uses `num_pixels` which is a global variable reflecting the total number of
pixels, combined with `index` (index of the pixel in the string, from `0` to
`num_pixels-1`). Therefore `(index % num_pixels) / num_pixels` returns a
floating point value from 0.0 (at the beginning of the string) to almost 1.0
(at the end). This floating point value is used as the hue parameter of the
`hsv()` function which returns an HSV color. So the hue of each pixel varies
smoothly from the beginning to the end of the LED string.

10. Simple moving animation are easy by combining the `index` and `frame` number:

```
def render(index, frame):
    return black if ((index - frame) % 20) else red
```

This displays red dots separated by 20 pixels that move along the LED string at
a speed of 1 pixel per frame. Very complex effects are typically implemented by
pre-rendering in a Python `array`, and having the `render()` function just read
from the `array`. For example see the LED Them Fight effect
[Fireworks.py](effect_library/Fireworks.py).

# Effect Module Reference

Effect modules are written in Python. Any valid Python code is OK. They
are loaded and executed by the Python interpreter. Typically the standard
library modules `random`, `math` are useful to write effects. For examples,
see the effects that ship with LED Them Fight:
[effect_library/](effect_library/)

The module must define a `render(index, frame)` function. LED Them Fight calls
this function for every pixel, for every frame. The function must return
the color of the pixel. The `index` argument is the index of the pixel in the
LED string from 0 to N-1 if you have N pixels. The `frame` argument is the
number of the frame, starting from 0; it increments by 1 for every frame, so it
increments by 60 every second as by default LED Them Fight renders effects at
60 frames per second.

Optionally, the module may also define a `before_frame(frame)` function. LED Them
Fight calls this function once per frame, before calling `render()` for each pixel.
Typically this is useful for LED animations that need to calculate the state of the
animation, for example see [Color_Wipe.py](effect_library/Color_Wipe.py).

The color returned by render() can be specified as:
* Constants: `red`, `black`, `green`, etc (see the list at top of [worker_led.py](worker_led.py))
* 3-digit hex notation as a string: `"#rgb"`
* 6-digit hex notation as a string: `"#rrggbb"`
* Floating point RGB values, eg. white is: `rgb(1, 1, 1)`
* Floating point HSV values, eg. red is: `hsv(0, 1, 1)`

Some variables and functions are exposed to effect modules:

`num_pixels` is a global integer reflecting the number of pixels in the LED string.

`rgb(r, g, b)` creates an RGB color, where the components should be floating-point
values between 0.0 and 1.0. However note that LED Them Fight implements the
concept of global brightness, controlled by a slider in the web interface. An effect
that returns rgb(1, 1, 1) will render a white pixel that is clamped to the global brightness.
However it is possible to still render a pixel brighter than this by using values greater
than 1 for example rgb(2, 2, 2). This should be use sporadically only when warranted, such
as implementing a sparkling effect when just a few pixels in the string are sparkling
brighter than most other pixels.

`hsv(h, s, v)` creates an HSV color, where the components should be floating-point
values between 0.0 and 1.0. Cool for [rainbows](effect_library/Rainbow.py).

`dim(color, f)` to dim a color. `color` must be either an `rgb()` or `hsv()`
value.  `f` is a floating-point factor to reduce the brightness. For example
f=2 will reduce the brightness by a factor 2.

`mul(color, f)` to multiply color components by a floating-point value. `color`
must be either an `rgb()` or `hsv()` value. `f` can be for example 0.5 or 2 to
respectively dim or brighten the color. `mul(color, 0.5)` is equivalent to
`dim(color, 2)`.

# Relay Support

When addressable LED strings are "off", displaying pure black, they still draw some power. So if you have them on a dedicated power supply, it is a good idea to wire a relay in series on the LED power supply AC input, so that LED Them Fight can physically turn it on and off.

Get a suitable relay that can be controlled from the Pi's 3.3V output level,
and connect it to GPIO15 (pin 10) and GND (eg. pin 9). LED Them Fight will
drive GPIO15 high—activating the relay—when the LEDs are lit. I like to use
this [relay-enabled power strip](https://www.digital-loggers.com/iot2.html)
([SparkFun](https://www.sparkfun.com/products/14236),
[Adafruit](https://www.adafruit.com/product/2935),
[Amazon](https://www.amazon.com/dp/B00WV7GMA2))
as there is no need to work directly with high AC voltage wires.

# GPIO Pin Reference

LED Them Fight uses the following hardcoded Raspberry Pi pins:

* GPIO18: data output for the 1st LED string
* GPIO13: data output for the 2nd LED string (not yet supported - work in progress)
* GPIO15: relay output, driven high when an effect is being rendered on one of the LED strings

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

# Architecture

The main process [ledthemfight.py](ledthemfight.py) runs the web server. All
of the web server support code is in this file. I want to keep LED Them Fight
simple (KISS) so I use Python's built-in `http.server`. When starting up,
the code also forks 2 sub-processes:

1. `led_driver`: the entry point is `drive_led_forever()` in [worker_led.py](worker_led.py).
  This process imports the `rpi_ws281x` module and drives the LED string.

2. `seqgen` or sequence generator: the entry point is `seqgen_forever()` in
  [worker_led.py](worker_led.py). The role of this process is merely to monitor
  effect module files in [effect_library/](effect_library/), and when it detects
  a change it will load the effect, run it on a virtual 60-pixel LED string,
  and save 10 seconds (600 frames) worth of sequence of frames containing the RGB colors for
  each pixel. The output is saved in binary sequence files, in [www/sequence/](www/sequence/).
  It is a raw binary format containing 3 (bytes per pixel) * 60 (pixels) * 600
  (frames) = 108,000 bytes of data. I should probably change this to the standard
  xLights FSEQ format. The purpose of these sequence files is so that the web interface
  can download them and show effect previews in the `<canvas>` elements.

The very first time LED Them Fight is launched, it creates sequence files for all the
built-in effects, which takes ~600 ms per effect (on Raspberry Pi 4), so ~13
seconds for the 21 built-in effects. So if you load the browser page during
these first ~13 seconds some previews will be missing.

The first time LED Them Fight is launched, it takes you through a configuration
wizard. The settings are saved in the configuration file `/etc/ledthemfight.conf`.
You may edit this file by hand if needed, then relaunch LED Them Fight to reload
the new settings. For example I have a system with 1 LED string of 466 pixels,
so the wizard generated this config file for me:

```
{
  "set_up": true,
  "name": "My LEDs",
  "nr_led_strings": 1,
  "num_pixels": 466,
  "inverted": false
}
```

For inter-process communication, when the web server needs to communicate with
the led driver, or vice versa, I use two `multiprocessing.Queue` objects named
`to_led_driver` and `to_web_server`. For example when the end-user clicks in the
web interface on the Rainbow effect to render it, the web server puts the array object
`["/button", ("effect", "Rainbow")]` in the `to_led_driver` queue, and the
led driver process gets it, loads the Rainbow.py module, and renders it on the LED
string. The `to_web_server` queue is only used so the led driver can report its
status back to the web server.

# Similar Software

## Pixelblaze

After I started LED Them Fight, and decided on implementing the concept of effect modules, I eventually discovered [Pixelblaze](https://electromage.com/pixelblaze) which implements the same concept, and is close to my ideal product. It is much more featureful, however:

* it is closed-source (deal breaker for me; I need hackability)
* it runs on ESP32 instead of a Raspberry Pi (the latter offerts more CPU power for more complex effects)
* their effects are written in a subset of JavaScript (full support of Python and its standard library is more flexible and easier to code for)
* their effects have to be edited in-browser (a proper text editor with syntax highlighting and autocompletion is more convenient)
* being microcontroller-based, firmware updates are error-prone and can be a pain (whereas LED Them Fight can always be tweaked and broken and repaired all from the comfort of an SSH session)
* the visual quality of their [library of effects](https://electromage.com/patterns) is dubious—their single most popular effect "KITT" has non-smooth red gradients, their 3rd most popular effect "sparkfire" is weirdly grainy near the base, "fire - red" is inexplicalby dim, "policeLights" are red/purple instead of red/blue??, and so on

It seems to me the Pixelblaze effect library is more curated for 2D LED arrays, not 1D LED strings.

## led-control

I recently stumbled upon [led-control](https://github.com/jackw01/led-control)
which is very similar to LED Them Fight. It is Python based, more featureful,
but has more software dependencies.

I like the fact that in addition to being able to run on the Pi and having the
LED string directly connected to a GPIO, just like LED Them Fight, it can also
control a string connected to a Pi Pico that is itself connected to the Pi via
a USB cable. The project provides a simple firmware for the Pico that exposes a
USB virtual serial interface for relaying pixel data to the string. This means
in theory led-control could be extended to support an arbitrary number of
LED strings, with the help of an arbitrary number of Picos connected to the
Pi's USB ports (potentially through a USB hub). Although as of March 2024,
led-control does not allow this.
