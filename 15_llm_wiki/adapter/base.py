from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any


class BaseLLMAdapter(ABC):
    """Common interface implemented by every LLM provider adapter."""

    def __init__(self) -> None:
        self.system_instruction: str | None = None
        self.tools: list[dict[str, Any]] = []
        self.last_tool_calls: list[dict[str, Any]] = []

    def set_system_instruction(self, instruction: str | None) -> "BaseLLMAdapter":
        """Set the default system instruction used for future requests."""
        self.system_instruction = instruction
        return self

    def set_tools(self, tools: list[dict[str, Any]] | None) -> "BaseLLMAdapter":
        """Attach OpenAI-compatible function-tool definitions to future requests."""
        self.tools = tools or []
        return self

    def clear_tools(self) -> "BaseLLMAdapter":
        """Remove the currently attached tools."""
        self.tools = []
        return self

    @abstractmethod
    def invoke(
        self,
        prompt: str,
        system_instruction: str | None = None,
        tools: list[dict[str, Any]] | None = None,
    ) -> str:
        """Return the complete response for one user prompt."""

    @abstractmethod
    def stream(
        self,
        prompt: str,
        system_instruction: str | None = None,
        tools: list[dict[str, Any]] | None = None,
    ) -> Iterator[str]:
        """Yield response text as it is generated."""
