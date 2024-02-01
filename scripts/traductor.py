import re
from googletrans import Translator
import os
import json

def file_translate(input_file, output_file, final_language):
    translator = Translator()

    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    translations = []

    for line in lines:
        match = re.match(r"(\$string\['[^']+'] = ')([^']*)';", line)
        if match:
            prefix, value = match.groups()
            try:
                text_translate = translator.translate(value.strip(), dest=final_language).text
            except Exception as e:
                print(f"Error during translation: {e}")
                text_translate = value.strip()
            translate = f"{prefix}{text_translate}';\n"
            translations.append(translate)
            print(f"Translated: {line.strip()} -> {translate.strip()}")
        else:
            translations.append(line)

    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(translations)

if __name__ == "__main__":
    input_txt = os.path.join(os.path.dirname(__file__), "str-eng.txt")
    output_txt = "str-cat.txt"

    # idioma al que se quiere traducir
    target_language = "ca"

    print("Translating...")
    file_translate(input_txt, output_txt, target_language)
    print("Translation complete.")
