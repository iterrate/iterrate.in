#!/usr/bin/env python3
"""Builds the Iterrate company site (../docs/*.html) from the page texts below.

Edit the page bodies here, then run:  python3 build.py
Every page gets the same header, navigation and footer.
"""
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "docs"

NAV = [
    ("index.html", "Home"),
    ("saho.html", "Saho"),
    ("how-we-work.html", "How we work"),
    ("about.html", "About"),
    ("updates.html", "Updates"),
    ("company.html", "Company"),
    ("contact.html", "Contact"),
]

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="favicon.ico">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" href="fonts/crimson-pro-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="index.html"><img src="iterrate-logo.svg" alt="Iterrate" width="150" height="63"></a>
    <nav aria-label="Main"><ul class="nav">{nav}</ul></nav>
  </div>
</header>
<main id="main">
"""

FOOT = """</main>
<footer class="site-foot">
  <div class="wrap">
    <img src="iterrate-icon.svg" alt="" width="44" height="44">
    <div>
      <p><strong>Iterrate (OPC) Private Limited</strong> · CIN U85500KL2024OPC090447</p>
      <p>House No. KP 16/356, V.K. Koickal, Enikkara, Karakulam P.O., Thiruvananthapuram, Kerala 695564</p>
      <p><a href="mailto:contact@iterrate.in">contact@iterrate.in</a> · <a href="tel:+918412897977">+91 84128 97977</a></p>
      <p>Queries and grievances: Sangeeth Saji Varma, Director</p>
    </div>
    <ul>
      <li><a href="company.html#disclosures">Statutory disclosures</a></li>
      <li><a href="contact.html">Contact</a></li>
      <li>© 2026 Iterrate</li>
    </ul>
  </div>
</footer>
{scripts}</body>
</html>
"""

PAGES = {}

INSTITUTIONS = "a library, a college, a panchayat, a hospital"

# ---------------------------------------------------------------- Home
PAGES["index.html"] = ("Iterrate · Tools that belong to the places that use them",
"Iterrate builds Saho, an open, federated learning platform that any institution can run for itself.",
f"""
<div class="wrap">
  <div class="hero">
    <h1>Tools that <em>belong</em> to the places that use them.</h1>
    <p class="lede">Iterrate is a small company building Saho, an open, federated learning platform. Any institution ({INSTITUTIONS}) can run its own Saho, and learners own what they learn.</p>
    <div class="btns">
      <a class="btn primary" href="saho.html">Meet Saho</a>
      <a class="btn" href="how-we-work.html">How we work</a>
    </div>
  </div>

  <div class="now">
    <strong>Now</strong>
    <span>November 2026: Saho's architecture is settled and we're building its first test version.</span>
    <a href="updates.html">Updates</a>
  </div>

  <section>
    <div class="grid">
      <div class="tile leaf">
        <h3>Saho</h3>
        <p>A guide and a circle for people learning on their own, at any stage of life. For finding a direction, not cramming for one exam.</p>
        <a class="go" href="saho.html">What Saho is</a>
      </div>
      <div class="tile sky">
        <h3>Federated by design</h3>
        <p>Every institution can run its own Saho. They connect to each other, and nobody owns the whole network.</p>
        <a class="go" href="how-we-work.html">Our principles</a>
      </div>
      <div class="tile earth">
        <h3>Free to choose</h3>
        <p>People and institutions shouldn't depend on one platform or one AI model. Saho lets them choose, and run their own.</p>
        <a class="go" href="how-we-work.html">Why it matters</a>
      </div>
    </div>
  </section>
</div>

<div class="band">
  <div class="wrap">
    <p class="big"><em>Communities should own the tools they learn with.</em></p>
    <p>Keralam built its public libraries village by village, through people who wanted knowledge to be shared and run locally. We want the software of learning to work the same way: open source, run close to the people who use it, and answerable to them.</p>
    <p><a href="how-we-work.html">Read how we work</a></p>
  </div>
</div>
""")

# ---------------------------------------------------------------- Saho
PAGES["saho.html"] = ("Saho · Iterrate",
"Saho is an open, federated learning platform for self-learners, in Malayalam and English, run by the institutions that use it.",
f"""
<div class="wrap narrow">
  <section style="margin-top:40px">
    <span class="mark"></span>
    <h1>Saho</h1>
    <p class="lede">An open learning platform, in Malayalam and English. Saho is a guide and a circle: it helps you work out what to learn next, and finds you people to learn it with.</p>
    <p class="small">Saho is in development. Its own site will be <a href="https://saho.day">saho.day</a>.</p>
  </section>

  <section>
    <span class="mark"></span>
    <h2>Who it's for</h2>
    <p>Saho is for people learning on their own, at any stage of life or study. Think of a recent graduate doing part-time work, unsure of what comes next, who wants to explore their world, their skills and what's possible, at their own pace and in their own language.</p>
    <p class="quote">Saho is not a coaching app. It's for finding a direction, not cramming for a single exam.</p>
    <p>Institutions can use it too, for their own people. A hospital could run Saho to help its staff keep learning.</p>
  </section>

  <section>
    <span class="mark earth"></span>
    <h2>What it does</h2>
    <div class="grid two">
      <div class="tile leaf"><h3>A guide</h3><p>Talk things through in Malayalam, English or Manglish. The guide suggests paths and next steps. It doesn't lecture.</p></div>
      <div class="tile sky"><h3>Circles</h3><p>Small groups of learners who meet where they are, online and in person.</p></div>
      <div class="tile earth"><h3>Paths</h3><p>Learning paths shared between places, with credit to the people who made them.</p></div>
      <div class="tile leaf"><h3>Your record</h3><p>A record of what you've learned that belongs to you and goes with you.</p></div>
    </div>
  </section>

  <section>
    <span class="mark sky"></span>
    <h2>Places, not a platform</h2>
    <p>Any institution ({INSTITUTIONS}) can run its own Saho, which we call a <em>place</em>. Places talk to each other, so a learner at a village library can join a circle at a college nearby.</p>
    <p>Every learner has one home for their account and record. They decide what each place can see, and they can take that back. Private conversations with the guide stay at home.</p>
    <p>One instance can serve every library in a panchayat. A single person can also run their own.</p>
  </section>

  <section>
    <span class="mark"></span>
    <h2>Where it stands</h2>
    <p>Saho's architecture is settled and we're building a first test version. After that we plan a small pilot. Saho will be released as open-source software.</p>
    <p><a href="updates.html">See our updates</a> or <a href="contact.html">get in touch</a> if your institution would like to take part.</p>
  </section>
  <section>
    <span class="mark earth"></span>
    <h2>The name</h2>
    <p><em>Saho</em> is a call to work together, named for Sahodaran Ayyappan and his ideals of fraternity and equality.</p>
    <p><em>saho.day</em> reads as <em>sahoday</em>: rising together.</p>
  </section>
</div>
""")

# ---------------------------------------------------------------- How we work
PAGES["how-we-work.html"] = ("How we work · Iterrate",
"Iterrate's principles: federated, learner-owned, local first, open source, and free to choose your AI.",
"""
<div class="wrap narrow">
  <section style="margin-top:40px">
    <span class="mark"></span>
    <h1>How we work</h1>
    <p class="lede">We're a company, but we started Iterrate because of what we believe about learning and technology. These principles shape what we build.</p>
  </section>

  <ol class="principles">
    <li><h3>Federated, not central</h3><p>No single company, us included, should hold everyone's learning in one place. Institutions run their own instances, and those instances work together.</p></li>
    <li><h3>Learners own their record</h3><p>What you learn and say belongs to you. Places see only what you allow, and you can take that back.</p></li>
    <li><h3>Local first</h3><p>Malayalam and Manglish come first, not as an afterthought. Saho should run on modest hardware, close to the people who use it.</p></li>
    <li><h3>Open source</h3><p>The software will be open, so that anyone can inspect it, run it and improve it, and so that no one is locked in to us.</p></li>
    <li><h3>Free to choose your AI</h3><p>People and institutions shouldn't depend on a single platform or model. Saho works with whichever AI model a place chooses, including ones it runs itself. AI helps people think and find their way; it doesn't replace teachers, librarians or each other.</p></li>
  </ol>

  <section>
    <span class="mark sky"></span>
    <h2>Why now</h2>
    <p>Keralam aims to be a knowledge society. AI is changing what knowledge work looks like, and we want people here to learn how to use these tools in their work and lives on their own terms, without handing that over to a few distant platforms.</p>
  </section>

  <section>
    <span class="mark earth"></span>
    <h2>How Iterrate is paid</h2>
    <p>The basic platform is free for learners. Institutions pay for licences, setup, hosting and support. An institution can add its own courses or fees, and learners can pay for premium features beyond what their institution covers.</p>
    <p>We aim to price fairly and put any surplus back into the work.</p>
  </section>
</div>
""")

# ---------------------------------------------------------------- About
PAGES["about.html"] = ("About · Iterrate",
"About Iterrate (OPC) Private Limited.",
"""
<div class="wrap narrow">
  <section style="margin-top:40px">
    <span class="mark"></span>
    <h1>About Iterrate</h1>
    <p class="lede">Iterrate (OPC) Private Limited is a small company in Thiruvananthapuram, incorporated on 8 November 2024 and recognised as a startup by DPIIT and Kerala Startup Mission.</p>
  </section>

  <section>
    <span class="mark sky"></span>
    <h2>Who we are</h2>
    <p>Iterrate was founded by Sangeeth, its director. It is a one-person company for now. You can read more about Sangeeth at <a href="https://sangeethvarma.com">sangeethvarma.com</a>.</p>
  </section>

  <section>
    <span class="mark"></span>
    <h2>What we do</h2>
    <p>We build <a href="saho.html">Saho</a>, and we help institutions set it up, run it and look after it. Read <a href="how-we-work.html">how we work</a>.</p>
  </section>

  <section class="strip">
    <img src="iterrate-logo.svg" alt="The Iterrate logo" width="200" height="84">
    <div>
      <p><strong>The name</strong> is <em>i + terra + te</em>: a person, and the earth they stand on. Together it reads <em>iterate</em>: try, reflect, try again.</p>
      <p><strong>The logo</strong> draws that loop, with a sky line over the top and an earth line underneath, and a green arrow that breaks out at the end. Each turn of learning carries you out into the world.</p>
    </div>
  </section>
</div>
""")

# ---------------------------------------------------------------- Updates
PAGES["updates.html"] = ("Updates · Iterrate",
"Iterrate's milestones, newest first.",
"""
<div class="wrap narrow">
  <section style="margin-top:40px">
    <span class="mark"></span>
    <h1>Milestones</h1>
  </section>

  <ol class="timeline">
    <li><time datetime="2026-11">November 2026</time><h3>Saho's architecture settled; first test version under way</h3></li>
    <li class="past"><time datetime="2025-04">April 2025</time><h3>Obtained startup recognition from DPIIT and Kerala Startup Mission</h3></li>
    <li class="past"><time datetime="2024-11-08">November 2024</time><h3>Iterrate incorporated in Thiruvananthapuram</h3></li>
  </ol>

  <div class="subscribe">
    <h3>Get updates by email</h3>
    <p class="small" style="margin:0">Write to <a href="mailto:contact@iterrate.in?subject=Updates">contact@iterrate.in</a> with "Updates" in the subject. We'll email you at each milestone, and nothing else. Reply "Stop" at any time.</p>
  </div>
</div>
""")

# ---------------------------------------------------------------- Company
PAGES["company.html"] = ("Company information and disclosures · Iterrate",
"Registered details and statutory disclosures of Iterrate (OPC) Private Limited, including annual returns.",
"""
<div class="wrap narrow">
  <section style="margin-top:40px">
    <span class="mark earth"></span>
    <h1>Company information</h1>
  </section>

  <section>
    <div class="card">
      <dl class="facts">
        <dt>Name</dt><dd>Iterrate (OPC) Private Limited</dd>
        <dt>Corporate Identity Number</dt><dd>U85500KL2024OPC090447</dd>
        <dt>Registered office</dt><dd>House No. KP 16/356, V.K. Koickal, Enikkara,<br>Karakulam P.O., Thiruvananthapuram,<br>Kerala 695564, India</dd>
        <dt>Telephone</dt><dd><a href="tel:+918412897977">+91 84128 97977</a></dd>
        <dt>Email</dt><dd><a href="mailto:contact@iterrate.in">contact@iterrate.in</a></dd>
        <dt>Queries and grievances</dt><dd>Sangeeth Saji Varma, Director<br><a href="mailto:contact@iterrate.in">contact@iterrate.in</a></dd>
        <dt>GSTIN</dt><dd>32AAHCI9117Q1Z3</dd>
        <dt>DPIIT recognition</dt><dd>DIPP198219</dd>
        <dt>Kerala Startup Mission</dt><dd>DIPP198219/2024/KSUM4141</dd>
      </dl>
    </div>
  </section>

  <section id="disclosures">
    <span class="mark"></span>
    <h2>Statutory disclosures</h2>
    <p>Annual returns, published under section 92(3) of the Companies Act, 2013.</p>
    <div class="card">
      <table class="docs">
        <thead><tr><th>Document</th><th>Financial year</th><th></th></tr></thead>
        <tbody>
          <tr><td>Annual return (Form MGT-7A)</td><td>2025-26</td><td><a href="annual-returns/Iterrate-MGT-7A-FY2025-26.pdf">PDF</a></td></tr>
          <tr><td>Annual return (Form MGT-7A)</td><td>2024-25</td><td><a href="annual-returns/Iterrate-MGT-7A-FY2024-25.pdf">PDF</a></td></tr>
        </tbody>
      </table>
    </div>
  </section>
</div>
""")

# ---------------------------------------------------------------- Contact
PAGES["contact.html"] = ("Contact · Iterrate",
"How to contact Iterrate (OPC) Private Limited.",
"""
<div class="wrap narrow">
  <section style="margin-top:40px">
    <span class="mark sky"></span>
    <h1>Get in touch</h1>
    <p class="lede">Does your institution want to run Saho, or would you like to help build it? We'd like to hear from you. Write in Malayalam or English.</p>
  </section>

  <section>
    <div class="grid two">
      <div class="tile leaf">
        <h3>Email</h3>
        <p><a href="mailto:contact@iterrate.in">contact@iterrate.in</a><br>The best way to reach us.</p>
      </div>
      <div class="tile sky">
        <h3>Phone</h3>
        <p><a href="tel:+918412897977">+91 84128 97977</a></p>
      </div>
      <div class="tile earth">
        <h3>Post</h3>
        <p>Iterrate (OPC) Private Limited<br>House No. KP 16/356, V.K. Koickal, Enikkara,<br>Karakulam P.O., Thiruvananthapuram,<br>Kerala 695564</p>
      </div>
      <div class="tile leaf">
        <h3>Queries and grievances</h3>
        <p>Sangeeth, Director<br><a href="mailto:contact@iterrate.in">contact@iterrate.in</a></p>
      </div>
    </div>
  </section>
</div>
""")

SCRIPTS = {"index.html": '<script src="{loop}"></script>\n'}


def asset(name):
    """Link to a file with a short content hash, so browsers fetch it again after each change."""
    import hashlib
    h = hashlib.sha1((SITE / name).read_bytes()).hexdigest()[:8]
    return f"{name}?v={h}"


def build():
    for fname, (title, desc, body) in PAGES.items():
        nav = "".join(
            f'<li><a href="{href}"{" aria-current=\"page\"" if href == fname else ""}>{label}</a></li>'
            for href, label in NAV
        )
        html = HEAD.replace('href="style.css"', f'href="{asset("style.css")}"').format(title=title, desc=desc, nav=nav) + body + FOOT.format(scripts=SCRIPTS.get(fname, "").replace("{loop}", asset("loop.js")))
        (SITE / fname).write_text(html, encoding="utf-8")
        print("wrote", fname)


if __name__ == "__main__":
    build()
