"""
Professional Architecture Diagram Generator
Using Agno Agentic SDK and Google Gemini
"""
import os
import sys
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from architecture_agent import create_architecture_agent, DiagramRequest
from diagram_generator import DiagramGenerator
from templates import get_template_names, get_template

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Architecture Diagram Generator",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #FF4B4B 0%, #FF8E53 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #888;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #FF4B4B 0%, #FF8E53 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: bold;
        border-radius: 8px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.4);
    }
    .diagram-container {
        border: 2px solid #333;
        border-radius: 12px;
        padding: 1rem;
        background-color: #1a1a1a;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #1a4d2e;
        border-left: 4px solid #4caf50;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 8px;
        background-color: #1a2a4d;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if "generated_diagram" not in st.session_state:
        st.session_state.generated_diagram = None
    if "diagram_response" not in st.session_state:
        st.session_state.diagram_response = None
    if "api_key_verified" not in st.session_state:
        st.session_state.api_key_verified = False


def verify_api_key(api_key: str) -> bool:
    """Verify that the API key is set"""
    return bool(api_key and api_key.strip() and api_key != "your_google_api_key_here")


def main():
    """Main application"""
    initialize_session_state()

    # Header
    st.markdown('<h1 class="main-header">🏗️ Architecture Diagram Generator</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Create professional architecture diagrams using AI-powered Agno Agents with Google Gemini</p>',
        unsafe_allow_html=True
    )

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        # API Key input
        google_api_key = st.text_input(
            "Google API Key",
            value=os.getenv("GOOGLE_API_KEY", ""),
            type="password",
            help="Enter your Google AI API key for Gemini"
        )

        st.session_state.api_key_verified = verify_api_key(google_api_key)

        if not st.session_state.api_key_verified:
            st.warning("⚠️ Please enter your Google API key to continue")
            st.info("Get your API key from: https://makersuite.google.com/app/apikey")
            st.stop()
        else:
            st.success("✅ API Key verified")

        st.divider()

        # Template selector
        st.header("📋 Quick Templates")
        use_template = st.checkbox("Use a template", value=False)

        selected_template = None
        if use_template:
            template_names = get_template_names()
            selected_template = st.selectbox(
                "Choose a template",
                options=template_names,
                help="Select a pre-built architecture template"
            )

        st.divider()

        # About
        st.header("ℹ️ About")
        st.markdown("""
        This app uses:
        - **Agno Agentic SDK** for AI orchestration
        - **Google Gemini** for intelligent diagram generation
        - **Diagrams library** for professional visualization

        Created with ❤️ by Claude
        """)

    # Main content area
    tab1, tab2, tab3 = st.tabs(["🎨 Generate Diagram", "📖 View Code", "📚 Gallery"])

    with tab1:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Diagram Requirements")

            # If template selected, populate fields
            if use_template and selected_template:
                template = get_template(selected_template)
                st.info(f"📋 Using template: **{selected_template}**")
            else:
                template = {}

            # Input fields
            description = st.text_area(
                "Describe your architecture",
                value=template.get("description", ""),
                height=120,
                placeholder="E.g., A scalable e-commerce platform with user authentication, product catalog, shopping cart, payment processing, and order management",
                help="Provide a detailed description of the architecture you want to create"
            )

            col_a, col_b = st.columns(2)
            with col_a:
                architecture_type = st.selectbox(
                    "Architecture Type",
                    options=["cloud", "microservices", "serverless", "data", "ml", "event-driven", "devops", "network"],
                    index=["cloud", "microservices", "serverless", "data", "ml", "event-driven", "devops", "network"].index(
                        template.get("architecture_type", "cloud")
                    ) if template.get("architecture_type") in ["cloud", "microservices", "serverless", "data", "ml", "event-driven", "devops", "network"] else 0,
                    help="Type of architecture pattern"
                )

            with col_b:
                cloud_provider = st.selectbox(
                    "Cloud Provider",
                    options=["AWS", "GCP", "Azure", "Generic"],
                    index=["AWS", "GCP", "Azure", "Generic"].index(
                        template.get("cloud_provider", "AWS")
                    ) if template.get("cloud_provider") in ["AWS", "GCP", "Azure", "Generic"] else 0,
                    help="Select your cloud provider"
                )

            components = st.text_input(
                "Specific Components (optional)",
                value=template.get("components", ""),
                placeholder="E.g., Lambda, API Gateway, DynamoDB, S3",
                help="List specific services or components to include"
            )

        with col2:
            st.subheader("Actions")
            st.markdown("---")

            generate_button = st.button(
                "🚀 Generate Diagram",
                type="primary",
                disabled=not description or not st.session_state.api_key_verified,
                use_container_width=True
            )

            if st.session_state.generated_diagram:
                st.download_button(
                    label="💾 Download Diagram",
                    data=open(st.session_state.generated_diagram, "rb").read(),
                    file_name="architecture_diagram.png",
                    mime="image/png",
                    use_container_width=True
                )

            st.markdown("---")
            st.markdown("### 💡 Tips")
            st.markdown("""
            - Be specific about your requirements
            - Mention data flows and interactions
            - Include security and scaling needs
            - Specify integration points
            """)

        # Generate diagram
        if generate_button:
            with st.spinner("🤖 AI Agent is designing your architecture..."):
                try:
                    # Create the agent
                    agent = create_architecture_agent(google_api_key)

                    # Create diagram request
                    request = DiagramRequest(
                        description=description,
                        architecture_type=architecture_type,
                        cloud_provider=cloud_provider if cloud_provider != "Generic" else None,
                        components=components if components else None
                    )

                    # Generate diagram code
                    response = agent.generate_diagram_code(request)
                    st.session_state.diagram_response = response

                    # Display progress
                    st.success("✅ Diagram code generated!")

                except Exception as e:
                    st.error(f"❌ Error generating diagram code: {str(e)}")
                    st.stop()

            with st.spinner("🎨 Creating professional diagram..."):
                try:
                    # Generate the actual diagram
                    generator = DiagramGenerator(output_dir="outputs")
                    success, output_path, error = generator.generate_diagram(
                        response.diagram_code,
                        output_filename="architecture_diagram"
                    )

                    if success:
                        st.session_state.generated_diagram = output_path
                        st.balloons()
                        st.success("🎉 Diagram generated successfully!")
                    else:
                        st.error(f"❌ Error generating diagram: {error}")
                        st.stop()

                except Exception as e:
                    st.error(f"❌ Error creating diagram: {str(e)}")
                    st.stop()

        # Display generated diagram
        if st.session_state.generated_diagram:
            st.divider()
            st.subheader("📊 Generated Architecture Diagram")

            # Show diagram
            st.image(
                st.session_state.generated_diagram,
                use_container_width=True,
                caption="Professional Architecture Diagram"
            )

            # Show description and details
            if st.session_state.diagram_response:
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### 📝 Description")
                    st.info(st.session_state.diagram_response.description)

                    st.markdown("#### 🔧 Components")
                    for component in st.session_state.diagram_response.components:
                        st.markdown(f"- {component}")

                with col2:
                    st.markdown("#### ✨ Best Practices Applied")
                    for practice in st.session_state.diagram_response.best_practices:
                        st.markdown(f"- {practice}")

    with tab2:
        st.subheader("📖 Generated Python Code")

        if st.session_state.diagram_response:
            st.markdown("This is the Python code generated to create your diagram:")

            st.code(
                st.session_state.diagram_response.diagram_code,
                language="python",
                line_numbers=True
            )

            st.download_button(
                label="💾 Download Code",
                data=st.session_state.diagram_response.diagram_code,
                file_name="architecture_diagram.py",
                mime="text/x-python",
            )
        else:
            st.info("Generate a diagram first to see the code here.")

    with tab3:
        st.subheader("📚 Architecture Patterns Gallery")

        st.markdown("""
        Explore common architecture patterns and templates:
        """)

        # Display templates in a grid
        templates = get_template_names()
        cols = st.columns(2)

        for idx, template_name in enumerate(templates):
            with cols[idx % 2]:
                with st.expander(f"📐 {template_name}"):
                    template = get_template(template_name)
                    st.markdown(f"**Description:** {template['description']}")
                    st.markdown(f"**Type:** {template['architecture_type']}")
                    st.markdown(f"**Provider:** {template.get('cloud_provider', 'N/A')}")
                    st.markdown(f"**Components:** {template.get('components', 'N/A')}")


if __name__ == "__main__":
    main()
