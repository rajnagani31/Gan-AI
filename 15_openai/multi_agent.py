from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


def review_pull_request(diff: str) -> str:
    response = client.beta.responses.create(
        model="gpt-5.6-sol",
        input=(
            "Review the pull-request diff below with three agents: one for "
            "correctness, one for security, and one for missing tests. "
            "Reconcile duplicate or conflicting findings, then return a "
            "prioritized review with file and line references.\n\n"
            f"<diff>\n{diff}\n</diff>"
        ),
        multi_agent={
            "enabled": True,
            "max_concurrent_subagents": 3,
        },
        betas=["responses_multi_agent=v1"],
    )

    return "".join(
        part.text
        for item in response.output
        if (
            item.type == "message"
            and item.agent is not None
            and item.agent.agent_name == "/root"
            and item.phase == "final_answer"
        )
        for part in item.content
        if part.type == "output_text"
    )