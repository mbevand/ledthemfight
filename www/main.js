var n_pixels = 60;
var n_sec = 10;
var sequences = {};

function get(url, handler, is_binary) {
    var req = new XMLHttpRequest();
    req.open("GET", url);
    if (is_binary)
	req.responseType = "arraybuffer";
    req.onload = handler;
    req.send();
}

function post(url, data_to_send) {
    var req = new XMLHttpRequest();
    req.open("POST", url);
    req.setRequestHeader("Content-Type", "application/json");
    req.send(JSON.stringify(data_to_send));
}

function button(e) {
    post("/button", { id: e.target.id });
}

function effect(e) {
    // When clicking a <label> containing an <input>, it fires two events,
    // one for the label which as an id and one for the input which doesn't.
    // We ignore the second one
    if (!e.target.id)
	return ;
    post("/effect", { id: e.target.id });
}

function drawCanvasOne(index, canvas) {
    if (!(canvas.id in sequences))
        return;
    seq = sequences[canvas.id].seq;
    var ctx = canvas.getContext("2d");
    var buf = new ImageData(canvas.width, canvas.height);
    for (var i = 0; i < canvas.width * canvas.height; i++) {
        base = 3 * canvas.width * sequences[canvas.id].frame + i * 3;
        base %= seq.length;
        r = seq[base + 0];
        g = seq[base + 1];
        b = seq[base + 2];
        buf.data.set([r, g, b, 255], i * 4);
    }
    ctx.putImageData(buf, 0, 0);
    sequences[canvas.id].frame += 1;
}

function drawCanvas() {
    $("canvas").each(drawCanvasOne);
}

function initCanvasOne(index, canvas) {
    canvas.width = n_pixels;
    canvas.height = 1;
    name = canvas.id.substr(4);
    get('/sequence/' + name + '.bin', function() {
        sequences[canvas.id] = { seq: new Uint8Array(this.response), frame: 0 };
    }, true);
}

function initCanvas() {
    $("canvas").each(initCanvasOne);
}

get('/get/effects', function() {
    resp = JSON.parse(this.responseText);
    const s = '' +
	resp['effects'].map((fx) =>
	    '<label id="' + fx + '">' +
	    '<input type="radio" name="g1" />' +
            '<canvas id="can_' + fx + '"></canvas>' +
            fx +
	    '</label>\n').join('');
    $("#effects").html(s);
    $("#effects > label").on("click", effect);
    initCanvas();
    // render at 60 fps to match the fps we aim at on the physical LED string
    setInterval(drawCanvas, 1000 / 60);
});
$("#pseudo_effects > label").on("click", button);
$("button").on("click", button);
