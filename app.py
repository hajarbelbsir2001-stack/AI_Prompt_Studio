import streamlit as st
import requests
from reportlab.pdfgen import canvas
from io import BytesIO
from prompt_generator import generate_prompt

if "history" not in st.session_state:
    st.session_state.history = []

if "total_prompts" not in st.session_state:
    st.session_state.total_prompts = 0

st.set_page_config(
    page_title="AI Prompt Studio",
    page_icon="🤖",
    layout="centered"
)

def create_pdf(prompt):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    y = 800

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(40, y, "AI Prompt Studio")
    y -= 35

    pdf.setFont("Helvetica", 11)
    for ligne in prompt.split("\n"):
        pdf.drawString(40, y, ligne)
        y -= 20

        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 11)
            y = 800

    pdf.save()
    buffer.seek(0)
    return buffer

theme = st.sidebar.radio("🎨 Thème", ["Clair", "Sombre"])

if theme == "Clair":
    background = "linear-gradient(135deg, #f8fbff 0%, #eef4ff 45%, #fdfcff 100%)"
    text_color = "#1e293b"
    card_color = "white"
    sidebar_bg = "linear-gradient(180deg, #eff6ff 0%, #dbeafe 100%)"
else:
    background = "linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #111827 100%)"
    text_color = "#f8fafc"
    card_color = "#1e293b"
    sidebar_bg = "linear-gradient(180deg, #020617 0%, #0f172a 100%)"

st.markdown(f"""
<style>
.stApp {{
    background: {background};
}}

.block-container {{
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}}

h1 {{
    text-align: center;
    color: {text_color};
    font-size: 3.3rem !important;
    font-weight: 900;
}}

h2, h3, p, label {{
    color: {text_color} !important;
}}

[data-testid="stSidebar"] {{
    background: {sidebar_bg};
    border-right: 1px solid #bfdbfe;
}}

[data-testid="stForm"] {{
    background: {card_color};
    padding: 34px;
    border-radius: 28px;
    border: 1px solid #e2e8f0;
    box-shadow: 0px 18px 45px rgba(15, 23, 42, 0.12);
}}

.stButton > button {{
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white !important;
    border-radius: 16px;
    padding: 13px 30px;
    font-weight: 800;
    border: none;
}}

.stDownloadButton > button {{
    background: linear-gradient(90deg, #10b981, #0ea5e9);
    color: white !important;
    border-radius: 16px;
    padding: 13px 28px;
    font-weight: 800;
    border: none;
}}

textarea {{
    background-color: #ffffff !important;
    border-radius: 18px !important;
    border: 1px solid #cbd5e1 !important;
    color: #0f172a !important;
}}

.stAlert {{
    border-radius: 18px;
}}
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Prompt Studio")
st.markdown("### Générateur intelligent de prompts avec FastAPI et Streamlit")
st.write("Créez des prompts professionnels selon le domaine, le niveau, la langue et le type de besoin.")

st.sidebar.title("📌 À propos")
st.sidebar.info(
    "AI Prompt Studio est une application qui aide les utilisateurs à créer "
    "des prompts clairs, précis et adaptés à leurs besoins."
)

st.sidebar.markdown("---")
st.sidebar.subheader("📊 Statistiques")
st.sidebar.metric("Prompts générés", st.session_state.total_prompts)
st.sidebar.metric("Historique", len(st.session_state.history))

with st.form("prompt_form"):
    st.subheader("📝 Informations du prompt")

    prompt_type = st.selectbox(
        "Type de prompt",
        [
            "Éducation",
            "Programmation",
            "Marketing",
            "Business",
            "Intelligence Artificielle",
            "Cybersécurité",
            "Résumé",
            "Traduction"
        ]
    )

    domain = st.selectbox(
        "Domaine",
        ["Informatique", "Intelligence Artificielle", "Data Science", "Réseaux", "Cybersécurité"]
    )

    subject = st.text_input("Sujet", "Python")
    objective = st.text_input("Objectif", "Apprendre les bases")

    level = st.selectbox(
        "Niveau",
        ["Débutant", "Intermédiaire", "Avancé"]
    )

    language = st.selectbox(
        "Langue",
        ["Français", "Anglais", "Arabe"]
    )

    tone = st.selectbox(
        "Ton",
        ["Académique", "Professionnel", "Simple", "Technique"]
    )

    submitted = st.form_submit_button("🚀 Générer le prompt")

if submitted:
    enhanced_objective = f"{objective}. Type de prompt demandé : {prompt_type}."

    response = requests.get(
        "http://127.0.0.1:8000/generate",
        params={
            "domain": domain,
            "subject": subject,
            "objective": enhanced_objective,
            "level": level,
            "language": language,
            "tone": tone
        }
    )

    if response.status_code == 200:
        prompt = response.json()["prompt"]

        st.session_state.history.append(prompt)
        st.session_state.total_prompts += 1

        st.success("Prompt généré avec succès ✅")
        st.subheader("📌 Résultat")

        st.text_area("Prompt généré", prompt, height=300)

        st.info("📋 Pour copier le prompt : utilisez le bouton de copie dans le bloc ci-dessous.")
        st.code(prompt, language="text")

        st.download_button(
            label="📄 Télécharger le prompt en TXT",
            data=prompt,
            file_name="prompt_genere.txt",
            mime="text/plain"
        )

        pdf = create_pdf(prompt)

        st.download_button(
            label="📕 Télécharger le prompt en PDF",
            data=pdf,
            file_name="prompt_genere.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Erreur lors de la génération du prompt.")

st.sidebar.markdown("---")
st.sidebar.subheader("📜 Historique des prompts")

if st.sidebar.button("🗑️ Vider l'historique"):
    st.session_state.history = []

if len(st.session_state.history) == 0:
    st.sidebar.write("Aucun prompt généré pour le moment.")
else:
    for i, item in enumerate(st.session_state.history, start=1):
        st.sidebar.text_area(f"Prompt {i}", item, height=120)