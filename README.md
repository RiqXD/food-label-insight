# food-label-insight
A smart nutrition analyzer leveraging Gemini's multimodal capabilities to directly read and parse food labels.

## Features
- **AI-Powered Extraction**: Uses Google Gemini to instantly parse nutritional facts from uploaded images or camera captures.
- **AKG Comparison**: Automatically calculates and compares nutritional intake against Indonesian AKG guidelines based on user age and gender.
- **Smart Dashboard**: Visualizes data with a modern, responsive UI built using Streamlit.
- **AI Recommendation**: Generates personalized consumption advice, helping users understand whether a product fits their daily nutritional goals.

## Tech Stack
- **Frontend**: Streamlit
- **Vision/AI**: Google Gemini API (Multimodal)
- **Text Analysis**: OpenRouter (OpenAI-compatible API)
- **Data Processing**: Pandas

## Getting Started

### Prerequisites
- Python 3.9+
- An API Key for [Google Gemini](https://aistudio.google.com/)
- An API Key for [OpenRouter](https://openrouter.ai/) (or OpenAI)
