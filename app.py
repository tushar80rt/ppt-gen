import streamlit as st
from pptAgent import run_ppt_task

# Page configuration with dark theme
st.set_page_config(
    page_title="AI PowerPoint Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark Theme with white title
st.markdown("""
    <style>
        :root {
            --primary-color: #9fef00;
            --bg-color: #0a0a0a;
            --text-color: #ffffff;
            --secondary-text: #b3b3b3;
            --card-bg: #1a1a1a;
            --title-color: #ffffff; /* Added white title color */
        }
        
        body {
            background-color: var(--bg-color);
            color: var(--text-color);
        }
        
        .main {
            padding: 2rem;
            background-color: var(--bg-color);
        }
        
        .header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .title {
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--title-color) !important; /* Changed to white */
        }
        
        .subtitle {
            font-size: 1rem;
            color: var(--secondary-text);
            margin-bottom: 2rem;
        }
        
        .stTextArea textarea {
            min-height: 150px !important;
            background-color: var(--card-bg) !important;
            color: var(--text-color) !important;
            border: 1px solid #333 !important;
        }
        
        .generate-btn {
            width: 100%;
            padding: 0.5rem;
            font-weight: 500;
        }
        
        .success-box {
            background-color: #1e3a1e;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            border-left: 4px solid var(--primary-color);
        }
        
        .download-btn {
            width: 100%;
            padding: 0.5rem;
            background-color: var(--primary-color) !important;
            color: #000 !important;
            font-weight: bold !important;
        }
        
        .sidebar .sidebar-content {
            background-color: #111 !important;
        }
        
        [data-testid="stSidebar"] {
            background-color: #111 !important;
            border-right: 1px solid #333;
        }
        
        .stSlider .thumb {
            background-color: var(--primary-color) !important;
        }
        
        .stSlider .track {
            background-color: #333 !important;
        }
        
        .stSelectbox, .stSlider {
            color: var(--text-color) !important;
        }
        
        .st-bb, .st-at, .st-ae, .st-af, .st-ag, .st-ah, .st-ai, .st-aj, .st-ak, .st-al {
            background-color: var(--card-bg) !important;
        }
        
        .stButton>button {
            border: 1px solid var(--primary-color) !important;
        }
        
        .stButton>button:hover {
            opacity: 0.8;
        }
    </style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("## ⚙️ Presentation Settings")
    
  
    slide_count = st.slider(
        "Number of slides",
        min_value=3,
        max_value=20,
        value=10,
        help="Select how many slides you want in your presentation"
    )
    
   
    presentation_style = st.selectbox(
        "Presentation Style",
        options=["Professional", "Creative", "Academic", "Minimalist", "Business"],
        index=0,
        help="Select the style of your presentation"
    )
    
 
    color_theme = st.selectbox(
        "Color Theme",
        options=["Dark", "Matrix", "Midnight", "Cyberpunk", "Obsidian"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("This tool uses AI to generate PowerPoint presentations instantly. Just describe what you need!")
    st.markdown("Powered by CAMEL-AI + PPTXToolkit")

# Main content area (Dark Theme with white title)
st.markdown("""
    <div class="header">
        <div class="title" style="color: #ffffff !important;">💡Smart Presentation Maker</div>
        <div class="subtitle">Create professional presentations in seconds</div>
    </div>
""", unsafe_allow_html=True)

# Main input section
with st.container():
    task = st.text_area(
        "**Presentation Request**",
        placeholder=f"Example: 'Create a {slide_count}-slide {presentation_style.lower()} presentation about renewable energy trends with statistics and diagrams'",
        height=180,
        help="Be as specific as possible for best results"
    )

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        generate_btn = st.button(
            "🚀 Generate Presentation",
            key="generate",
            use_container_width=True,
            type="primary"
        )
    with col2:
        example_btn = st.button(
            "💡 Show Examples",
            use_container_width=True
        )

if example_btn:
    st.info("""
    **Example Prompts:**
    - "Create a 12-slide business presentation about digital marketing trends in 2024 with charts"
    - "Make a 5-slide academic presentation about quantum computing basics with diagrams"
    - "Generate a 8-slide creative pitch deck for a startup idea about sustainable fashion"
    """)


if generate_btn:
    if not task.strip():
        st.warning("Please enter a valid presentation request")
    else:
       
        enhanced_task = f"{task}. Make it {slide_count} slides in {presentation_style.lower()} style with {color_theme.lower()} color theme."
        
        with st.spinner(f"🔮 Generating your {slide_count}-slide {presentation_style.lower()} presentation... This may take a moment."):
            path = run_ppt_task(enhanced_task)
        
        if path:
            st.markdown('<div class="success-box"> Your presentation has been successfully generated!</div>', unsafe_allow_html=True)
            
            with open(path, "rb") as f:
                st.download_button(
                    "📥 Download PowerPoint File",
                    f,
                    f"presentation_{presentation_style.lower()}.pptx",
                    key="download",
                    help="Click to download your generated PowerPoint file",
                    use_container_width=True
                )
            
            st.markdown("""
                <div style="text-align: center; margin-top: 1rem; color: var(--secondary-text);">
                    Need changes? Modify your request above and generate again.
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error("Failed to generate presentation. Please check your request and try again.")







































































































































