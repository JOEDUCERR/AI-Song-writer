import streamlit as st
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from pydantic import SecretStr

# Load environment variables from .env
# load_dotenv()

# Set up OpenAI API key
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

if not OPENAI_API_KEY:
    st.error("OpenAI API key not found. Please add it to your .env file as OPENAI_API_KEY.")
    st.stop()

st.set_page_config(
    page_title="LyricCraft",
    page_icon="🎵"
)

st.title("🎵 LyricCraft")
st.write("""
Welcome! Get creative songwriting ideas by selecting a mood, genre, and adding any extra details you want. Fill out the form and press 'Generate Song Lyrics' to get your lyrics instantly!
""")

# Dropdown options
moods = ["Happy", "Sad", "Energetic", "Calm", "Romantic", "Melancholic", "Uplifting", "Dark"]
genres = ["Pop", "Rock", "Jazz", "Hip-Hop", "Country", "Folk", "Electronic", "Classical"]

# Sidebar for song context
with st.form("song_form"):
    st.header("Song Context")
    mood = st.selectbox("Select the mood of your song:", moods)
    genre = st.selectbox("Select the genre of your song:", genres)
    extra = st.text_area("Any extra ideas or specifications? (Optional)")
    submitted = st.form_submit_button("Generate Song Lyrics")

# Function to get lyrics from the LLM
def get_lyrics(mood, genre, extra):
    template = '''
    You are a creative songwriting assistant. Write original song lyrics in the following style:
    - Mood: {mood}
    - Genre: {genre}
    - Extra specifications: {extra}
    
    The lyrics should be creative, engaging, and fit the given mood and genre. If extra specifications are provided, incorporate them into the lyrics.
    '''
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(api_key=SecretStr(str(OPENAI_API_KEY)))
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({
        "mood": mood,
        "genre": genre,
        "extra": extra or "None"
    })

if submitted:
    with st.spinner("Generating your song lyrics..."):
        try:
            lyrics = get_lyrics(mood, genre, extra)
            st.markdown("### 🎤 Generated Song Lyrics")
            st.write(lyrics)
        except Exception as e:
            st.error(f"Error generating song lyrics: {e}") 