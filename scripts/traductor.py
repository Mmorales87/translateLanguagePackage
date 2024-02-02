import re
import os
import requests
from googletrans import Translator

SPANISH = "es"
ENGLISH = "en"
FRENCH = "fr"
GERMAN = "de"
ITALIAN = "it"
PORTUGUESE = "pt"
CATALAN = "ca"
DUTCH = "nl"
SWEDISH = "sv"
NORWEGIAN = "no"
DANISH = "da"
FINNISH = "fi"
RUSSIAN = "ru"
CHINESE = "zh"
JAPANESE = "ja"
KOREAN = "ko"
ARABIC = "ar"
HEBREW = "he"
HINDI = "hi"
TURKISH = "tr"


def translate_to_catalan(text):
    try:
        response = requests.get(
            "https://www.softcatala.org/api/traductor/translate",
            params={
                "langpair": f"spa|cat",  # Establece el par de idiomas de español a catalán
                "q": text.strip(),
            }
        )
        response.raise_for_status()
        translated_text = response.json()["responseData"]["translatedText"]
    except Exception as e:
        print(f"Error during translation: {e}")
        translated_text = text.strip()

    return translated_text


def file_translate(input_file, output_file, final_language):
    translator = Translator()

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    translations = []

    for line in lines:
        match = re.match(r"(\$string\['[^']+'] = ')([^']*)';", line)
        if match:
            prefix, value = match.groups()

            if final_language.lower() == CATALAN:
                translated_text = translate_to_catalan(value)
            else:
                # Utilizar googletrans para traducir a otros idiomas
                translated_text = translator.translate(value.strip(), dest=final_language).text

            translate = f"{prefix}{translated_text}';\n"
            translations.append(translate)
            print(f"Translated: {line.strip()} -> {translate.strip()}")
        else:
            translations.append(line)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(translations)


if __name__ == "__main__":
    input_txt = os.path.join(os.path.dirname(__file__), "workplace-esp.txt")
    output_txt = "workplace-cat.txt"

    # Idioma al que se quiere traducir
    target_language = CATALAN

    print("Translating...")
    file_translate(input_txt, output_txt, target_language)
    print(" ------- Translation complete ------- ")
