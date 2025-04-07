from playwright.sync_api import sync_playwright
def execute_actions(actions, screenshot_dir="screenshots", headless=False):
    # path(screenshot_dir).mkdir(parents=True, exist_ok=True)

    p = sync_playwright().start()
    browser = p.chromium.launch(headless=headless)
    page = browser.new_page()

    for idx, action in enumerate(actions, 1):
        action_type = action.get("type")
        try:
            print(f"🚀 Step {idx}: {action_type}")

            if action_type == "goto":
                page.goto(action["url"])

            elif action_type == "wait":
                seconds = float(action["time"])
                print(f"⏱ Waiting for {seconds} seconds")
                time.sleep(seconds)

            elif action_type == "fill":
                selector = action["selector"]
                text = action["text"]
                print(f"📝 Clicking & Typing '{text}' in {selector}")
                page.locator(selector).click()
                page.locator(selector).fill("")  # clear if needed
                page.type(selector, text, delay=50)  # mimics real typing

            elif action_type == "press":
                key = action["key"]
                print(f"⌨️ Pressing key '{key}' on focused element")
                # Press key on last focused input or best guess (Google example)
                page.locator("input[name='q']").press(key)

            elif action_type == "click":
                print(f"🖱 Clicking on '{action['selector']}'")
                page.click(action["selector"])

            elif action_type == "screenshot":
                # path = path(screenshot_dir) / action["path"]
                # page.screenshot(path=str(path), full_page=action.get("fullPage", False))
                print(f"📸 Manual Screenshot saved: ")
                continue

            else:
                print(f"⚠️ Unsupported action type: {action_type}")

            # 📸 Screenshot for every step
            # shot_path = path(screenshot_dir) / f"step_{idx}_{action_type}.png"
            # page.screenshot(path=str(shot_path), full_page=True)
            print(f"📸 Screenshot saved: ")

        except Exception as e:
            print(f"❌ Error at step {idx} ({action_type}): {e}")

    browser.close()
    p.stop()


actions = [
    {'type': 'goto', 'url': 'https://www.google.com'},
    {'type': 'wait', 'time': 2},
    {'type': 'fill', 'selector': "input[name='q']", 'text': 'partha sai guttikonda'},
    {'type': 'press', 'key': 'Enter'},
    {'type': 'wait', 'time': 3},
    {'type': 'click', 'selector': 'h3'}
]

execute_actions(actions, screenshot_dir="screenshots/google_test", headless=False)