import streamlit as st
from utils import generate_design_idea, fetch_image_from_lexica, generate_stability_image, validate_inputs

# Page configuration
st.set_page_config(
    page_title="Custom Home Design Assistant",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Universal box-sizing for consistent layout */
    *, *::before, *::after {
        box-sizing: border-box;
    }

    /* Base HTML and Body styles */
    html, body {
        margin: 0;
        padding: 0;
        min-height: 100vh;
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

    /* Responsive design breakpoints */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        .sub-header {
            font-size: 1.2rem;
        }
        .input-section, .result-section {
            padding: 1.5rem;
        }
        .stButton>button {
            padding: 0.5rem 1rem;
            font-size: 1rem;
        }
    }

    @media (max-width: 480px) {
        .main-header {
            font-size: 2rem;
        }
        .sub-header {
            font-size: 1rem;
        }
        .input-section, .result-section {
            padding: 1rem;
        }
    }

    /* Full-screen image modal styling */
    .image-container {
        position: relative;
        width: 100%;
        margin-bottom: 1rem;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
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

    .fullscreen-button {
        position: absolute;
        bottom: 15px;
        right: 15px;
        background: rgba(255, 255, 255, 0.9);
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }

    .fullscreen-button:hover {
        background: white;
        transform: scale(1.1);
    }

    /* Full-screen modal */
    .modal {
        display: none;
        position: fixed;
        z-index: 9999;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.95);
        overflow: auto;
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .modal.show {
        opacity: 1;
    }

    .modal-content {
        margin: auto;
        display: block;
        max-width: 90%;
        max-height: 90vh;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) scale(0.9);
        transition: transform 0.3s ease;
        border-radius: 8px;
        box-shadow: 0 0 30px rgba(0,0,0,0.3);
    }

    .modal.show .modal-content {
        transform: translate(-50%, -50%) scale(1);
    }

    .close {
        position: absolute;
        top: 20px;
        right: 35px;
        color: #f1f1f1;
        font-size: 40px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
    }

    .close:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: rotate(90deg);
    }

    /* Overall page and container styling */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
        color: #333333 !important;
        font-family: 'Inter', 'Segoe UI', Roboto, "Helvetica Neue", Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    /* Header styling with animation */
    .main-header {
        text-align: center;
        color: #4A90E2;
        font-size: 3.5rem;
        margin-bottom: 1rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: fadeIn 1s ease-out;
    }

    .sub-header {
        text-align: center;
        color: #7A7A7A;
        font-size: 1.4rem;
        margin-bottom: 3rem;
        font-weight: 300;
        animation: fadeIn 1s ease-out 0.3s backwards;
    }

    /* Section styling with animations */
    .input-section {
        background-color: #FFFFFF;
        padding: 2.5rem;
        border-radius: 16px;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #E0E0E0;
        transition: all 0.3s ease-in-out;
        animation: fadeIn 0.8s ease-out;
    }

    .input-section:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }

    .result-section {
        background-color: #FFFFFF;
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 6px solid #4A90E2;
        transition: all 0.3s ease-in-out;
        animation: fadeIn 0.8s ease-out;
    }

    .result-section:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }

    /* Enhanced button styling */
    .stButton>button {
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
        color: white;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease-in-out;
        border: none;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.2);
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #357ABD 0%, #2C6AA0 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(74, 144, 226, 0.3);
    }

    .stButton>button:active {
        transform: translateY(0);
    }

    /* Enhanced input styling */
    .stTextInput>div>div>input {
        border-radius: 12px;
        border: 2px solid #E0E0E0;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease-in-out;
        background-color: #FFFFFF !important;
        color: #333333 !important;
        font-size: 1rem;
    }

    .stTextInput>div>div>input:focus {
        border-color: #4A90E2;
        box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2);
        outline: none;
    }

    /* Sidebar styling */
    .css-1d391kg.e1fqkh3o1 {
        background: linear-gradient(135deg, #E6F0FF 0%, #D4E5FF 100%) !important;
        padding: 2rem;
        border-right: 1px solid #D0D0D0;
        animation: slideIn 0.5s ease-out;
    }

    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(74, 144, 226, 0.3);
        border-radius: 50%;
        border-top-color: #4A90E2;
        animation: spin 1s ease-in-out infinite;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>

<script>
    // Function to handle full-screen image display
    function openFullScreen(img) {
        var modal = document.createElement('div');
        modal.className = 'modal';
        document.body.appendChild(modal);
        
        var modalImg = document.createElement('img');
        modalImg.className = 'modal-content';
        modalImg.src = img.src;
        
        var closeBtn = document.createElement('span');
        closeBtn.className = 'close';
        closeBtn.innerHTML = '&times;';
        closeBtn.onclick = function() {
            modal.classList.remove('show');
            setTimeout(() => modal.remove(), 300);
        };
        
        modal.appendChild(modalImg);
        modal.appendChild(closeBtn);
        
        // Trigger reflow
        modal.offsetHeight;
        
        // Show modal with animation
        modal.style.display = 'block';
        setTimeout(() => modal.classList.add('show'), 10);
        
        // Close modal when clicking outside the image
        modal.onclick = function(e) {
            if (e.target === modal) {
                modal.classList.remove('show');
                setTimeout(() => modal.remove(), 300);
            }
        };
    }

    // Function to scroll to generated content
    function scrollToContent() {
        const content = document.querySelector('.result-section');
        if (content) {
            content.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    // Add loading animation to button
    document.addEventListener('DOMContentLoaded', function() {
        const button = document.querySelector('.stButton>button');
        if (button) {
            button.addEventListener('click', function() {
                this.innerHTML = '<span class="loading"></span> Generating...';
                this.disabled = true;
            });
        }
    });
</script>
""", unsafe_allow_html=True)

def main():
    # Initialize session state variables if they don't exist
    if 'design_idea' not in st.session_state:
        st.session_state.design_idea = None
    if 'image_url' not in st.session_state:
        st.session_state.image_url = None

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
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        style = st.text_input(
            "🎨 Design Style",
            placeholder="e.g., Modern, Rustic, Contemporary",
            help="Enter your preferred architectural and interior design style",
            key="design_style_input"
        )
    
    with col2:
        size = st.text_input(
            "📏 Home Size",
            placeholder="e.g., 2000 sq ft, Large, Medium",
            help="Specify the size of your home in square feet or general terms",
            key="home_size_input"
        )
    
    with col3:
        rooms = st.text_input(
            "🏠 Number of Rooms",
            placeholder="e.g., 4, 5, 6",
            help="Enter the total number of rooms you want",
            key="rooms_input"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional preferences section
    with st.expander("🔧 Additional Preferences (Optional)"):
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
            
        st.markdown("---") # Separator for visual clarity
        st.subheader("🖼️ Image Source")
        image_source = st.radio(
            "Choose how to get design inspiration images:",
            ("Lexica.art (Image Search)", "AI Image Generation"),
            index=0, # Default to Lexica.art
            help="Select whether to search existing images or generate new ones."
        )
    
    # Generate button
    if st.button("🚀 Generate Custom Home Design", type="primary", use_container_width=True):
        print("Button clicked!") # Debugging: Button click
        
        # Clear previous results and messages
        st.session_state.design_idea = None
        st.session_state.image_url = None
        
        # Placeholder for messages, to be updated dynamically
        message_placeholder = st.empty()

        # Validate inputs
        errors = validate_inputs(style, size, rooms)
        
        if errors:
            for error in errors:
                message_placeholder.error(error)
                print(f"Validation error: {error}") # Debugging: Validation errors
        else:
            message_placeholder.info("🎨 Creating your custom home design...")
            
            try:
                # Generate design idea
                st.session_state.design_idea = generate_design_idea(style, size, rooms)
                print(f"design_idea set in session_state: {st.session_state.design_idea[:50]}...") # Debugging: Design idea content
                
                if st.session_state.design_idea:
                    message_placeholder.success("✅ Home design plan generated!")
                else:
                    message_placeholder.warning("⚠️ Could not generate design plan. Please try again.")

            except Exception as e:
                message_placeholder.error(f"❌ Error generating design plan: {e}")
                st.session_state.design_idea = None # Ensure design_idea is None on error
                print(f"Error generating design plan: {e}")

            # Conditional image fetching/generation
            if st.session_state.design_idea: # Only proceed if design plan was successfully generated
                if image_source == "Lexica.art (Image Search)":
                    message_placeholder.info("🖼️ Fetching design inspiration image from Lexica.art...")
                    try:
                        st.session_state.image_url = fetch_image_from_lexica(style)
                        print(f"image_url set in session_state: {st.session_state.image_url}") # Debugging: Image URL content
                        if st.session_state.image_url:
                            message_placeholder.success("✔️ Design inspiration image fetched from Lexica.art!")
                        else:
                            message_placeholder.info("ℹ️ No image found on Lexica.art or unable to fetch image at this time.")

                    except Exception as e:
                        message_placeholder.warning(f"⚠️ Error fetching image from Lexica.art: {e}")
                        st.session_state.image_url = None # Ensure image_url is None on error
                        print(f"Error fetching image from Lexica.art, setting image_url to None: {e}") # Debugging: Image fetch error
                
                elif image_source == "AI Image Generation":
                    message_placeholder.info("✨ Generating design inspiration image using AI...")
                    try:
                        # Use the design idea as the prompt for image generation
                        image_prompt = st.session_state.design_idea.split('## ')[0].strip() + f" {style} home design" # Extracting a concise part of the plan as prompt
                        st.session_state.image_url = generate_stability_image(style, size, rooms)
                        print(f"AI generated image_url set in session_state: {st.session_state.image_url}") # Debugging: AI Image URL content
                        
                        if st.session_state.image_url:
                            message_placeholder.success("🎉 AI design inspiration image generated!")
                        else:
                            message_placeholder.info("ℹ️ AI could not generate an image at this time. Please try again or select Lexica.art.")

                    except Exception as e:
                        message_placeholder.warning(f"⚠️ Error generating AI image: {e}")
                        st.session_state.image_url = None # Ensure image_url is None on error
                        print(f"Error generating AI image, setting image_url to None: {e}") # Debugging: AI Image generation error
            
            # Clear the message after all operations are done
            message_placeholder.empty()

    # Display results if available in session state
    if st.session_state.design_idea:
        print("Displaying design idea...") # Debugging: Entering display block
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        
        # Create two columns for layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("## 📋 Your Custom Home Design Plan")
            st.markdown(st.session_state.design_idea)
        
        with col2:
            if st.session_state.image_url:
                st.markdown("## 🖼️ Design Inspiration")
                # Enhanced image container with fullscreen button
                st.markdown(f"""
                <div class="image-container">
                    <img src="{st.session_state.image_url}" alt="{style} Home Design Inspiration">
                    <button class="fullscreen-button" onclick="openFullScreen(this.parentElement.querySelector('img'))">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path>
                        </svg>
                    </button>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("No image available or unable to fetch design inspiration image at this time.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add JavaScript to scroll to content after generation
        st.markdown("""
        <script>
            window.onload = function() {
                scrollToContent();
            }
        </script>
        """, unsafe_allow_html=True)
        
        # Download option
        st.markdown("---")
        st.markdown("### 💾 Save Your Design")
        st.download_button(
            label="📄 Download Design Plan as Text",
            data=st.session_state.design_idea,
            file_name=f"{style.lower().replace(' ', '_')}_home_design.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main() 