import os
import json
import re
import time
from pathlib import Path
from datetime import datetime

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from playwright.sync_api import sync_playwright
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import Tool
from langchain.agents import initialize_agent, AgentType


# 🔑 OpenAI Key
os.environ["OPENAI_API_KEY"] = "Place your API key here"

# 📥 Load task from txt file
with open("task.txt", "r") as f:
    user_task = f.read().strip()

# 🔎 Define DuckDuckGo tool
search_tool = Tool(
    name="DuckDuckGoSearch",
    func=DuckDuckGoSearchRun().run,
    description="Useful to find URLs or page titles before automation"
)

# 🧠 LLM Setup
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 🤖 Agent + Toolchain
agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 🔍 Prompt to convert task → JSON after optional search
conversion_prompt = PromptTemplate.from_template("""
You're a browser automation assistant. If needed, use the search tool to find the correct page or element for the task below.

Then convert the task into a **pure JSON array** of Playwright MCP `actions`.

TASK: {task}

RESPONSE FORMAT:
[
  {{ "type": "goto", "url": "..." }},
  {{ "type": "click", "selector": "..." }},
  ...
]
Pass wait time in sec like 2 sec not 2000 ms
Return only the JSON. No markdown. No explanation.
""")

chain = LLMChain(llm=llm, prompt=conversion_prompt)
final_prompt = conversion_prompt.format(task=user_task)

# Use Agent to do search + generation
search_augmented = agent.run(final_prompt)

# 🔎 Extract JSON actions
match = re.search(r"\[\s*{.*?}\s*\]", search_augmented, re.DOTALL)
if not match:
    raise ValueError("❌ Failed to extract JSON from LLM output")

actions = json.loads(match.group(0))

# 📸 Screenshot dir
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
screenshot_dir = Path(f"screenshots/{timestamp}")
screenshot_dir.mkdir(parents=True, exist_ok=True)

# ▶️ Executor
def execute_actions(actions, screenshot_dir, headless=False):
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=headless)
    page = browser.new_page()

    for idx, action in enumerate(actions, 1):
        t = action.get("type")
        try:
            if t == "goto":
                page.goto(action["url"])
            elif t == "wait":
                time.sleep(float(action["time"]))
            elif t == "click":
                page.click(action["selector"])
            elif t == "fill":
                sel, txt = action["selector"], action["text"]
                page.locator(sel).click()
                page.type(sel, txt, delay=50)
            elif t == "press":
                page.locator("input[name='q']").press(action["key"])
            elif t == "screenshot":
                path = screenshot_dir / action["path"]
                page.screenshot(path=str(path), full_page=action.get("fullPage", False))
                continue
            # 📸 Step screenshot
            path = screenshot_dir / f"step_{idx}_{t}.png"
            page.screenshot(path=str(path), full_page=True)
        except Exception as e:
            print(f"❌ Error at step {idx}: {t}: {e}")
    browser.close()
    p.stop()

# 🚀 Run
execute_actions(actions, screenshot_dir, headless=False)