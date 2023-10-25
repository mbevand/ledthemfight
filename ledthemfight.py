#!/usr/bin/env python3

import argparse, os, json, urllib.parse
from multiprocessing import Process, Queue
from http.server import HTTPServer, SimpleHTTPRequestHandler

conf_file = '/etc/ledthemfight.conf'
conf = None
worker_q = Queue()

def conf_save():
    dat = json.dumps(conf, indent=2)
    open(conf_file, 'w').write(dat)

def update_worker_conf():
    worker_q.put(['/initial_setup', conf])

class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='www', **kwargs)

    def end_headers(self):
        # 'no-cache' means client CAN cache but must revalidate the cached
        # response every reuse, which is what we want as files often change
        # (eg. the sequence binary files)
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def parse_form(self):
        assert self.headers['Content-Type'] == \
                'application/x-www-form-urlencoded'
        cl = int(self.headers['Content-Length'])
        dat = self.rfile.read(cl).decode()
        return urllib.parse.parse_qs(dat)

    def parse_json(self):
        assert self.headers['Content-Type'] == 'application/json'
        cl = int(self.headers['Content-Length'])
        dat = self.rfile.read(cl).decode()
        return json.loads(dat)

    def write_data(self, data):
        self.wfile.write(data.encode())

    def get_data(self, path):
        if path == '/get/effects':
            dname = os.path.dirname(__file__) + '/effect_library'
            resp = { 'effects' :
            [x[:-3] for x in sorted(os.listdir(dname)) if x.endswith('.py')] }
        else:
            return self.send_error(404)
        self.send_response(200)
        self.end_headers()
        self.write_data(json.dumps(resp) + '\n')

    def do_GET(self):
        if self.path == '/':
            if not conf['set_up']:
                self.send_response(302)
                self.send_header('Location', '/welcome.html')
                self.end_headers()
                return
            self.path = '/index.html'
        if self.path.startswith('/get/'):
            return self.get_data(self.path)
        # whitelist of URL paths
        if not self.path.startswith('/sequence/') and \
           self.path not in (
                '/cash.js',
                '/index.html',
                '/main.css',
                '/main.js',
                '/welcome.html',
                ):
            return self.send_error(404)
        return super().do_GET()

    def do_POST(self):
        if self.path == '/initial_setup':
            form = self.parse_form()
            conf.update({
                'set_up': True,
                'name': form.get('name')[0],
                'nr_led_strings': int(form.get('nr_led_strings')[0]),
                'num_pixels': int(form.get('num_pixels')[0]),
                'inverted': 'inverted' in form,
                })
            conf_save()
            update_worker_conf()
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
        elif not conf['set_up']:
            self.send_error(500, 'Server is not set up')
        elif self.path not in ('/button', '/effect'):
            self.send_error(404)
        else:
            j = self.parse_json()
            worker_q.put([self.path, j['id']])
            self.send_response(200)
            self.end_headers()

def worker_process(q):
    import worker_led
    worker_led.run_forever(q)

def sequence_generator_process():
    import worker_led
    worker_led.seqgen_forever()

def main():
    global conf
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=80)
    args = parser.parse_args()
    try:
        conf = json.load(open(conf_file))
        update_worker_conf()
    except FileNotFoundError:
        conf = { 'set_up': False }
    # start worker process
    Process(target=worker_process, args=(worker_q,)).start()
    # start sequence generator
    Process(target=sequence_generator_process, args=()).start()
    # start web server
    HTTPServer.allow_reuse_address = True
    httpd = HTTPServer(('', args.port), MyHandler)
    print(f'Web server running on port {args.port}/tcp')
    httpd.serve_forever()

if __name__ == '__main__':
    main()
