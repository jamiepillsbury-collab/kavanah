# Headless test of Explore lessons (cloud only: needs Playwright). Copy app files to /tmp/site, set TITLES, run.
import asyncio, subprocess, sys, time
from playwright.async_api import async_playwright
TITLES = ["Jonah (1): Running away", "Jonah (2): Inside the fish", "Jonah (3): What God saw", "Jonah (4): The plant and the question"]
async def run_lesson(p, title, errs):
    pg = await p.new_page(viewport={"width": 390, "height": 844})
    pg.on("pageerror", lambda e: errs.append(f"{title}: {e}"))
    await pg.route("**/*googleapis*", lambda r: r.abort())
    await pg.goto("http://localhost:8765/index.html", wait_until="domcontentloaded")
    await pg.wait_for_timeout(1200); await pg.click("[data-tab=explore]"); await pg.wait_for_selector("button.lesson")
    await pg.evaluate("document.querySelectorAll('details').forEach(d=>d.open=true)")
    await pg.locator("button.lesson", has_text=title).first.click()
    steps = 0
    for steps in range(80):
        await pg.wait_for_timeout(120)
        opts = pg.locator(".opt:visible")
        chk = pg.locator("button.primary:visible", has_text="Check")
        if await chk.count():
            if await opts.count(): await opts.nth(steps % await opts.count()).click()
            else:
                while await pg.locator(".chip:visible").count() and await chk.first.is_disabled():
                    chips = pg.locator(".chip:not(.sure):visible"); n = await chips.count()
                    await chips.nth(n - 1).click()
            await chk.first.click(); await pg.wait_for_timeout(100)
            await pg.locator("button.primary:visible", has_text="Continue").first.click(); continue
        done = pg.locator("button.primary:visible", has_text="Done")
        if await done.count(): await done.first.click(); await pg.close(); return f"{title}: Done ({steps} steps)"
        nxt = pg.locator("button.primary:visible", has_text="Next")
        if await nxt.count(): await nxt.first.click(); continue
        cont = pg.locator("button.primary:visible", has_text="Continue")
        if await cont.count(): await cont.first.click(); continue
        await pg.close(); return f"{title}: STUCK at step {steps}: " + (await pg.inner_text("body"))[:300]
    await pg.close(); return f"{title}: did not finish"
async def main():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", "8765", "-d", "/tmp/site"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    errs = []
    try:
        async with async_playwright() as pw:
            b = await pw.chromium.launch()
            for t in TITLES: print(await run_lesson(b, t, errs))
            await b.close()
    finally: srv.terminate()
    print("JS errors:", errs or "none")
asyncio.run(main())
