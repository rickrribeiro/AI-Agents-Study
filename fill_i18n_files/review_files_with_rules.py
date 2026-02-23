import os
from time import sleep
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

file_extensions = [".json", ".po"]

def get_system_prompt(language: str) -> str:
    return (
        f"""
Review this i18n file with the translations in {language}.

Your task is to ONLY fix translations that violate the official glossary or rules below.
Do NOT rewrite, rephrase, improve style, or change anything else.
If a translation is already correct, keep it exactly as it is.

You must return the entire file content with the errors fixed.
Do not return explanations, comments, or anything besides the final file.

--- OFFICIAL GLOSSARY ---

    Main terms:
    PT -> EN -> ES
    

    --- GENERAL RULES ---

    1. Never translate "Fit Cultural" into Spanish.
    2. Never use "test" or "tests" in English (always use "Assessment(s)").
    3. Never use "puesto" for "Vacante".
    4. English always uses "Template"; Portuguese and Spanish always use "Modelo".

    Only apply changes when a term conflicts with this glossary or rules.
    """

    )


def generate_response(file_content: str, language: str):
    system_prompt = get_system_prompt(language)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": file_content},
    ]

    response = completion(
        model="gemini/gemini-3-flash-preview",
        messages=messages
    )

    return response.choices[0].message.content


def process_po_files(folder="."):
    for filename in os.listdir(folder):
        if any(filename.endswith(ext) for ext in file_extensions):
            path = os.path.join(folder, filename)
            print(f"Processando {filename}")

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            language = "spanish" if ".es." in filename else "english"
            reviewed_content = generate_response(content, language)

            with open(path, "w", encoding="utf-8") as f:
                f.write(reviewed_content)

            print(f"{filename} atualizado\n")
            sleep(30)

if __name__ == "__main__":
    process_po_files()
