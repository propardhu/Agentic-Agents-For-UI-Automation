# UI Automation Agent using Playwright MCP

This project uses the [@playwright/mcp](https://github.com/microsoft/playwright-mcp) server and mimics the functionality of the [mcp-use](https://github.com/mcp-use/mcp-use) client to automate browser tasks via Python.

---

## ✅ Features

- Automates any webpage using MCP server
- Written in **Python** using `requests`
- Supports:
  - Page navigation
  - Input typing
  - Key presses
  - Screenshot capture
  - DOM extraction

---

## 🔄 working code is in structured Approch folder.

## 🔧 Requirements

- Python 3.8+
- MCP server running locally at `http://localhost:3000` (refer this to learn how to run MCP server locally [this](https://huggingface.co/blog/lynn-mikami/microsoft-playwright-mcp))

---

## 🚀 Setup

### 1. Install Python dependencies

```bash
pip install python-dotenv langchain langchain-openai mcp-use

