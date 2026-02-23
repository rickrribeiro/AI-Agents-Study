import os
from time import sleep
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

language = "spanish"
# file_extension = ".po"
file_extension = ".json"

SYSTEM_PROMPT = (
    f"Fill this i18n file with the translations in {language}. "
    "You must return the entire file content filled. "
    "Dont return anything else."
)

def generate_response(file_content: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": file_content},
    ]

    response = completion(
        model="gemini/gemini-3-flash-preview",
        messages=messages
    )

    return response.choices[0].message.content


def process_json_files(folder="."):
    for filename in os.listdir(folder):
        if filename.endswith(file_extension):
            path = os.path.join(folder, filename)
            print(f"Processando {filename}")

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            translated_content = generate_response(content)

            with open(path, "w", encoding="utf-8") as f:
                f.write(translated_content)

            print(f"{filename} atualizado\n")
            sleep(30)

if __name__ == "__main__":
    process_json_files()
