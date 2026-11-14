// Draws the logo's loop around the home page headline, sized to the box.
// Same parts as the logo: an earth line coming in from the left and kicking up,
// green uprights (the a and the t), a sky line over the top ending in a half
// arrowhead, and a green exit arrow breaking out to the right.
// On load the loop draws itself in the order it reads, one line after another:
// earth -> right upright (up) -> sky (across and down) -> left upright (down and
// round the corner) -> exit arrow out of the loop.
(function () {
  var hero = document.querySelector('.hero');
  if (!hero) return;
  var NS = 'http://www.w3.org/2000/svg';
  var svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('class', 'loop draw');
  svg.setAttribute('aria-hidden', 'true');
  hero.insertBefore(svg, hero.firstChild);

  function line(cls) {
    var el = document.createElementNS(NS, 'path');
    el.setAttribute('class', cls);
    svg.appendChild(el);
    return el;
  }
  var earth = line('earth');
  var rightUp = line('leaf');
  var sky = line('sky');
  // A paper-coloured line under the left green line, 4px wider, cuts a 2px gap in the
  // earth line that follows the green curve exactly (on both sides of the corner).
  var knock = line('knock');
  var leftDown = line('leaf');
  var exit = line('leaf');
  var exitBarb = line('leaf');   // second barb of the exit arrowhead

  var TOTAL = 2.2;   // s, the whole loop, whatever the screen size
  var PAUSE = 0.06;  // s, a beat at each gap where one line hands over to the next

  var timed = false;
  function draw() {
    var w = hero.clientWidth, h = hero.clientHeight;
    svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
    var small = w < 520;
    var xl = small ? 12 : 30;            // left upright (the t)
    var xr = w - (small ? 24 : 70);      // right upright (the a)
    var top = 4, bot = h - 16;           // sky line, earth line
    var r = 14, a = small ? 10 : 13;     // corner radius, arrowhead size
    var kick = small ? 22 : 30;          // earth line's diagonal kick
    var g = 10;                          // gap between line centres: 5px visible

    var kx = xr - 6, ky = bot - kick;
    var skyStart = top + 34, skyEnd = top + 26;
    var ex = w - 4, exStart = kx - kick + g * Math.SQRT2;

    // earth: in from the left, along the bottom, kicking up, then its half arrowhead
    earth.setAttribute('d', 'M0 ' + bot + ' H' + (kx - kick) + ' L' + kx + ' ' + ky + ' H' + (kx - a - 4));
    // right upright, drawn upwards
    rightUp.setAttribute('d', 'M' + xr + ' ' + (ky - g) + ' V' + (skyStart + g));
    // sky: up, across the top to the left, down, and its half arrowhead
    sky.setAttribute('d',
      'M' + xr + ' ' + skyStart + ' V' + (top + r) + ' Q' + xr + ' ' + top + ' ' + (xr - r) + ' ' + top +
      ' H' + (xl + r) + ' Q' + xl + ' ' + top + ' ' + xl + ' ' + (top + r) + ' V' + skyEnd +
      ' L' + (xl + a) + ' ' + (skyEnd - a));
    // left upright, drawn downwards and round the corner
    var leftD = 'M' + xl + ' ' + (skyEnd + g) + ' V' + (bot - r) + ' Q' + xl + ' ' + bot + ' ' + (xl + r) + ' ' + bot;
    leftDown.setAttribute('d', leftD);
    knock.setAttribute('d', leftD);
    // exit: out to the right, then one barb continuous with the line, and the other barb
    exit.setAttribute('d', 'M' + exStart + ' ' + bot + ' H' + ex + ' L' + (ex - a) + ' ' + (bot - a));
    exitBarb.setAttribute('d', 'M' + ex + ' ' + bot + ' L' + (ex - a) + ' ' + (bot + a));

    // Timing: each line starts when the one before it ends; constant speed throughout.
    var total = [earth, rightUp, sky, leftDown, exit, exitBarb]
      .reduce(function (sum, el) { return sum + el.getTotalLength(); }, 0);
    var SPEED = total / (TOTAL - 4 * PAUSE);
    var t = 0;
    function time(el, start) {
      var len = el.getTotalLength();
      var L = Math.ceil(len) + 1;
      // Plain numbers only (no calc() in SVG dash properties: Safari ignores it).
      el.style.setProperty('--dash', L + ' ' + (L + 10));
      el.style.setProperty('--off', String(L + 6));
      if (!timed) {   // set timing once, so a redraw (fonts loading, resize) doesn't restart it
        el.style.setProperty('--delay', start.toFixed(3) + 's');
        el.style.setProperty('--dur', (len / SPEED).toFixed(3) + 's');
      }
      return start + len / SPEED;
    }
    t = time(earth, t) + PAUSE;
    t = time(rightUp, t) + PAUSE;
    t = time(sky, t) + PAUSE;
    time(knock, t);
    t = time(leftDown, t) + PAUSE;
    var exitLineEnd = t + (ex - exStart) / SPEED;
    time(exit, t);
    time(exitBarb, exitLineEnd);
    timed = true;
  }
  draw();
  // Redraw whenever the box changes size (fonts loading, window resizing).
  var first = true;
  new ResizeObserver(function () {
    if (first) { first = false; return; }
    draw();
  }).observe(hero);
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () { draw(); });
  }
})();
