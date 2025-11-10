import time, random, struct, array, math, sys, os, traceback, signal, importlib, importlib.util, colorsys, gpiozero
from rpi_ws281x import Color, PixelStrip

LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal
LED_INVERT = False    # True to invert the output signal (useful when using
                      #   NPN transistor level shift)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

fps_goal = 60 # aim at rendering at this fps rate
proc_name = None
pkg_name = 'effect_library'
pkg_path = os.path.dirname(__file__) + '/' + pkg_name
seq_path = os.path.dirname(__file__) + '/www/sequence'
brightness = 128
# strings must be a global as it's accessed by graceful_exit()
strings = []
ftimes = []
_gamma = {}
colors = {
        'black': (0, 0, 0),
        'red': (1, 0, 0),
        'lime': (0, 1, 0),
        'yellow': (1, 1, 0),
        'blue': (0, 0, 1),
        'magenta': (1, 0, 1),
        'cyan': (0, 1, 1),
        'white': (1, 1, 1),
        'green': (0, .5, 0),
        'pink': (1, .75, .8),
        'silver': (.75, .75, .75),
        'gray': (.5, .5, .5),
        'grey': (.5, .5, .5),
        'purple': (.5, 0, .5),
        'orange': (1, .65, 0),
        'orange_halloween': (.90, .40, 0),
        }

def log(m):
    sys.stdout.write(f'{proc_name}: {m}\n')

def err(m):
    sys.stderr.write(f'{proc_name}: {m}\n')

def gamma(x, ɣ):
    # x is 0-255
    if ɣ not in _gamma:
        _gamma[ɣ] = array.array('B',
                [round(255 * (x / 255) ** ɣ) for x in range(256)])
    return _gamma[ɣ][x]

def cto8b(color, ɣ=2.2):
    # Convert a color, as returned by an effect module's render() function,
    # to 8-bit 0-255 values. The color can be specified as:
    # - 3-digit hex notation as a string: "#rgb"
    # - 6-digit hex notation as a string: "#rrggbb"
    # - floating point RGB values as a tuple: (1.0, 0.5, 0)
    # The hex or floating-point values are relative to the "brightness" level.
    # That is, #f or #ff or 1.0 will be converted to the maximum brightness.
    # For example, assuming brightness=128, color (1.0, 0.5, 0) is converted to
    # (128, 64, 0). Then gamma correction is applied; and with the default ɣ=2.2
    # this example would convert to (56, 12, 0), which is the final color that
    # would be sent to the physical LED string. Notice that unlike the #rgb or
    # #rrggbb notation, the floating-point notation allows effect modules to
    # pass values greater than 1.0 if they intentionally want to render pixels
    # brighter than "brightness".
    if type(color) == str:
        assert(color.startswith('#'))
        color = color[1:]
        if len(color) == 3:
            r = [int(c, 16) / 15 for c in color]
        elif len(color) == 6:
            r = [int(color[i:i + 2], 16) / 255 for i in range(0, len(color), 2)]
        else:
            raise Exception(f'color is not in the format #rgb or #rrggbb: #{color}')
        color = tuple(r)
    
    # Add validation to ensure values don't cause IndexError in gamma lookup
    result = []
    for idx, x in enumerate(color):
        val = min(255, round(x * brightness))
        if val < 0 or val > 255:
            raise ValueError(f'Color component {idx} out of range after brightness calculation: '
                           f'{x} * {brightness} = {x * brightness}, clamped to {val}. '
                           f'Original color: {color}')
        result.append(gamma(val, ɣ))
    return result

def solid(strip, color):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)

#
# Effects
#

def rgb(r, g, b):
    return (r, g, b)

def hsv(h, s, v):
    return colorsys.hsv_to_rgb(h, s, v)

def dim(color, f=2):
    return tuple([x / f for x in color])

def mul(color, f):
    return tuple([x * f for x in color])

def enrich_namespace(num_pixels, mod):
    # put some variables and functions in the module's namespace
    mod.num_pixels = num_pixels
    mod.rgb = rgb
    mod.hsv = hsv
    mod.dim = dim
    mod.mul = mul
    for (k, v) in colors.items():
        setattr(mod, k, v)

def fx_getmtime(mod_name):
    return os.path.getmtime(pkg_path + '/' + mod_name + '.py')

def fx_load(num_pixels, mod_name):
    mod_file = mod_name + '.py'
    mname = pkg_name + '.' + mod_name
    try:
        # Python doc states invalidate_caches() should be called if modules
        # are installed while program is running
        importlib.invalidate_caches()
        # Instead of importlib.import_module() we are going to use
        # importlib.util.spec_from_file_location() and
        # importlib.util.module_from_spec() so we can inject some variables
        # and functions in the module's namespace before it is executed
        spec = importlib.util.spec_from_file_location(mname, pkg_path + "/" + mod_file)
        m = importlib.util.module_from_spec(spec)
        enrich_namespace(num_pixels, m)
        spec.loader.exec_module(m)
    except ModuleNotFoundError:
        err(f'{pkg_path + "/" + mod_file}: file not found')
        return None
    except Exception as e:
        # use limit=-1 to make the stack trace less verbose, not showing all the
        # internal importlib entries
        err(''.join(traceback.format_exception(*sys.exc_info(), limit=-1)))
        return None
    if not hasattr(m, 'render') or not callable(m.render):
        err(f'{pkg_path}/{mod_file}: function "render()" not found')
        return None
    return m

#
# Core code
#

class PixelString:
    def __init__(self, num_pixels, led_pin, inverted):
        self.num_pixels = num_pixels
        # led_pin is GPIO pin to led string (18 uses PWM, 10 uses SPI, etc)
        self.led_pin = led_pin
        self.ps = PixelStrip(num_pixels, led_pin, LED_FREQ_HZ, LED_DMA,
                                LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.ps.begin()
        self.relay = gpiozero.LED(15)
        self.effect = None
        self.fx_mod = None
        self.inverted = inverted
    def start(self, effect, fx_mtime, fx_mod):
        self.effect = effect
        self.fx_mtime = fx_mtime
        self.fx_mod = fx_mod
        self.last_stat = 0
        self.frame = 0
        if self.relay:
            self.relay.on()
    def stop(self):
        self.effect = None
        self.fx_mtime = None
        self.fx_mod = None
        solid(self.ps, Color(0, 0, 0))
        self.ps.show()
        if self.relay:
            self.relay.off()

def render_one_frame(strings):
    ftimes.insert(0, time.time())
    if len(ftimes) > 30:
        ftimes.pop()
    for st in strings:
        if hasattr(st.fx_mod, 'before_frame'):
            st.fx_mod.before_frame(st.frame)
        for i in range(st.num_pixels):
            phys_i = i if not st.inverted else st.num_pixels - 1 - i
            # do not pass a 2nd arg to cto8b() so as to perform gamma-correction
            # as we are rendering on a physical LED string
            st.ps.setPixelColor(phys_i, Color(*cto8b(st.fx_mod.render(i, st.frame))))
        st.ps.show()
        st.frame += 1

def check_edits(strings, to_led_driver):
    now = time.time()
    for st in strings:
        if st.effect and abs(now - st.last_stat) > .5:
            st.last_stat = now
            new_mtime = fx_getmtime(st.effect)
            if new_mtime != st.fx_mtime:
                log(f'module file for effect "{st.effect}" changed, reloading')
                # led driver process sends a msg to itself to reload the effect
                to_led_driver.put(['/button', ('effect', st.effect)])

def do_get(to_web_server, strings, arg):
    if arg == '/state':
        fxs = [x[:-3] for x in sorted(os.listdir(pkg_path)) if x.endswith('.py')]
        lf = len(ftimes)
        to_web_server.put([arg, {
            'nr_led_strings': len(strings),
            'brightness': brightness,
            'effects': fxs,
            'rendering': [st.effect for st in strings],
            'fps': lf / (ftimes[0] - ftimes[-1]) if lf > 1 else 0,
            }])
    else:
        to_web_server.put(['error', f'invalid request: /get{arg}'])

def do_initial_setup(strings, conf):
    log(f'configuring {conf["nr_led_strings"]} led string(s)'
        f' with {conf["num_pixels"]} pixel(s)')
    strings.clear()
    strings.append(PixelString(conf["num_pixels"], 18, conf["inverted"]))

def do_effect(strings, effect):
    try:
        mtime = fx_getmtime(effect)
        log(f'loading effect {pkg_path}/{effect}.py')
        mod = fx_load(strings[0].num_pixels, effect)
        if mod == None:
            return
        log(f'showing effect {effect}')
        strings[0].start(effect, mtime, mod)
    except FileNotFoundError:
        log(f'no such effect: {effect}')

def do_button(strings, arg):
    b_name, b_val = arg
    if b_name == 'effect':
        do_effect(strings, b_val)
    elif b_name == 'stop':
        log('stopping effect')
        strings[0].stop()
        ftimes.clear()
    elif b_name == 'brightness':
        global brightness
        brightness = max(1, min(255, int(b_val)))

def wait_next_frame():
    if not(len(ftimes)):
        return
    s = ftimes[0] + 1 / fps_goal - time.time()
    if s > 50e-6: # don't bother to sleep for less than 50 µsec
        time.sleep(s)

def button_handlers(to_led_driver):
    button = gpiozero.Button(23)
    button.when_pressed = \
        lambda : to_led_driver.put(['/button', ('effect', 'TurnOn')])
    button.when_released = \
        lambda : to_led_driver.put(['/button', ('effect', 'TurnOff')])

def graceful_exit(signal_number, stack_frame):
    for st in strings:
        st.stop()
    sys.exit(0)

def drive_led_forever(to_led_driver, to_web_server):
    global proc_name
    proc_name = 'led_driver'
    #button_handlers(to_led_driver)
    # handle SIGTERM, the default signal sent by kill(1)
    signal.signal(signal.SIGTERM, graceful_exit)
    while True:
        try:
            is_rendering = len(strings) and strings[0].effect
            if not is_rendering or (is_rendering and not to_led_driver.empty()):
                action, arg = to_led_driver.get()
                if action == '/get':
                    do_get(to_web_server, strings, arg)
                elif action == '/initial_setup':
                    do_initial_setup(strings, arg)
                elif action == '/button':
                    do_button(strings, arg)
                else:
                    raise Exception(f'unknown action {action}')
                continue
            render_one_frame(strings)
            check_edits(strings, to_led_driver)
        except KeyboardInterrupt:
            # handle Ctrl-C
            graceful_exit(None, None)
        except Exception:
            err(f'exception:\n' +
                ''.join(traceback.format_exception(*sys.exc_info())))
        wait_next_frame()

#
# Sequence generator
#

def render(num_pixels, frame_count, m):
    frames = []
    for frame in range(frame_count):
        pixels = []
        if hasattr(m, 'before_frame'):
            m.before_frame(frame)
        for i in range(num_pixels):
            # pass 1.0 as the 2nd arg of cto8b() in order to disable gamma
            # correction, because sequences are rendered in a browser shown
            # on a display device that already performs gamma correction
            pixels.append(cto8b(m.render(i, frame), 1.0))
        frames.append(pixels)
    return frames

def write_bin(fname, num_pixels, n_sec, frames):
    buf = b''
    for fr in frames:
        for i in fr:
            r, g, b = i
            buf += struct.pack('BBB', r, g, b)
    open(fname, 'wb').write(buf)

def regenerate(mod_name):
    try:
        log(f'regenerating sequence for {mod_name}')
        num_pixels = 60
        n_sec = 10
        frame_count = 60 * n_sec
        m = fx_load(num_pixels, mod_name)
        frames = render(num_pixels, frame_count, m)
        os.makedirs(seq_path, mode=0o777, exist_ok=True)
        write_bin(seq_path + '/' + mod_name + '.bin', num_pixels, n_sec, frames)
    except Exception:
        err(f'exception in effect "{mod_name}":\n' +
            ''.join(traceback.format_exception(*sys.exc_info())))

def seqgen_forever():
    global brightness, proc_name
    proc_name = 'seqgen'
    # We set brightness to a bit below 0xff so that effects that sparkle even
    # brighter (eg. the stars in Flag_US) can still be barely visible
    brightness = 0xe0
    while True:
        try:
            for fname in os.listdir(pkg_path):
                noext, ext = os.path.splitext(fname)
                if ext != '.py':
                    continue
                try:
                    mtime_source = os.path.getmtime(pkg_path + '/' + fname)
                except FileNotFoundError:
                    # The file may have just been deleted right after listdir()
                    continue
                try:
                    mtime_bin = os.path.getmtime(seq_path + '/' + noext + '.bin')
                except FileNotFoundError:
                    mtime_bin = 0
                if mtime_source > mtime_bin:
                    regenerate(noext)
        except KeyboardInterrupt:
            # handle Ctrl-C
            sys.exit(0)
        time.sleep(1)
