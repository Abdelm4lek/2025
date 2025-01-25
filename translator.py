from googletrans import Translator

translator = Translator()

def translate_text(original_text: str, target_language: str = 'en') -> str:
    translation = translator.translate(original_text, dest=target_language)
    translated_text, original_language = translation.text, translation.src
    return translated_text, original_language