# -*- coding: utf-8 -*-
"""Données communes du site Konig Formation (coordonnées, liens, avis, financement)."""

SITE_URL = "https://www.konigformation.com"
NAME = "Konig Formation"
PHONE = "06 18 70 07 47"
PHONE_INTL = "+33618700747"
EMAIL = "contact@konigformation.com"
RDV = "https://dashboard.meninbot.com/rdv/WDGniasDpOPphQg5231Y9v"
GTM_ID = "GTM-KHWRG8FH"

# Formulaires : laisser vide = le formulaire prépare un e-mail vers contact@.
# Pour recevoir les demandes directement, coller ici l'URL d'un service
# de formulaire (Formspree, Basin, Web3Forms…).
FORM_ENDPOINT = ""

LINKS = {
    "qualiopi_pdf": "assets/docs/d14dff_8df2676bdb914abbaa383f1eb28108ae1.pdf",
    "qualiopi_drive": "https://drive.google.com/file/d/1eFTo2mwWQ5cwcjzHyH2Gs2IHD7De3HP5/view?usp=sharing",
    "reclamation": "https://drive.google.com/file/d/1WOkaBjo7eX14-D1mam8hrXYx8KQ2bFs5/view?usp=drive_link",
    "cgv": "assets/docs/CGV-Konig-formation.pdf",
    "cpf_home": "https://www.moncompteformation.gouv.fr/espace-prive/html/#/formation/recherche/90818028400014_Marketing-collectif/90818028400014_Marketing-coll01",
    "france_travail": "https://candidat.francetravail.fr/formations/detail/11232155/true/false",
    "sante": "https://www.konigformation.fr/",
    "francenum": "https://www.francenum.gouv.fr/",
    "instagram": "https://www.instagram.com/konigformation/",
    "facebook": "https://www.facebook.com/p/Konig-formation-100067011892505/",
}

QUALIOPI_TEXT = ("« Certifié conformément aux exigences du Référentiel National de Certification Qualité "
                 "des organismes mentionnés à l’article L.6351-1 du Code du travail. La certification qualité "
                 "a été délivrée au titre de la ou des catégories d’actions suivantes : actions de formation "
                 "(OF – L.6313-1, 1°) »")

CPF_MENTION = ("Cette formation professionnelle de par son caractère certifiant peut être prise en charge par le CPF. "
               "Toute action ne rentrant pas dans le cadre de l’article L6313-1 du code du travail ne rentre pas "
               "dans ce dispositif de prise en charge.")

FINANCEMENT = [
    ("CPF", "Compte Personnel de Formation",
     "Utilisez vos droits acquis pour couvrir tout ou partie des frais. Nos formations sont 100 % éligibles au CPF."),
    ("OPCO", "Opérateurs de Compétences",
     "Salarié ? Votre entreprise peut financer votre formation grâce aux aides des OPCO."),
    ("FAF", "Fonds d’Assurance Formation",
     "Indépendant ? Les FAF prennent en charge vos formations pour développer vos compétences."),
    ("France Travail", "ex-Pôle Emploi",
     "En recherche d’emploi ? Profitez des aides spécifiques comme l’AIF pour accéder à nos programmes."),
]

HANDICAP = ("La formation est aménageable sur demande à un public en situation de handicap. "
            "Pour toute demande : contact@konigformation.com ou 06 18 70 07 47.")

AVIS_NOTE = "Excellent · basé sur 17 avis Google"
AVIS = [
    ("Melvin Beshaies", "Je recommande vivement ce centre de formation ! Les formateurs sont compétents, pédagogues et toujours à l’écoute. Le contenu des formations est riche et bien structuré. Merci à M. Romito et son équipe !"),
    ("Fcf Iso", "Super centre de formation qui vous conseille et vous accompagne même pour les prises en charge. Les dossiers de prise en charge, surtout dans le domaine du bâtiment, sont très compliqués mais ils ont pris le temps de tout nous expliquer. Je suis super satisfait et je repasserai par eux les prochaines fois."),
    ("Max Paul", "Je recommande vivement Konig Formation ! Pédagogie, professionnalisme, expérience, formateurs compétents et à l’écoute : tout est réuni pour acquérir de nouvelles compétences."),
    ("Asghar Changaiz", "Une formation de qualité avec un environnement agréable et des formateurs au top du top ! Je recommande fortement."),
    ("Steeves Chaouat", "Pour ma formation tout s’est très bien passé. Une équipe efficace de A à Z. Très bonne écoute de la part de l’équipe pédagogique. Merci."),
    ("Guillaume Fleury", "Super centre de formation, très à l’écoute de nos besoins et s’adapte à notre situation pro. Je recommande la formation Community Management."),
    ("You Digital", "J’ai eu le plaisir de collaborer avec Konig Formation pour la création de leur site internet. Une superbe collaboration avec une entreprise engagée dans la montée en compétences de ses apprenants ! Je recommande Konig Formation à 100 % pour leur sérieux et la qualité de leur accompagnement."),
    ("Valentine Clmt", "Ils ont su adapter parfaitement mon parcours de formation à ma demande."),
    ("Wilson Rocha", "Formation au top ainsi que les formateurs, très à l’écoute. Je recommande."),
    ("Ritish Beshaies", "Rien à dire, au top !"),
]

CHIFFRES = [
    ("100", "%", "de satisfaction"),
    ("0", "%", "d’abandon"),
    ("25", "ans", "d’expérience dans la formation"),
    ("100", "h+", "de formation"),
]

CATEGORIES = {
    "intelligence-artificielle": "Intelligence Artificielle",
    "pack-office": "Pack Office",
    "marketing-digital": "Marketing Digital",
}
