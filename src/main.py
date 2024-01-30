import asyncio
from playwright.async_api import async_playwright
from playwright._impl._errors import TimeoutError


class YouTubeParse:
    def __init__(self, keyword: str = 'Python'):
        self.keyword = keyword
        self.set_shorts = set()
        self.set_ids = set()

    async def click_shorts_chip(self):
        await self.page.wait_for_selector('#chip-bar', timeout=5000)
        await self.page.locator("#chip-bar").get_by_text("Shorts").click()
        await self.page.wait_for_timeout(2000)

    async def get_short_links(self):
        search_result = await self.page.query_selector("#contents.style-scope.ytd-item-section-renderer")
        links = await search_result.query_selector_all('a[href^="/shorts"]')
        short_links = [await link.get_attribute('href') for link in links]
        return short_links

    async def run(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            self.page = await context.new_page()
            await self.page.goto(f"https://www.youtube.com/results?search_query={self.keyword}")
            try:
                await self.click_shorts_chip()
                shorts_links = await self.get_short_links()
                for link in shorts_links:
                    full_url = f'https://www.youtube.com/{link}'
                    self.set_shorts.add(full_url)
                    short_id = link.split("/shorts/")[-1]
                    self.set_ids.add(short_id)
                print(len(self.set_shorts))
                print(self.set_shorts)
                print(self.set_ids)
            except TimeoutError:
                print('Shorts не найдены')


asyncio.run(YouTubeParse().run())