# FIFA World Cup 2026 Player Analytics Dashboard

An interactive **Streamlit dashboard** for exploring FIFA World Cup 2026 player statistics across multiple performance categories. The project combines **web scraping**, **PCA feature engineering**, **K-Means clustering**, and **interactive visualization** to transform raw player statistics into meaningful insights.

---

## Features

- **Interactive Analytics Dashboard**: Multi-page app built with Streamlit & Plotly.
- **Player Analysis**: Detailed player profile, ratings, radar chart vs. archetype average, and 5 nearest similar player profiles.
- **Player Comparison**: Side-by-side radar and numerical metric comparison of any two players.
- **Player Space**: Interactive 2D PCA scatter plot visualizing player archetype distributions.
- **Country Analytics**: Aggregated national team metrics, country rankings, performance bar charts, and top player per nation.
- **Dataset Insights**: Overview metrics, position distributions, archetype breakdown, and overall rating distributions.

---

## Analytics Categories

- ⚽ Attacking
- 🛡️ Defending
- 🎯 Distribution
- 🧤 Goalkeeping
- 🏃 Movement
- 🟨 Discipline
- 🏆 Golden Boot

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core Language |
| Streamlit | Web Application & Dashboard |
| Pandas | Data Processing & Transformation |
| Scikit-Learn | PCA Feature Engineering & K-Means Clustering |
| Plotly / Matplotlib | Interactive Visualizations |
| Playwright | Automated Web Scraping (Development) |
| Git | Version Control |

---

## Project Structure

```text
FIFA-WorldCup-2026-Player-Analytics/
│
├── app.py                     # Main Streamlit Entrypoint
├── utils.py                   # Data loading & similarity engine helpers
├── requirements.txt           # Production dependencies for Streamlit Cloud
├── requirements-dev.txt       # Optional development dependencies
├── README.md
│
├── pages/                     # Streamlit Multi-Page App Pages
│   ├── 1_Player_Analysis.py
│   ├── 2_Compare_Players.py
│   ├── 3_Player_Space.py
│   ├── 4_Country_Analytics.py
│   └── 5_Dataset_Insights.py
│
├── data/
│   ├── raw/                   # Scraped raw category CSVs
│   └── processed/             # Cleaned, engineered, & clustered datasets
│
├── dashboard/                 # Dashboard module backup
│   ├── app.py
│   ├── utils.py
│   └── pages/
│
├── scraper/                   # Playwright scraping scripts
│   ├── constants.py
│   ├── fifa_scraper.py
│   ├── main.py
│   └── parser.py
│
└── src/                       # Machine Learning Pipeline
    ├── preprocessing.py
    ├── feature_engineering.py
    ├── cluster.py
    └── similarity.py
```

---

## Installation & Local Execution

### 1. Clone the repository

```bash
git clone https://github.com/your-username/FIFA-WorldCup-2026-Player-Analytics.git
cd FIFA-WorldCup-2026-Player-Analytics
```

### 2. Create and activate a virtual environment

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Dashboard

```bash
streamlit run app.py
```

---

## Deployment on Streamlit Community Cloud

1. Push this repository to GitHub.
2. Log in to [Streamlit Community Cloud](https://streamlit.io/cloud).
3. Click **New App** and select your repository.
4. Set the **Main file path** to: `app.py`.
5. Click **Deploy!**

---

## License

This project is licensed under the MIT License.
