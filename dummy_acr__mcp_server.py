from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
import httpx

mcp = FastMCP("AutoCodeReview")

ACR_BASE_URL = "https://acr.com/api/v1"
ACR_TOKEN = "your-secure-auth-token"  # ideally use os.getenv()

# Raw API call to submit code for review
@mcp.tool()
def fetch_raw_review(email_id: str, code: str, language: str) -> str:
    try:
        response = httpx.post(
            f"{ACR_BASE_URL}/review",
            headers={"Authorization": f"Bearer {ACR_TOKEN}"},
            json={
                "email_id": email_id,
                "code": code,
                "language": language
            }
        )
        response.raise_for_status()
        return response.text  # return raw text for formatting
    except Exception as e:
        return f"Error: {str(e)}"



# Tool: Submit code for review and get a formatted report
@mcp.tool()
def review_code_formatted(email_id: str, code: str, language: str) -> str:
    """Submit code for review and receive a formatted report"""
    raw_review = fetch_raw_review(email_id, code, language)
    if raw_review.startswith("Error:"):
        return raw_review
    return format_review_prompt(raw_review)

# Tool: Fetch past reports
@mcp.tool()
def get_review_reports(email_id: str) -> str:
    """Get past review reports"""
    try:
        response = httpx.post(
            f"{ACR_BASE_URL}/reports",
            headers={"Authorization": f"Bearer {ACR_TOKEN}"},
            json={"email_id": email_id}
        )
        response.raise_for_status()
        return f"Review Reports: {response.json()}"
    except Exception as e:
        return f"Error fetching reports: {str(e)}"

# Greeting
@mcp.resource("greeting://{name}")
def greet(name: str) -> str:
    return f"Hi {name}, welcome to Auto Code Review service!"
# Prompt to format raw review report
@mcp.prompt()
def format_review_prompt(raw_output: str) -> list[base.Message]:
    return [
        base.SystemMessage("You are a professional code review formatter. You make reports concise, professional, and easy to follow."),
        base.UserMessage("Format the following raw review into a clean, readable report. Use bullet points and organize into Summary, Issues Found, and Recommendations."),
        base.AssistantMessage(raw_output)
    ]

if __name__ == "__main__":
    mcp.run()
