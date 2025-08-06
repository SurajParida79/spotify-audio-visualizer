# Spotify Audio Features Visualizer 🎵📊

A Python project that fetches your top tracks from Spotify and visualizes their audio features (danceability, energy, tempo, valence). Built using mock data to simulate Spotify’s `/audio-features` endpoint due to API limitations.

## Features
- Spotify Authorization Code flow (refresh tokens used securely)
- Retrieves and displays top 5 tracks
- Visualizes mock audio features using Matplotlib

## Tech Stack
- Python
- `requests`, `dotenv`, `matplotlib`
- Mock data for offline development

## Prerequisites
Make sure you have the following installed:

Python 3.8+

Git

pip

## How to Run
1. Clone the repo:

Open a terminal in the folder where you want to store the project, then run:

git clone https://github.com/yourusername/spotify-audio-features-visualizer.git

cd spotify-audio-features-visualizer

Replace 'yourusername' with your actual GitHub username.

2. Set up the environment:

Install the required packages:

pip install -r requirements.txt

3. Set up `.env` file based on `.env.example`
   
4. Run the script:

   
python main.py

## Notes
- API token scopes must include: `user-top-read`
- Due to Spotify API restrictions, this demo uses mock data for audio features
- Real audio features can be added by upgrading your Spotify developer account

## License
MIT
