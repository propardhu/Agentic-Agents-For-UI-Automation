import os
from pathlib import Path
from datetime import datetime

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_sync_playwright_browser
from langchain_community.tools.playwright.extractors import ExtractTextTool, ExtractHyperlinksTool, ExtractHTMLTool

# 🔑 OpenAI Key
os.environ["OPENAI_API_KEY"] = "sk-your-openai-key"

# 📅 Load task from txt file
with open("task.txt", "r") as f:
    user_task = f.read().strip()

# 🌐 Playwright browser & toolkit
browser = create_sync_playwright_browser(headless=False)
toolkit = PlayWrightBrowserToolkit.from_browser(sync_browser=browser)

# 🛠️ Tools (browser automation + content extraction)
tools = toolkit.get_tools() + [
    ExtractTextTool(browser=browser),
    ExtractHyperlinksTool(browser=browser),
    ExtractHTMLTool(browser=browser)
]

# 🧠 LLM Setup
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 🦾 Enhanced Prompt
prompt = PromptTemplate.from_template(
    """
You are a smart browser automation assistant. Begin by navigating to the page and extracting the complete HTML structure using the HTML extraction tool.
Use that HTML to reason about selectors. Never guess selectors.
Then perform any required actions like clicking, typing, or pressing keys.

User Task: {input}

{agent_scratchpad}
"""
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
