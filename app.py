import glob
import os
from datetime import date
from string import Template

import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

NAME = "Veneerick Joel M. Ondon II"           
SECTION = "CSIT 349 · F1"    
PROGRAM = "BS Computer Science"     
YEAR = "3rd Year"            

st.set_page_config(
    page_title=f"{NAME} | Portfolio",
    page_icon=":D",
    layout="wide",
    initial_sidebar_state="collapsed",
)

INK, PAPER, YELLOW, RED, BLUE = "#111111", "#FFF8E7", "#FFD60A", "#E63946", "#2EC4F1"

#styling
COMIC_CSS = Template("""
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Comic+Neue:wght@400;700&display=swap');

/* paper with halftone dots */
.stApp {
  background-color: $PAPER;
  background-image:
    radial-gradient(circle, rgba(230,57,70,.22) 1.6px, transparent 2px),
    radial-gradient(circle, rgba(46,196,241,.22) 1.6px, transparent 2px);
  background-size: 18px 18px, 18px 18px;
  background-position: 0 0, 9px 9px;
}
html, body, [class*="css"] { font-family: 'Comic Neue', 'Comic Sans MS', sans-serif; font-size: 1.05rem; color: $INK; }
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] { display: none; }
[data-testid="stHeader"] { background: transparent; }

/* headings */
h1, h2, h3 { font-family: 'Bangers', 'Comic Sans MS', cursive !important; letter-spacing: 2px; color: $INK !important; font-weight: 400 !important; }
h1 { font-size: 4.2rem !important; color: $RED !important; -webkit-text-stroke: 2px $INK; text-shadow: 5px 5px 0 $INK;
     transform: rotate(-1.5deg); display: inline-block; line-height: 1.1; }
h2 { display: inline-block; background: $YELLOW; border: 3px solid $INK; box-shadow: 6px 6px 0 $INK;
     padding: 4px 18px !important; margin-top: 2.5rem; transform: rotate(-1deg); font-size: 2.2rem !important; }
h3 { font-size: 1.7rem !important; }

/* dotted dividers */
hr { border: 0 !important; border-top: 5px dotted $INK !important; opacity: 1 !important; }

/* metric panels with halftone corner */
[data-testid="stMetric"] {
  background: linear-gradient(100deg, #fff 50%, rgba(255,255,255,0) 100%), radial-gradient(circle, $BLUE 2.2px, transparent 2.8px);
  background-size: auto, 11px 11px; background-color: #fff;
  border: 3px solid $INK; border-radius: 4px; padding: 12px 16px; box-shadow: 6px 6px 0 $INK;
}
[data-testid="stMetricValue"] { font-family: 'Bangers', cursive; color: $RED; font-size: 2.6rem; letter-spacing: 2px; }
[data-testid="stMetricLabel"] { font-weight: 700; }

/* images look like comic panels */
[data-testid="stImage"] img { border: 4px solid $INK; box-shadow: 8px 8px 0 $INK; border-radius: 2px; }
.hero-photo [data-testid="stImage"] img { transform: rotate(-2deg); }

/* panels: containers created with key="card_*" */
[class*="st-key-card"] {
  background: linear-gradient(115deg, #fff 62%, rgba(255,255,255,0) 100%), radial-gradient(circle, $YELLOW 2.4px, transparent 3px);
  background-size: auto, 12px 12px; background-color: #fff;
  border: 3px solid $INK; border-radius: 10px; padding: 18px 22px; box-shadow: 8px 8px 0 $INK;
}

/* buttons */
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button, .stLinkButton > a {
  background: $YELLOW; color: $INK !important; border: 3px solid $INK; border-radius: 6px;
  font-family: 'Bangers', cursive; font-size: 1.25rem; letter-spacing: 1.5px; box-shadow: 4px 4px 0 $INK;
  transition: transform .08s, box-shadow .08s;
}
.stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover, .stLinkButton > a:hover {
  background: $RED; color: #fff !important; border-color: $INK; transform: translate(3px, 3px); box-shadow: 1px 1px 0 $INK;
}

/* skill stickers */
.chip { display: inline-block; margin: 6px 10px 6px 0; padding: 6px 18px; border: 3px solid $INK; background: #fff;
        font-family: 'Bangers', cursive; font-size: 1.3rem; letter-spacing: 1.5px; box-shadow: 4px 4px 0 $INK; border-radius: 6px; }
.chip:nth-child(3n+1) { background: $YELLOW; transform: rotate(-2deg); }
.chip:nth-child(3n+2) { background: $BLUE;   transform: rotate(1.5deg); }
.chip:nth-child(3n)   { background: #fff;    transform: rotate(-1deg); }

/* top navigation */
.nav a { font-family: 'Bangers', cursive; font-size: 1.3rem; letter-spacing: 1.5px; color: $INK; text-decoration: none;
         margin-right: 22px; padding: 2px 8px; border-bottom: 4px solid $RED; }
.nav a:hover { background: $YELLOW; }

/* speech bubble for project summaries */
.bubble { position: relative; background: #fff; border: 3px solid $INK; border-radius: 18px; padding: 14px 18px; margin: 6px 0 26px;
          box-shadow: 4px 4px 0 $INK; }
.bubble::after { content: ""; position: absolute; left: 34px; bottom: -22px; border-width: 22px 14px 0 0; border-style: solid;
                 border-color: $INK transparent transparent transparent; }
.bubble::before { content: ""; position: absolute; left: 37px; bottom: -15px; border-width: 17px 10px 0 0; border-style: solid;
                  border-color: #fff transparent transparent transparent; z-index: 1; }

/* carousel dots */
.dots { text-align: center; color: $INK; font-size: 1.6rem; letter-spacing: 8px; padding-top: 14px; }

/* form and alerts */
[data-testid="stForm"] { background: #fff; border: 3px solid $INK; border-radius: 10px; box-shadow: 8px 8px 0 $INK; padding: 20px; }
[data-testid="stAlert"] { border: 3px solid $INK; border-radius: 8px; box-shadow: 4px 4px 0 $INK; }
.stTextInput input, .stTextArea textarea { border: 2px solid $INK !important; background: #fff; }
""")
st.markdown(
    "<style>" + COMIC_CSS.substitute(INK=INK, PAPER=PAPER, YELLOW=YELLOW, RED=RED, BLUE=BLUE) + "</style>",
    unsafe_allow_html=True,
)

SMOOTH_CSS = """
html { scroll-behavior: smooth; }

/* softer, rounder shapes + smooth hover motion */
h2 { border-radius: 14px; }
[class*="st-key-card"], [data-testid="stMetric"], [data-testid="stForm"] {
  border-radius: 18px; transition: transform .25s ease, box-shadow .25s ease; }
[class*="st-key-card"]:hover, [data-testid="stMetric"]:hover {
  transform: translate(-3px, -3px); box-shadow: 9px 9px 0 #111111; }
[data-testid="stImage"] img { border-radius: 12px; transition: transform .3s ease, box-shadow .3s ease; }
.bubble { border-radius: 22px; }
.chip { transition: transform .2s ease, box-shadow .2s ease; }
.chip:hover { transform: rotate(0deg) translateY(-4px) scale(1.06) !important; box-shadow: 6px 8px 0 #111111; }
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button, .stLinkButton > a {
  border-radius: 999px; transition: transform .15s ease, box-shadow .15s ease, background .2s ease, color .2s ease; }
.stTextInput input, .stTextArea textarea { border-radius: 10px; transition: box-shadow .2s ease; }
.stTextInput input:focus, .stTextArea textarea:focus { box-shadow: 0 0 0 3px #2EC4F1; }

/* entrance animations */
@keyframes pop { 0% { opacity: 0; scale: .7; } 70% { opacity: 1; scale: 1.06; } 100% { opacity: 1; scale: 1; } }
@keyframes floaty { 0%, 100% { translate: 0 0; } 50% { translate: 0 -8px; } }
@keyframes slideIn { from { opacity: 0; translate: 0 20px; } to { opacity: 1; translate: 0 0; } }
h1 { animation: pop .7s cubic-bezier(.2, .9, .3, 1.3) both; }
.hero-photo [data-testid="stImage"] img { animation: floaty 5s ease-in-out infinite; }
[class*="st-key-card_project"] { animation: slideIn .45s ease both; }

/* scroll-triggered reveals (Chrome, Edge, Safari; other browsers just show everything) */
@supports (animation-timeline: view()) {
  @keyframes revealUp    { from { opacity: 0; translate: 0 50px; }  to { opacity: 1; translate: 0 0; } }
  @keyframes revealLeft  { from { opacity: 0; translate: -70px 0; } to { opacity: 1; translate: 0 0; } }
  @keyframes revealRight { from { opacity: 0; translate: 70px 0; }  to { opacity: 1; translate: 0 0; } }
  h2, [data-testid="stMetric"], [data-testid="stForm"], .stDownloadButton {
    animation: revealUp linear both; animation-timeline: view(); animation-range: entry 0% entry 40%; }
  .st-key-card_background, .st-key-card_interests {
    animation: revealLeft linear both; animation-timeline: view(); animation-range: entry 0% entry 45%; }
  .st-key-card_education, .st-key-card_milestones {
    animation: revealRight linear both; animation-timeline: view(); animation-range: entry 0% entry 45%; }
}

@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; scroll-behavior: auto !important; }
}
"""
st.markdown("<style>" + SMOOTH_CSS + "</style>", unsafe_allow_html=True)

FONT_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&family=Bangers&family=Comic+Neue:wght@400;700&display=swap');

/* body text: Comic Neue everywhere (the old rule missed Streamlit's own text classes) */
.stApp, .stApp p, .stApp li, .stApp label, .stApp input, .stApp textarea, .stApp td, .stApp a,
.stApp [data-testid="stMetricLabel"], .stApp [data-testid="stMetricLabel"] *,
.stApp [data-testid="stSlider"] *, .stApp [data-testid="stAlert"] *, .stApp textarea::placeholder, .stApp input::placeholder {
  font-family: 'Comic Neue', 'Comic Sans MS', 'Chalkboard SE', cursive, sans-serif !important; }
.stApp p, .stApp li, .stApp td { font-size: 1.15rem; }
.stApp label, .stApp label * { font-weight: 700; }

/* handwritten marker for captions and tags */
.stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stCaptionContainer"] * {
  font-family: 'Permanent Marker', 'Comic Sans MS', cursive !important; font-size: 1rem; letter-spacing: .5px; color: #111111; }

/* display font: headings, buttons, stickers, nav, numbers, table headers */
.stApp h1, .stApp h2, .stApp h3, .stApp h1 *, .stApp h2 *, .stApp h3 *,
.stApp button, .stApp button *, .stApp .stLinkButton a, .stApp .stLinkButton a *,
.stApp .chip, .stApp .nav a, .stApp [data-testid="stMetricValue"], .stApp [data-testid="stMetricValue"] *, .stApp th {
  font-family: 'Bangers', 'Comic Sans MS', cursive !important; letter-spacing: 1.5px; font-weight: 400; }

/* tables (st.table is HTML, so it can match the comic style) */
[data-testid="stTable"] table { border-collapse: separate; border-spacing: 0; border: 3px solid #111111; border-radius: 12px; overflow: hidden; background: #fff; }
[data-testid="stTable"] th { background: #FFD60A; font-size: 1.3rem; border-bottom: 3px solid #111111; }
[data-testid="stTable"] td { border-bottom: 2px dotted #111111; }
"""
st.markdown("<style>" + FONT_CSS + "</style>", unsafe_allow_html=True)

#helpers
def placeholder(label: str, size=(600, 450)) -> Image.Image:
    """A clearly labeled stand-in image with a halftone gradient."""
    w, h = size
    img = Image.new("RGB", size, YELLOW)
    d = ImageDraw.Draw(img)
    for y in range(0, h, 16):
        r = 1 + 6 * (y / h)
        for x in range(0, w, 16):
            d.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    try:
        font = ImageFont.load_default(size=30)
    except TypeError:
        font = ImageFont.load_default()
    box = d.textbbox((0, 0), label, font=font)
    tw, th = box[2] - box[0], box[3] - box[1]
    cx, cy = w / 2, h / 2
    d.rectangle([cx - tw / 2 - 18, cy - th / 2 - 14, cx + tw / 2 + 18, cy + th / 2 + 14], fill="#FFFFFF", outline=INK, width=5)
    d.text((cx - tw / 2 - box[0], cy - th / 2 - box[1]), label, fill=INK, font=font)
    d.rectangle([3, 3, w - 3, h - 3], outline=INK, width=6)
    return img


def chips(items):
    st.markdown("".join(f'<span class="chip">{i}</span>' for i in items), unsafe_allow_html=True)


#data
SKILLS = [
    "C#", "Java", "C", "C++", "Python", "UI Design", "QA Testing", "3D Modeling(Blender)", "Game Development", "Graphics Design", "Photoshop", "Premier Pro", "After Effects",
]

INTERESTS = ["Coding", "Game Development", "3D Art", "Writing", "Gaming"]  

PROJECTS = [
    {
        "title": "T(n)-spector",
        "tag": "Group project · UI and QA",
        "summary": (
            "A desktop app that helps students learn algorithm efficiency. Users assemble an "
            "algorithm from drag-and-drop blocks and the app computes its theoretical running time, "
            "with a shared repository for saving and viewing code snippets."
        ),
        "role": "UI and QA",
        "tools": ["Java", "JavaFX", "MySQL"],
        "outcome": "The project that made me learn how to properly work with others",
        "links": [("GitHub", "https://github.com/Kianbel/Tn-spector")],
        "image": "projects/tn-spector.png",
    },
    {
        "title": "Cebu Survival Guide",
        "tag": "Solo project · Sole developer",
        "summary": "This is an ongoing project that I am making in order to help people adapt to life in cebu",
        "role": "Sole developer",
        "tools": ["C#", "Blazor"],
        "outcome": "Still to be determined, but for now it is a fantastic learning experience",
        "links": [("GitHub", "https://github.com/Veneerick/Cebu-Survival-Guide")],
        "image": "projects/cebu-survival-guide.png",
    },
    {
        "title": "Mangga Dyip Simulator",
        "tag": "Game project · 3D assets and environments",
        "summary": "A game jam submission for the filipino horror jam",
        "role": "3D assets and environments",
        "tools": ["3D modeling", "Blender"],  
        "outcome": "A whole lot of 3d modelling made me learn a lot of ",
        "links": [("Play on itch.io", "https://b1nggb0ngg.itch.io/mangga-dyip-simulator")],
        "image": "projects/mangga-dyip-simulator.jpg",
    },
]

MILESTONES = pd.DataFrame(
    {
        "Year": [2024, 2025, 2025, 2026],
        "Milestone": [
            "Started College",
            "Learned C",
            "Learned C++ and Java",
            "Made a Game",
        ],
    }
)

CERT_FILES = sorted(
    f for ext in ("png", "jpg", "jpeg", "webp") for f in glob.glob(f"certs/*.{ext}")
)

#session state
st.session_state.setdefault("proj_idx", 0)
st.session_state.setdefault("messages", [])


def step(delta: int):
    st.session_state.proj_idx = (st.session_state.proj_idx + delta) % len(PROJECTS)


#header
st.title(f"Wazzup, I'm {NAME}")
st.caption(f"{PROGRAM} · {YEAR} · {SECTION}")
st.markdown(
    '<div class="nav"><a href="#about">About</a><a href="#autobiography">Autobiography</a>'
    '<a href="#skills">Skills</a><a href="#projects">Projects</a>'
    '<a href="#certifications">Certifications</a><a href="#contact">Contact</a></div>',
    unsafe_allow_html=True,
)
st.divider()

#about
st.header("About Me", anchor="about")
col_photo, col_bio = st.columns([1, 2], gap="large")

with col_photo:
    st.markdown('<div class="hero-photo">', unsafe_allow_html=True)
    st.image("photo.jpg", caption=NAME)

with col_bio:
    st.write("I am Veneerick Ondon, and I am a 3rd year student currently studying CS in Cebu Institute of Technology University! Having lived in Calbayog City, Samar for most of my life, I grew up without much context for anything outside of the vicinity. But upon entering Highschool I entered a special program in the arts. There I learned about using software like Photoshop and Premier as well as learning the basics of Radio Broadcasting and the principles of design. Upon entering Senior Highschool I went to the ABM strand and mostly learned about accountancy, to which I became incredibly bored. Fast forward to today, and I have chosen CS in college, a decision that came out of nowhere and now I am currently surviving! Wish me luck!")
    all_tools = {t for p in PROJECTS for t in p["tools"]}
    m1, m2, m3 = st.columns(3)
    m1.metric("Projects", len(PROJECTS))
    m2.metric("Certifications", len(CERT_FILES))
    m3.metric("Tools used", len(all_tools))

#autobiography
st.header("Autobiography", anchor="autobiography")
r1a, r1b = st.columns(2, gap="large")
with r1a.container(key="card_background"):
    st.subheader("Background")
    st.write("I grew up in Calbayog City, Samar. I studied Media Arts in Highschool and have now come to study Computer Science to further broaden my horizons!")
with r1b.container(key="card_education"):
    st.subheader("Education")
    st.markdown("- Christ the King College (Elementary) \n- Calbayog City National Highschool\n- Cebu Institute of Technology - University")

r2a, r2b = st.columns(2, gap="large")
with r2a.container(key="card_interests"):
    st.subheader("Interests")
    chips(INTERESTS)
with r2b.container(key="card_milestones"):
    st.subheader("Milestones")
    this_year = date.today().year
    start, end = st.slider("Timeline range", 2010, this_year, (2015, this_year))
    shown = MILESTONES[MILESTONES["Year"].between(start, end)]
    st.table(shown.set_index("Year"))

bio_text = f"{NAME}\n{PROGRAM}, {YEAR}\n\n I am Veneerick Ondon, and I am a 3rd year student currently studying CS in Cebu Institute of Technology University! \n\nHaving lived in Calbayog City, Samar for most of my life, I grew up without much context for anything outside of the vicinity. But upon entering Highschool I entered a special program in the arts. There I learned about using software like Photoshop and Premier as well as learning the basics of Radio Broadcasting and the principles of design. Upon entering Senior Highschool I went to the ABM strand and mostly learned about accountancy, to which I became incredibly bored. Fast forward to today, and I have chosen CS in college, a decision that came out of nowhere and now I am currently surviving! Wish me luck!\n"
st.download_button("Download my bio in text form!", bio_text, file_name="autobiography.txt")

#skills
st.header("Skills", anchor="skills")
st.write("Over the years I have delved into a lot of disciplines, these are the ones I am most confident in!")
chips(SKILLS)

#projects
st.header("Projects", anchor="projects")
idx = st.session_state.proj_idx
proj = PROJECTS[idx]

prev_col, card_col, next_col = st.columns([1, 12, 1], vertical_alignment="center")
prev_col.button("◀", key="prev", on_click=step, args=(-1,), help="Previous project")
next_col.button("▶", key="next", on_click=step, args=(1,), help="Next project")

with card_col.container(key=f"card_project_{idx}"):
    text_col, img_col = st.columns([3, 2], gap="large")
    with text_col:
        st.caption(f"{proj['tag']} · {idx + 1} of {len(PROJECTS)}")
        st.subheader(proj["title"])
        st.markdown(f'<div class="bubble">{proj["summary"]}</div>', unsafe_allow_html=True)
        st.write(f"**My role:** {proj['role']}")
        st.write(f"**Tools:** {', '.join(proj['tools'])}")
        st.write(f"**Outcome:** {proj['outcome']}")
        for label, url in proj["links"]:
            st.link_button(label, url)
    with img_col:
        if os.path.exists(proj["image"]):
            st.image(proj["image"], caption=proj["title"])
        else:
            st.image(placeholder(proj["title"]), caption=f"Stand-in (add {proj['image']})")

st.markdown(
    f'<div class="dots">{" ".join("●" if i == idx else "○" for i in range(len(PROJECTS)))}</div>',
    unsafe_allow_html=True,
)

# crertifications
st.header("Certifications", anchor="certifications")
if CERT_FILES:
    cols = st.columns(3, gap="large")
    for i, path in enumerate(CERT_FILES):
        cols[i % 3].image(path, caption=os.path.splitext(os.path.basename(path))[0].replace("_", " "))
else:
    st.info("Add your certificate images (png, jpg, jpeg or webp) to the certs/ folder and they will appear here.")

# contact
st.header("Contact & Feedback", anchor="contact")
with st.form("contact_form", clear_on_submit=True):
    f1, f2 = st.columns(2)
    sender = f1.text_input("Your name")
    email = f2.text_input("Your email")
    rating = st.slider("Rate this site", 1, 5, 4)
    message = st.text_area("Message")
    submitted = st.form_submit_button("Send")

if submitted:
    if not sender or not message:
        st.warning("Please enter your name and a message.")
    else:
        st.session_state.messages.append({"Name": sender, "Rating": rating, "Message": message})
        st.success(f"Thanks, {sender}! Your message was received.")
        st.balloons()

if st.session_state.messages:
    st.subheader("Messages this session")
    st.table(pd.DataFrame(st.session_state.messages))

st.divider()
st.caption(f"© {date.today().year} {NAME} · {SECTION} · Built with Streamlit")
