import streamlit as st
from utils import generate_design_idea, fetch_image_from_lexica, generate_stability_image, validate_inputs

# Page configuration
st.set_page_config(
    page_title="Custom Home Design Assistant",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="auto"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Reset and Base Styles */
    *, *::before, *::after {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }

    /* Responsive Typography */
    html {
        font-size: 16px;
    }

    @media (max-width: 768px) {
        html {
            font-size: 14px;
        }
    }

    @media (max-width: 480px) {
        html {
            font-size: 12px;
        }
    }

    /* Smooth Scrolling */
    html, body {
        scroll-behavior: smooth;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    /* Responsive Layout */
    .stApp {
        max-width: 100%;
        overflow-x: hidden;
    }

    /* Main Container */
    .main-container {
        animation: fadeIn 0.5s ease-out;
        padding: 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    /* Header Styles */
    .main-header {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        animation: fadeIn 0.5s ease-out;
    }

    .sub-header {
        font-size: 1.2rem;
        margin-bottom: 2rem;
        animation: fadeIn 0.5s ease-out 0.2s;
    }

    /* Section Styles */
    .section {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        animation: fadeIn 0.5s ease-out;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .section:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

    /* Form Elements */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        transform: scale(1.02);
    }

    /* Button Styles */
    .stButton > button {
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    /* Image Container */
    .image-container {
        position: relative;
        width: 100%;
        margin-bottom: 1rem;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out;
    }

    .image-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }

    .image-container img {
        width: 100%;
        height: auto;
        display: block;
        transition: transform 0.3s ease;
    }

    .image-container:hover img {
        transform: scale(1.02);
    }

    /* Dark Mode Styles */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background: linear-gradient(135deg, #2c3e50 0%, #1a2c3e 100%) !important;
            color: #ecf0f1 !important;
        }

        .section {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Form Elements in Dark Mode */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > div {
            background-color: #34495e !important;
            color: #ecf0f1 !important;
            border-color: #4a657e !important;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > div:focus {
            border-color: #5DADE2 !important;
            box-shadow: 0 0 0 1px #5DADE2 !important;
        }

        /* Button Styles in Dark Mode */
        .stButton > button {
            background-color: #3498db !important;
            color: white !important;
        }

        .stButton > button:hover {
            background-color: #2980b9 !important;
        }
    }

    /* Responsive Grid */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }

        .sub-header {
            font-size: 1rem;
        }

        .section {
            padding: 1rem;
        }

        /* Adjust column layouts for mobile */
        [data-testid="stHorizontalBlock"] {
            flex-direction: column;
        }

        [data-testid="stHorizontalBlock"] > div {
            width: 100% !important;
        }
    }

    /* Loading Animation */
    .loading {
        display: inline-block;
        width: 50px;
        height: 50px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #3498db;
        animation: spin 1s ease-in-out infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    /* Error Message Styling */
    .error-message {
        background-color: rgba(231, 76, 60, 0.1);
        border-left: 4px solid #e74c3c;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
        animation: fadeIn 0.3s ease-out;
    }

    /* Success Message Styling */
    .success-message {
        background-color: rgba(46, 204, 113, 0.1);
        border-left: 4px solid #2ecc71;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
        animation: fadeIn 0.3s ease-out;
    }

    /* Info Message Styling */
    .info-message {
        background-color: rgba(52, 152, 219, 0.1);
        border-left: 4px solid #3498db;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
        animation: fadeIn 0.3s ease-out;
    }
</style>
""", unsafe_allow_html=True)

def display_error(message):
    """Display error message with custom styling"""
    st.markdown(f"""
    <div class="error-message">
        <strong>❌ Error:</strong> {message}
    </div>
    """, unsafe_allow_html=True)

def display_success(message):
    """Display success message with custom styling"""
    st.markdown(f"""
    <div class="success-message">
        <strong>✅ Success:</strong> {message}
    </div>
    """, unsafe_allow_html=True)

def display_info(message):
    """Display info message with custom styling"""
    st.markdown(f"""
    <div class="info-message">
        <strong>ℹ️ Info:</strong> {message}
    </div>
    """, unsafe_allow_html=True)

def main():
    # Initialize session state variables if they don't exist
    if 'design_idea' not in st.session_state:
        st.session_state.design_idea = None
    if 'image_url' not in st.session_state:
        st.session_state.image_url = None

    # Main container with animation
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Application header
    st.markdown('<h1 class="main-header">🏠 Custom Home Design Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Create your dream home with AI-powered design recommendations</p>', unsafe_allow_html=True)
    
    # Sidebar for additional information
    with st.sidebar:
        st.header("About This Tool")
        st.write("""
        This AI-powered assistant helps you create custom home designs based on your preferences. 
        Simply enter your desired style, size, and room requirements to get started.
        """)
        
        st.header("Design Styles Examples")
        st.write("""
        - Modern
        - Traditional
        - Contemporary
        - Rustic
        - Mediterranean
        - Colonial
        - Craftsman
        - Victorian
        - Minimalist
        - Industrial
        """)
        
        st.header("Tips for Best Results")
        st.write("""
        - Be specific about your style preferences
        - Include square footage or approximate size
        - Consider both indoor and outdoor needs
        - Think about your lifestyle requirements
        """)
    
    # Main input section
    st.markdown('<div class="section">', unsafe_allow_html=True)

    # Add a decorative header for the input section
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #3498db; font-size: 1.8rem; margin-bottom: 0.5rem;">✨ Start Your Design Journey</h2>
        <p style="color: #7f8c8d; font-size: 1.1rem;">Fill in the details below to create your dream home</p>
    </div>
    """, unsafe_allow_html=True)

    # Create a grid for the main inputs
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 0.5rem;">
            <span style="font-size: 1.2rem;">🎨</span>
        </div>
        """, unsafe_allow_html=True)
        style = st.text_input(
            "Design Style",
            placeholder="e.g., Modern, Rustic, Contemporary",
            help="Enter your preferred architectural and interior design style",
            key="design_style_input"
        )

    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 0.5rem;">
            <span style="font-size: 1.2rem;">📏</span>
        </div>
        """, unsafe_allow_html=True)
        size = st.text_input(
            "Home Size",
            placeholder="e.g., 2000 sq ft, Large, Medium",
            help="Specify the size of your home in square feet or general terms",
            key="home_size_input"
        )

    with col3:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 0.5rem;">
            <span style="font-size: 1.2rem;">🏠</span>
        </div>
        """, unsafe_allow_html=True)
        rooms = st.text_input(
            "Number of Rooms",
            placeholder="e.g., 4, 5, 6",
            help="Enter the total number of rooms you want",
            key="rooms_input"
        )

    # Add a decorative separator
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <div style="height: 1px; background: linear-gradient(to right, transparent, #3498db, transparent);"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional preferences section
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown("### 🔧 Additional Preferences")
    col1, col2 = st.columns(2)
    
    with col1:
        budget_range = st.selectbox(
            "💰 Budget Range",
            ["Not specified", "Budget-friendly", "Mid-range", "Luxury", "Ultra-luxury"]
        )
        
        outdoor_space = st.selectbox(
            "🌿 Outdoor Space",
            ["Not specified", "Small patio", "Large deck", "Garden", "Pool area", "Extensive landscaping"]
        )
    
    with col2:
        special_features = st.multiselect(
            "✨ Special Features",
            ["Home office", "Gym", "Library", "Wine cellar", "Home theater", "Guest suite", "Walk-in closet"]
        )
        
        eco_friendly = st.checkbox("🌱 Eco-friendly design considerations")
    
    st.markdown("---")
    st.subheader("🖼️ Image Source")
    image_source = st.radio(
        "Choose how to get design inspiration images:",
        ("AI Image Generation", "Lexica.art (Image Search)"),
        index=0,
        help="Select whether to generate new images or search existing ones."
    )
    
    st.info("💡 Tip: AI Image Generation creates unique, custom designs based on your preferences. This may take a few moments but will provide more personalized results.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Detailed Home Planning section
    with st.expander("📝 Detailed Home Planning (Optional)"):
        st.markdown('<div class="section">', unsafe_allow_html=True)
        # Room Configuration
        st.subheader("Room Configuration")
        col1, col2 = st.columns(2)
        
        with col1:
            num_bedrooms = st.number_input("Number of Bedrooms", min_value=1, max_value=10, value=3)
            num_bathrooms = st.number_input("Number of Bathrooms", min_value=1, max_value=8, value=2)
            num_doors = st.number_input("Number of Exterior Doors", min_value=1, max_value=10, value=2)
            
        with col2:
            num_windows = st.number_input("Number of Windows", min_value=1, max_value=30, value=8)
            ceiling_height = st.selectbox("Ceiling Height", 
                ["Standard (8ft)", "High (9ft)", "Very High (10ft+)", "Vaulted", "Custom"])
            floor_material = st.selectbox("Preferred Floor Material",
                ["Hardwood", "Tile", "Carpet", "Concrete", "Mixed", "Other"])

        # Room Details using tabs instead of expanders
        st.subheader("Room Details")
        room_details = {}
        
        # Create tabs for different rooms
        room_tabs = st.tabs(["Living Room", "Kitchen", "Master Bedroom"])
        
        # Living Room Tab
        with room_tabs[0]:
            col1, col2 = st.columns(2)
            with col1:
                room_details["living_room"] = {
                    "size": st.text_input("Size (sq ft)", key="living_size", 
                        help="Enter the desired size in square feet"),
                    "layout": st.selectbox("Preferred Layout", 
                        ["Open", "Traditional", "Modern", "Minimalist"], key="living_layout"),
                    "features": st.multiselect("Special Features",
                        ["Fireplace", "Entertainment Center", "Reading Nook", "Bar Area"], key="living_features")
                }

        # Kitchen Tab
        with room_tabs[1]:
            col1, col2 = st.columns(2)
            with col1:
                room_details["kitchen"] = {
                    "size": st.text_input("Size (sq ft)", key="kitchen_size",
                        help="Enter the desired size in square feet"),
                    "layout": st.selectbox("Preferred Layout",
                        ["Open", "Galley", "L-shaped", "U-shaped", "Island"], key="kitchen_layout"),
                    "features": st.multiselect("Special Features",
                        ["Island", "Breakfast Bar", "Walk-in Pantry", "Wine Storage"], key="kitchen_features")
                }

        # Master Bedroom Tab
        with room_tabs[2]:
            col1, col2 = st.columns(2)
            with col1:
                room_details["master_bedroom"] = {
                    "size": st.text_input("Size (sq ft)", key="master_size",
                        help="Enter the desired size in square feet"),
                    "features": st.multiselect("Special Features",
                        ["Walk-in Closet", "En-suite Bathroom", "Sitting Area", "Balcony"], key="master_features")
                }

        # Additional Requirements
        st.subheader("Additional Requirements")
        additional_requirements = st.text_area(
            "Describe any specific requirements or preferences for your home design:",
            placeholder="Example: Need a home office with natural light, prefer open concept living areas, want a mudroom for storage...",
            height=100
        )

        # Timeline and Priority
        st.subheader("Project Timeline and Priority")
        col1, col2 = st.columns(2)
        with col1:
            timeline = st.selectbox("Project Timeline",
                ["Not specified", "Immediate (1-3 months)", "Short-term (3-6 months)", 
                 "Medium-term (6-12 months)", "Long-term (1+ year)"])
        with col2:
            priority = st.selectbox("Design Priority",
                ["Not specified", "Functionality", "Aesthetics", "Cost-effectiveness", 
                 "Sustainability", "Resale Value"])
        st.markdown('</div>', unsafe_allow_html=True)

    # Generate button
    if st.button("🚀 Generate Custom Home Design", type="primary", use_container_width=True):
        try:
            # Validate inputs
            errors = validate_inputs(style, size, rooms)
            
            if errors:
                for error in errors:
                    display_error(error)
            else:
                display_info("🎨 Creating your custom home design...")
                
                try:
                    # Generate design idea
                    st.session_state.design_idea = generate_design_idea(
                        style=style,
                        size=size,
                        rooms=rooms,
                        room_details=room_details,
                        num_bedrooms=num_bedrooms,
                        num_bathrooms=num_bathrooms,
                        num_doors=num_doors,
                        num_windows=num_windows,
                        ceiling_height=ceiling_height,
                        floor_material=floor_material,
                        additional_requirements=additional_requirements,
                        timeline=timeline,
                        priority=priority
                    )
                    
                    if st.session_state.design_idea:
                        display_success("✅ Home design plan generated!")
                    else:
                        display_error("⚠️ Could not generate design plan. Please try again.")

                except Exception as e:
                    display_error(f"Error generating design plan: {str(e)}")
                    st.session_state.design_idea = None

                # Image generation/fetching
                if st.session_state.design_idea:
                    try:
                        if image_source == "AI Image Generation":
                            display_info("✨ Generating design inspiration image using AI...")
                            st.session_state.image_url = generate_stability_image(style, size, rooms)
                            if st.session_state.image_url:
                                display_success("🎉 AI design inspiration image generated!")
                            else:
                                display_error("⚠️ Could not generate AI image. Please try again.")
                        else:
                            display_info("🖼️ Fetching design inspiration image from Lexica.art...")
                            st.session_state.image_url = fetch_image_from_lexica(style)
                            if st.session_state.image_url:
                                display_success("✔️ Design inspiration image fetched!")
                            else:
                                display_error("⚠️ Could not fetch image. Please try again.")
                    except Exception as e:
                        display_error(f"Error with image generation/fetching: {str(e)}")
                        st.session_state.image_url = None

        except Exception as e:
            display_error(f"An unexpected error occurred: {str(e)}")

    # Display results if available
    if st.session_state.design_idea:
        st.markdown('<div class="section">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("## 📋 Your Custom Home Design Plan")
            st.markdown(st.session_state.design_idea)
        
        with col2:
            if st.session_state.image_url:
                st.markdown("## 🖼️ Design Inspiration")
                st.markdown(f"""
                <div class="image-container">
                    <img src="{st.session_state.image_url}" alt="{style} Home Design Inspiration">
                </div>
                """, unsafe_allow_html=True)
            else:
                display_info("No image available at this time.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download option
        st.markdown("---")
        st.markdown("### 💾 Save Your Design")
        st.download_button(
            label="📄 Download Design Plan as Text",
            data=st.session_state.design_idea,
            file_name=f"{style.lower().replace(' ', '_')}_home_design.txt",
            mime="text/plain"
        )

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 