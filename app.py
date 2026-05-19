import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY", "16ee22ef")
BASE_URL = "http://www.omdbapi.com/"

st.set_page_config(
    page_title="CineScope",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e0d5 !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background: #111118 !important; }

.hero {
    background: linear-gradient(135deg, #0a0a0f 0%, #1a0a22 50%, #0a0f1a 100%);
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding: 2.5rem 0 2rem;
    text-align: center;
    margin-bottom: 2rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3rem, 8vw, 6rem);
    letter-spacing: 0.12em;
    background: linear-gradient(90deg, #e8b86d, #e84d4d, #b86de8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin: 0;
}
.hero-sub {
    font-size: 0.85rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: rgba(232,224,213,0.4);
    margin-top: 0.5rem;
}

[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 2px !important;
    color: #e8e0d5 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
}
[data-testid="stTextInput"] input:focus {
    border-color: #e8b86d !important;
    box-shadow: 0 0 0 2px rgba(232,184,109,0.15) !important;
}
[data-testid="stTextInput"] label {
    color: rgba(232,224,213,0.5) !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
}

.section-label {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 0.1em;
    color: #e8e0d5;
    margin: 2rem 0 1rem;
    padding-left: 0.2rem;
    border-left: 3px solid #e8b86d;
    padding-left: 0.75rem;
}

.movie-card {
    position: relative;
    border-radius: 3px;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    background: #111118;
    aspect-ratio: 2/3;
    border: 1px solid rgba(255,255,255,0.06);
}
.movie-card:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0,0,0,0.6), 0 0 0 1px rgba(232,184,109,0.3);
}
.movie-card img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: opacity 0.2s;
}
.movie-card-overlay {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    background: linear-gradient(transparent, rgba(0,0,0,0.92));
    padding: 2rem 0.7rem 0.7rem;
    transform: translateY(2px);
    transition: transform 0.25s;
}
.movie-card:hover .movie-card-overlay { transform: translateY(0); }
.card-title {
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    font-size: 0.78rem;
    color: #e8e0d5;
    line-height: 1.3;
    margin: 0 0 0.2rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.card-year {
    font-size: 0.68rem;
    color: rgba(232,224,213,0.45);
    letter-spacing: 0.08em;
}
.card-rating {
    position: absolute;
    top: 0.5rem; right: 0.5rem;
    background: rgba(0,0,0,0.75);
    color: #e8b86d;
    font-size: 0.65rem;
    font-weight: 600;
    padding: 0.2rem 0.4rem;
    border-radius: 2px;
    letter-spacing: 0.05em;
}
.no-poster {
    width: 100%; height: 100%;
    display: flex; align-items: center; justify-content: center;
    background: linear-gradient(135deg, #1a1a28, #0f0f1a);
    font-size: 3rem;
    aspect-ratio: 2/3;
}

.detail-backdrop {
    border-radius: 4px;
    overflow: hidden;
    position: relative;
    background: linear-gradient(135deg, #111118, #1a0a22);
    border: 1px solid rgba(255,255,255,0.07);
    padding: 2rem;
    margin-bottom: 1.5rem;
}
.detail-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(2rem, 5vw, 3.5rem);
    letter-spacing: 0.08em;
    color: #e8e0d5;
    line-height: 1.05;
    margin: 0 0 0.3rem;
}
.detail-meta {
    font-size: 0.78rem;
    color: rgba(232,224,213,0.45);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.detail-genres span {
    display: inline-block;
    border: 1px solid rgba(232,184,109,0.4);
    color: #e8b86d;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.15rem 0.55rem;
    border-radius: 2px;
    margin-right: 0.4rem;
    margin-bottom: 0.4rem;
}
.detail-plot {
    font-size: 0.95rem;
    line-height: 1.75;
    color: rgba(232,224,213,0.8);
    margin: 1rem 0;
    max-width: 65ch;
}
.rating-pill {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: rgba(232,184,109,0.12);
    border: 1px solid rgba(232,184,109,0.25);
    color: #e8b86d;
    padding: 0.4rem 0.9rem;
    border-radius: 2px;
    font-size: 0.88rem;
    font-weight: 600;
    margin-right: 0.6rem;
    margin-bottom: 0.6rem;
}
.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 1.5rem;
}
.info-block {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    padding: 0.9rem 1rem;
    border-radius: 3px;
}
.info-block-label {
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: rgba(232,224,213,0.35);
    margin-bottom: 0.3rem;
}
.info-block-value {
    font-size: 0.9rem;
    font-weight: 500;
    color: #e8e0d5;
}

.cast-chip {
    display: inline-block;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.09);
    color: #e8e0d5;
    font-size: 0.78rem;
    padding: 0.3rem 0.75rem;
    border-radius: 50px;
    margin: 0.2rem;
}

[data-testid="stButton"] button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: rgba(232,224,213,0.7) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.45rem 1.2rem !important;
    border-radius: 2px !important;
    transition: all 0.2s !important;
}
[data-testid="stButton"] button:hover {
    border-color: #e8b86d !important;
    color: #e8b86d !important;
}

[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 2px !important;
    color: #e8e0d5 !important;
}

hr { border-color: rgba(255,255,255,0.06) !important; }

[data-testid="stSpinner"] { color: #e8b86d !important; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: rgba(232,184,109,0.3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


def omdb_get(params: dict) -> dict | None:
    params["apikey"] = API_KEY
    try:
        r = requests.get(BASE_URL, params=params, timeout=8)
        data = r.json()
        return data if data.get("Response") == "True" else None
    except Exception:
        return None


def search_movies(query: str, page: int = 1, type_filter: str = ""):
    params = {"s": query, "page": page}
    if type_filter:
        params["type"] = type_filter
    return omdb_get(params)


def get_details(imdb_id: str) -> dict | None:
    return omdb_get({"i": imdb_id, "plot": "full"})


if "selected_id" not in st.session_state:
    st.session_state.selected_id = None
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

TRENDING = [
    ("tt9362722", "Spider-Man: Across the Spider-Verse"),
    ("tt15398776", "Oppenheimer"),
    ("tt1517268", "Barbie"),
    ("tt14998742", "Anyone But You"),
    ("tt6263850", "Dune: Part Two"),
    ("tt21823606", "Poor Things"),
]

CLASSICS = [
    ("tt0111161", "The Shawshank Redemption"),
    ("tt0068646", "The Godfather"),
    ("tt0468569", "The Dark Knight"),
    ("tt0137523", "Fight Club"),
    ("tt0816692", "Interstellar"),
    ("tt0110912", "Pulp Fiction"),
]


def render_card(col, movie: dict):
    imdb_id = movie.get("imdbID", "")
    title = movie.get("Title", "Unknown")
    year = movie.get("Year", "")
    poster = movie.get("Poster", "N/A")
    rating = movie.get("imdbRating", "")

    with col:
        if poster and poster != "N/A":
            img_html = f'<img src="{poster}" alt="{title}" loading="lazy"/>'
        else:
            img_html = '<div class="no-poster">🎬</div>'

        rating_badge = f'<div class="card-rating">★ {rating}</div>' if rating and rating != "N/A" else ""

        card_html = f"""
        <div class="movie-card">
            {img_html}
            {rating_badge}
            <div class="movie-card-overlay">
                <div class="card-title">{title}</div>
                <div class="card-year">{year}</div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        if st.button("View", key=f"card_{imdb_id}_{title[:6]}"):
            st.session_state.selected_id = imdb_id
            st.rerun()


def render_grid(movies: list[dict], cols: int = 6):
    chunks = [movies[i:i+cols] for i in range(0, len(movies), cols)]
    for chunk in chunks:
        grid = st.columns(cols)
        for i, movie in enumerate(chunk):
            render_card(grid[i], movie)



def show_detail(imdb_id: str):
    with st.spinner("Loading…"):
        data = get_details(imdb_id)

    if not data:
        st.error("Could not load details.")
        return

    if st.button("← Back"):
        st.session_state.selected_id = None
        st.rerun()

    poster = data.get("Poster", "N/A")
    title = data.get("Title", "—")
    year = data.get("Year", "")
    rated = data.get("Rated", "")
    runtime = data.get("Runtime", "")
    genre = data.get("Genre", "")
    director = data.get("Director", "")
    writer = data.get("Writer", "")
    actors = data.get("Actors", "")
    plot = data.get("Plot", "")
    language = data.get("Language", "")
    country = data.get("Country", "")
    awards = data.get("Awards", "")
    imdb_rating = data.get("imdbRating", "N/A")
    imdb_votes = data.get("imdbVotes", "")
    box_office = data.get("BoxOffice", "N/A")
    released = data.get("Released", "")
    media_type = data.get("Type", "movie").capitalize()
    total_seasons = data.get("totalSeasons", "")

    
    ratings = data.get("Ratings", [])

    col_poster, col_info = st.columns([1, 2.8])

    with col_poster:
        if poster and poster != "N/A":
            st.image(poster, use_container_width=True)
        else:
            st.markdown('<div style="background:#1a1a28;aspect-ratio:2/3;display:flex;align-items:center;justify-content:center;font-size:4rem;border-radius:3px;">🎬</div>', unsafe_allow_html=True)

        
        in_wl = imdb_id in [w["imdbID"] for w in st.session_state.watchlist]
        if in_wl:
            if st.button("✓ In Watchlist", key="wl_toggle"):
                st.session_state.watchlist = [w for w in st.session_state.watchlist if w["imdbID"] != imdb_id]
                st.rerun()
        else:
            if st.button("+ Add to Watchlist", key="wl_toggle"):
                st.session_state.watchlist.append({"imdbID": imdb_id, "Title": title, "Year": year, "Poster": poster})
                st.rerun()

    with col_info:
    
        genre_html = " ".join([f"<span>{g.strip()}</span>" for g in genre.split(",") if g.strip()])

        st.markdown(f"""
        <div class="detail-backdrop">
            <div style="font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:rgba(232,184,109,0.6);margin-bottom:0.4rem">{media_type} {f"· {total_seasons} Seasons" if total_seasons else ""}</div>
            <div class="detail-title">{title}</div>
            <div class="detail-meta">{released} &nbsp;·&nbsp; {runtime} &nbsp;·&nbsp; {rated} &nbsp;·&nbsp; {country}</div>
            <div class="detail-genres">{genre_html}</div>
            <p class="detail-plot">{plot}</p>
        </div>
        """, unsafe_allow_html=True)

        # Ratings row
        rating_html = ""
        if imdb_rating != "N/A":
            rating_html += f'<span class="rating-pill">⭐ IMDb &nbsp; {imdb_rating}/10 <span style="opacity:0.45;font-weight:400;font-size:0.75rem">({imdb_votes})</span></span>'
        for r in ratings:
            src = r.get("Source", "")
            val = r.get("Value", "")
            if "Rotten" in src:
                rating_html += f'<span class="rating-pill">🍅 {val}</span>'
            elif "Metacritic" in src:
                rating_html += f'<span class="rating-pill">Ⓜ️ {val}</span>'
        st.markdown(rating_html, unsafe_allow_html=True)

        
        info_items = [
            ("Director", director),
            ("Writer", writer),
            ("Language", language),
            ("Box Office", box_office),
            ("Awards", awards),
        ]
        if total_seasons:
            info_items.append(("Seasons", total_seasons))

        grid_html = '<div class="info-grid">'
        for label, val in info_items:
            if val and val != "N/A":
                grid_html += f'<div class="info-block"><div class="info-block-label">{label}</div><div class="info-block-value">{val}</div></div>'
        grid_html += "</div>"
        st.markdown(grid_html, unsafe_allow_html=True)

    if actors and actors != "N/A":
        st.markdown('<div class="section-label">Cast</div>', unsafe_allow_html=True)
        chips = " ".join([f'<span class="cast-chip">{a.strip()}</span>' for a in actors.split(",")])
        st.markdown(chips, unsafe_allow_html=True)

    first_genre = genre.split(",")[0].strip() if genre else ""
    if first_genre:
        st.markdown(f'<div class="section-label">More {first_genre}</div>', unsafe_allow_html=True)
        similar = search_movies(first_genre)
        if similar and similar.get("Search"):
            items = [m for m in similar["Search"] if m.get("imdbID") != imdb_id][:6]
            if items:
                render_grid(items, cols=6)



def show_home():
    st.markdown("""
    <div class="hero">
        <div class="hero-title">CineScope</div>
        <div class="hero-sub">Your cinematic universe, explored</div>
    </div>
    """, unsafe_allow_html=True)

    sc1, sc2, sc3 = st.columns([4, 1, 1])
    with sc1:
        query = st.text_input("", placeholder="Search movies, shows, series…", label_visibility="collapsed")
    with sc2:
        media_type = st.selectbox("Type", ["All", "Movie", "Series", "Episode"], label_visibility="collapsed")
    with sc3:
        do_search = st.button("Search", use_container_width=True)

    type_map = {"All": "", "Movie": "movie", "Series": "series", "Episode": "episode"}
    selected_type = type_map[media_type]

    if query or do_search:
        if query.strip():
            st.markdown(f'<div class="section-label">Results for "{query}"</div>', unsafe_allow_html=True)
            with st.spinner("Searching…"):
                results = search_movies(query, type_filter=selected_type)
            if results and results.get("Search"):
                total = results.get("totalResults", "?")
                st.caption(f"{total} results found")
                render_grid(results["Search"], cols=5)
            else:
                st.info("No results found. Try a different title.")
        return

    st.markdown('<div class="section-label">Trending Now</div>', unsafe_allow_html=True)
    with st.spinner("Loading trending…"):
        trending_movies = []
        for tid, fallback in TRENDING:
            d = omdb_get({"i": tid})
            if d:
                trending_movies.append(d)
    if trending_movies:
        render_grid(trending_movies, cols=6)

    st.markdown('<div class="section-label">All-Time Classics</div>', unsafe_allow_html=True)
    with st.spinner("Loading classics…"):
        classic_movies = []
        for tid, _ in CLASSICS:
            d = omdb_get({"i": tid})
            if d:
                classic_movies.append(d)
    if classic_movies:
        render_grid(classic_movies, cols=6)

    st.markdown('<div class="section-label">Top Rated TV Series</div>', unsafe_allow_html=True)
    TV_IDS = [
        ("tt0903747", "Breaking Bad"),
        ("tt0944947", "Game of Thrones"),
        ("tt7366338", "Chernobyl"),
        ("tt0795176", "Planet Earth"),
        ("tt5753856", "Dark"),
        ("tt0386676", "The Office"),
    ]
    with st.spinner("Loading series…"):
        tv_shows = []
        for tid, _ in TV_IDS:
            d = omdb_get({"i": tid})
            if d:
                tv_shows.append(d)
    if tv_shows:
        render_grid(tv_shows, cols=6)

    if st.session_state.watchlist:
        st.markdown('<div class="section-label">Your Watchlist</div>', unsafe_allow_html=True)
        render_grid(st.session_state.watchlist, cols=6)

    st.markdown('<div class="section-label">Browse by Genre</div>', unsafe_allow_html=True)
    genres = ["Action", "Comedy", "Horror", "Sci-Fi", "Thriller", "Romance", "Drama", "Animation"]
    g_cols = st.columns(len(genres))
    for i, g in enumerate(genres):
        with g_cols[i]:
            if st.button(g, key=f"genre_{g}", use_container_width=True):
                st.session_state.search_query = g
                st.query_params["q"] = g
                st.rerun()



if st.session_state.selected_id:
    show_detail(st.session_state.selected_id)
else:
    show_home()