# Football Fan Sentiment Analysis

This project aims to analyze the sentiment of football fans based on comments fetched from Reddit. It uses a combination of web scraping, translation, and sentiment analysis to process and evaluate the comments.

## Project Structure

- `main.py`: The main script that orchestrates the reading of comments, language detection, translation (if necessary), and sentiment analysis.
- `model.py`: Contains the "RoBerta" pre-trained model for sentiment analysis and preprocessing functions.
- `translator.py`: Handles the translation of comments to English using Google Translate API.
- `scraper.py`: Fetches Reddit posts and comments using the PRAW library.
- `config.ini`: Configuration file containing Reddit API credentials.

## How It Works

1. **Scraping Reddit**: The `scraper.py` script fetches posts and comments from specified subreddits using the Reddit API and save them to a JSON file.
2. **Reading Comments**: The `main.py` script reads the fetched comments from the pre-saved JSON file.
3. **Language Detection and Translation**: Comments are translated to English if they are not in a language supported by the sentiment analysis model.
4. **Sentiment Analysis**: The sentiment of each comment is predicted using a pre-trained RoBERTa model.

## Requirements

- Python 3.6+
- `transformers` library
- `praw` library
- `googletrans` library

## Running the Project

1. Ensure you have the required libraries installed.
2. Update the `config.ini` file with your Reddit API credentials.
3. Run the `scraper.py` script to fetch Reddit comments.
4. Run the `main.py` script to perform sentiment analysis on the fetched comments.

## License

This project is licensed under the MIT License.