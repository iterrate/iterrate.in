// Draws the logo's loop around the home page headline, sized to the box.
// Same parts as the logo: sky line over the top ending in a half arrowhead,
// green uprights (the t and the a), earth line underneath kicking up into the
// right upright, and the green exit arrow carrying on out to the right.
(function () {
  var hero = document.querySelector('.hero');
  if (!hero) return;
  var NS = 'http://www.w3.org/2000/svg';
  var svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('class', 'loop draw');
  svg.setAttribute('aria-hidden', 'true');
  hero.insertBefore(svg, hero.firstChild);

  var parts = [
    ['earth', 0], ['leaf', 0.35], ['sky', 0.55], ['leaf', 0.9], ['leaf', 1.1]
  ];
  var paths = parts.map(function (p) {
    var el = document.createElementNS(NS, 'path');
    el.setAttribute('class', p[0]);
    el.style.setProperty('--delay', p[1] + 's');
    svg.appendChild(el);
    return el;
  });

  function draw() {
    var w = hero.clientWidth, h = hero.clientHeight;
    svg.setAttribute('viewBox', '0 0 ' + w + ' ' + h);
    var small = w < 520;
    var xl = small ? 12 : 30;            // left upright (the t)
    var xr = w - (small ? 24 : 70);      // right upright (the a)
    var top = 4, bot = h - 16;           // sky line, earth line
    var r = 14, a = small ? 10 : 13;     // corner radius, arrowhead size
    var kick = small ? 22 : 30;          // earth line's diagonal kick

    // earth: from outside the loop on the left, under everything, kicking up into the right upright
    var kx = xr - 6, ky = bot - kick;
    paths[0].setAttribute('d',
      'M0 ' + bot + ' H' + (kx - kick) + ' L' + kx + ' ' + ky + ' M' + kx + ' ' + ky + ' H' + (kx - a - 4));
    // left upright: down from under the sky arrowhead, curving into the earth line like the top-right corner
    paths[1].setAttribute('d', 'M' + xl + ' ' + (top + 40) + ' V' + (bot - r) + ' Q' + xl + ' ' + bot + ' ' + (xl + r) + ' ' + bot);
    // sky: up from the right upright, across the top, down into the left upright with a half arrowhead
    paths[2].setAttribute('d',
      'M' + xr + ' ' + (top + 34) + ' V' + (top + r) + ' Q' + xr + ' ' + top + ' ' + (xr - r) + ' ' + top +
      ' H' + (xl + r) + ' Q' + xl + ' ' + top + ' ' + xl + ' ' + (top + r) + ' V' + (top + 26) +
      ' L' + (xl + a) + ' ' + (top + 26 - a));
    // right upright
    paths[3].setAttribute('d', 'M' + xr + ' ' + (top + 50) + ' V' + (ky - 12));
    // exit arrow
    var ex = w - 4;
    paths[4].setAttribute('d',
      'M' + (kx + 12) + ' ' + bot + ' H' + ex + ' M' + (ex - a) + ' ' + (bot - a) + ' L' + ex + ' ' + bot + ' L' + (ex - a) + ' ' + (bot + a));

    paths.forEach(function (p) {
      p.style.setProperty('--len', Math.ceil(p.getTotalLength()) + 1);
    });
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
