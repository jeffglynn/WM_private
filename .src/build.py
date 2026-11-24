#!/usr/bin/env python3
"""Build web/index.html from the wget mirror of the live Drupal page.
Keeps header/nav/carousel markup + CSS exactly; swaps body content; removes footer."""
import re, pathlib

web = pathlib.Path(__file__).resolve().parent.parent / "web"
h = (web / "custom-private-tours-banff.html").read_text()

# Links to the real site instead of the local ddev site.
h = h.replace("https://whitemountain.ddev.site", "https://www.whitemountainadventures.com")

# No autoplay.
h = h.replace("&quot;autoplay&quot;:true", "&quot;autoplay&quot;:false")

# --- Carousel block: find it and its matching closing div.
start = h.index('<div class="views-element-container block block-views block-views-blocktop-images-carousel')
depth, i = 0, start
for m in re.finditer(r"<div\b|</div>", h[start:]):
    depth += 1 if m.group() == "<div" else -1
    if depth == 0:
        end = start + m.end()
        break
summer = h[start:end]

items = re.findall(r'<div><div class="views-field views-field-field-top-images">.*?</div></div></div>', summer, re.S)
winter_imgs = ["images/winter/01.jpg", "images/winter/02.jpg", "images/winter/03.jpg", "images/winter/04.jpg"]
winter_items = "\n".join(
    f'<div><div class="views-field views-field-field-top-images"><div class="field-content">  <img loading="eager" src="{src}" width="960" height="640" alt="" class="image-style-top-images-carousel" />\n\n\n</div></div></div>'
    for src in winter_imgs)
winter = summer.replace(items[0], "@@ITEMS@@", 1)
for it in items[1:]:
    winter = winter.replace(it, "", 1)
winter = winter.replace("@@ITEMS@@", winter_items)
winter = winter.replace('id="block-b5subtheme-views-block-top-images-carousel-block-1"', 'id="block-winter-carousel"')
winter = re.sub(r"js-view-dom-id-\w+", "js-view-dom-id-winter", winter)

h = h[:start] + ('<div class="season-carousel">\n<div class="summer-carousel">' + summer +
                 '</div>\n<div class="winter-carousel" aria-hidden="true">' + winter + '</div>\n</div>') + h[end:]

# --- Title row: replace "Have a Question?" button with the season switch.
switch = '''<div class="season">
  <span class="lb on" data-season="summer">Summer</span>
  <button class="switch" type="button" role="switch" aria-checked="false" aria-label="Toggle summer / winter"><span class="knob">
    <svg class="ico-sun" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
    <svg class="ico-snow" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"><path d="M12 2v20M3.3 7l17.4 10M3.3 17L20.7 7M9 4l3 2 3-2M9 20l3-2 3 2"/></svg>
  </span></button>
  <span class="lb" data-season="winter">Winter</span>
</div>'''
h = re.sub(r'<div class="field field--name-field-have-a-question2.*?</a></div>', switch, h, count=1, flags=re.S)

# --- Body content (replaces the old two-column grid).
card = '''    <div class="home-thumb"><a class="thumb-link" href="#">
      <div class="thumb-img"><img src="images/cards/{img}" alt="{title}"></div>
      <div class="thumb-text">
        <div class="thumb-title">{title}</div>
        <p>{tag}</p>
        <p class="thumb-duration"><i class="fa-solid fa-clock" aria-hidden="true"></i> &nbsp;{dur}{diff}</p>
      </div></a></div>'''
def diff(d):
    return f'&nbsp;&nbsp;<span class="thumb-diff"><i class="fa-solid fa-person-hiking" aria-hidden="true"></i> &nbsp;{d}</span>' if d else ""
summer_cards = "\n".join(card.format(**{**c, "diff": diff(c.get("diff"))}) for c in [
    dict(img="ebike-tours-banff-canmore.webp", title="Guided Ebike Tours in Banff and Canmore", tag="See the best of Banff’s natural beauty via active, accessible guided e-bike tours", dur="2 - 4 hours", diff="Easy"),
    dict(img="heli-hiking-canadian-rockies.webp", title="Heli-Hiking in the Canadian Rockies", tag="The Pinnacle of hiking in the Canadian Rockies!", dur="4 hours", diff="Light/Moderately Strenuous"),
    dict(img="atv-assisted-hiking.webp", title="ATV-Assisted Hiking", tag="Fortress backcountry ridgeline hike.", dur="4 hours", diff="Light/Moderately Strenuous"),
])
cards = "\n".join(card.format(**{**c, "diff": diff(c.get("diff"))}) for c in [
    dict(img="twilight.jpg", title="Banff Twilight Tour", tag="Evening tour through Banff as the peaks light up at dusk. Fridays and Saturdays.", dur="2.5 hours", diff="Easy"),
    dict(img="grassi.jpg", title="Grassi Lakes Winter Hike", tag="Frozen waterfalls and emerald lakes above Canmore", dur="3.5 hours", diff="Moderate"),
    dict(img="ross-lake.jpg", title="Ross Lake and Winter Forest Snowshoe", tag="Quiet snowshoe through old-growth forest to a hidden lake", dur="4 hours", diff="Light/Moderate"),
])
body = f'''<div class="private-body">
<div  class="grid">
<div  class="col1">
  <p class="intro">Experience the Canadian Rockies on your own terms. Our private tours pair your group with a professional interpretive guide for a day built around your pace, your interests and your schedule &ndash; whether you're travelling as a family, a group of friends or a corporate team.</p>
  <p class="intro">Choose one of our ready-to-book tours for an easy, proven half-day adventure, or work with our trip designers on a fully custom experience planned from the ground up.</p>
</div>
<div  class="col2">
  <div class="clearfix text-formatted field field--name-field-highlights field--type-text-long field--label-above">
    <div class="field__label">Highlights</div>
    <div class="field__item swap">
      <div class="summer-only"><ul>
<li>Fully custom and private</li>
<li>Go at your own pace</li>
<li>Alpine meadows, glacier-fed lakes and ridgeline views</li>
<li>Hike, heli-hike, e-bike or ATV</li>
<li>All age groups</li>
<li>Multi-lingual guides for English, French, German and Spanish</li>
<li>Transportation provided by private van</li>
</ul></div>
      <div class="winter-only"><ul>
<li>Fully custom and private</li>
<li>Go at your own pace</li>
<li>Frozen waterfalls, snowy forests and frozen lakes</li>
<li>Icewalks, snowshoeing and winter sightseeing</li>
<li>All age groups</li>
<li>Multi-lingual guides for English, French, German and Spanish</li>
<li>Transportation provided by private van</li>
</ul></div>
    </div>
  </div>
</div>
</div>
  <section class="ready-tours">
  <h2>Ready to Book Private Tours</h2>
  <div class="swap">
  <p class="summer-only">These tours are regularly offered throughout the summer and are perfect for a half day for your private group.</p>
  <p class="winter-only">These tours are regularly offered throughout the winter and are perfect for a half day for your private group.</p>
  </div>
  <p class="tour-cost"><span><strong>1/2 day:</strong> from $1080 + GST</span><span><strong>Full day:</strong> from $1760 + GST</span></p>
  <div class="swap">
  <div class="private-thumbs summer-cards summer-only">
{summer_cards}
  </div>
  <div class="private-thumbs winter-cards winter-only">
{cards}
  </div>
  </div>
  </section>
  <h2>Custom Trip Planning</h2>
  <p class="intro">Have something specific in mind? Our trip designers will build a program around your group's interests, fitness level and timeline, from a single day to a multi-day itinerary. Custom private programs are the best way to fit in everything on your list.</p>
  <div class="where-box">
    <h3 class="where-title">Where We Go</h3>
    <p>We guide throughout the national and provincial parks of Alberta and British Columbia, plus a wide range of tour and hiking routes across the region.</p>
    <ul>
      <li>Banff National Park</li>
      <li>Jasper National Park</li>
      <li>Yoho National Park</li>
      <li>Kootenay National Park</li>
      <li>Waterton National Park</li>
      <li>Glacier/Revelstoke National Parks</li>
      <li>Kananaskis Country</li>
      <li>Mt. Assiniboine Provincial Park</li>
      <li>Manning Provincial Park</li>
      <li>Kokanee Glacier Provincial Park</li>
      <li>Badlands of Alberta</li>
      <li>Calgary, Edmonton, Vancouver &amp; Victoria</li>
    </ul>
  </div>''' + (pathlib.Path(__file__).parent / 'form.html').read_text() + f'''
</div>'''
h = re.sub(r'<div  class="grid">.*?</article>', lambda m: body + "\n  </div>\n</article>", h, count=1, flags=re.S)

# --- Remove footer.
h = re.sub(r"<footer\b.*?</footer>", "", h, count=1, flags=re.S)

# --- Custom assets.
h = h.replace("</head>", '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">\n<link rel="stylesheet" href="custom/season.css">\n</head>', 1)
h = h.replace("</body>", '<script src="custom/season.js"></script>\n</body>', 1)

h = re.sub(r'src="sites/www.whitemountainadventures.com/files/js/js_[^"]*"', 'src="sites/www.whitemountainadventures.com/files/js/site.js"', h)
h = h.replace("<h1>Custom and Private Tours </h1>", "<h1>Private Tours &amp; Custom Trip Planning</h1>")

# Turn off navbar menu links (keep tel: and dropdown toggles working).
def _kill(m):
    tag = m.group(0)
    if 'href="tel:' in tag: return tag
    return re.sub(r'href="[^"]*"', 'href="#" data-disabled-link', tag, count=1)
a0 = h.index('navbar-nav'); a1 = h.index('</header>')
h = h[:a0] + re.sub(r'<a [^>]*class="[^"]*(nav-link|dropdown-item)[^"]*"[^>]*>', _kill, h[a0:a1]) + h[a1:]
(web / "index.html").write_text(h)
print("ok", len(items), "summer items")
