from model import predict_sentiment, ROBERTA_SUPPORTED_LANGUAGES
from translator import translate_text
import json

def read_comments(file_path: str) -> list[dict[str, str]]:
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            data = json.load(file)
            list_of_comments = [entry["comment_body"] for entry in data]
        return list_of_comments
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON file.")
        return []


comments = read_comments("./reddit_comments.json")



sentiment_by_id = {}

for index, comment in enumerate(comments):
    comment_text = comment
    detected_language = translate_text(comment_text)[1]

    if detected_language in ROBERTA_SUPPORTED_LANGUAGES:
        sentiment = predict_sentiment(comment_text)
    else:
        translated_text = translate_text(comment_text)[0]
        sentiment = predict_sentiment(translated_text)

    sentiment_by_id[index] = sentiment


print(sentiment_by_id)
