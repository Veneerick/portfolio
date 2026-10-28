import glob
import os
from datetime import date
from string import Template

import pandas as pd
import streamlit as st
from PIL import Image, ImageDraw, ImageFont

# ----------------------------------------------------------------------------
# TODO: replace every placeholder below with your own details and writing.
# ----------------------------------------------------------------------------
NAME = "Your Name"                    # TODO
SECTION = "CSIT 349 · Section X"      # TODO: your section
PROGRAM = "BS Computer Science"       # TODO
YEAR = "3rd Year"                     # TODO

st.set_page_config(
    page_title=f"{NAME} | Portfolio",
    page_icon="👋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

INK, PAPER, YELLOW, RED, BLUE = "#111111", "#FFF8E7", "#FFD60A", "#E63946", "#2EC4F1"

# ------------------------------- styling ------------------------------------
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


# ------------------------------- helpers ------------------------------------
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


# ------------------------------- data ---------------------------------------
SKILLS = [  # TODO: edit to match what you can really do
    "C#", "Blazor", "Java", "JavaFX", "UI Design", "QA Testing", "3D Modeling", "Environment Art",
]

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
        "outcome": "TODO: what you designed, what you tested, what you learned.",
        "links": [("GitHub", "https://github.com/Kianbel/Tn-spector")],
        "image": "projects/tn-spector.png",
    },
    {
        "title": "Cebu Survival Guide",
        "tag": "Solo project · Sole developer",
        "summary": "TODO: one or two sentences on what the guide is and who it is for.",
        "role": "Sole developer",
        "tools": ["C#", "Blazor"],
        "outcome": "TODO: what you built end to end and how it turned out.",
        "links": [("GitHub", "https://github.com/Veneerick/Cebu-Survival-Guide")],
        "image": "projects/cebu-survival-guide.png",
    },
    {
        "title": "Mangga Dyip Simulator",
        "tag": "Game project · 3D assets and environments",
        "summary": "TODO: one or two sentences on the game and its setting.",
        "role": "3D assets and environments",
        "tools": ["3D modeling", "Environment art"],  # TODO: add the software you used
        "outcome": "TODO: which assets and environments you made and what you learned.",
        "links": [("Play on itch.io", "https://b1nggb0ngg.itch.io/mangga-dyip-simulator")],
        "image": "projects/mangga-dyip-simulator.png",
    },
]

MILESTONES = pd.DataFrame(  # TODO: your own timeline
    {
        "Year": [2015, 2020, 2023, 2025],
        "Milestone": [
            "TODO: an early milestone",
            "TODO: a turning point",
            "TODO: started college",
            "TODO: a recent achievement",
        ],
    }
)

CERT_FILES = sorted(
    f for ext in ("png", "jpg", "jpeg", "webp") for f in glob.glob(f"certs/*.{ext}")
)

# ---------------------------- session state ---------------------------------
st.session_state.setdefault("proj_idx", 0)
st.session_state.setdefault("messages", [])


def step(delta: int):
    st.session_state.proj_idx = (st.session_state.proj_idx + delta) % len(PROJECTS)


# ------------------------------- header -------------------------------------
st.title(f"👋 Hi, I'm {NAME}")
st.caption(f"{PROGRAM} · {YEAR} · {SECTION}")
st.markdown(
    '<div class="nav"><a href="#about">About</a><a href="#autobiography">Autobiography</a>'
    '<a href="#skills">Skills</a><a href="#projects">Projects</a>'
    '<a href="#certifications">Certifications</a><a href="#contact">Contact</a></div>',
    unsafe_allow_html=True,
)
st.divider()

# ------------------------------- about --------------------------------------
st.header("About Me", anchor="about")
col_photo, col_bio = st.columns([1, 2], gap="large")

with col_photo:
    st.markdown('<div class="hero-photo">', unsafe_allow_html=True)
    if os.path.exists("photo.jpg"):
        st.image("photo.jpg", caption=NAME)
    else:
        st.image(placeholder("PHOTO PLACEHOLDER", (400, 400)), caption="Stand-in photo (add photo.jpg)")
    st.markdown("</div>", unsafe_allow_html=True)

with col_bio:
    st.write("TODO: write a short biography in your own words: who you are, what you study, and what you want to do.")
    all_tools = {t for p in PROJECTS for t in p["tools"]}
    m1, m2, m3 = st.columns(3)
    m1.metric("Projects", len(PROJECTS))
    m2.metric("Certifications", len(CERT_FILES))
    m3.metric("Tools used", len(all_tools))

# ------------------------------- autobiography ------------------------------
st.header("Autobiography", anchor="autobiography")
r1a, r1b = st.columns(2, gap="large")
with r1a.container(key="card_background"):
    st.subheader("Background")
    st.write("TODO: where you grew up, family, what shaped you.")
with r1b.container(key="card_education"):
    st.subheader("Education")
    st.markdown("- TODO: Elementary\n- TODO: High school\n- TODO: College / program")

r2a, r2b = st.columns(2, gap="large")
with r2a.container(key="card_interests"):
    st.subheader("Interests")
    interests = st.pills(
        "Tap what you enjoy",  # TODO: edit options to match you
        ["Coding", "Game dev", "3D art", "Music", "Gaming", "Reading", "Travel"],
        selection_mode="multi",
        default=["Coding"],
    )
    st.write("I enjoy: " + (", ".join(interests) if interests else "nothing selected yet"))
with r2b.container(key="card_milestones"):
    st.subheader("Milestones")
    this_year = date.today().year
    start, end = st.slider("Timeline range", 2010, this_year, (2015, this_year))
    shown = MILESTONES[MILESTONES["Year"].between(start, end)]
    st.dataframe(shown, hide_index=True)

bio_text = f"{NAME}\n{PROGRAM}, {YEAR}\n\nTODO: paste your autobiography here.\n"
st.download_button("⬇️ Download my bio (.txt)", bio_text, file_name="autobiography.txt")

# ------------------------------- skills -------------------------------------
st.header("Skills", anchor="skills")
st.write("TODO: a sentence or two on how you picked these skills up.")
chips(SKILLS)

# ------------------------------- projects (carousel) ------------------------
st.header("Projects", anchor="projects")
idx = st.session_state.proj_idx
proj = PROJECTS[idx]

prev_col, card_col, next_col = st.columns([1, 12, 1], vertical_alignment="center")
prev_col.button("◀", key="prev", on_click=step, args=(-1,), help="Previous project")
next_col.button("▶", key="next", on_click=step, args=(1,), help="Next project")

with card_col.container(key="card_project"):
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

# ------------------------------- certifications -----------------------------
st.header("Certifications", anchor="certifications")
if CERT_FILES:
    cols = st.columns(3, gap="large")
    for i, path in enumerate(CERT_FILES):
        cols[i % 3].image(path, caption=os.path.splitext(os.path.basename(path))[0].replace("_", " "))
else:
    st.info("Add your certificate images (png, jpg, jpeg or webp) to the certs/ folder and they will appear here.")

# ------------------------------- contact ------------------------------------
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
