import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END


# Load environment variables
load_dotenv()


# Define pipeline state
class PipelineState(TypedDict):
    raw_data: str
    edited_txt: str
    script_txt: str
    final_output: str


# Initialize Groq LLM
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Please add it to your .env file."
    )

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3,
    api_key=api_key,
)


# Node 1: Edit and proofread the source text
def editor_node(state: PipelineState) -> dict:
    prompt = f"""
You are a professional text editor.

Rules:
1. Fix grammar, spelling, punctuation, and sentence structure.
2. Preserve the original meaning and language.
3. Do not add new facts or ideas.
4. Do not summarize or unnecessarily shorten the text.
5. Return only the corrected text.

SOURCE TEXT:
{state['raw_data']}
"""

    response = llm.invoke(prompt)
    return {"edited_txt": response.content.strip()}


# Node 2: Create a short and relevant Hinglish script
def script_writer_node(state: PipelineState) -> dict:
    prompt = f"""
You are a professional short-video scriptwriter.

Convert the source text into an engaging Hinglish script.

STRICT RULES:
1. Aim for 50-80 words when the source supports it.
2. Use only information supported by the source text.
3. Do not invent facts, statistics, examples, or claims.
4. Preserve the main message of the source.
5. Start with a short, engaging hook.
6. Use simple, natural, conversational Hinglish.
7. Write Hindi/Urdu words using English letters only.
8. Keep common English technical terms where appropriate.
9. Use proper grammar, punctuation, and word spacing.
10. Avoid repetition and unnecessary filler.
11. If the source is short, do not add unsupported information
    just to reach the word limit.
12. Return only the script.

SOURCE TEXT:
{state['edited_txt']}
"""

    response = llm.invoke(prompt)
    return {"script_txt": response.content.strip()}


# Node 3: Polish the final Hinglish script
def translator_node(state: PipelineState) -> dict:
    prompt = f"""
You are a professional Hinglish script editor.

Polish the script so it sounds natural when spoken aloud.

Rules:
1. Use conversational Hinglish in English letters only.
2. Do not use Urdu or Devanagari script.
3. Preserve the original meaning and information.
4. Do not add examples, facts, or new ideas.
5. Correct grammar, spelling, punctuation, and spacing.
6. Never merge separate words.
7. Keep common English technical terms where natural.
8. Keep the script concise.
9. Return only the final script.

SCRIPT:
{state['script_txt']}
"""

    response = llm.invoke(prompt)
    return {"final_output": response.content.strip()}


# Build the LangGraph pipeline
graph_builder = StateGraph(PipelineState)

graph_builder.add_node("editor", editor_node)
graph_builder.add_node("script_writer", script_writer_node)
graph_builder.add_node("translator", translator_node)

graph_builder.add_edge(START, "editor")
graph_builder.add_edge("editor", "script_writer")
graph_builder.add_edge("script_writer", "translator")
graph_builder.add_edge("translator", END)

# Compile the graph
app = graph_builder.compile()


# Execute the pipeline
if __name__ == "__main__":
    source_text = """
Artificial intelligence is changing the world.
It helps people solve problems and makes work easier.
In the future, AI will become even more important.
"""

    initial_state: PipelineState = {
        "raw_data": source_text.strip(),
        "edited_txt": "",
        "script_txt": "",
        "final_output": "",
    }

    try:
        result = app.invoke(initial_state)

        print("\n" + "=" * 55)
        print("1. EDITED TEXT")
        print("=" * 55)
        print(result["edited_txt"])

        print("\n" + "=" * 55)
        print("2. SHORT HINGLISH SCRIPT")
        print("=" * 55)
        print(result["script_txt"])

        print("\n" + "=" * 55)
        print("3. FINAL HINGLISH SCRIPT")
        print("=" * 55)
        print(result["final_output"])

    except Exception as error:
        print(f"\nPipeline error: {error}")

