from pathlib import Path

from langchain_core.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get the weather for a given city."""

    print(f"Getting weather for {city}...")
    return f"The weather in {city} is 32."


@tool
def get_product_index() -> str:
    """Return the product guide index so the LLM can decide which markdown file is relevant."""

    index_path = Path(__file__).resolve().parent / "index.md"
    if not index_path.exists():
        return "No product index file was found."

    return index_path.read_text(encoding="utf-8")


@tool
def get_product_doc_content(file_name: str) -> str:
    """Read the contents of a product markdown file using its file name, such as 01-overview.md."""

    if not file_name or not file_name.strip():
        return "Please provide a markdown file name."

    name = file_name.strip()
    if not name.endswith(".md"):
        name = f"{name}.md"

    if Path(name).name != name:
        return "Invalid file name. Use a file name from the product index."

    doc_path = Path(__file__).resolve().parent / "product" / name
    if not doc_path.exists():
        available_files = ", ".join(sorted(p.name for p in (Path(__file__).resolve().parent / "product").glob("*.md")))
        return f"Markdown file '{name}' was not found. Available files: {available_files}"

    return doc_path.read_text(encoding="utf-8")
