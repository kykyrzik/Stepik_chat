from typing import Any

from aiogram.utils.formatting import as_section, Bold, Text


def section_builder(head: str, body: list[str]) -> dict[str, Any]:
    text = [f"{value}\n" for value in body]
    section = as_section(Bold(head), *text)
    return section.as_kwargs()
