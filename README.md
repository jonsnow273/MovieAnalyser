# 🎬 CineScope — MovieAnalyser

A cinematic movie & TV show explorer built with **Python**, **Streamlit**, and the **OMDb API**. Search for any film or series, browse trending titles, explore full cast & ratings, and build your personal watchlist — all in a sleek dark UI inspired by Letterboxd.

---

## ✨ Features

- 🔍 **Search** — Find any movie, series, or episode by title with type filtering
- 🎞️ **Poster Grid** — Letterboxd-style poster cards with hover effects and ratings
- 📄 **Detail Page** — Full plot, cast, director, box office, IMDb + Rotten Tomatoes + Metacritic ratings
- 🔥 **Trending Now** — Curated list of recent popular films
- 🏆 **All-Time Classics** — Top IMDb-rated movies
- 📺 **Top Rated TV Series** — Best-rated shows including Breaking Bad, Dark, Chernobyl
- 🎭 **Browse by Genre** — Quick-search buttons for Action, Horror, Sci-Fi, and more
- 📌 **Watchlist** — Add/remove movies to a personal watchlist during your session
- 🎨 **Dark Cinema UI** — Custom CSS with Bebas Neue + DM Sans fonts, amber accents

---

## 📸 Preview

> _Add a screenshot here after deploying_

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| UI Framework | [Streamlit](https://streamlit.io/) |
| API | [OMDb API](https://www.omdbapi.com/) |
| HTTP Requests | `requests` |
| Environment Variables | `python-dotenv` |
| Language | Python 3.10+ |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/jonsnow273/MovieAnalyser.git
cd MovieAnalyser
```

### 2. Install dependencies

```bash
pip install -r requirement.txt
```

### 3. Set up your API key

Create a `.env` file in the root folder:

```
OMDB_API_KEY=your_api_key_here
```

> Get a free API key at [omdbapi.com](https://www.omdbapi.com/apikey.aspx)

### 4. Run the app

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📁 Project Structure

```
MovieAnalyser/
├── app.py              # Main Streamlit application
├── requirement.txt     # Python dependencies
├── .env                # API key (not committed)
├── .gitignore          # Ignores .env and other files
└── README.md
```

---

## ⚙️ Requirements

```
streamlit
requests
python-dotenv
```

> Make sure you're on **Python 3.10 or higher** (required for the type hint syntax used in the code).

---

## 🔑 API

This project uses the [OMDb API](https://www.omdbapi.com/) — a free RESTful web service to obtain movie information.

- Free tier: 1,000 requests/day
- Endpoints used: `s=` (search by title), `i=` (fetch by IMDb ID)

---

## 🙌 Author

Made by [@jonsnow273](https://github.com/jonsnow273)
