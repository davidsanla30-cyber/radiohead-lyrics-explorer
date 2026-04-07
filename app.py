import streamlit as st
import pandas as pd
import re
from collections import Counter
import matplotlib.pyplot as plt

st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

h1 {
    color: #00FFAA;
    text-align: center;
}

h2, h3 {
    color: #FAFAFA;
}

.stMetric {
    background-color: #262730;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
}

.stDataFrame {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Radiohead Lyrics Explorer", layout="wide")

STOPWORDS = {
    "the","and","a","an","to","of","in","on","for","is","it","you","me","my",
    "i","we","our","your","that","this","with","be","am","are","was","were",
    "do","does","did","so","but","if","not","no","yes","oh","ah","ooh","la",
    "all","can","get","got","what","when","where","who","why","how",
    "just","will","into","out","off","down","up","back","there","here",
    "don","dont","didnt","cant","wont","im","youre","theyre","ive",
    "like","know","one","two","three","yeah","hey",
    "they","want","now","come","never","let","have","from","take","around","over"
}

def clean_lyrics(text):
    text = str(text).lower()
    text = re.sub(r"\[.*?\]", " ", text)
    text = text.replace("\n", " ")
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    words = [w for w in text.split() if len(w) > 2 and w not in STOPWORDS]
    return words

@st.cache_data
def load_data():
    return pd.read_csv("radiohead_studio_tracks.csv")

df = load_data()

st.title("Radiohead Lyrics Explorer")
st.markdown(
    "<h1>🎵 Radiohead Lyrics Explorer</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>Explora canciones, letras y patrones de palabras en los álbumes de Radiohead</p>",
    unsafe_allow_html=True
)

albums = sorted(df["album"].dropna().unique())
selected_album = st.selectbox("Selecciona un álbum", albums)

album_df = df[df["album"] == selected_album].copy()

all_words = []
for lyrics in album_df["lyrics"].dropna():
    all_words.extend(clean_lyrics(lyrics))

word_counts = Counter(all_words)
top_words = word_counts.most_common(15)

col1, col2 = st.columns(2)

with col1:
    st.metric("Canciones del álbum", len(album_df))
with col2:
    st.metric("Palabras analizadas", len(all_words))

st.subheader("Canciones del álbum")
st.dataframe(
    album_df[["name", "release_date"]].rename(
        columns={"name": "Canción", "release_date": "Fecha"}
    ),
    use_container_width=True
)

st.subheader("Palabras más frecuentes")

if top_words:
    words = [w for w, _ in top_words]
    counts = [c for _, c in top_words]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(words, counts)
    ax.set_facecolor("#0E1117")
    fig.patch.set_facecolor("#0E1117")
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")
    ax.set_title(f"Palabras más frecuentes en {selected_album}")
    ax.set_xlabel("Palabras")
    ax.set_ylabel("Frecuencia")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)

    top_df = pd.DataFrame(top_words, columns=["Palabra", "Frecuencia"])
    st.dataframe(top_df, use_container_width=True)
else:
    st.warning("No hay letras disponibles para este álbum.")

with st.expander("Mostrar letra"):
    st.dataframe(
        album_df[["name", "lyrics"]].rename(columns={"name": "Canción", "lyrics": "Letra"}),
        use_container_width=True
    )