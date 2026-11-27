#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Générateur du site statique Konig Formation.
Usage : python3 build.py   → génère le site dans docs/ (servi par GitHub Pages).
Aucune dépendance externe."""
import json, os, re, shutil, sys, html, datetime
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "content"))
import sitedata as S
from formations import FORMATIONS, HUBS

OUT = os.path.join(ROOT, "docs")
E = html.escape
MOIS = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]
DOMAINS = {"ia": "Intelligence artificielle", "marketing": "Marketing digital", "office": "Pack Office"}
FBY = {f["slug"]: f for f in FORMATIONS}
PAGES = []  # (path, lastmod) pour le sitemap
TODAY = datetime.date.today().isoformat()
# Passer à True le jour de la bascule DNS (ajoute le fichier CNAME pour GitHub Pages)
CUSTOM_DOMAIN = False
VER = datetime.datetime.now().strftime("%Y%m%d%H%M")

def fdate(iso):
    y, m, d = iso[:10].split("-")
    return f"{int(d)} {MOIS[int(m)-1]} {y}"

def strip(s): return re.sub(r"<[^>]+>", "", s)

def dur(f):
    return re.split(r" — | selon| en synchrone", f["facts"][0][1])[0]

# ------------------------------------------------------------------ gabarit
def pre(path): return "../" * path.count("/")
def L(path, target):
    """Lien relatif depuis `path` vers `target` ('' = accueil, 'slug/' = page)."""
    p = pre(path) + target
    return p or "./"

def blocks(bl):
    out = []
    for b in bl:
        if isinstance(b, tuple) and b[0] == "ul":
            out.append("<ul>" + "".join(f"<li>{x}</li>" for x in b[1]) + "</ul>")
        else:
            out.append(f"<p>{b}</p>")
    return "\n".join(out)

def brand(path, cls=""):
    img = "logo-konig-white.png" if cls == "light" else "logo-konig-ink.png"
    return (f'<a class="brand {cls}" href="{L(path,"")}" aria-label="Konig Formation — accueil">'
            f'<img src="{L(path,"assets/img/"+img)}" alt="Konig Formation" width="1023" height="437"></a>')

def mega(path):
    cols = []
    for dom in ("ia", "office"):
        links = "".join(f'<a href="{L(path,f["slug"]+"/")}">{E(f["short"])}<small>{f["code"]}</small></a>'
                        for f in FORMATIONS if f["domain"] == dom)
        hub = next((h for h in HUBS if h["domain"] == dom), None)
        if hub: links += f'<a href="{L(path,hub["slug"]+"/")}"><span class="link-arrow">Vue d’ensemble</span></a>'
        cols.append(f'<div class="mega__col"><h4>{DOMAINS[dom]}</h4>{links}</div>')
    return (f'<div class="mega" data-mega><div class="wrap"><div><span class="label label--brass">Catalogue 2026</span>'
            f'<h3>Toutes nos formations sont <em>certifiantes</em></h3><p class="muted small">Éligibles CPF, finançables par OPCO, FAF ou France Travail. 100 % à distance.</p>'
            f'<a class="link-arrow small" href="{S.RDV}">Formation sur mesure : parlons-en</a></div>{"".join(cols)}</div></div>')

def header(path):
    m = "".join(f'<a href="{L(path,f["slug"]+"/")}">{E(f["short"])}</a>' for f in FORMATIONS)
    return f'''<a class="skip" href="#main">Aller au contenu</a>
<div class="topbar"><div class="wrap"><div><span>Organisme certifié Qualiopi</span><span class="t-hide">Formations éligibles CPF</span><span class="t-hide">100 % à distance</span></div>
<div><a href="tel:{S.PHONE_INTL}">{S.PHONE}</a><a class="t-hide" href="mailto:{S.EMAIL}">{S.EMAIL}</a></div></div></div>
<header class="header"><div class="wrap">{brand(path)}
<nav class="nav" aria-label="Navigation principale">
<button type="button" data-mega-btn aria-expanded="false">Formations</button>
<a href="{L(path,"programmes/")}">Programmes</a>
<a href="{L(path,"")}#financement">Financement</a>
<a href="{L(path,"blog/")}">Blog</a>
<a class="btn" href="{S.RDV}">Prendre rendez-vous</a></nav>
<button class="burger" type="button" data-burger aria-expanded="false" aria-label="Ouvrir le menu"><span></span></button>
</div>{mega(path)}</header>
<nav class="mnav" data-mnav aria-label="Menu mobile"><h4>Formations</h4>{m}
<h4>Le centre</h4><a href="{L(path,"formation-intelligence-artificielle/")}">Intelligence artificielle</a><a href="{L(path,"formation-pack-office-2/")}">Pack Office</a><a href="{L(path,"programmes/")}">Programmes</a><a href="{L(path,"")}#financement">Financement</a><a href="{L(path,"blog/")}">Blog</a>
<a class="btn" href="{S.RDV}">Prendre rendez-vous</a></nav>'''

def footer(path):
    fl = "".join(f'<li><a href="{L(path,f["slug"]+"/")}">{E(f["menu"])}</a></li>' for f in FORMATIONS)
    return f'''<footer class="footer"><div class="wrap">
<div class="footer__top">
<div>{brand(path, "light")}<p style="margin-top:1.4rem;max-width:34ch">Organisme de formation certifié Qualiopi. Formations certifiantes en intelligence artificielle et Pack Office, 100 % à distance.</p>
<a class="fn" href="{S.LINKS["francenum"]}" rel="noopener"><img src="{L(path,"assets/img/logo-Activateur.jpg")}" alt="Activateur France Num" width="120" height="44" loading="lazy"></a></div>
<div><h4>Formations</h4><ul>{fl}</ul></div>
<div><h4>Le centre</h4><ul><li><a href="{L(path,"formation-intelligence-artificielle/")}">Univers IA</a></li><li><a href="{L(path,"formation-pack-office-2/")}">Univers Pack Office</a></li><li><a href="{L(path,"programmes/")}">Programmes</a></li><li><a href="{L(path,"blog/")}">Blog</a></li><li><a href="{S.LINKS["sante"]}" rel="noopener">Formations Santé ↗</a></li><li><a href="{S.RDV}">Prendre rendez-vous</a></li></ul></div>
<div><h4>Contact</h4><ul><li><a href="tel:{S.PHONE_INTL}">{S.PHONE}</a></li><li><a href="mailto:{S.EMAIL}">{S.EMAIL}</a></li><li>125 bd du Général Koenig<br>92200 Neuilly-sur-Seine</li>
<li style="margin-top:.6rem"><a href="{S.LINKS["instagram"]}" rel="noopener">Instagram</a> · <a href="{S.LINKS["facebook"]}" rel="noopener">Facebook</a></li></ul></div>
</div>
<div class="footer__q"><a class="qlogo" href="{L(path,S.LINKS["qualiopi_pdf"])}"><img src="{L(path,"assets/img/Logo-Qualiopi-300dpi-Avec-Marianne-1.jpg")}" alt="Certificat Qualiopi — processus certifié, République française" width="140" height="54" loading="lazy"></a><p>{S.QUALIOPI_TEXT}</p></div>
<div class="footer__bottom"><span>© {datetime.date.today().year} SARL Konig — Konig Formation</span>
<nav aria-label="Informations légales"><a href="{L(path,S.LINKS["cgv"])}">CGV</a><a href="{L(path,"mentions-legales/")}">Mentions légales</a><a href="{L(path,"politique-de-confidentialite/")}">Confidentialité</a><a href="{S.LINKS["reclamation"]}" rel="noopener">Formulaire de réclamation</a><a href="{L(path,S.LINKS["qualiopi_pdf"])}">Certificat Qualiopi</a></nav></div>
</div></footer>'''

def page(path, title, desc, body, *, chrome="full", jsonld=None, og_img=None, og_type="website", robots=None, extra_head=""):
    p = pre(path)
    url = S.SITE_URL + "/" + path
    og = S.SITE_URL + "/" + (og_img or "assets/img/konig-formation-2.png")
    ld = "".join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False)}</script>' for j in (jsonld or []))
    top = header(path) if chrome == "full" else f'<header class="header"><div class="wrap">{brand(path)}<a class="btn btn--ghost" href="tel:{S.PHONE_INTL}">{S.PHONE}</a></div></header>'
    doc = f'''<!doctype html>
<html lang="fr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script>document.documentElement.className='js'</script>
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
{f'<meta name="robots" content="{robots}">' if robots else ''}
<meta property="og:locale" content="fr_FR"><meta property="og:type" content="{og_type}"><meta property="og:site_name" content="Konig Formation">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0A2A4E">
<link rel="icon" href="{p}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{p}assets/fonts/Unbounded-normal-400_800-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{p}assets/fonts/Onest-normal-400_700-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/fonts/fonts.css"><link rel="stylesheet" href="{p}assets/css/site.css?v={VER}">
{extra_head}{ld}
</head><body>
{top}
<main id="main">{body}</main>
{footer(path)}
<script src="{p}assets/js/site.js?v={VER}" defer></script>
</body></html>
'''
    dest = os.path.join(OUT, path, "index.html") if path == "" or path.endswith("/") else os.path.join(OUT, path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    open(dest, "w").write(doc)
    if robots is None: PAGES.append(path)


PHOTOS = {
 "groupe":("Apprenants échangeant autour d’ordinateurs portables",1067),
 "atelier":("Atelier de formation en petit groupe",1067),
 "ia":("Main robotique, symbole de l’intelligence artificielle",1152),
 "office":("Ordinateur portable affichant un tableau de bord",1140),
 "sur-mesure":("Échange entre un formateur et un apprenant devant un ordinateur",1067),
 "centre":("Session de formation avec formateur et apprenants équipés d’ordinateurs",1067),
 "formation-ia":("Deux personnes travaillant sur un ordinateur portable",1067),
 "formation-ia-automatisation":("Équipe travaillant ensemble sur ordinateur",1067),
 "formation-ia-marketing-de-contenus":("Groupe échangeant autour d’une tablette",1067),
 "formation-pack-office":("Prise de notes à un bureau",1067),
 "formation-excel":("Graphiques et données sur un écran",1160),
 "formation-microsoft-365":("Réunion en visioconférence sur un ordinateur portable",1200),
}
def photo(path, name, cls="", sizes="(max-width: 900px) 100vw, 1200px", eager=False):
    alt, h = PHOTOS[name]
    b = L(path, "assets/photos/" + name)
    return (f'<figure class="ph {cls}"><img src="{b}.jpg" srcset="{b}-800.jpg 800w, {b}.jpg 1600w" sizes="{sizes}" '
            f'alt="{E(alt)}" width="1600" height="{h}" {"fetchpriority=high" if eager else "loading=lazy"} decoding="async"></figure>')
def video(path, name, label, cls=""):
    return (f'<figure class="vid {cls}"><video autoplay muted loop playsinline preload="metadata" aria-label="{E(label)}">'
            f'<source src="{L(path,"assets/video/"+name+".mp4")}" type="video/mp4"></video></figure>')

# ------------------------------------------------------------------ blocs partagés
def financement(path, mention=True):
    cols = "".join(f'<article><span class="num">{chr(65+i)}</span><h3>{E(a)}</h3><span class="sub">{E(b)}</span><p>{E(c)}</p></article>'
                   for i, (a, b, c) in enumerate(S.FINANCEMENT))
    note = f'<p class="fund-note">{S.CPF_MENTION}</p>' if mention else ""
    return f'''<section class="section section--paper2" id="financement"><div class="wrap">
<div class="shead rv"><div><span class="label">Financement</span><h2>Comment financer <em>ma formation</em> ?</h2></div>
<p>Financer votre formation n’a jamais été aussi simple ! Voici les principales options à votre disposition. Nos conseillers vous accompagnent dans vos démarches.</p></div>
<div class="fund rv">{cols}</div>{note}
<div class="btns" style="margin-top:2.4rem"><a class="btn" href="{S.RDV}">Étudier mon financement avec un conseiller</a></div>
</div></section>'''

def avis(title="Ce que disent <em>nos apprenants</em>", intro=None, n=10):
    items = "".join(f'<figure class="review"><blockquote>{E(t)}</blockquote><figcaption>{E(a)} · Avis Google</figcaption></figure>' for a, t in S.AVIS[:n])
    return f'''<section class="section"><div class="wrap">
<div class="shead rv"><div><span class="label">Avis vérifiés</span><h2>{title}</h2></div>
<div><div class="reviews__top"><span class="stars" aria-label="5 étoiles sur 5">★★★★★</span><span class="label">{S.AVIS_NOTE}</span></div>{f"<p>{intro}</p>" if intro else ""}</div></div>
<div class="reviews">{items}</div></div></section>'''

def contact_band(path, title="Contactez-nous pour démarrer votre formation <em>éligible CPF</em>"):
    return f'''<section class="section section--navy" id="contact"><div class="wrap cta">
<div class="rv"><span class="label">Contact</span><h2 style="margin-top:1.2rem">{title}</h2></div>
<div class="cta__side rv"><p>Besoin d’aide pour choisir votre formation ? Notre équipe vous accompagne dans le choix de la formation idéale et dans vos démarches de financement (CPF, OPCO, FAF, France Travail).</p>
<div class="cta__contacts"><a href="tel:{S.PHONE_INTL}">{S.PHONE}</a><a href="mailto:{S.EMAIL}">{S.EMAIL}</a></div>
<div class="btns"><a class="btn btn--light" href="{S.RDV}">Prendre rendez-vous avec un conseiller</a></div></div>
</div></section>'''

def qualiopi_band(path, programme=None, programme_label="Recevez le programme complet"):
    prog = ""
    if programme:
        ext = programme.startswith("http")
        href = programme if ext else L(path, programme)
        prog = f'<a class="btn {"btn--ext" if ext else "btn--dl"}" href="{href}" {"rel=noopener" if ext else ""}>{programme_label}</a>'
    return f'''<section class="section--tight"><div class="wrap"><div class="docband">
<a href="{L(path,S.LINKS["qualiopi_pdf"])}"><img src="{L(path,"assets/img/Logo-Qualiopi-300dpi-Avec-Marianne-1.jpg")}" alt="Certifié Qualiopi" width="180" height="72" loading="lazy"></a>
<p>{S.QUALIOPI_TEXT} <a class="link" href="{S.LINKS["qualiopi_drive"]}" rel="noopener">Télécharger le certificat</a></p>
<div class="btns">{prog}</div></div></div></section>'''

def post_card(path, p, cls="post-card"):
    return (f'<a class="{cls}" href="{L(path,p["slug"]+"/")}"><div class="post-card__img"><img src="{L(path,p["cover"])}" alt="" width="1200" height="630" loading="lazy"></div>'
            f'<div class="meta"><span class="label label--brass">{S.CATEGORIES[p["category"]]}</span><span class="label">{fdate(p["date"])}</span></div>'
            f'<h3>{E(p["title"])}</h3><p>{E(p["description"])}</p></a>')

# ------------------------------------------------------------------ articles
def load_posts():
    posts = []
    d = os.path.join(ROOT, "content", "posts")
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".html"): continue
        raw = open(os.path.join(d, fn)).read()
        m = re.match(r"<!--\s*(\{.*?\})\s*-->\s*(.*)", raw, re.S)
        meta = json.loads(m.group(1)); meta["html"] = m.group(2)
        meta["words"] = len(strip(meta["html"]).split())
        posts.append(meta)
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts

# ------------------------------------------------------------------ pages
def build_home(posts):
    path = ""
    toc = "".join(f'<li><a href="{L(path,f["slug"]+"/")}"><span class="num">{i:02d}</span><b>{E(f["short"])}</b><small>{f["code"]}</small></a></li>'
                  for i, f in enumerate(FORMATIONS, 1))
    rows = "".join(f'''<a class="index__row" href="{L(path,f["slug"]+"/")}"><span class="num">{i:02d}</span>
<span class="index__title">{E(f["short"])}<small>{E(strip(f["display_title"]))}</small></span>
<span class="mono c-dom">{DOMAINS[f["domain"]]}</span><span class="mono c-cert">{f["code"]}</span><span class="mono c-dur">{E(dur(f))}</span><span class="index__go" aria-hidden="true">→</span></a>'''
                   for i, f in enumerate(FORMATIONS, 1))
    rows += f'''<a class="index__row" href="{S.RDV}"><span class="num">{len(FORMATIONS)+1:02d}</span><span class="index__title">Formation sur mesure<small>Un programme construit pour vous, en individuel ou en collectif</small></span><span class="mono c-dom">Toutes thématiques</span><span class="mono c-cert">Sur devis</span><span class="mono c-dur">À définir</span><span class="index__go" aria-hidden="true">→</span></a>'''
    univ = [("Intelligence artificielle","formation-intelligence-artificielle/","Découvrez comment l’IA peut transformer vos projets et votre carrière : de l’IA générative à l’automatisation, en passant par le marketing de contenus."),
            ("Pack Office","formation-pack-office-2/","Gagnez en productivité avec une maîtrise complète des outils bureautiques. Apprenez à créer des documents, analyser des données et collaborer."),
            ("Sur mesure",None,"Nous créons un programme adapté à vos besoins, qu’il s’agisse d’une formation individuelle ou collective. Contenu, durée, objectifs : tout est ajusté pour répondre à vos attentes.")]
    uimg = ["ia", "office", "sur-mesure"]
    uni = "".join(f'<article>{photo(path, uimg[i], "ph--card", "(max-width: 860px) 100vw, 400px")}<span class="num">{chr(65+i)}</span><h3>{t}</h3><p>{d}</p><a class="link-arrow small" href="{L(path,u) if u else S.RDV}">{"Découvrir" if u else "Nous contacter"}</a></article>' for i,(t,u,d) in enumerate(univ))
    figs = "".join(f'<div><b>{a}<sup>{b}</sup></b><span>{c}</span></div>' for a, b, c in S.CHIFFRES)
    latest = "".join(post_card(path, p) for p in posts[:3])
    flag = next(f for f in FORMATIONS if f.get("flagship"))
    body = f'''
<section class="hero"><div class="wrap">
<div class="hb"><div><span class="chip">★ Organisme certifié Qualiopi</span>
<h1>Développez vos compétences à votre rythme, où que vous soyez, avec nos formations en ligne éligibles CPF</h1>
<div class="btns"><a class="btn btn--lime" href="{S.RDV}">Contacter un conseiller</a><a class="btn btn--line" href="#formations">Voir les formations</a></div>
<a class="hero__sante" href="{S.LINKS["sante"]}" rel="noopener">Découvrez aussi nos formations Santé ↗</a></div>
{video(path,"formation-paperboard","Séance de formation animée par un formateur")}</div>
<div class="logos">
<a href="{L(path,S.LINKS["qualiopi_pdf"])}"><img src="{L(path,"assets/img/Logo-Qualiopi-300dpi-Avec-Marianne-1.jpg")}" alt="Qualiopi" width="110" height="40">Certifié Qualiopi</a>
<a href="{S.LINKS["cpf_home"]}" rel="noopener"><img src="{L(path,"assets/img/Logo-officiel-cpf-1.png")}" alt="Mon Compte Formation" width="70" height="40">Éligible CPF</a>
<a href="{S.LINKS["france_travail"]}" rel="noopener"><img src="{L(path,"assets/img/logo-france-travail-removebg-preview.webp")}" alt="France Travail" width="70" height="40">France Travail</a>
<div><img src="{L(path,"assets/img/OPCO-logo-Cib-formation-1.png")}" alt="OPCO" width="70" height="40">Finançable OPCO</div></div>
<div class="hero__toc"><aside class="hero__aside" aria-label="Sommaire des formations"><span class="label"><span>Sommaire</span><span>{len(FORMATIONS)} formations certifiantes</span></span><ol class="toc">{toc}</ol></aside></div>
</div></section>
<section class="section" id="formations"><div class="wrap">
<div class="shead rv"><div><span class="label">Nos formations</span><h2>Un parcours <em>adapté</em> à vos besoins</h2></div>
<p>Découvrez nos formations 100 % en ligne, conçues pour s’adapter à votre rythme. Que vous souhaitiez maîtriser de nouvelles technologies ou améliorer vos performances professionnelles, nos programmes certifiés et éligibles au CPF vous accompagnent à chaque étape pour transformer vos ambitions en réalité.</p></div>
<div class="univers rv">{uni}</div>
<div style="height:clamp(48px,6vw,88px)"></div>
<div class="index rv" role="list">
<div class="index__row index__head" aria-hidden="true"><span>N°</span><span>Formation</span><span>Univers</span><span>Certification</span><span>Durée</span><span></span></div>
{rows}</div>
<div class="btns" style="margin-top:2.4rem"><a class="btn" href="{S.RDV}">Contacter un conseiller</a></div>
</div></section>
<section class="section section--navy"><div class="wrap">
<div class="shead rv"><div><span class="label">Chiffres clés</span><h2>Des résultats <em>qui parlent</em></h2></div>
<p>Choisir notre formation, c’est opter pour l’excellence et la réussite. Découvrez en quelques chiffres clés pourquoi nos apprenants nous font confiance.</p></div>
<div class="figures rv">{figs}</div>
<div class="figures2 rv"><p><b>100 %</b>de nos modules sont accessibles 24/7, pour apprendre à votre rythme, où que vous soyez.</p><p><b>95 %</b>des apprenants recommandent nos formations pour leur qualité et leur pertinence.</p></div>
</div></section>
<section class="section"><div class="wrap split">
<div class="rv"><span class="label">Le centre</span><h2 style="margin-top:1.2rem">Un centre de formation dédié à <em>votre réussite</em></h2>
<p class="lead">Notre centre vous accompagne à chaque étape de votre parcours. Avec des programmes certifiés Qualiopi et éligibles au CPF, nous proposons des solutions flexibles, accessibles 24/7, et adaptées à vos besoins.</p></div>
<div class="rv">{video(path,"visio","Formation suivie à distance en visioconférence","vid--side")}<p class="pull" style="margin-top:2rem">Que vous souhaitiez développer vos compétences, évoluer professionnellement ou vous reconvertir, nous sommes là pour transformer vos ambitions en réussite.</p>
<div style="margin-top:2.4rem;padding-top:1.6rem;border-top:1px solid var(--rule)"><span class="label label--brass">Notre formation phare</span>
<h3 style="font-size:1.7rem;margin:.6rem 0 .6rem">{flag["display_title"]}</h3><p class="muted">{flag["code"]} · {E(flag["facts"][0][1])}</p><a class="link-arrow" href="{L(path,flag["slug"]+"/")}">Découvrir la formation</a></div></div>
</div></section>
{financement(path)}
{avis()}
<section class="section section--card"><div class="wrap">
<div class="shead rv"><div><span class="label">Le blog</span><h2>Apprendre, <em>chaque semaine</em></h2></div><p>IA, marketing digital, Pack Office : des articles concrets pour progresser entre deux formations. <a class="link-arrow" href="{L(path,"blog/")}">Tous les articles</a></p></div>
<div class="posts">{latest}</div></div></section>
{contact_band(path)}'''
    ld = [{"@context":"https://schema.org","@type":"EducationalOrganization","name":"Konig Formation","legalName":"SARL Konig","url":S.SITE_URL+"/",
           "logo":S.SITE_URL+"/assets/img/konig-formation-2.png","telephone":S.PHONE_INTL,"email":S.EMAIL,
           "address":{"@type":"PostalAddress","streetAddress":"125 Boulevard du Général Koenig","postalCode":"92200","addressLocality":"Neuilly-sur-Seine","addressCountry":"FR"},
           "sameAs":[S.LINKS["instagram"],S.LINKS["facebook"]]}]
    page(path, "Formations en ligne certifiées CPF | Konig Formation",
         "Konig Formation, organisme certifié Qualiopi : formations en ligne certifiantes et éligibles CPF en intelligence artificielle et Pack Office.",
         body, jsonld=ld)

def build_formation(f, i):
    path = f["slug"] + "/"
    hub = next((h for h in HUBS if h["domain"] == f["domain"]), None)
    crumbs = f'<a href="{L(path,"")}">Accueil</a><span>/</span>' + (f'<a href="{L(path,hub["slug"]+"/")}">{DOMAINS[f["domain"]]}</a><span>/</span>' if hub else f'{DOMAINS[f["domain"]]}<span>/</span>') + E(f["short"])
    facts = "".join(f"<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>" for a, b in f["facts"])
    if f.get("public"): pass
    secs = [("presentation","Présentation"),("programme","Programme"),("objectifs","Objectifs"),("certification","Certification"),("avantages","Avantages"),("debouches","Débouchés")]
    if f.get("form"): pass
    side = "".join(f'<li><a href="#{a}">{t}</a></li>' for a, t in secs) + '<li><a href="#financement">Financement</a></li>'
    mods = "".join(f'''<details{" open" if k==1 else ""}><summary><span class="num">Module {k:02d}</span><b>{t}</b><i aria-hidden="true">+</i></summary><div class="mbody"><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></div></details>'''
                   for k, (t, items) in enumerate(f["modules"], 1))
    req = f'<div><h3>Prérequis</h3><div class="prose">{blocks(f["prereq"])}</div></div>'
    if f.get("public"): req += f'<div><h3>Public</h3><p>{f["public"]}</p></div>'
    objs = "".join(f"<div><h3>{E(t)}</h3><p>{E(d)}</p></div>" for t, d in f["objectifs"])
    feats = "".join(f"<div><h3>{E(t)}</h3><p>{E(d)}</p></div>" for t, d in f["avantages"]) + f"<div><h3>Référent handicap</h3><p>{E(S.HANDICAP)}</p></div>"
    note = f'<p class="note">{E(f["price_note"])}</p>' if f.get("price_note") else ""
    prog_ext = f["programme"].startswith("http")
    prog_href = f["programme"] if prog_ext else L(path, f["programme"])
    body = f'''
<div class="wrap crumbs">{crumbs}</div>
<section class="phero"><div class="wrap phero__grid">
<div><span class="label label--brass">Formation certifiante · {f["code"]}{(" · " + E(f["kicker_extra"])) if f.get("kicker_extra") else ""}</span>
<h1>{f["display_title"]}</h1>
<p class="official"><b>Intitulé :</b> {E(f["title"])}</p>
{"".join(f'<p class="lead">{x}</p>' for x in f["lead"])}
<div class="btns" style="margin-top:2rem"><a class="btn" href="{S.RDV}">{E(f["hero_cta"])}</a><a class="btn btn--ghost {"btn--ext" if prog_ext else "btn--dl"}" href="{prog_href}" {"rel=noopener" if prog_ext else ""}>Programme</a></div>
<p class="cpfnote">{S.CPF_MENTION}</p></div>
<aside class="fiche"><h2>Fiche technique</h2><dl>{facts}</dl>{note}
<div class="fiche__logos"><a href="{f["cpf"]}" rel="noopener" title="Voir sur Mon Compte Formation"><img src="{L(path,"assets/img/Logo-officiel-cpf-1.png")}" alt="Mon Compte Formation" width="90" height="44"></a><img src="{L(path,"assets/img/logo-france-travail-removebg-preview.webp")}" alt="France Travail" width="90" height="44"><a href="{L(path,S.LINKS["qualiopi_pdf"])}"><img src="{L(path,"assets/img/Logo-Qualiopi-300dpi-Avec-Marianne-1.jpg")}" alt="Qualiopi" width="100" height="44"></a></div></aside>
</div></section>
<div class="wrap">{photo(path, f["slug"], "ph--wide", eager=False)}</div>
<div class="wrap doc">
<aside class="toc-side"><span class="label">Sur cette page</span><ol>{side}</ol><a class="btn" href="{S.RDV}">Parler à un conseiller</a></aside>
<div>
<section class="block" id="presentation"><h2><span class="num">01</span>{f["intro_title"]}</h2><div class="prose">{blocks(f["intro"])}</div></section>
<section class="block" id="programme"><h2><span class="num">02</span>Programme de formation</h2>
<div class="req">{req}</div>
<div class="modtools"><span class="label">{len(f["modules"])} modules</span><button type="button" data-toggle-modules>Tout déplier</button></div>
<div class="modules">{mods}</div></section>
<section class="block" id="objectifs"><h2><span class="num">03</span>Objectifs de la formation</h2><div class="objs">{objs}</div></section>
<section class="block" id="certification"><h2><span class="num">04</span>Certification et évaluation</h2>
<div class="certbox"><span class="label">Certification enregistrée à France Compétences</span><div class="code">{f["code"]}</div><div class="prose">{blocks(f["certif"])}</div>
<a class="btn btn--light btn--ext" href="{f["certif_link"]}" rel="noopener" style="margin-top:.8rem">Fiche France Compétences</a></div></section>
<section class="block" id="avantages"><h2><span class="num">05</span>Les avantages de cette formation</h2><div class="feats">{feats}</div></section>
<section class="block" id="debouches"><h2><span class="num">06</span>{f["debouches_title"]}</h2><div class="prose">{blocks(f["debouches"])}</div>
<div class="btns" style="margin-top:1.6rem"><a class="btn" href="{S.RDV}">Contacter un conseiller</a></div></section>
</div></div>
{financement(path, mention=False)}
{avis()}
{contact_band(path, "Vous souhaitez en savoir plus sur <em>cette formation</em> ?")}
{qualiopi_band(path, f["programme"])}'''
    ld = [{"@context":"https://schema.org","@type":"Course","name":f["title"],"description":f["description"],"courseCode":f["code"],
           "provider":{"@type":"EducationalOrganization","name":"Konig Formation","sameAs":S.SITE_URL+"/"},
           "hasCourseInstance":{"@type":"CourseInstance","courseMode":"online","inLanguage":"fr"}}]
    page(path, f'{f["menu"]} certifiante ({f["code"]}) | Konig Formation', f["description"], body, jsonld=ld)

def build_hub(h):
    path = h["slug"] + "/"
    cards = "".join(f'<a href="{L(path,s+"/")}" class="rv">{photo(path, s, "ph--card", "(max-width: 900px) 100vw, 400px")}<span class="mono">{FBY[s]["code"]} · {E(dur(FBY[s]))}</span><h3>{E(FBY[s]["short"])}</h3><p>{d}</p><span class="link-arrow small">En savoir plus</span></a>' for s, d in h["items"])
    formats = ""
    if h.get("formats"):
        formats = '<div class="feats" style="margin-top:2rem">' + "".join(f"<div><h3>{E(t)}</h3><p>{E(d)}</p></div>" for t, d in h["formats"]) + "</div>"
    feats = "".join(f"<div><h3>{t}</h3><p>{d}</p></div>" for t, d in [
        ("Formation reconnue : certifiée Qualiopi et éligible CPF","Profitez d’une formation certifiée répondant aux standards de qualité les plus exigeants. Grâce à son éligibilité au CPF, vous pouvez financer tout ou partie de votre parcours."),
        ("Accompagnement personnalisé","Vous n’êtes jamais seul : un formateur expert vous accompagne tout au long de votre parcours, avec des conseils personnalisés et un suivi régulier.")])
    body = f'''
<div class="wrap crumbs"><a href="{L(path,"")}">Accueil</a><span>/</span>{DOMAINS[h["domain"]]}</div>
<section class="phero"><div class="wrap"><span class="label label--brass">{DOMAINS[h["domain"]]} · {len(h["items"])} formations certifiantes</span>
<h1 style="max-width:18ch">{h["display_title"]}</h1><p class="lead">{h["lead"]}</p>
<div class="btns" style="margin-top:2rem"><a class="btn" href="{S.RDV}">Boostez votre carrière avec une certification</a><a class="btn btn--ghost" href="#parcours">Voir les parcours</a></div></div></section>
<div class="wrap">{photo(path, "ia" if h["domain"]=="ia" else "office", "ph--wide")}</div>
<section class="section" id="parcours"><div class="wrap">
<div class="shead rv"><div><span class="label">Pourquoi se former</span><h2>{h["why_title"]}</h2></div><p>{h["why"]}</p></div>
<div class="hubs">{cards}</div>{formats}</div></section>
<section class="section section--paper2"><div class="wrap split">
<div class="rv"><span class="label">Certification</span><h2 style="margin-top:1.2rem">Une certification <em>reconnue</em> par France Compétences</h2><p class="lead">{h["certif"]}</p>
<p class="muted">{h["avantages_intro"]}</p><div class="feats" style="margin-top:1.6rem">{feats}</div></div>
<div class="rv"><span class="label">Débouchés</span><h2 style="margin-top:1.2rem">Quels débouchés <em>après la formation</em> ?</h2><div class="prose">{blocks(h["debouches"])}</div>
<div class="btns" style="margin-top:1.4rem"><a class="btn" href="{S.RDV}">Contacter un conseiller</a></div></div>
</div></section>
{financement(path, mention=False)}
{avis()}
{contact_band(path, f"Vous souhaitez en savoir plus sur nos formations <em>{DOMAINS[h['domain']].lower()}</em> ?")}
{qualiopi_band(path)}'''
    page(path, f'{h["menu"]} certifiante, éligible CPF | Konig Formation', h["description"], body)

def build_blog(posts):
    def listing(path, items, current, title, intro):
        filt = f'<a href="{L(path,"blog/")}" {"aria-current=page" if current is None else ""}>Tous</a>' + "".join(
            f'<a href="{L(path,"category/"+k+"/")}" {"aria-current=page" if current==k else ""}>{v}</a>' for k, v in S.CATEGORIES.items())
        first, rest = items[0], items[1:]
        feat = (f'<a class="post-feature" href="{L(path,first["slug"]+"/")}"><div class="post-card__img"><img src="{L(path,first["cover"])}" alt="" width="1200" height="630"></div>'
                f'<div><div class="meta" style="display:flex;gap:.8rem"><span class="label label--brass">{S.CATEGORIES[first["category"]]}</span><span class="label">{fdate(first["date"])}</span></div>'
                f'<h2>{E(first["title"])}</h2><p class="muted">{E(first["description"])}</p><span class="link-arrow">Lire l’article</span></div></a>')
        grid = "".join(post_card(path, p) for p in rest)
        return f'''<section class="phero" style="border:0;padding-bottom:0"><div class="wrap"><span class="label label--brass">Le blog Konig Formation · {len(items)} articles</span>
<h1 style="max-width:16ch">{title}</h1><p class="lead">{intro}</p></div></section>
<section class="section" style="padding-top:clamp(32px,4vw,56px)"><div class="wrap"><nav class="filters" aria-label="Catégories">{filt}</nav>{feat}<div class="posts">{grid}</div></div></section>
{contact_band(path, "Prêt à passer <em>à la pratique</em> ?")}'''
    page("blog/", "Blog — IA, marketing digital et Pack Office | Konig Formation",
         "Articles concrets sur l’intelligence artificielle, le marketing digital et le Pack Office (Excel, Word, Copilot) par Konig Formation, organisme certifié Qualiopi.",
         listing("blog/", posts, None, "Apprendre, <em>chaque semaine</em>", "Intelligence artificielle, marketing digital, Pack Office : des méthodes concrètes, des nouveautés décryptées et quelques idées reçues démontées."))
    for k, v in S.CATEGORIES.items():
        items = [p for p in posts if p["category"] == k]
        path = f"category/{k}/"
        page(path, f"{v} — Blog | Konig Formation", f"Tous les articles du blog Konig Formation consacrés à : {v}.",
             listing(path, items, k, f"<em>{v}</em>", f"Les articles du blog consacrés à : {v.lower()}."))

def build_post(p, posts):
    path = p["slug"] + "/"
    pr = pre(path)
    content = re.sub(r'href="/(?!/)', f'href="{pr}', p["html"])
    mins = max(2, round(p["words"] / 220))
    related = [q for q in posts if q["category"] == p["category"] and q["slug"] != p["slug"]][:3]
    rel = "".join(post_card(path, q) for q in related)
    body = f'''
<div class="wrap crumbs"><a href="{L(path,"")}">Accueil</a><span>/</span><a href="{L(path,"blog/")}">Blog</a><span>/</span><a href="{L(path,"category/"+p["category"]+"/")}">{S.CATEGORIES[p["category"]]}</a></div>
<header class="ahead"><div class="wrap"><div class="meta"><span class="label label--brass">{S.CATEGORIES[p["category"]]}</span><span class="label">{fdate(p["date"])}</span><span class="label">{mins} min de lecture</span></div>
<h1>{E(p["title"])}</h1></div></header>
<div class="wrap"><img class="acover" src="{L(path,p["cover"])}" alt="" width="1200" height="630"></div>
<div class="wrap alayout"><article class="article">{content}</article>
<aside><div class="aside-cta"><span class="label">Se former</span><h2>Passez de la lecture <em>à la pratique</em></h2><p>Formations certifiantes, éligibles CPF, 100 % à distance. Un conseiller vous répond et étudie votre financement.</p><a class="btn btn--light" href="{S.RDV}">Prendre rendez-vous</a><p class="small" style="margin:1rem 0 0"><a href="{L(path,"")}#formations">Voir les formations</a></p></div></aside></div>
{f'<section class="section section--card"><div class="wrap"><div class="shead"><div><span class="label">À lire ensuite</span><h2>Dans la même <em>catégorie</em></h2></div></div><div class="posts">{rel}</div></div></section>' if rel else ""}'''
    ld = [{"@context":"https://schema.org","@type":"BlogPosting","headline":p["title"],"description":p["description"],"datePublished":p["date"],
           "image":S.SITE_URL+"/"+p["cover"],"author":{"@type":"Organization","name":"Konig Formation"},"publisher":{"@type":"Organization","name":"Konig Formation"},
           "mainEntityOfPage":S.SITE_URL+"/"+path}]
    page(path, f'{p["title"]} | Konig Formation', p["description"], body, jsonld=ld, og_img=p["cover"], og_type="article")


def build_programmes():
    path = "programmes/"
    items = []
    for i, f in enumerate(FORMATIONS, 1):
        mods = "".join(f'<li><span class="num">Module {k:02d}</span> {t}</li>' for k, (t, _) in enumerate(f["modules"], 1))
        ext = f["programme"].startswith("http")
        href = f["programme"] if ext else L(path, f["programme"])
        facts = " · ".join(E(b) for a, b in f["facts"][:2])
        items.append(f'''<article class="prog rv" id="{f["slug"]}">{photo(path, f["slug"], "ph--prog", "(max-width: 760px) 100vw, 360px")}
<div class="prog__head"><span class="num">{i:02d}</span><div><span class="label label--brass">{DOMAINS[f["domain"]]} · {f["code"]}</span>
<h2>{f["display_title"]}</h2><p class="muted">{facts}</p></div></div>
<ol class="prog__mods">{mods}</ol>
<div class="btns"><a class="btn {"btn--ext" if ext else "btn--dl"}" href="{href}" {"rel=noopener" if ext else ""}>Télécharger le programme</a><a class="btn btn--ghost" href="{L(path,f["slug"]+"/")}">Programme détaillé en ligne</a></div>
</article>''')
    body = f'''<div class="wrap crumbs"><a href="{L(path,"")}">Accueil</a><span>/</span>Programmes</div>
<section class="phero"><div class="wrap"><h1>Nos programmes de formation</h1>
<p class="lead">Le contenu de chaque formation, module par module. Chaque programme est téléchargeable et détaillé sur la fiche de la formation : objectifs, prérequis, modalités d’évaluation et certification.</p></div></section>
<section class="section" style="padding-top:0"><div class="wrap progs">{"".join(items)}</div></section>
{contact_band(path, "Une question sur un <em>programme</em> ?")}'''
    page(path, "Programmes de formation | Konig Formation", "Programmes détaillés des formations certifiantes Konig Formation : IA générative, IA et automatisation, IA et marketing de contenus, Word, Excel, Microsoft 365.", body)

def build_landing():
    path = "intelligence-artificielle-konig-formation/"
    f = FBY["formation-ia"]
    why = [("Certification officielle","Inscrite au Répertoire Spécifique (RS6776) et reconnue par France Compétences."),
           ("Prise en charge","Aucune avance de frais via Mon Compte Formation, France Travail ou OPCO."),
           ("Formation 100 % à distance","En visio, sur 3 jours, avec un formateur en direct."),
           ("Pratique et concrète","Utilisation réelle de ChatGPT, Gemini, Copilot, Adobe Firefly…"),
           ("Valorisez votre CV","La certification RS6776 est un vrai levier d’évolution professionnelle, reconnue par les employeurs."),
           ("Maîtrise des enjeux éthiques","Apprenez à créer du contenu sécurisé, conforme au RGPD et aux directives européennes (IA Act).")]
    w = "".join(f'<div><span class="num">{i:02d}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(why, 1))
    body = f'''
<section class="lp-hero"><div class="wrap lp-hero__grid">
<div><span class="label" style="color:var(--brass-2)">Formation certifiante · RS6776</span>
<h1>Maîtrisez l’<em>IA générative</em> pour booster votre carrière</h1>
<p class="lead" style="color:var(--on-navy-muted)">Une formation certifiante, finançable par votre CPF, France Travail ou votre OPCO.</p>
<span class="label" style="color:var(--on-navy-muted)">Contenu de la formation</span>
<ul><li>Stratégie d’implémentation de l’IA générative</li><li>Création de contenus rédactionnels et visuels (ChatGPT, Copilot, Firefly…)</li><li>Confidentialité et sécurité des données (RGPD)</li><li>Contenus inclusifs et accessibles</li><li>Conformité éthique et IA Act</li></ul></div>
<div class="lp-form"><span class="label label--brass">Vérifiez votre éligibilité</span><h2>Un conseiller vous rappelle et étudie votre <em>financement</em></h2>
<p class="muted">Réservez un créneau de 45 minutes en visio : nous vérifions ensemble vos droits CPF et la prise en charge possible.</p>
<div class="btns" style="flex-direction:column;align-items:stretch"><a class="btn" href="{S.RDV}" style="justify-content:space-between">Je vérifie mon éligibilité</a><a class="btn btn--ghost" href="tel:{S.PHONE_INTL}" style="justify-content:space-between">Appeler le {S.PHONE}</a></div></div>
</div></section>
<section class="section"><div class="wrap split">
<div class="rv"><span class="label">Certification</span><h2 style="margin-top:1.2rem">Obtenez une certification officielle <em>reconnue par l’État</em></h2>{photo(path,"groupe","ph--side")}</div>
<div class="rv"><p class="lead">À l’issue de la formation, vous passez la certification « Création de contenus rédactionnels et visuels par l’usage responsable de l’intelligence artificielle générative », enregistrée au Répertoire Spécifique de France Compétences sous le numéro RS6776.</p>
<div class="btns"><a class="btn" href="{S.RDV}">Je profite de la formation prise en charge</a><a class="link-arrow" href="{L(path,"formation-ia/")}">Programme détaillé</a></div></div></div></section>
<section class="section section--paper2"><div class="wrap">
<div class="shead rv"><div><span class="label">Pourquoi suivre la formation ?</span><h2>Une compétence devenue <em>indispensable</em></h2></div>
<p>L’intelligence artificielle n’est plus une simple tendance passagère. Elle transforme en profondeur les méthodes de travail dans tous les secteurs, en particulier dans les métiers du tertiaire. Savoir utiliser les outils d’IA générative n’est plus un atout, c’est devenu une compétence indispensable pour rester compétitif, gagner en efficacité et répondre aux nouvelles exigences des employeurs.</p></div>
<div class="why rv">{w}</div></div></section>
<section class="section section--navy"><div class="wrap">
<div class="shead rv"><div><span class="label">En chiffres</span><h2>Les chiffres <em>parlent d’eux-mêmes</em></h2></div></div>
<div class="figures rv" style="grid-template-columns:repeat(3,1fr)"><div><b>+82<sup>%</sup></b><span>des entreprises intègrent l’IA</span></div><div><b>3<sup>h/j</sup></b><span>de productivité gagnée en moyenne</span></div><div><b>+96<sup>%</sup></b><span>constatent un gain immédiat</span></div></div></div></section>
<section class="section"><div class="wrap split">
<div class="rv"><span class="label">Les outils</span><h2 style="margin-top:1.2rem">Les principaux outils d’<em>IA générative</em></h2>
<p class="muted">L’intelligence artificielle transforme notre façon de travailler, de créer et d’apprendre. Dans cette formation, vous découvrirez une sélection d’outils puissants pour booster votre productivité, stimuler votre créativité et optimiser votre efficacité au quotidien.</p></div>
<div class="rv tools"><span>ChatGPT</span><span>Google Gemini</span><span>Microsoft Copilot</span><span>Adobe Firefly</span><span>Midjourney</span></div></div></section>
{avis("Ils ont franchi le pas, <em>ils témoignent</em>", "Gain de temps, nouvelles opportunités professionnelles, montée en compétences… leurs témoignages parlent d’eux-mêmes.")}
<section class="section section--navy"><div class="wrap cta"><div><h2>Prêt à maîtriser l’<em>IA générative</em> ?</h2></div>
<div class="cta__side"><p>Inscrivez-vous dès maintenant à notre formation certifiante et apprenez à créer des contenus puissants avec ChatGPT, Copilot, Firefly et bien plus. Formation accessible sous 15 jours, compatible handicap.</p><a class="btn btn--light" href="{S.RDV}">Je vérifie mon éligibilité</a></div></div></section>'''
    page(path, "Formation IA générative certifiante RS6776 prise en charge | Konig Formation",
         "Maîtrisez l’IA générative (ChatGPT, Copilot, Firefly) avec une formation certifiante RS6776 à distance, finançable CPF, France Travail ou OPCO.",
         body, chrome="landing")

def build_legal():
    ml = f'''<div class="wrap legal"><span class="label label--brass">Informations légales</span><h1 style="font-size:var(--step-4)">Mentions légales</h1>
<h2>Édition du site</h2><p>Le site konigformation.com (ci-après « le Site ») est édité par Alexis ROMITO en qualité de gérant de SARL KONIG, société à responsabilité limitée (SARL) au capital social de 1 000 euros, immatriculée au Registre du Commerce et des Sociétés de Nanterre sous le numéro RCS Nanterre B 908 180 284.</p>
<p>Siège social : 125 Boulevard du Général Koenig, 92200 Neuilly-sur-Seine<br>Numéro SIRET : 908 180 284 00014<br>Numéro de TVA intracommunautaire : FR14908180284</p>
<p>Contact : téléphone {S.PHONE} — courriel <a href="mailto:{S.EMAIL}">{S.EMAIL}</a></p>
<p>Directeur de la publication : Alexis ROMITO, en qualité de gérant de SARL KONIG.</p>
<h2>Hébergement</h2><p>Le Site est hébergé par GitHub, Inc. (service GitHub Pages), 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis — <a href="https://github.com/contact" rel="noopener">github.com/contact</a>.</p>
<h2>Conception du site</h2><p>Conception initiale : El Jaouhari Younes, webmaster indépendant (SIRET 979 797 966 00012). Refonte 2026 : Konig Formation.</p>
<h2>Crédits photos et vidéos</h2><p>Photographies : Unsplash (licence Unsplash). Vidéos : Pexels (licence Pexels).</p>
<h2>Propriété intellectuelle</h2><p>L’ensemble des contenus du Site (textes, logo, éléments graphiques) est la propriété de SARL KONIG, sauf mention contraire. Toute reproduction sans autorisation préalable est interdite.</p></div>'''
    page("mentions-legales/", "Mentions légales | Konig Formation", "Mentions légales du site konigformation.com — SARL Konig, Neuilly-sur-Seine.", ml)
    pc = f'''<div class="wrap legal"><span class="label label--brass">Informations légales</span><h1 style="font-size:var(--step-4)">Politique de confidentialité</h1>
<p>Konig Formation (« nous », « notre », « nos ») exploite le site konigformation.com (ci-après le « Service »). Cette page explique nos politiques en matière de collecte, d’utilisation et de communication des données à caractère personnel lorsque vous utilisez notre Service, ainsi que les choix qui s’offrent à vous concernant ces données.</p>
<h2>Définitions</h2>
<p><strong>Service</strong> — le site konigformation.com exploité par SARL Konig.</p>
<p><strong>Données à caractère personnel</strong> — données concernant un individu vivant qui peut être identifié à partir de ces données (ou à partir de ces données et d’autres informations en notre possession ou susceptibles d’entrer en notre possession).</p>
<p><strong>Données d’utilisation</strong> — données recueillies automatiquement, générées par l’utilisation du Service ou par son infrastructure (par exemple, durée de consultation d’une page).</p>
<p><strong>Responsable du traitement</strong> — la personne qui détermine les finalités et modalités de traitement des données à caractère personnel. Aux fins de la présente politique, nous sommes le responsable du traitement de vos données.</p>
<p><strong>Sous-traitants</strong> — toute personne physique ou morale qui traite les données au nom du responsable du traitement.</p>
<h2>Données recueillies</h2>
<p>Lorsque vous nous contactez (téléphone, e-mail, prise de rendez-vous), nous pouvons vous demander des données permettant de vous recontacter : adresse e-mail, prénom et nom, numéro de téléphone.</p>
<p>Comme tout site web, l’hébergeur du Service peut enregistrer des données techniques de connexion (adresse IP, type et version du navigateur, pages visitées, heure de la visite) à des fins de sécurité et de bon fonctionnement.</p>
<p>Le Service n’utilise pas de cookies publicitaires ni de traceurs de mesure d’audience.</p>
<h2>Utilisation des données</h2><ul><li>Répondre à vos demandes et vous accompagner dans votre projet de formation et son financement ;</li><li>Fournir et maintenir le Service ;</li><li>Garantir la sécurité et détecter d’éventuelles failles techniques.</li></ul>
<h2>Fondement juridique</h2><p>En vertu du Règlement Général sur la Protection des Données (RGPD), le traitement de vos données repose sur : votre consentement, l’exécution d’un contrat ou de mesures précontractuelles, une obligation légale, ou nos intérêts légitimes, sauf si vos droits priment ces intérêts.</p>
<h2>Conservation</h2><p>Nous conservons vos données aussi longtemps que nécessaire aux fins décrites dans cette politique, sauf obligation légale contraire.</p>
<h2>Communication des données</h2><p>Nous pouvons partager vos données pour répondre à une obligation légale, pour protéger nos droits, ou avec des prestataires de services intervenant pour notre compte (hébergement, prise de rendez-vous, messagerie).</p>
<h2>Sécurité</h2><p>Nous nous efforçons de protéger vos données, mais aucune méthode de transmission sur Internet n’est sûre à 100 %.</p>
<h2>Vos droits</h2><p>Conformément au RGPD, vous disposez d’un droit d’accès, de rectification, d’opposition et de limitation du traitement, d’effacement et de portabilité de vos données. Pour les exercer : <a href="mailto:{S.EMAIL}">{S.EMAIL}</a>. Vous pouvez également introduire une réclamation auprès de la CNIL.</p>
<h2>Liens externes</h2><p>Le Service contient des liens vers des sites tiers (Mon Compte Formation, France Compétences, prise de rendez-vous…). Nous ne sommes pas responsables de leur contenu ni de leurs politiques de confidentialité.</p>
<h2>Modifications</h2><p>Nous nous réservons le droit de modifier cette politique. Les modifications seront publiées sur cette page.</p></div>'''
    page("politique-de-confidentialite/", "Politique de confidentialité | Konig Formation", "Politique de confidentialité et protection des données personnelles — Konig Formation.", pc)
    merci = f'''<section class="section"><div class="wrap" style="max-width:760px;text-align:center"><span class="label label--brass">Merci</span>
<h1 style="font-size:var(--step-4);margin-top:1rem">Votre demande a bien été <em>envoyée</em></h1>
<p class="lead" style="margin:0 auto 1rem">Nous avons bien reçu votre message et nous vous remercions de nous avoir contactés. Notre équipe va traiter votre demande avec soin et vous répondra sous 24 heures ouvrées.</p>
<p>Encore merci pour votre confiance et à très bientôt !<br><em>L’équipe Konig Formation</em></p>
<div class="btns" style="justify-content:center;margin-top:2rem"><a class="btn" href="{L("page-de-remerciement/","")}">Retour à l’accueil</a></div></div></section>'''
    page("page-de-remerciement/", "Merci | Konig Formation", "Votre demande a bien été envoyée.", merci, robots="noindex")
    nf = f'''<section class="section"><div class="wrap" style="max-width:760px"><span class="label label--brass">Erreur 404</span>
<h1 style="font-size:var(--step-5);margin-top:1rem">Page <em>introuvable</em></h1><p class="lead">Cette page n’existe pas ou a été déplacée lors de la refonte du site.</p>
<div class="btns"><a class="btn" href="/">Retour à l’accueil</a><a class="btn btn--ghost" href="/blog/">Le blog</a></div></div></section>'''
    page("404.html", "Page introuvable | Konig Formation", "Page introuvable.", nf, robots="noindex")

def redirect(path, target):
    dest = os.path.join(OUT, path, "index.html"); os.makedirs(os.path.dirname(dest), exist_ok=True)
    url = S.SITE_URL + "/" + target
    open(dest, "w").write(f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Redirection</title><link rel="canonical" href="{url}"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url={L(path,target)}"></head><body><a href="{L(path,target)}">Continuer vers la page</a></body></html>')

def favicon():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#0A2A4E"/>'
           '<text x="32" y="46" text-anchor="middle" font-family="Didot,Bodoni 72,Georgia,serif" font-size="40" fill="#F3EFE6">K</text></svg>')
    open(os.path.join(OUT, "assets/img/favicon.svg"), "w").write(svg)

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, "static"), OUT)
    favicon()
    posts = load_posts()
    build_home(posts)
    for i, f in enumerate(FORMATIONS, 1): build_formation(f, i)
    for h in HUBS: build_hub(h)
    build_blog(posts)
    for p in posts: build_post(p, posts)
    build_programmes(); build_landing(); build_legal()
    redirect("formations-en-ligne-certifiees-cpf/", "")
    redirect("formation-marketing-digital-en-ligne/", "")
    if CUSTOM_DOMAIN: open(os.path.join(OUT, "CNAME"), "w").write("www.konigformation.com\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {S.SITE_URL}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{S.SITE_URL}/{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in PAGES)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    print(f"OK — {len(PAGES)} pages indexables générées dans docs/")

if __name__ == "__main__":
    main()
