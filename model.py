import os, re
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig


MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
ROBERTA_SUPPORTED_LANGUAGES = ('ar', 'en', 'fr', 'de', 'hi', 'it', 'es', 'pt')


if not os.path.exists(MODEL):
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)
    model.save_pretrained(MODEL)
    tokenizer.save_pretrained(MODEL)
else:
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)


# Preprocess text (username and link placeholders)
def preprocess(text):
    # Replace usernames
    text = re.sub(r'@\w+', '@user', text)
    # Replace links
    text = re.sub(r'http\S+', 'http', text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def predict_sentiment(text: str) -> str:
    if not text or text.isspace():
        return "Invalid input: Text is empty or contains only spaces."
    
    processed_text = preprocess(text)
    encoded_input = tokenizer(processed_text, return_tensors='pt')
    output = model(**encoded_input)
    index_of_sentiment = output.logits.argmax().item()
    sentiment = config.id2label[index_of_sentiment]
    return sentiment