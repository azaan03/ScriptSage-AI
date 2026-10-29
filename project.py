
import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables from .env
load_dotenv()


# Define pipeline state
class PipelineState(TypedDict):
    raw_data: str
    edited_txt: str
    script_txt: str
    final_output: str


# Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)


# Script editor node
def editor_node(state: PipelineState) -> dict:

    prompt = f"""
You are a professional script editor and proofreader.

Your task is to edit the provided script to make it clear,
grammatically correct, natural, and easy to understand.

Follow these rules carefully:

1. Correct grammar, spelling, punctuation, and sentence structure.
2. Improve clarity, readability, and flow.
3. Remove unnecessary repetition and awkward wording.
4. Preserve the original meaning, message, intent, and key details.
5. Maintain the original language and tone of the script.
6. Do not add new facts, ideas, or unsupported information.
7. Do not summarize or unnecessarily shorten the script.
8. Preserve names, dialogue, and important formatting.
9. If a sentence is already correct, do not change it without reason.
10. Return only the edited script.
    Do not include explanations, notes, or introductory text.

SCRIPT TO EDIT:
{state['raw_data']}

EDITED SCRIPT:
"""

    response = llm.invoke(prompt)

    return {
        "edited_txt": response.content.strip()
    }

def script_writer_node(state: PipelineState) -> dict:

    prompt = f"""
You are a professional scriptwriter.

Your task is to transform the edited text into a complete,
engaging, and well-structured script.

Follow these guidelines:

1. Use the edited text as the main source of information.
2. Preserve its original meaning, purpose, and key details.
3. Organize the script with a clear beginning, middle, and ending.
4. Make the writing natural, engaging, and easy to understand.
5. Use smooth transitions between ideas and sections.
6. Write natural dialogue when appropriate for the content.
7. Do not invent facts or introduce unsupported information.
8. Keep the script in the same language as the input.
9. Avoid unnecessary repetition and filler.
10. Return only the completed script without explanations,
    notes, or additional commentary.

Edited Text:
{state['edited_txt']}

Complete Script:
"""

    response = llm.invoke(prompt)

    return {
        "script_txt": response.content.strip()
    }

def translator_node(state: PipelineState) -> dict:

    target_language = "Urdu"  # Change to English, Arabic, etc.

    prompt = f"""
You are a professional translator.

Translate the provided script into {target_language}.

Follow these guidelines:

1. Preserve the original meaning, context, and intent.
2. Use natural, fluent, and grammatically correct language.
3. Preserve the tone, style, and emotions of the original script.
4. Keep names, numbers, and important details accurate.
5. Translate idioms and expressions naturally rather than literally.
6. Do not add, remove, or summarize information.
7. Preserve dialogue and formatting where possible.
8. Return only the translated script without explanations
   or additional commentary.

Script to Translate:
{state['script_txt']}

Translated Script:
"""

    response = llm.invoke(prompt)

    return {
        "final_output": response.content.strip()
    }
