"""LangChain model, LLMChain, message, and streaming helpers."""

from __future__ import annotations

from typing import Any, Dict, Iterator

from langchain.chains import LLMChain
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from .prompts import CHAT_FINANCIAL_TEMPLATE, NARRATIVE_CHAT_TEMPLATE


def build_llm(
    api_key: str,
    model_name: str = "gpt-4o-mini",
    temperature: float = 0.2,
) -> ChatOpenAI:
    """Create the OpenAI chat model."""
    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    return ChatOpenAI(
        api_key=api_key,
        model=model_name,
        temperature=temperature,
    )


def build_financial_chain(llm: ChatOpenAI) -> LLMChain:
    """Build the reusable assignment-required LLMChain."""
    return LLMChain(
        llm=llm,
        prompt=CHAT_FINANCIAL_TEMPLATE,
        verbose=False,
    )


def run_financial_chain(
    chain: LLMChain,
    inputs: Dict[str, Any],
) -> str:
    """Run the reusable LLMChain and return its text output."""
    result = chain.invoke(inputs)

    if isinstance(result, dict):
        return str(result.get("text", result))

    return str(result)


def demonstrate_messages() -> list:
    """Return raw System/Human/AI messages for viva/demo purposes.

    SystemMessage: defines assistant behavior and safety.
    HumanMessage: represents the user's request/data.
    AIMessage: represents an assistant response in a conversation.
    """
    return [
        SystemMessage(
            content="You are an educational financial analysis assistant."
        ),
        HumanMessage(
            content="Analyze my monthly budget using the supplied numbers."
        ),
        AIMessage(
            content="I can provide educational budgeting insights from the numbers supplied."
        ),
    ]


def stream_recommendations(
    llm: ChatOpenAI,
    inputs: Dict[str, Any],
) -> Iterator[str]:
    """Stream narrative recommendations from the model."""
    messages = NARRATIVE_CHAT_TEMPLATE.format_messages(**inputs)

    for chunk in llm.stream(messages):
        content = getattr(chunk, "content", "")
        if content:
            yield content
