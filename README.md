# LED Them Fight

Official site: https://github.com/mbevand/ledthemfight

*LED Them Fight* is a controller for addressable LED strings. It runs on Raspberry Pi hardware; LED strings are connected directly to GPIO pins. It is easy to use and customize through its built-in web server:
* Tiny Python codebase (less than 1k lines of code), only one dependency: [rpi-ws281x](https://github.com/jgarff/rpi_ws281x) library
* Intuitive responsive web interface, ideal for smartphones, tablets, and computers
* Many pre-defined animated or static effects
* Custom effects can be added with as little as 1 or 2 lines of Python code
* In-browser preview of effects using animated `<canvas>` elements
* Various types of LED strings, strips, and arrays are supported: WS2811, WS2812, WS2813, WS2814, WS2815, SK6812, SK6813, SK6822, NeoPixels, etc; specifically anything supported by the underlying rpi-ws281x library
* Maximum of 2 LED strings, each on a unique GPIO output
* Global brightness variable
* Optional activation of a relay to automatically switch on a power supply when the LEDs are lit
* Simple HTTP API that can be used for example from `curl`

![LED Them Fight](logo.gif)

# Motivation

The main reason I created LED Them Fight is that I wanted to make it *dead simple* to create custom effects rendered live and reliably. No streaming real-time pixel data over unreliable Wi-Fi. No downloading hundreds of megabytes of firmware development packages. No reflashing microcontrollers. No recompiling anything. Just type simple Python code which is instantly rendered on a locally-attached LED string. From a factory-reset Raspberry Pi **it takes less than 60 seconds to install & configure LED Them Fight and code your first custom effect!**

Compare this to current solutions: for example if you are using the popular [WLED](https://kno.wled.ge/) controller, there are two options to create custom effects:

1. Either you stream real-time pixel data from a computer [over UDP to WLED](https://kno.wled.ge/interfaces/udp-realtime/), but WLED runs on ESP32 which is typically on Wi-Fi, so animations will inevitably glitch. And even if you want to get an Ethernet-enabled ESP32 it is not convenient or may not be possible to wire Ethernet where you need. Plus the requirement to have two systems (computer + ESP32) adds complexity and cost.

2. Or you download and install [hundreds of megabytes of Visual Studio Code / PlatformIO packages](https://kno.wled.ge/advanced/compiling-wled/), then edit WLED's source to code your effect in C++, then compile and reflash your ESP32, then figure out your effect has some bugs so you re-compile, re-flash, re-test, and continuously waste time with these test cycles.

But with LED Them Fight, all you need is a text editor to write effects in as little as 1 or 2 lines of Python, and when you edit a `red` to `blue`, it **instantly and automatically** notices the edit and renders blue on the LED string. You have basically a live view of your effect code as you are typing it! This allows to very, very quickly iterate and experiment with animations and colors.

# Quick Start Guide

1. A [Raspberry Pi](https://www.raspberrypi.com/products/) computer is required. I recommend installing the [Raspberry Pi OS "Lite" version](https://www.raspberrypi.com/software/) without desktop. Or else, with the desktop version you may have to jump through hoops to disable audio device drivers as they [interfere with `rpi-ws281x`](https://github.com/jgarff/rpi_ws281x#limitations)

2. Connect the Pi to the LED string:
   * GPIO18 (pin 12) to the LED data input line
   * GND (eg. pin 14) to the LED ground line

3. I recommend powering the LEDs with a dedicated DC power supply:
   * Power supply positive terminal to the LED VCC
   * Power supply negative terminal to the LED ground line (meaning all the grounds—Pi's, LED's, power supply's—are tied together)

That is it for the hardware side. Now, for the software side, you need less than 60 seconds to install & configure LED Them Fight and code your first custom effect:

4. On the Pi, install LED Them Fight and its dependencies:

```
$ sudo apt install python3-pip && sudo pip3 install rpi-ws281x
$ git clone https://github.com/mbevand/ledthemfight
$ cd ledthemfight
$ sudo ./ledthemfight.py  # add "-p 1234" to listen on a port other than 80/tcp
```

5. Browse http://x.x.x.x (IP address of the Pi). The web interface will prompt for the number of LED strings and LED pixels per string. Accept the defaults, click submit. You land on the main web interface, where you can render built-in effects:

![Screenshot](screenshot.png)

6. Now, the fun part. You are going to write your own effect. They are defined in
the [effect_library/](effect_library/) directory:

```
$ ls effect_library/
Blink.py       Fireworks.py  Rainbow.py      Sparkles.py
Breathe.py     Flag_FR.py    Random.py	     Spreading_Colors.py
...
```

7. Create a new effect file in this directory named `MyEffect.py`. Let's say you want the LED string to display a static red color, so write this in `MyEffect.py`:

```
def render(index, frame):
    return red
```

8. As you save the file, LED Them Fight automatically detects it and renders it in a simulated LED string, which you can preview by reloading your browser page. The simulated LED string appears in the web interface under the name "MyEffect". Then click on it to render it on the physical LED string, showing your nice red color. Done! 60 seconds as promised!

9. Let's make it flash red and blue. Edit `MyEffect.py` to this:

```
def render(index, frame):
    return red if (frame % 60) < 30 else blue
```

Save the file. LED Them Fight automatically detects the edit, and instantly starts rendering this new version on the LED string. By default it renders at 60 frames per second, so this code will make it flash red and blue once a second.

10. Let's animate it. Also simple:

```
def render(index, frame):
    return black if ((index - frame) % 20) else red
```

Again, the edit is instantly picked up, so now you see red dots separated by 20 pixels
move along your LED string at a speed of 1 pixel per frame.

# Effect Module Reference

Effect modules are written in Python. Any valid Python code is OK. They
are loaded and executed by the Python interpreter. Typically the standard
library modules `random`, `math` are useful to write effects. For examples,
just read the built-in ones:
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
animation.

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

# Architecture

The main process [ledthemfight.py](ledthemfight.py) runs the web server. All
of the web server code is in this file. I wanted to keep LED Them Fight simple
(KISS) so I use Python's built-in `http.server`. Before the web server runs
the code forks 2 sub-processes:

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
the new settings:

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

# Pixelblaze

After I started LED Them Fight, and decided on implementing the concept of effect modules, I eventually discovered [Pixelblaze](https://electromage.com/pixelblaze) which is close to my ideal product. It is much more featureful, however:

* it is closed-source (deal breaker for me; I need hackability)
* it runs on ESP32 instead of a Raspberry Pi (the latter offerts more CPU power for more complex effects)
* their effects are written in a subset of JavaScript (full support of Python and its standard library is more flexible and easier to code for)
* their effects have to be edited in-browser (a proper text editor with syntax highlighting and autocompletion is more convenient)
* being microcontroller-based, firmware updates are error-prone and can be a pain (whereas LED Them Fight can always be tweaked and broken and repaired all from the comfort of an SSH session)
* the visual quality of their [library of effects](https://electromage.com/patterns) is dubious—their single most popular effect "KITT" has non-smooth red gradients, their 3rd most popular effect "sparkfire" is weirdly grainy near the base, "fire - red" is inexplicalby dim, "policeLights" are red/purple instead of red/blue??, and so on

It seems to me the Pixelblaze effect library is more curated for 2D LED arrays, not 1D LED strings.
