import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient


async def main():
    # Load environment variables
    load_dotenv()

    # Create MCPClient from config file
    client = MCPClient.from_config_file(os.path.join(os.path.dirname(__file__), "browser_mcp.json"))

    # Create LLM
    llm = ChatOpenAI(model="o4-mini")

    # Create agent with the client
    agent = MCPAgent(llm=llm, client=client, max_steps=30, verbose=True)

    # Run the query
    result = await agent.run(
        """
        Navigate to https://github.com/mcp-use/mcp-use, got to list of issues.
        """,
        max_steps=30,
    )
    print(f"\nResult: {result}")


if __name__ == "__main__":
    # Run the appropriate example
    asyncio.run(main())
