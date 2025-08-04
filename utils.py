import os
import requests
from bs4 import BeautifulSoup
import time
import unicodedata

CACHE_FILE = "force_content.txt"
TIMESTAMP_FILE = "cache_timestamp.txt"
EXPIRATION_SECONDS = 90 * 24 * 60 * 60  # 3 mois

URLS = [
   
"https://preprod2.force-n.sn",
"https://preprod2.force-n.sn/",
"https://preprod2.force-n.sn/?page=0",
"https://preprod2.force-n.sn/?page=1",
"https://preprod2.force-n.sn/a-propos",
"https://preprod2.force-n.sn/a-propos?page=0",
"https://preprod2.force-n.sn/a-propos?page=1",
"https://preprod2.force-n.sn/actualites",
"https://preprod2.force-n.sn/actualites?page=0",
"https://preprod2.force-n.sn/actualites?page=1",
"https://preprod2.force-n.sn/articles/animation-scientifique-eno-dakar-mermoz-28-juillet",
"https://preprod2.force-n.sn/articles/composante-aipen-participe-latelier-sur-les-besoins",
"https://preprod2.force-n.sn/articles/conference-de-ndioum-dans-le-cadre-de-la-vulgarisation",
"https://preprod2.force-n.sn/articles/exposition-force-n-met-les-mathematiques-lhonneur-au-musee-des-civilisations-noires",
"https://preprod2.force-n.sn/articles/force-n-lance-la-1ere-edition-du-forum-des-metiers-et-de-lentreprenariat",
"https://preprod2.force-n.sn/articles/force-n-lance-le-dispositif-ami-pour-promouvoir-lauto-emploi-des-jeunes-au-forum-foreme",
"https://preprod2.force-n.sn/articles/force-n-organise-un-bootcamp-pour-renforcer-le-leadership-de-ses-alumnis",
"https://preprod2.force-n.sn/articles/forum-economique-de-touba-darou-marnane-deuxieme-edition",
"https://preprod2.force-n.sn/articles/jipen-2025-force-n-mobilise-350-jeunes-autour-de-lentrepreneuriat-numerique-saint-louis",
"https://preprod2.force-n.sn/articles/journee-dintegration-du-reseau-des-alumni-2024-plus-masterclass",
"https://preprod2.force-n.sn/articles/lancement-de-la-plateforme-dapprentissage-stemd-au-lycee-limamou-laye",
"https://preprod2.force-n.sn/articles/le-programme-force-n-senegal-debute",
"https://preprod2.force-n.sn/articles/lun-chk-et-la-signent-une-convention-pour-le-developpement-des-competences-numeriques",
"https://preprod2.force-n.sn/articles/parc-2025-force-n-et-daust-font-de-saly-un-laboratoire-didees-de-science-de-technologie-et",
"https://preprod2.force-n.sn/articles/preparation-aux-olympiades",
"https://preprod2.force-n.sn/articles/semaine-des-sciences-diourbel-30-decembre-2022",
"https://preprod2.force-n.sn/carrieres",
"https://preprod2.force-n.sn/certificat/commerce-digital",
"https://preprod2.force-n.sn/certificat/cybersecurite",
"https://preprod2.force-n.sn/certificat/data-analysis",
"https://preprod2.force-n.sn/certificat/data-engineering",
"https://preprod2.force-n.sn/certificat/developpement-logiciel-java",
"https://preprod2.force-n.sn/certificat/developpement-logiciel-php",
"https://preprod2.force-n.sn/certificat/developpement-logiciel-python",
"https://preprod2.force-n.sn/certificat/developpement-mobile",
"https://preprod2.force-n.sn/certificat/ecriture-de-scenario",
"https://preprod2.force-n.sn/certificat/entrepreneuriat-numerique",
"https://preprod2.force-n.sn/certificat/front-end",
"https://preprod2.force-n.sn/certificat/intelligence-artificielle-pour-tous",
"https://preprod2.force-n.sn/certificat/intelligence-artificielle-traitement-du-langage-naturel-vision-par-ordinateur",
"https://preprod2.force-n.sn/certificat/internet-des-objets-iot",
"https://preprod2.force-n.sn/certificat/marketing-digital",
"https://preprod2.force-n.sn/certificat/modelisation",
"https://preprod2.force-n.sn/certificat/montage-video",
"https://preprod2.force-n.sn/certificat/no-code-low-code",
"https://preprod2.force-n.sn/certificat/pilotage-de-drones",
"https://preprod2.force-n.sn/certificat/prise-de-son-et-sound-design",
"https://preprod2.force-n.sn/certificat/salesforce",
"https://preprod2.force-n.sn/certificat/traitement-de-donnees-niveaux-1-2",
"https://preprod2.force-n.sn/certificat/web-3",
"https://preprod2.force-n.sn/commerce.digital@unchk.edu.sn ",
"https://preprod2.force-n.sn/composantes/aipen",
"https://preprod2.force-n.sn/composantes/fcc",
"https://preprod2.force-n.sn/composantes/stemd",
"https://preprod2.force-n.sn/en",
"https://preprod2.force-n.sn/en/about-us",
"https://preprod2.force-n.sn/en/about-us?page=0",
"https://preprod2.force-n.sn/en/about-us?page=1",
"https://preprod2.force-n.sn/en/articles/preparing-olympics",
"https://preprod2.force-n.sn/en/articles/second-edition-touba-darou-marnane-economic-forum",
"https://preprod2.force-n.sn/en/careers",
"https://preprod2.force-n.sn/en/cookie-policy",
"https://preprod2.force-n.sn/en/formations/artificial-intelligence-and-data",
"https://preprod2.force-n.sn/en/formations/creating-audiovisual-and-animated-content",
"https://preprod2.force-n.sn/en/formations/e-business",
"https://preprod2.force-n.sn/en/formations/emerging-technologies-and-cybersecurity",
"https://preprod2.force-n.sn/en/formations/software-development",
"https://preprod2.force-n.sn/en/initiatory-journey",
"https://preprod2.force-n.sn/en/legal-mentions",
"https://preprod2.force-n.sn/en/news",
"https://preprod2.force-n.sn/en/news?page=0",
"https://preprod2.force-n.sn/en/news?page=1",
"https://preprod2.force-n.sn/en/node",
"https://preprod2.force-n.sn/en/node/125",
"https://preprod2.force-n.sn/en/node/127",
"https://preprod2.force-n.sn/en/node/139",
"https://preprod2.force-n.sn/en/node/140",
"https://preprod2.force-n.sn/en/node/141",
"https://preprod2.force-n.sn/en/node/141?page=0",
"https://preprod2.force-n.sn/en/node/141?page=1",
"https://preprod2.force-n.sn/en/node/142",
"https://preprod2.force-n.sn/en/node/143",
"https://preprod2.force-n.sn/en/node/144",
"https://preprod2.force-n.sn/en/node/145",
"https://preprod2.force-n.sn/en/node/146",
"https://preprod2.force-n.sn/en/node/147",
"https://preprod2.force-n.sn/en/node/148",
"https://preprod2.force-n.sn/en/node/149",
"https://preprod2.force-n.sn/en/node/150",
"https://preprod2.force-n.sn/en/node/157",
"https://preprod2.force-n.sn/en/node/158",
"https://preprod2.force-n.sn/en/node/159",
"https://preprod2.force-n.sn/en/node/160",
"https://preprod2.force-n.sn/en/node/161",
"https://preprod2.force-n.sn/en/node/162",
"https://preprod2.force-n.sn/en/node/163",
"https://preprod2.force-n.sn/en/node/1?page=0",
"https://preprod2.force-n.sn/en/node/1?page=1",
"https://preprod2.force-n.sn/en/node/26",
"https://preprod2.force-n.sn/en/node/27",
"https://preprod2.force-n.sn/en/node/28",
"https://preprod2.force-n.sn/en/node/29",
"https://preprod2.force-n.sn/en/node/48",
"https://preprod2.force-n.sn/en/node/49",
"https://preprod2.force-n.sn/en/node/73",
"https://preprod2.force-n.sn/en/node/74",
"https://preprod2.force-n.sn/en/node/75",
"https://preprod2.force-n.sn/en/node/76",
"https://preprod2.force-n.sn/en/node/77",
"https://preprod2.force-n.sn/en/node/78",
"https://preprod2.force-n.sn/en/node/79",
"https://preprod2.force-n.sn/en/node/80",
"https://preprod2.force-n.sn/en/node/81",
"https://preprod2.force-n.sn/en/node/82",
"https://preprod2.force-n.sn/en/node/83",
"https://preprod2.force-n.sn/en/node/84",
"https://preprod2.force-n.sn/en/node/85",
"https://preprod2.force-n.sn/en/node/86",
"https://preprod2.force-n.sn/en/node/87",
"https://preprod2.force-n.sn/en/node/93",
"https://preprod2.force-n.sn/en/node/94",
"https://preprod2.force-n.sn/en/node/95",
"https://preprod2.force-n.sn/en/node/96",
"https://preprod2.force-n.sn/en/our-trainings",
"https://preprod2.force-n.sn/en/promoting-science",
"https://preprod2.force-n.sn/en/services/sciences-promotion",
"https://preprod2.force-n.sn/en/services/support-professional-integration",
"https://preprod2.force-n.sn/en/services/trainings",
"https://preprod2.force-n.sn/en/sigui",
"https://preprod2.force-n.sn/en/sigui?page=0",
"https://preprod2.force-n.sn/en/sigui?page=1",
"https://preprod2.force-n.sn/en?page=0",
"https://preprod2.force-n.sn/en?page=1",
"https://preprod2.force-n.sn/faq",
"https://preprod2.force-n.sn/formations",
"https://preprod2.force-n.sn/formations/developpement-logiciel",
"https://preprod2.force-n.sn/formations/e-business",
"https://preprod2.force-n.sn/formations/intelligence-artificielle-et-data",
"https://preprod2.force-n.sn/formations/technologies-emergentes-et-cybersecurite",
"https://preprod2.force-n.sn/les-composantes",
"https://preprod2.force-n.sn/les-partenaires",
"https://preprod2.force-n.sn/mentions-legales",
"https://preprod2.force-n.sn/missions-et-objectifs",
"https://preprod2.force-n.sn/missions-et-objectifs?page=0",
"https://preprod2.force-n.sn/missions-et-objectifs?page=1",
"https://preprod2.force-n.sn/news",
"https://preprod2.force-n.sn/node/1?page=0",
"https://preprod2.force-n.sn/node/1?page=1",
"https://preprod2.force-n.sn/opportunites",
"https://preprod2.force-n.sn/opportunites/vous-etes-entrepreneur",
"https://preprod2.force-n.sn/opportunites/vous-etes-entreprise",
"https://preprod2.force-n.sn/parcours-daccompagnement",
"https://preprod2.force-n.sn/parcours-initiatique",
"https://preprod2.force-n.sn/politique-de-cookies",
"https://preprod2.force-n.sn/promotion-des-sciences",
"https://preprod2.force-n.sn/qui-sommes-nous",
"https://preprod2.force-n.sn/services/accompagnement-linsertion-professionnelle",
"https://preprod2.force-n.sn/services/formations",
"https://preprod2.force-n.sn/services/promotion-des-sciences",
"https://preprod2.force-n.sn/sigui",
"https://preprod2.force-n.sn/sigui?page=0",
"https://preprod2.force-n.sn/sigui?page=1",
]

def get_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        print(f"[Erreur scraping] {url} — {e}")
        return ""

def should_refresh_cache():
    if not os.path.exists(TIMESTAMP_FILE):
        return True
    with open(TIMESTAMP_FILE, 'r') as f:
        try:
            last = int(f.read())
        except:
            return True
    return time.time() - last > EXPIRATION_SECONDS

def get_force_content():
    if os.path.exists(CACHE_FILE) and not should_refresh_cache():
        print("Contenu chargé depuis le cache local .txt")
        with open(CACHE_FILE, "r") as f:
            return f.read()

    print("Scraping en cours...")
    all_texts = [get_text_from_url(url) for url in URLS]
    content = "\n\n".join(all_texts)
    with open(CACHE_FILE, "w") as f:
        f.write(content)
    with open(TIMESTAMP_FILE, "w") as f:
        f.write(str(int(time.time())))
    print("Scraping terminé et sauvegardé.")
    return content

def normalize(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text.lower())
        if unicodedata.category(c) != 'Mn'
    )

def get_relevant_context(message, full_text, max_length=30000):
    keywords = ["fode", "certificat", "formation", "accompagnement", "service", "inscription"]
    msg = normalize(message)
    for kw in keywords:
        if kw in msg:
            paragraphs = full_text.split("\n\n")
            matches = [p for p in paragraphs if kw in normalize(p)]
            if matches:
                print(f"Fallback sur '{kw}'")
                return "\n\n".join(matches)[:max_length]
    return full_text[:max_length]
