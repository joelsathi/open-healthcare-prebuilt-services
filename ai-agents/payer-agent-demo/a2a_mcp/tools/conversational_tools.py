import httpx
from mcp.shared._httpx_utils import create_mcp_http_client
from pydantic import Field
from utils.configs import ServerConfigs
from typing_extensions import Annotated


configs = ServerConfigs()


def get_agent_url(agent: str) -> str:
    if agent == "PolicyReviewer":
        return configs.POLICY_REVIEWER_URL
    elif agent == "MedicalReviewer":
        return configs.MEDICAL_REVIEWER_URL
    # elif agent == "PayerOrchestrator":
    #     return configs.PAYER_OCHESTRATOR_URL
    else:
        raise ValueError(f"Unknown agent: {agent}")
    

def register_tools(mcp):

    @mcp.tool(
        description=(
            "Used to send messages to Personal Policy Reviewer, and Medical Reviewer agents."
            "Use this tool when you need to send a message to one of these agents."
        )
    )
    async def send_message_to_policy_agents(
        agent: Annotated[
            str,
            Field(
                description="The agent to send the message to. Must be one of: PolicyReviewer, MedicalReviewer",
                examples=["PolicyReviewer", "MedicalReviewer"],
            ),
        ],
        conversationID: Annotated[
            str,
            Field(
                description="The unique identifier for the conversation. Autogenerate if not provided.",
                examples=["1", "2"],
            ),
        ],
        message: Annotated[str, Field(description="The message to send to the agent.")],
    ) -> dict:
        agent_url = get_agent_url(agent)
        try:
            async with create_mcp_http_client() as client:
                response = await client.post(
                    agent_url, json={"sessionId": conversationID, "message": message}
                )
                response.raise_for_status()  # Good practice to check for HTTP errors
                # FIX: Removed 'await' from the line below
                data = response.json()
                return data
        except httpx.HTTPStatusError as e:
            # Be more specific about the error
            return {"error": f"HTTP error occurred: {e.response.status_code} - {e.response.text}"}
        except Exception as e:
            return {"error": str(e)}

