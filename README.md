# AI-Driven Custom Home Design Assistant

An AI-powered web application that generates personalized home design plans based on user inputs. The application uses Google's Gemini AI for generating detailed design recommendations and Lexica.art for fetching relevant design inspiration images.

## Features

- Generate custom home designs based on style, size, and room requirements
- Get detailed design plans with room-by-room breakdown
- View design inspiration images
- Download design plans as text files
- Additional preferences for budget, outdoor space, and special features
- Eco-friendly design considerations

## Prerequisites

- Python 3.8 or higher
- Google Gemini API key
- Internet connection for API calls

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd home-design-assistant
```

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv home_design_env

# Activate virtual environment (Windows)
home_design_env\Scripts\activate

# Activate virtual environment (macOS/Linux)
source home_design_env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Google API key:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to `http://localhost:8501`

3. Enter your design preferences:
   - Design Style (e.g., Modern, Rustic, Contemporary)
   - Home Size (e.g., 2000 sq ft)
   - Number of Rooms
   - Additional preferences (optional)

4. Click "Generate Custom Home Design" to create your design plan

5. View the generated design plan and inspiration image

6. Download the design plan as a text file if desired

## Project Structure

```
home-design-assistant/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── config.py             # Configuration settings
├── utils.py              # Utility functions
├── .env                  # Environment variables (API keys)
├── .gitignore           # Git ignore file
└── README.md            # Project documentation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini AI for design generation
- Lexica.art for design inspiration images
- Streamlit for the web application framework 