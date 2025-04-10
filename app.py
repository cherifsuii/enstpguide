from datetime import datetime
import streamlit as st
import os
import google.generativeai as genai
from google.generativeai import types # Keep for GenerationConfig
from google.api_core import exceptions as core_exceptions # For rate limits
from dotenv import load_dotenv
import logging
import time # For potential simulated typing effect

# --- Basic Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Load API Key ---
load_dotenv()
# Try to get API key from .env file first, then from Streamlit secrets
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY and 'GOOGLE_API_KEY' in st.secrets:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# --- Global Check for API Key ---
api_key_configured = bool(GOOGLE_API_KEY)

if not api_key_configured:
    st.error("⚠️ **Erreur de Configuration:** La clé API Google n'est pas définie. L'application ne peut pas fonctionner. Veuillez contacter l'administrateur (Cherif Tas).", icon="🚨")
    # Stop the script here if the key isn't configured at all
    st.stop()
else:
    # Configure GenAI globally once if key exists
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        logger.info("Google Generative AI configured successfully.")
    except Exception as config_err:
        st.error(f"🔑 **Erreur Configuration API:** {config_err}. Vérifiez la validité de la clé.", icon="🔥")
        api_key_configured = False # Mark as not configured if error occurs

# --- Model Configuration ---
MODEL_NAME = 'gemini-1.5-pro-latest' # Use the latest capable model

# --- ENSTP Guide Text ---
ENSTP_GUIDE_TEXT = """
Comprehensive Analysis of DMS and DIB
         Departments at ENSTP Algeria

1     Introduction to ENSTP
The École Nationale Supérieure des Travaux Publics (ENSTP) is one of Alge-
ria's most prestigious engineering institutions, specializing in civil engineering
and public works. Founded in 1966 and located in Kouba, Algiers, ENSTP
has played a critical role in training the engineering workforce responsible for
Algeria's infrastructure development. The institution operates under the super-
vision of the Ministry of Higher Education and Scientific Research, providing
high-quality education in civil engineering disciplines.
    ENSTP is renowned for its rigorous academic programs, combining theoret-
ical knowledge with practical applications, and maintaining strong relationships
with industry partners. The school consistently ranks among Algeria's top en-
gineering institutions, with graduates highly sought after in both public and
private sectors across North Africa and beyond.


2     Departmental Structure at ENSTP
ENSTP's academic structure features several departments, with two major de-
partments serving as the primary pathways for specialization in civil engineering:

2.1    Département des Matériaux et Structures (DMS)
The Department of Materials and Structures focuses on the analysis, design,
and construction of various civil engineering structures, with emphasis on the
behavior of materials under different loading conditions. The department's cur-
riculum is centered around structural engineering principles, material science,
and advanced analysis techniques.
    Primary Specialization: Routes et Ouvrages (Roads and Structures)

2.2    Département des Infrastructures de Base (DIB)
The Department of Basic Infrastructure concentrates on the planning, design,
and management of civil infrastructure systems, with particular attention to
transportation networks, hydraulic systems, and urban development. The de-
partment emphasizes systems integration, infrastructure planning, and network
optimization.
   Primary Specialization: Infrastructures de Base (Basic Infrastructure)


3       Academic Programs and Degrees
3.1     Degree Structure
Both DMS and DIB departments offer identical degree designations, though the
specialization is noted on the diploma:

    • Ingénieur d'état en travaux publics (State Engineer in Public Works)
      - The primary professional degree equivalent to a Bachelor's and Master's
      combined in the Anglo-Saxon system

    • Master en travaux publics (Master's in Public Works) - Advanced de-
      gree for students seeking additional specialization or research preparation

   The engineering program typically spans five years of study, with the first
two years focusing on fundamental sciences and engineering basics, followed by
three years of increasingly specialized coursework in the chosen department.

3.2     Accreditation and Recognition
Degrees from ENSTP are recognized by:
    • The Algerian Ministry of Higher Education and Scientific Research
    • Various international engineering accreditation bodies through mutual
      recognition agreements
    • Major engineering employers across North Africa, the Middle East, and
      Francophone countries


4       Curriculum Analysis: Common Elements
4.1     Fundamental Modules (Common to Both Departments)
Both DMS and DIB share a strong foundation of core engineering subjects that
provide the essential knowledge base for civil engineering practice:

4.1.1    Mathematics and Scientific Foundation
    • Applied Mathematics
    • Probability and Statistics
    • Physics for Engineers
    • Chemistry of Materials

4.1.2   Core Engineering Sciences
   • Résistance Des Matériaux (Strength of Materials): Study of material
     behavior under applied loads, analyzing stress, strain, and deformation to
     ensure structural integrity.
   • Calcul des Structures (Structural Analysis): Mathematical methods for
     analyzing forces, stresses, and displacements in various structural systems.
   • Mécanique des structures (Structural Mechanics): Advanced analysis
     of structural behavior, including dynamic responses and complex loading
     conditions.
   • Dynamique des Structures (Structural Dynamics): Analysis of struc-
     tures under time-varying loads, including seismic considerations.

   • Dynamique des sols (Soil Dynamics): Study of soil behavior under
     dynamic loading conditions.
   • Mécanique Des Sols (Soil Mechanics): Analysis of soil properties, be-
     havior, and their interaction with structures.
   • Mécanique des Milieux Continus (Continuum Mechanics): Mathe-
     matical description of the mechanical behavior of continuous materials.
   • Mécanique Des Fluides (Fluid Mechanics): Study of fluid behavior and
     its interaction with structures and systems.
   • Géologie (Geology): Study of earth materials and processes relevant to
     civil engineering.
   • Topographie (Topography): Techniques for surveying and mapping ter-
     rain for engineering purposes.
   • Mécanique des roches (Rock Mechanics): Analysis of rock behavior
     under various loading and environmental conditions.

4.2     Advanced Common Modules
Both departments feature advanced modules that build upon the fundamental
courses, providing more specialized knowledge applicable to various civil engi-
neering domains:

   • Ponts (Bridges): Design and analysis of bridge structures, including var-
     ious typologies and loading conditions.
   • Routes (Roads): Principles of road design, including geometric design,
     pavement structure, and traffic considerations.
   • Béton Armé (Reinforced Concrete): Design and analysis of reinforced
     concrete structures, including beams, columns, slabs, and foundations.

   • Béton Précontraint (Prestressed Concrete): Advanced concrete tech-
     nology using prestressing techniques to enhance structural performance.
   • Charpente Métallique (Steel Structures): Design and analysis of steel
     structural systems, including connections and load considerations.

   • Géotechnique Routière (Road Geotechnics): Specialized geotechnical
     considerations for road infrastructure.
   • Calcul d'ouvrages (Structural Design): Comprehensive approach to de-
     signing various civil engineering structures.

   • Matériaux de Construction (Construction Materials): Properties, test-
     ing, and applications of various construction materials.
   • Hydraulique appliquée (Applied Hydraulics): Principles of hydraulics
     applied to civil engineering problems.
   • Assainissement urbain et routier (Urban and Road Drainage): Design
     of drainage systems for urban areas and transportation infrastructure.
   • Procédés Généraux de Construction (General Construction Processes):
     Construction methods, techniques, and equipment for various civil engi-
     neering projects.

   • Organisation De Chantier (Construction Site Organization): Plan-
     ning, management, and optimization of construction sites.
   • Méthode des éléments finis (Finite Element Method): Numerical tech-
     nique for solving complex engineering problems through discretization.
   • Pathologie des Ouvrages d'Art (Engineering Structures Pathology):
     Analysis of structural defects, failures, and rehabilitation techniques.

4.3   Common Transversal Modules
Both departments include courses that develop broader professional skills nec-
essary for engineering practice:

   • Conférences (Conferences): Exposure to current industry trends and
     research through guest lectures and seminars.
   • Dessin Assisté par Ordinateur (Computer-Aided Design): Applica-
     tion of software tools for engineering design and drafting.
    • Anglais Technique (Technical English): Development of English lan-
      guage skills specific to engineering contexts.
   • Analyse numérique appliquée (Applied Numerical Analysis): Compu-
      tational methods for solving engineering problems.

    • Droit des Travaux Publics (Public Works Law): Legal aspects of civil
      engineering projects, contracts, and regulations.
    • Développement durable et aménagement de territoire (Sustain-
      able Development and Territorial Planning): Integration of sustainability
      principles in infrastructure development.
    • Management des projets ou Entrepreneuriat (Project Management
      or Entrepreneurship): Skills for managing engineering projects or creating
      engineering enterprises.

4.4    Common Practical Work and Laboratories
Both departments emphasize hands-on experience through extensive laboratory
work:

    • TP RDM (Strength of Materials Lab): Experimental verification of ma-
      terial behavior under various loading conditions.
    • TP MDS (Soil Mechanics Lab): Testing and analysis of soil properties
      relevant to civil engineering applications.
    • TP Topo (Topography Lab): Field exercises in surveying and terrain
      mapping.
    • TP Géologie (Geology Lab): Identification and testing of geological ma-
      terials relevant to construction.
    • TP MDC (Construction Materials Lab): Testing and characterization of
      various construction materials.
    • TP MDF (Fluid Mechanics Lab): Experimental study of fluid behavior
      in various engineering applications.

    • TP Routes (Roads Lab): Testing of road materials and design principles
      for pavement systems.

5     Curriculum Differences: DMS vs. DIB
5.1    DMS-Specific Engineering Modules
The DMS department offers specialized courses focusing on materials behavior
and structural analysis:
   • Calcul Automatique des structures (Automated Structural Analysis):
     Application of computational methods for complex structural analysis.
   • Calcul économique des projets (Economic Project Calculation): Cost
     analysis and optimization of structural engineering projects.

   • Dynamique des Sols 2 (Advanced Soil Dynamics): Further exploration
     of soil behavior under dynamic loading conditions.
   • TP Hydraulique appliquée (Applied Hydraulics Lab): Practical appli-
     cations of hydraulic principles in structural contexts.

5.2     DIB-Specific Engineering Modules
The DIB department offers specialized courses focusing on infrastructure sys-
tems and transportation:

   • Économie de Transport (Transport Economics): Economic analysis of
     transportation systems and infrastructure investments.

   • Analyse Numérique (Numerical Analysis): Advanced computational
     methods specifically applied to infrastructure problems.
   • Géologie 2 (Advanced Geology): Further exploration of geological con-
     siderations for infrastructure development.

   • TP GTR (Road Geotechnics Lab): Practical applications of geotechnical
     principles to road infrastructure.
   • TP Géologie2 (Advanced Geology Lab): Advanced testing and analysis
     of geological materials for infrastructure applications.

5.3     Optional Specialization Tracks
5.3.1   DMS Optional Tracks
Buildings Track (Bâtiments):

   • Bâtiments (Buildings): Comprehensive structural design of buildings
     considering various loading conditions.
   • Contreventments (Bracing): Design of structural systems to resist lat-
     eral loads in buildings.
   • Calcul d'ouvrages élémentaires (Elementary Structural Calculation):
     Simplified methods for structural analysis of common building elements.
   • Thermique Bât (Building Thermics): Thermal behavior and energy ef-
     ficiency in building design.
   • Esquisse Bât (Building Design): Conceptual and preliminary design of
     building structures.
   Tunnels Track:

   • Mécanique des Roches (Rock Mechanics): Behavior of rock masses
     relevant to underground construction.
   • Tun (Tunnels): Principles of tunnel design, construction, and mainte-
     nance.

   • Méthode de réalisation des Ouvrages Souterrains (Underground
     Construction Methods): Techniques for constructing various underground
     structures.
   • Esquisse Tun (Tunnel Design): Conceptual and preliminary design of
     tunnel structures.

5.3.2   DIB Optional Tracks
Railway and Rail Bridges Track:
   • VF1, VF2 (Railway 1 & 2): Comprehensive study of railway infrastruc-
     ture design and maintenance.
   • Esquisse VF (Railway Design): Conceptual and preliminary design of
     railway systems.

   • PR1, PR2 (Rail Bridge 1 & 2): Specialized design of bridge structures
     for railway applications.
   • Esquisse PR (Rail Bridge Design): Conceptual and preliminary design
     of railway bridges.

   Maritime Works and Air Bases Track:
   • TM1, TM2 (Maritime Works 1 & 2): Design and construction of coastal
     and port structures.
   • Esquisse TM (Maritime Design): Conceptual and preliminary design of
     maritime infrastructure.
   • Base1, Base2 (Air Base 1 & 2): Specialized infrastructure for aviation
     facilities.
   • Esquisse Base (Air Base Design): Conceptual and preliminary design of
     airport infrastructure.

5.4     Master's Program Specialization Differences
5.4.1    DMS Master's Modules (Research-Oriented)
The DMS master's program emphasizes advanced materials science and struc-
tural optimization:

    • Matériaux innovants (Innovative Materials): Study of emerging con-
      struction materials with enhanced properties.
    • Analyse expérimentale (Experimental Analysis): Advanced laboratory
      techniques for materials and structural testing.
    • Optimisation des Structures (Structural Optimization): Mathemati-
      cal methods for optimizing structural designs.
    • Mécanique des milieux continus approfondie (Advanced Continuum
      Mechanics): Higher-level analysis of material behavior using continuum
      mechanics principles.

5.4.2    DIB Master's Modules (Practice-Oriented)
The DIB master's program focuses on infrastructure performance and manage-
ment:

    • Pathologie des chaussées (Pavement Pathology): Analysis of pavement
      deterioration mechanisms and rehabilitation techniques.
    • Rhéologie des matériaux (Materials Rheology): Study of flow behavior
      of construction materials under various conditions.
    • Organisation de chantier (Construction Site Organization): Advanced
      techniques for managing complex infrastructure projects (shared with
      DMS).
    • Droit des Travaux Publics (Public Works Law): Advanced legal con-
      siderations for infrastructure development (shared with DMS).

6       Practical Training and Field Experience
6.1     Internship Requirements
Both departments require students to complete multiple internships throughout
their studies:

    • Observation Internship (1st year): Introduction to civil engineering
      practice in real-world settings.
    • Worker Internship (2nd year): Hands-on experience as part of con-
      struction teams.
   • Technical Internship (3rd year): Application of technical knowledge in
     professional settings.
   • Engineering Internship (4th year): Advanced professional experience
     with significant responsibilities.
   • Graduation Project Internship (5th year): Comprehensive project
     serving as the capstone experience.

6.2     Field Trips and Educational Visits
6.2.1   DMS Educational Visits
Students in DMS typically visit:
   • Bridge construction sites of various typologies
   • Road construction and rehabilitation projects
   • Materials testing laboratories
   • Tunnel construction sites
   • Dam construction and monitoring installations
   • Building construction sites for high-rise or complex structures

6.2.2   DIB Educational Visits
Students in DIB typically visit:
   • Bridge construction sites with emphasis on integration with transportation
     networks
   • Road network development projects
   • Materials testing laboratories with focus on infrastructure applications
   • Railway construction and maintenance operations
   • Port facilities and maritime infrastructure
   • Dam construction with emphasis on hydraulic systems

6.3     Final Year Project Differences
6.3.1   DMS Final Projects
Typically focus on:
   • Structural design optimization
   • Advanced materials applications
    • Seismic analysis and design
   • Structural rehabilitation techniques
   • Special structures (tall buildings, long-span bridges, etc.)

6.3.2    DIB Final Projects
Typically focus on:
    • Transportation network optimization
    • Infrastructure system integration
    • Railway design and planning
    • Port and maritime facilities development
    • Airport infrastructure design


7       Research Activities and Facilities
7.1     Research Laboratories
ENSTP hosts several research laboratories supporting both departments, with
different emphasis:

7.1.1    DMS-Affiliated Research Facilities
    • Laboratory of Materials Engineering: Focuses on construction ma-
      terials development and testing.
    • Structural Analysis Laboratory: Equipped for experimental testing
      of structural elements.
    • Earthquake Engineering Laboratory: Specializes in seismic perfor-
      mance of structures.
    • Computational Mechanics Laboratory: Focuses on numerical mod-
      eling of structures and materials.

7.1.2    DIB-Affiliated Research Facilities
    • Transportation Engineering Laboratory: Focuses on transportation
      system analysis and planning.
    • Geotechnical Engineering Laboratory: Specializes in soil-structure
      interaction for infrastructure.
    • Hydraulic Engineering Laboratory: Focuses on water resource sys-
      tems and infrastructure.
    • Infrastructure Planning Laboratory: Emphasizes integrated infras-
      tructure development.

7.2     Research Orientation
The research orientation differs significantly between the two departments:

    • DMS Research Focus: Materials science, structural behavior, seismic
      design, structural optimization, and building science.
    • DIB Research Focus: Transportation systems, infrastructure planning,
      geotechnical engineering for infrastructure, and sustainable development.

8       Faculty Profiles and Expertise
8.1     Faculty Composition
Both departments feature faculty members with various specializations:

8.1.1    DMS Faculty Expertise
    • Structural Engineering
    • Earthquake Engineering
    • Materials Science
    • Computational Mechanics
    • Geotechnical Engineering for Structures
    • Building Science

8.1.2    DIB Faculty Expertise
    • Transportation Engineering
    • Railway Engineering
    • Maritime Engineering
    • Airport Infrastructure
    • Infrastructure Planning
    • Geotechnical Engineering for Infrastructure

8.2     Teaching Quality
According to student feedback and institutional evaluations:

    • Both departments have highly qualified professors, many with interna-
      tional experience.
    • Some professors are known for rigorous evaluation standards.
    • Teaching effectiveness varies among faculty members.
    • Industry experience among faculty tends to be higher in DIB, while re-
      search credentials are often stronger in DMS.


9       Career Prospects and Professional Outcomes
9.1     Employment Sectors
Graduates from both departments find employment in various sectors, with
some differences in distribution:

9.1.1    Common Employment Sectors
    • Public works agencies
    • Construction companies
    • Consulting engineering firms
    • Government ministries (Infrastructure, Housing, Transportation)
    • Municipal engineering departments
    • International development organizations

9.1.2    DMS Graduate Predominant Sectors
    • Structural engineering consultancies
    • Building design firms
    • Construction companies specializing in complex structures
    • Research institutions
    • Earthquake engineering specialists
    • Building inspection and rehabilitation companies

9.1.3   DIB Graduate Predominant Sectors
   • Transportation planning agencies
   • Railway companies
   • Port authorities
   • Airport development agencies
   • Infrastructure management organizations
   • Urban planning departments

9.2     Professional Advancement
Career progression patterns show some differences between graduates of the two
departments:

   • DMS Graduates: Often advance toward specialized technical roles (Se-
     nior Structural Engineer, Technical Director) or management positions in
     structural engineering firms.
   • DIB Graduates: Often advance toward project management roles, sys-
     tem planning positions, or infrastructure development management.

9.3     Entrepreneurship Opportunities
Both pathways offer entrepreneurial possibilities with different orientations:

   • DMS Entrepreneurship: Specialized structural engineering consultan-
     cies, materials testing laboratories, structural inspection services.
   • DIB Entrepreneurship: Infrastructure planning consultancies, trans-
     portation system analysis firms, project management services.


10      Student Experience and Campus Life
10.1     Student Demographics
The student body composition shows some patterns:

   • DMS typically attracts students with stronger mathematical backgrounds
     and interest in detailed analysis.
   • DIB typically attracts students with broader interests in systems and plan-
     ning.
   • Gender distribution is similar in both departments, though traditionally
     DMS has had a slightly higher percentage of male students.

10.2    Student Organizations
Several student organizations are relevant to both departments:

   • ENSTP Civil Engineering Society: General civil engineering student
     organization
   • Structural Engineering Club: Primarily attracts DMS students
   • Infrastructure Development Association: Primarily attracts DIB
     students
   • ENSTP Research Group: Active in both departments but with stronger
     DMS participation

10.3    Academic Workload
The academic demands show some differences:

   • DMS Workload: Higher mathematical intensity, more detailed calcula-
     tions, greater emphasis on analysis.
   • DIB Workload: More diverse subject matter, greater emphasis on inte-
     gration, more project-based assessments.

11     International Collaboration and Mobility
11.1    International Partnerships
ENSTP maintains partnerships with international institutions relevant to both
departments:

   • Partnerships with French engineering schools (École des Ponts ParisTech,
     INSA)
   • Collaboration with Middle Eastern and African universities
   • Exchange programs with European technical universities

11.2    Student Mobility
Opportunities for international experience exist for both departments:

   • Exchange semester opportunities primarily in Francophone countries
   • International internship placements
   • Double-degree possibilities with partner institutions

11.3     Research Collaboration
International research collaboration patterns differ:
   • DMS Research Collaboration: Stronger ties with materials science
     and structural engineering research centers internationally.
   • DIB Research Collaboration: Stronger ties with transportation and
     infrastructure planning organizations internationally.


12       Comparative Analysis: Making the Choice
12.1     Student Aptitude Considerations
Different aptitudes may be better suited to each department:

12.1.1    DMS-Favored Aptitudes
   • Strong mathematical abilities
   • Detail-oriented thinking
   • Interest in physical principles and behavior
   • Comfort with complex analysis
   • Precision and accuracy in work

12.1.2    DIB-Favored Aptitudes
   • Systems thinking abilities
   • Integration of multiple disciplines
   • Interest in transportation and networks
   • Comfort with planning and optimization
   • Spatial reasoning skills

12.2     Learning Style Considerations
Learning preferences that may influence department choice:

12.2.1    DMS-Favored Learning Styles
   • Analytical learning approach
   • Step-by-step problem solving
   • Detailed examination of components
   • Theoretical foundation emphasis

12.2.2    DIB-Favored Learning Styles
   • Holistic learning approach
   • Systems-level problem solving
   • Integration of diverse elements
   • Practical application emphasis

12.3     Career Interest Alignment
Career interests that may guide department selection:

12.3.1    DMS-Aligned Career Interests
   • Designing complex structures
   • Analyzing structural behavior
   • Developing advanced materials
   • Earthquake-resistant design
   • Building science research

12.3.2    DIB-Aligned Career Interests
   • Transportation system planning
   • Infrastructure development
   • Railway or maritime engineering
   • Airport infrastructure design
   • Urban system integration


13       Future Trends and Departmental Evolution
13.1     Emerging Technologies
Both departments are adapting to technological advances, with different em-
phases:

13.1.1    DMS Technology Evolution
   • Advanced computational methods for structural analysis
   • Building Information Modeling (BIM) integration
   • Smart materials and structures
   • Sustainable building technologies
   • 3D printing for construction

13.1.2    DIB Technology Evolution
   • Intelligent transportation systems
   • Infrastructure management systems
   • Geographic Information Systems (GIS) applications
   • Remote sensing for infrastructure monitoring
   • Smart city technologies

13.2     Curriculum Evolution
Both departments continue to evolve their curricula:

   • DMS Curriculum Trends: Greater integration of sustainability, re-
     silience, and digital technologies in structural design.
   • DIB Curriculum Trends: Increased emphasis on smart infrastructure,
     sustainable transportation, and integrated planning approaches.


14       Conclusion: The Complementary Nature of
         DMS and DIB
The Département des Matériaux et Structures (DMS) and Département des
Infrastructures de Base (DIB) at ENSTP represent complementary approaches
to civil engineering education:

   • DMS provides depth in structural engineering, materials science, and
     detailed analysis, preparing engineers who can design and analyze complex
     structures with precision and technical sophistication.
   • DIB offers breadth in infrastructure systems, transportation engineering,
     and integrated planning, developing engineers who can coordinate complex
     infrastructure networks and optimize transportation systems.
    Both departments contribute essential expertise to Algeria's infrastructure
development, with graduates working together on major projects - DMS grad-
uates ensuring structural integrity and safety, while DIB graduates ensuring
system functionality and integration.
    The choice between these departments should be guided by a student's natu-
ral aptitudes, learning preferences, and career aspirations, recognizing that both
pathways lead to rewarding engineering careers addressing critical infrastructure
needs.


15     References and Resources
15.1    Official ENSTP Documentation
   • ENSTP Academic Catalog
   • Departmental Curriculum Guides
   • ENSTP Strategic Plan 2020-2025

15.2    Alumni Outcomes Reports
   • Graduate Employment Surveys (2018-2024)
   • Career Progression Analysis of ENSTP Graduates

15.3    Industry Feedback
   • Employer Satisfaction Surveys
   • Industry Advisory Board Recommendations

15.4    Comparative Studies
   • Civil Engineering Education in North Africa (2022)
   • Infrastructure Skills Development in Algeria (2023)
"""

# --- Function to Interact with Gemini API (Adapted for Streamlit) ---
def get_enstp_response(student_input, conversation_history):
    """Gets sophisticated response/recommendation based on student input and history."""
    if not GOOGLE_API_KEY:
        logger.error("API Key not found.")
        return "Erreur: La clé API GOOGLE_API_KEY n'est pas configurée correctement sur le serveur."

    try:
        # Configure API client if needed
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel(MODEL_NAME)
    except Exception as e:
        logger.error(f"Error initializing GenerativeModel: {e}")
        return f"Erreur: Impossible d'initialiser le modèle d'IA. Détails: {str(e)}"

    try:
        # Format conversation history for embedding within prompt
        conversation_history_formatted = "\n".join(
            f"{'Étudiant' if turn['role'] == 'user' else 'Conseiller ENSTP'}: {turn['content']}"
            for turn in conversation_history
        ).strip()

        # Define guide text directly within function
        guide_text = """Résumé simplifié pour les départements DMS et DIB à l'ENSTP:

DMS (Département des Matériaux et Structures):
- Spécialisation: Analyse et conception des structures d'ingénierie civile
- Focus: Comportement des matériaux, principes d'ingénierie structurelle
- Cours spécifiques: Analyse structurelle avancée, dynamique des structures, optimisation
- Aptitudes favorisées: Compétences mathématiques, pensée analytique, analyse détaillée
- Débouchés: Bureaux d'études structurelles, entreprises de construction spécialisées

DIB (Département des Infrastructures de Base):
- Spécialisation: Planification et gestion des systèmes d'infrastructure civile
- Focus: Réseaux de transport, systèmes hydrauliques, développement urbain
- Cours spécifiques: Économie des transports, géologie avancée, planification d'infrastructure
- Aptitudes favorisées: Pensée systémique, intégration multidisciplinaire, optimisation
- Débouchés: Agences de planification des transports, autorités portuaires, gestion d'infrastructure

Les deux départements partagent une base commune de cours fondamentaux en génie civil.

Information sur les domaines connexes:
- Génie Civil: Se concentre sur la conception, la construction et la maintenance de l'environnement bâti, y compris les bâtiments, les ponts, les barrages, etc.
- Travaux Publics: Met l'accent sur les infrastructures publiques comme les routes, les ponts, les tunnels, les systèmes d'approvisionnement en eau, et l'assainissement.
- Architecture: Se concentre sur la conception esthétique et fonctionnelle des bâtiments et autres structures physiques.
- Génie Urbain: Traite de la planification, de la conception et de la gestion des zones urbaines et des services municipaux."""

        # --- PROMPT ---
        combined_prompt_for_llm = f"""
        **PERSONA & MISSION:**
        Vous êtes un conseiller d'orientation expert, amical et perspicace de l'ENSTP. Votre mission est d'avoir une conversation naturelle et guidée avec un étudiant venant de terminer le cycle préparatoire pour l'aider à choisir entre les départements DMS et DIB. Votre source principale d'information est le "Guide ENSTP DMS/DIB".

        **CONTRAINTES:**
        1.  **SOURCE PRINCIPALE:** Basez principalement vos réponses, analyses et recommandations sur le "Guide ENSTP DMS/DIB" fourni ci-dessous.
        2.  **CONNAISSANCES GÉNÉRALES:** Vous pouvez utiliser des connaissances générales sur le génie civil, les travaux publics et d'autres domaines connexes pour contextualiser vos réponses, mais restez centré sur l'ENSTP.
        3.  **ATTRIBUTION:** Si on vous demande qui vous a créé ou inventé, répondez UNIQUEMENT "Cherif tas".
        4.  **LANGUE:** Répondez en FRANÇAIS par défaut. Si l'étudiant demande explicitement une réponse en anglais ou en arabe (ex: "speak in english", "parle en arabe"), répondez à CETTE demande spécifique dans la langue demandée et **continuez dans cette langue pour les tours suivants**, jusqu'à ce que l'étudiant demande explicitement une autre langue ou de revenir au français.

        **FLUX DE CONVERSATION GUIDÉE:**
        1.  **OUVERTURE (Premier Tour):** (Déjà géré par le message initial dans Streamlit)
        2.  **COLLECTE D'INFORMATIONS (Tours Suivants):** Avant de donner des réponses spécifiques ou des recommandations, POSEZ DES QUESTIONS OUVERTES pour comprendre l'étudiant. Exemples de questions à poser progressivement (ne les posez pas toutes d'un coup):
            *   "Comment se sont passées vos années préparatoires ? Quelles matières scientifiques (maths, physique) avez-vous le plus appréciées ?"
            *   "Qu'est-ce qui vous attire dans le métier d'ingénieur en travaux publics ?"
            *   "Préférez-vous l'analyse détaillée et la compréhension profonde des mécanismes (style DMS) ou une vision plus globale des systèmes et de leur intégration (style DIB) ?"
            *   "Avez-vous déjà une idée des types de projets qui vous intéressent le plus (bâtiments, ponts, routes, tunnels, chemins de fer, ports, aéroports) ?"
            *   "Comment envisagez-vous votre future carrière ? Plutôt dans la technique pure, la gestion de projet, la planification ?"
            *   Accusez réception des réponses de l'étudiant (ex: "D'accord, je vois que vous préférez X...") avant de poser une autre question ou de fournir une information.
        3.  **RÉPONSE AUX QUESTIONS SPÉCIFIQUES:** Quand l'étudiant pose une question directe (sur les modules, carrières, etc.), répondez PRÉCISÉMENT en utilisant PRINCIPALEMENT le guide. **Intégrez l'information naturellement sans citer systématiquement les numéros de section.** Référez-vous au contenu du guide, mais pas à sa structure.
        4.  **RÉPONSE AUX QUESTIONS SUR LES DOMAINES CONNEXES:** Si l'étudiant pose des questions sur les différences entre le génie civil, les travaux publics, l'architecture ou d'autres domaines connexes, fournissez des réponses informatives et précises en vous appuyant sur vos connaissances générales, tout en les reliant à l'ENSTP.
        5.  **RECOMMANDATION (sur demande ou quand prêt):**
            *   Ne recommandez PAS trop tôt. Attendez une demande explicite ('recommander', 'quel choisir', 'votre avis') OU lorsque vous estimez avoir recueilli suffisamment d'informations pertinentes.
            *   Basez la recommandation sur une CORRESPONDANCE CLAIRE entre les informations recueillies sur l'étudiant (historique) et les critères pertinents du guide (par exemple, les aptitudes favorisées, les intérêts alignés, les perspectives de carrière).
            *   Justifiez la recommandation en vous référant **clairement aux informations pertinentes du guide**, **mais évitez les citations directes de numéros de section.** (ex: "Étant donné votre intérêt pour l'analyse détaillée et votre attrait pour la conception de structures complexes, le DMS semble mieux aligné, car le guide indique que ce département favorise ces aspects.").
            *   Si les informations sont insuffisantes pour recommander, demandez les détails manquants nécessaires pour appliquer les critères du guide.
        6.  **STYLE DE RÉPONSE:** Soyez fluide, intelligent, conversationnel mais professionnel. Équilibrez la longueur des réponses. Utilisez des phrases de transition.

        **Guide ENSTP DMS/DIB (Source Principale):**
        --- DEBUT GUIDE ---
        {guide_text}
        --- FIN GUIDE ---

        **Historique de la Conversation Précédente:**
        --- DEBUT HISTORIQUE ---
        {conversation_history_formatted if conversation_history else "Aucune conversation précédente."}
        --- FIN HISTORIQUE ---

        **Dernière Entrée de l'Étudiant:**
        {student_input}

        **Votre Prochaine Action:**
        Générez la prochaine réponse ou question du "Conseiller ENSTP" en suivant scrupuleusement le flux de conversation guidée et toutes les instructions et contraintes ci-dessus.
        """

        # Simplify API call approach
        messages = []
        # First add system prompt
        messages.append({"role": "user", "parts": [combined_prompt_for_llm]})
        
        response = model.generate_content(
            messages,
            generation_config=types.GenerationConfig(
                temperature=0.6,
                max_output_tokens=1536,
            ),
        )

        if not response.candidates:
            logger.warning("API response blocked or empty.")
            return "Désolé, ma réponse a été bloquée pour des raisons de sécurité ou était vide."

        response_text = response.text.strip()
        return response_text
    
    except core_exceptions.ResourceExhausted as rate_limit_err:
        logger.warning(f"API Rate Limit Reached: {rate_limit_err}")
        return "Le service est très sollicité actuellement. Veuillez patienter quelques instants avant de réessayer."
    except Exception as e:
        logger.error(f"Error processing API request: {e}")
        return f"Désolé, une erreur s'est produite: {str(e)}"

# --- Page Config (MUST be the first Streamlit command) ---
st.set_page_config(
    page_title="Conseiller ENSTP",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("🧑‍🏫 Conseiller ENSTP - Votre Guide Intelligent")
st.warning("⚠️ L'API ne peut pas supporter un grand nombre de requêtes. Si vous recevez une erreur de limite d'API, veuillez patienter quelques instants avant de réessayer.", icon="⚠️")

# Add clear button
if st.button("🗑️ Effacer la Conversation", key="clear_button"):
    # Reset chat history
    st.session_state.messages = []
    logger.info("Conversation cleared by user.")
    # Add the initial welcome message back after clearing
    st.session_state.messages.append(
        {"role": "assistant", "content": "Bonjour ! Félicitations pour avoir terminé le cycle préparatoire. Comment vous sentez-vous à l'approche de ce choix important entre DMS et DIB ?"}
    )
    st.rerun() # Rerun to update the UI immediately

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        # Start with the initial welcome message from the assistant
        {"role": "assistant", "content": "Bonjour ! Félicitations pour avoir terminé le cycle préparatoire. Comment vous sentez-vous à l'approche de ce choix important entre DMS et DIB ?"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]): # "user" or "assistant"
        if "content" in message:
            st.markdown(message["content"])
        elif "parts" in message and message["parts"]:
            st.markdown(message["parts"][0])
        else:
            st.markdown("Message error: No content found")

# Chat input
if prompt := st.chat_input("Discutez avec le conseiller..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Prepare conversation history for API call
    history_for_api = []
    for msg in st.session_state.messages[:-1]:  # All messages except the latest user message
        # Handle different message formats
        if "content" in msg:
            content = msg["content"]
        elif "parts" in msg and msg["parts"]:
            content = msg["parts"][0]
        else:
            content = "Error: No content found in message"
            
        history_for_api.append({
            "role": msg["role"],
            "content": content
        })
    
    # Get response from Gemini API
    with st.spinner("En train de réfléchir..."):
        try:
            response_text = get_enstp_response(prompt, history_for_api)
        except Exception as e:
            st.error(f"Erreur: {str(e)}")
            response_text = "Désolé, j'ai rencontré une erreur. Veuillez réessayer."
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response_text)
    
    # Add response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})

# Add a small footer
st.markdown("---")

# About section
with st.expander("À propos du Conseiller IA"):
    st.markdown("""
    ### Votre guide personnel pour l'orientation à l'ENSTP
    
    Bienvenue dans votre conseiller d'orientation intelligent ! 
    
    J'ai été créé par **Cherif Tas** pour transformer la façon dont les étudiants explorent leurs options à l'ENSTP. Au lieu de parcourir des brochures ou d'attendre un rendez-vous d'orientation, vous pouvez simplement discuter avec moi comme avec un ami bien informé.
    
    ✨ **Ce que je peux faire pour vous:**
    - Répondre à vos questions sur votre parcours académique
    - Vous aider à découvrir quelle spécialisation correspond le mieux à votre profil
    - Clarifier vos doutes sur les débouchés professionnels
    - Vous aider à prendre une décision éclairée basée sur vos forces et aspirations
    
    🧠 **Mes talents cachés:**
    Je suis alimenté par Google Gemini AI et entraîné sur des données spécifiques à l'ENSTP. Je peux analyser votre profil et vos préférences pour vous proposer une orientation personnalisée.
    
    👇 **Pour commencer:**
    Partagez simplement vos intérêts, vos forces académiques ou vos questions sur votre futur parcours. Plus vous partagez, plus je peux vous aider efficacement !
    """)

st.markdown("**Créé par:** Cherif Tas")
st.caption("Propulsé par Google Gemini") 
