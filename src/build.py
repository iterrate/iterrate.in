#!/usr/bin/env python3
"""Builds the Iterrate company site (../docs/*.html) from the page texts below.

Edit the page bodies here, then run:  python3 build.py
Every page gets the same header, navigation and footer.
"""
import datetime
import hashlib
import json
import subprocess
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "docs"
BASE = "https://iterrate.in/"
YEAR = datetime.date.today().year

NAV = [
    ("./", "Home"),
    ("saho.html", "Saho"),
    ("how-we-work.html", "How we work"),
    ("about.html", "About"),
    ("updates.html", "Updates"),
    ("company.html", "Company"),
    ("contact.html", "Contact"),
]

HEAD = """<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Iterrate">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{base}share.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="The Iterrate logo and the line: Tools that belong to the places that use them.">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F6F3EA" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#282D2A" media="(prefers-color-scheme: dark)">
<meta name="darkreader-lock">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" href="iterrate-icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="fonts/crimson-pro-latin.woff2" as="font" type="font/woff2" crossorigin>
{extra_head}
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap">
    <a class="brand" href="./"><picture><source srcset="iterrate-logo-dark.svg" media="(prefers-color-scheme: dark)"><img src="iterrate-logo.svg" alt="Iterrate home" width="150" height="63"></picture></a>
    <nav aria-label="Main"><ul class="nav">{nav}</ul></nav>
    <script>(function(){{var n=document.querySelector('.nav'),c=n&&n.querySelector('[aria-current]');if(c&&n.scrollWidth>n.clientWidth)n.scrollLeft=c.offsetLeft-(n.clientWidth-c.offsetWidth)/2;}})();</script>
  </div>
</header>
<main id="main">
"""

FOOT = """</main>
<footer class="site-foot">
  <div class="wrap">
    <picture><source srcset="iterrate-icon-dark.svg" media="(prefers-color-scheme: dark)"><img src="iterrate-icon.svg" alt="" width="44" height="44"></picture>
    <div>
      <p><strong>Iterrate (OPC) Private Limited</strong> · CIN U85500KL2024OPC090447</p>
      <p>House No. KP 16/356, V.K. Koickal, Enikkara, Karakulam P.O., Thiruvananthapuram, Kerala 695564, India</p>
      <p><a href="mailto:contact@iterrate.in">contact@iterrate.in</a> · <a href="tel:+918412897977">+91&nbsp;84128&nbsp;97977</a></p>
      <p>Queries and grievances: Sangeeth Saji Varma, Director, <a href="mailto:sangeeth@iterrate.in">sangeeth@iterrate.in</a></p>
    </div>
    <ul>
      <li><a href="company.html#disclosures">Statutory disclosures</a></li>
      <li><a href="contact.html">Contact</a></li>
      <li><a href="contact.html#privacy">Privacy</a></li>
      <li>© {year} Iterrate</li>
    </ul>
  </div>
</footer>
{scripts}</body>
</html>
"""

PAGES = {}

# Milestones, newest first: (datetime, shown date, heading). Home's "Now" strip shows the first one.
MILESTONES = [
    ("2026-11", "November 2026", "Saho's architecture settled; first test version under way"),
    ("2025-04", "April 2025", "Startup recognition from DPIIT (Startup India) and Kerala Startup Mission obtained"),
    ("2024-11-08", "November 2024", "Iterrate incorporated in Thiruvananthapuram"),
]
NOW = MILESTONES[0]
TIMELINE = "\n".join(
    f'    <li{" class=\"past\"" if i else ""}><time datetime="{d}">{shown}</time><h2>{head}</h2></li>'
    for i, (d, shown, head) in enumerate(MILESTONES)
)

# Annual returns: every file named Iterrate-MGT-7A-FY2025-26.pdf (and so on) in docs/annual-returns/
# gets a row on the Company page, newest first. To publish a new year, drop the attachment-free
# copy into that folder with that name and run this script.
def annual_return_rows():
    rows = []
    for f in sorted((SITE / "annual-returns").glob("Iterrate-MGT-7A-FY*.pdf"), reverse=True):
        fy = re.search(r"FY(\d{4}-\d{2})", f.name).group(1)
        rows.append(f'          <tr><td>Annual return (Form MGT-7A)</td><td>{fy}</td>'
                    f'<td><a href="annual-returns/{f.name}">PDF<span class="vh">, annual return {fy}</span></a></td></tr>')
    return "\n".join(rows)

INSTITUTIONS = "a library, a college, a panchayat, a hospital"
PHONE = '<a href="tel:+918412897977">+91&nbsp;84128&nbsp;97977</a>'   # non-breaking spaces: never split across lines
# The registered address; each line is its own span so it can wrap naturally on phones (R2).
ADDRESS = ('<span class="line">House No. KP 16/356, V.K. Koickal, Enikkara, </span>'
           '<span class="line">Karakulam P.O., Thiruvananthapuram, </span>'
           '<span class="line">Kerala 695564, India</span>')

# ---------------------------------------------------------------- Home
PAGES["index.html"] = ("Iterrate · Tools that belong to the places that use them",
"Iterrate builds Saho, an open, federated learning platform that any institution can run for itself.",
f"""
<div class="wrap">
  <div class="hero">
    <h1>Tools that <em>belong</em> to the places that use them.</h1>
    <p class="lede">Iterrate is a small company building Saho, an open, federated learning platform.</p>
    <p class="lede">Any institution ({INSTITUTIONS}) can run its own Saho, and learners keep what they learn, wherever they go.</p>
    <div class="btns">
      <a class="btn primary" href="saho.html">Meet Saho</a>
      <a class="btn" href="how-we-work.html">How we work</a>
    </div>
  </div>

  <div class="now">
    <strong>Now</strong>
    <span>{NOW[1]}: {NOW[2]}.</span>
    <a href="updates.html">Updates</a>
  </div>

  <section aria-label="What we're building">
    <div class="grid">
      <div class="tile leaf">
        <h2>Saho</h2>
        <p>A guide and a circle for people learning on their own, at any stage of life. For finding a direction, not cramming for one exam.</p>
        <a class="go" href="saho.html">What Saho is</a>
      </div>
      <div class="tile sky">
        <h2>Federated by design</h2>
        <p>Every institution can run its own Saho. They connect to each other, and nobody owns the whole network.</p>
        <a class="go" href="how-we-work.html#federated">Our principles</a>
      </div>
      <div class="tile earth">
        <h2>Control over your AI</h2>
        <p>People and institutions shouldn't depend on one platform or one AI model. Saho lets them choose, and run their own.</p>
        <a class="go" href="how-we-work.html#ai">Why it matters</a>
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
  <section class="page-top">
    <span class="mark"></span>
    <h1>Saho</h1>
    <p class="lede">An open learning platform, in Malayalam and English. Saho is a guide and a circle: it helps you work out what to learn next, and finds you people to learn it with.</p>
    <p class="small">Saho is in development. Its own site, saho.day, is coming soon.</p>
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
      <div class="tile leaf"><h3>A guide</h3><p>Talk things through in Malayalam, English or a mix of Malayalam and English. The guide suggests paths and next steps. It doesn't lecture.</p></div>
      <div class="tile sky"><h3>Circles</h3><p>Small groups of learners who meet where they are, online and in person.</p></div>
      <div class="tile earth"><h3>Paths</h3><p>Learning paths shared between places, with credit to the people who made them.</p></div>
      <div class="tile leaf"><h3>Your record</h3><p>A record of what you've learned that belongs to you and goes with you.</p></div>
    </div>
  </section>

  <section>
    <span class="mark sky"></span>
    <h2>Places, not a platform</h2>
    <p>Any institution ({INSTITUTIONS}) can run its own Saho, which we call a <em>place</em>. Places talk to each other, so a learner at a village library can join a circle at a college nearby.</p>
    <p>Every learner has one home place for their account and record. They decide what each place can see, and they can take that back. Private conversations with the guide stay in their home place.</p>
    <p>One Saho can serve every library in a panchayat. A single person can also run their own.</p>
  </section>

  <section>
    <span class="mark"></span>
    <h2>Where it stands</h2>
    <p>Saho is being built now, and a small pilot comes next. It will be released as open-source software.</p>
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
"Iterrate's principles: federated, learner-owned, local first, open source, and control over your AI.",
"""
<div class="wrap narrow">
  <section class="page-top">
    <span class="mark"></span>
    <h1>How we work</h1>
    <p class="lede">We started Iterrate because of our belief in the power of learning and technology. These principles shape what we build.</p>
  </section>

  <ol class="principles">
    <li id="federated"><h2>Federated, not centralised</h2><p>No single company, including us, should hold everyone's learning in one place. Institutions run their own copies of Saho, called instances (we call each one a place), and those instances work together.</p></li>
    <li id="records"><h2>Learners own their records</h2><p>What you learn and say belongs to you. Places see only what you allow, and you can take that back.</p></li>
    <li id="local-first"><h2>Local first</h2><p>Malayalam, and a mix of Malayalam and English, come first, not as an afterthought. Saho should run on modest hardware, close to the people who use it.</p></li>
    <li id="open-source"><h2>Open source</h2><p>The software will be open, so that anyone can inspect it, run it and improve it, and so that no one is tied to us.</p></li>
    <li id="ai"><h2>Control over your AI</h2><p>People and institutions shouldn't depend on a single platform or model. Saho works with whichever AI model a place chooses, including ones it runs itself.</p><p>AI helps people think and find their way; it doesn't replace teachers, librarians or each other.</p></li>
  </ol>

  <section>
    <span class="mark sky"></span>
    <h2>Why now</h2>
    <p>Keralam aims to be a knowledge society. AI is changing what knowledge work looks like, and we want people here to learn how to use these tools in their work and lives on their own terms, without handing that over to a few distant platforms.</p>
  </section>

  <section>
    <span class="mark earth"></span>
    <h2>How Iterrate is paid</h2>
    <p>The basic platform is free for learners. Institutions pay for licences, setup, hosting and support.</p>
    <p>An institution can add its own courses or fees, and learners can pay for premium features beyond what their institution covers.</p>
    <p>We aim to price fairly and put any surplus back into the work.</p>
  </section>
</div>
""")

# ---------------------------------------------------------------- About
PAGES["about.html"] = ("About · Iterrate",
"Iterrate (OPC) Private Limited is a small company in Thiruvananthapuram, founded by Sangeeth in 2024, building Saho, an open, federated learning platform.",
"""
<div class="wrap narrow">
  <section class="page-top">
    <span class="mark"></span>
    <h1>About Iterrate</h1>
    <p class="lede">Iterrate (OPC) Private Limited is a small company in Thiruvananthapuram, incorporated on 8 November 2024 and recognised as a startup by DPIIT (Startup India) and Kerala Startup Mission.</p>
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
    <picture><source srcset="iterrate-logo-dark.svg" media="(prefers-color-scheme: dark)"><img src="iterrate-logo.svg" alt="The Iterrate logo" width="200" height="84"></picture>
    <div>
      <p><strong>The name</strong> is <em>i + terra + te</em>: a person and the earth they stand on, with <em>te</em> completing the word. Together it reads <em>iterate</em>: try, reflect, try again.</p>
      <p><strong>The logo</strong> draws that loop, with a sky line over the top and an earth line underneath, and a green arrow that breaks out at the end. Each turn of learning carries you out into the world.</p>
    </div>
  </section>
</div>
""")

# ---------------------------------------------------------------- Updates
PAGES["updates.html"] = ("Updates · Iterrate",
"Milestones in building Iterrate and Saho, newest first, and how to get an email at each new one.",
f"""
<div class="wrap narrow">
  <section class="page-top">
    <span class="mark"></span>
    <h1>Milestones</h1>
  </section>

  <ol class="timeline">
{TIMELINE}
  </ol>

  <div class="subscribe">
    <h2>Get updates by email</h2>
    <p class="small">Write to <a href="mailto:contact@iterrate.in?subject=Updates">contact@iterrate.in</a> with "Updates" in the subject. We'll email you at each milestone, and nothing else. Reply "Stop" at any time.</p>
    <p class="small">We use your address only for these emails and never share it. <a href="contact.html#privacy">Privacy</a></p>
  </div>
</div>
""")

# ---------------------------------------------------------------- Company
PAGES["company.html"] = ("Company information and disclosures · Iterrate",
"Registered details and statutory disclosures of Iterrate (OPC) Private Limited, including annual returns.",
f"""
<div class="wrap narrow">
  <section class="page-top">
    <span class="mark earth"></span>
    <h1>Company information</h1>
  </section>

  <section>
    <div class="card">
      <dl class="facts">
        <dt>Name</dt><dd>Iterrate (OPC) Private Limited</dd>
        <dt>Corporate Identity Number</dt><dd>U85500KL2024OPC090447</dd>
        <dt>Registered office</dt><dd class="addr">{ADDRESS}</dd>
        <dt>Telephone</dt><dd>{PHONE}</dd>
        <dt>Email</dt><dd><a href="mailto:contact@iterrate.in">contact@iterrate.in</a></dd>
        <dt>Queries and grievances</dt><dd>Sangeeth Saji Varma, Director<br><a href="mailto:sangeeth@iterrate.in">sangeeth@iterrate.in</a></dd>
        <dt>GSTIN</dt><dd>32AAHCI9117Q1Z3</dd>
        <dt>DPIIT (Startup India) recognition</dt><dd>DIPP198219</dd>
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
        <caption class="vh">Annual returns of Iterrate (OPC) Private Limited</caption>
        <thead><tr><th scope="col">Document</th><th scope="col">Financial year</th><th scope="col"><span class="vh">File</span></th></tr></thead>
        <tbody>
{annual_return_rows()}
        </tbody>
      </table>
    </div>
  </section>
</div>
""")

# ---------------------------------------------------------------- Contact
PAGES["contact.html"] = ("Contact · Iterrate",
"Contact Iterrate by email, phone or post. Includes our privacy note: no cookies, no analytics.",
f"""
<div class="wrap narrow">
  <section class="page-top">
    <span class="mark sky"></span>
    <h1>Get in touch</h1>
    <p class="lede">Does your institution want to run Saho, or would you like to help build it? We'd like to hear from you.</p>
  </section>

  <section>
    <div class="grid two">
      <div class="tile leaf">
        <h2>Email</h2>
        <p><a href="mailto:contact@iterrate.in">contact@iterrate.in</a><br>The best way to reach us.</p>
      </div>
      <div class="tile sky">
        <h2>Phone</h2>
        <p>{PHONE}</p>
      </div>
      <div class="tile earth">
        <h2>Post</h2>
        <p class="addr">Iterrate (OPC) Private Limited<br>{ADDRESS}</p>
      </div>
      <div class="tile leaf">
        <h2>Sangeeth, Director</h2>
        <p><a href="mailto:sangeeth@iterrate.in">sangeeth@iterrate.in</a></p>
      </div>
    </div>
  </section>

  <section id="privacy">
    <span class="mark earth"></span>
    <h2>Privacy</h2>
    <p>This site sets no cookies and uses no analytics or trackers. It is hosted on GitHub Pages, and GitHub logs visitors' IP addresses for security (see <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub's privacy statement</a>). Our email is handled by Zoho Mail.</p>
    <p>If you write to us, we use your email address and what you tell us only to reply. If you ask for updates, we use your address only to send milestone emails. We don't share it with anyone, and we delete it when you ask. Write to <a href="mailto:contact@iterrate.in">contact@iterrate.in</a> to see, correct or delete what we hold about you.</p>
  </section>
</div>
""")

SCRIPTS = {"index.html": '<script src="{loop}"></script>\n'}

# Extra lines in <head> for some pages. Home: preload the italic font ("belong" is at the top),
# and describe the company to search engines (structured data, schema.org).
ORG = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Iterrate",
    "legalName": "Iterrate (OPC) Private Limited",
    "url": BASE,
    "logo": BASE + "icon-512.png",
    "email": "contact@iterrate.in",
    "telephone": "+91 84128 97977",
    "foundingDate": "2024-11-08",
    "founder": {"@type": "Person", "name": "Sangeeth", "url": "https://sangeethvarma.com"},
    "address": {"@type": "PostalAddress",
                "streetAddress": "House No. KP 16/356, V.K. Koickal, Enikkara, Karakulam P.O.",
                "addressLocality": "Thiruvananthapuram", "addressRegion": "Kerala",
                "postalCode": "695564", "addressCountry": "IN"},
}
EXTRA_HEAD = {
    "index.html": '<link rel="preload" href="fonts/crimson-pro-italic-latin.woff2" as="font" type="font/woff2" crossorigin>\n'
                  '<script type="application/ld+json">' + json.dumps(ORG, ensure_ascii=False) + '</script>\n',
}


# ---------------------------------------------------------------- 404
PAGES["404.html"] = ("Page not found · Iterrate",
"This page doesn't exist.",
"""
<div class="wrap narrow">
  <section class="page-top">
    <span class="mark sky"></span>
    <h1>Page not found</h1>
    <p class="lede">There's nothing at this address. It may have moved, or the link may have a typo.</p>
    <div class="btns">
      <a class="btn primary" href="./">Go to the home page</a>
      <a class="btn" href="contact.html">Contact us</a>
    </div>
  </section>
</div>
""")


def asset(name):
    """Link to a file with a short content hash, so browsers fetch it again after each change."""
    h = hashlib.sha1((SITE / name).read_bytes()).hexdigest()[:8]
    return f"{name}?v={h}"


def typography(html):
    """Curly quotes and apostrophes in the visible text, so they can be typed straight here.
    Tags, attributes, scripts and styles are left alone."""
    out = []
    for part in re.split(r"(<script.*?</script>|<style.*?</style>|<[^>]+>)", html, flags=re.S):
        if part.startswith("<"):
            out.append(part)
            continue
        part = re.sub(r"(?<=\w)'(?=\w)", "\u2019", part)          # it's, don't
        part = re.sub(r"(^|[\s(\[\u2014-])'", "\\1\u2018", part)   # opening single
        part = part.replace("'", "\u2019")                          # closing single
        part = re.sub(r'(^|[\s(\[\u2014-])"', "\\1\u201c", part)   # opening double
        part = part.replace('"', "\u201d")                          # closing double
        out.append(part)
    return "".join(out)


def plain(text):
    """The same curly quotes for titles and descriptions (which sit inside attributes)."""
    return typography(text).replace('"', "&quot;")


def last_changed(fname, changed_now):
    """The date a page last really changed: today if this build changed it, otherwise the date
    of the last git commit that touched it (so unchanged pages keep their old date)."""
    if not changed_now:
        try:
            out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", f"{SITE.name}/{fname}"],
                                 cwd=SITE.parent, capture_output=True, text=True).stdout.strip()
            if out:
                return out
        except OSError:
            pass
    return datetime.date.today().isoformat()


def build():
    pages = []
    changed = {}
    for fname, (title, desc, body) in PAGES.items():
        nav = "".join(
            f'<li><a href="{href}"{" aria-current=\"page\"" if href == fname or (href == "./" and fname == "index.html") else ""}>{label}</a></li>'
            for href, label in NAV
        )
        url = BASE if fname == "index.html" else BASE + fname
        head = HEAD.replace('href="style.css"', f'href="{asset("style.css")}"').format(
            title=plain(title), desc=plain(desc), nav=nav, url=url, base=BASE,
            extra_head=EXTRA_HEAD.get(fname, ""))
        if fname == "404.html":
            # GitHub serves this page at any missing address, so links must start from the site root.
            head = head.replace("<head>\n", '<head>\n<base href="/">\n', 1).replace(
                '<link rel="canonical" href="https://iterrate.in/404.html">\n', "")
            head = head.replace('<meta name="description"', '<meta name="robots" content="noindex">\n<meta name="description"', 1)
        else:
            pages.append((url, fname))
        foot = FOOT.format(scripts=SCRIPTS.get(fname, "").replace("{loop}", asset("loop.js")), year=YEAR)
        html = head + typography(body) + typography(foot)
        changed[fname] = not (SITE / fname).exists() or (SITE / fname).read_text(encoding="utf-8") != html
        (SITE / fname).write_text(html, encoding="utf-8")
        print("wrote", fname)

    (SITE / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc><lastmod>{last_changed(f, changed[f])}</lastmod></url>\n" for u, f in pages)
        + "</urlset>\n", encoding="utf-8")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n", encoding="utf-8")
    print("wrote sitemap.xml, robots.txt")


if __name__ == "__main__":
    build()
