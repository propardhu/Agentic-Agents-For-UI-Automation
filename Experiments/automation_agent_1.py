import os
from pathlib import Path
from datetime import datetime

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_sync_playwright_browser
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import Tool

# 🔑 OpenAI Key
os.environ["OPENAI_API_KEY"] = ""

# 📥 Load task from txt file
with open("task.txt", "r") as f:
    user_task = f.read().strip()

# 🌐 Playwright browser & toolkit
browser = create_sync_playwright_browser(headless=False)
toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=browser)
playwright_tools = toolkit.get_tools()

# 🔍 Filtered DuckDuckGo tool to avoid Amazon.com

def filtered_search(query):
    results = DuckDuckGoSearchRun().run(query)
    if isinstance(results, str):
        return results
    return "\n".join([r for r in results.split("\n") if "amazon.com" not in r.lower()])

search_tool = Tool(
    name="DuckDuckGoFilteredSearch",
    func=filtered_search,
    description="Search the web for relevant information, excluding Amazon links."
)

# 🔧 Combine tools
tools = [search_tool] + playwright_tools

# 🧠 LLM Setup
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# ✅ Prompt Template with agent_scratchpad
prompt = PromptTemplate.from_template(
    """You are a smart browser automation assistant. Your job is to help the user complete browser tasks using available tools.

Use DuckDuckGoFilteredSearch to find relevant pages. Avoid defaulting to a specific website unless specified.

User's task: {input}

{agent_scratchpad}"""
)

# 🤖 Create the agent
agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=prompt)

# ⚙️ Agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 📸 Screenshot directory
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
Path(f"screenshots/{timestamp}").mkdir(parents=True, exist_ok=True)

# 🚀 Execute the task
agent_executor.invoke({"input": user_task})
