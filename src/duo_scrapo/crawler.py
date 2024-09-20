import asyncio
from datetime import timedelta
import os
import re

from anyio import sleep
from crawlee import ConcurrencySettings
from crawlee.playwright_crawler import PlaywrightCrawler, PlaywrightCrawlingContext
from crawlee.sessions import SessionPool
from crawlee.configuration import Configuration


INITIAL_URL = 'https://www.duolingo.com/learn'

async def main() -> None:
    username = os.getenv('DUOLINGO_USERNAME')
    if not username:
        raise Exception('Need username')

    password = os.getenv('DUOLINGO_PASSWORD')
    if not password:
        raise Exception('Need password')

    crawler = PlaywrightCrawler(
        # Limit the crawl to max requests. Remove or increase it for crawling all links.
        max_requests_per_crawl=2,
        # Headless mode, set to False to see the browser in action.
        headless=False,
        # Browser types supported by Playwright.
        browser_type='chromium',
        concurrency_settings=ConcurrencySettings(max_concurrency=1, desired_concurrency=1, min_concurrency=1),
        session_pool=SessionPool(max_pool_size=1),
        use_session_pool=True,
        request_handler_timeout=timedelta(minutes=10),
        configuration=Configuration(internal_timeout=timedelta(minutes=10)),
    )

    async def is_logged_in(context: PlaywrightCrawlingContext):
        button = await context.page.main_frame.query_selector('button[data-test="have-account"]')
        return button is None

    async def login(context: PlaywrightCrawlingContext):
        button = await context.page.main_frame.query_selector('button[data-test="have-account"]')
        if button is not None:
            await button.click()

            email_input = await context.page.query_selector('input[data-test="email-input"]')
            password_input = await context.page.query_selector('input[data-test="password-input"]')
            login_button = await context.page.query_selector('button[data-test="register-button"]')

            if email_input is not None and password_input is not None and login_button is not None:
                await email_input.fill(username)
                await sleep(1)
                await password_input.fill(password)
                await sleep(1.2)
                await login_button.click()


    async def navigate_to_practice(context: PlaywrightCrawlingContext):
        practice_button = context.page.locator('a[data-test="practice-hub-nav"]')
        await practice_button.wait_for()
        await practice_button.click()

        words_button = context.page.locator('button[data-test="practice-hub-collection-button"]', has=context.page.locator('span', has_text='Words'))
        await words_button.wait_for()
        await words_button.click()

    async def get_total_words(context: PlaywrightCrawlingContext) -> int | None:
        total_words: int | None = None

        total_words_pattern = re.compile(r'(\d+)\s+words', re.IGNORECASE)
        total_words_text = await (await context.page.locator('h2', has_text=total_words_pattern).element_handle()).text_content()

        if total_words_text is not None:
            match = total_words_pattern.match(total_words_text)
            if match is not None:
                total_words = int(match[1])

        return total_words


    # Define the default request handler, which will be called for every request.
    # The handler receives a context parameter, providing various properties and
    # helper methods. Here are a few key ones we use for demonstration:
    # - request: an instance of the Request class containing details such as the URL
    #   being crawled and the HTTP method used.
    # - page: Playwright's Page object, which allows interaction with the web page
    #   (see https://playwright.dev/python/docs/api/class-page for more details).
    @crawler.router.default_handler
    async def request_handler(context: PlaywrightCrawlingContext) -> None: # type: ignore
        context.log.info(f'Processing {context.request.url} ...')

        if not await is_logged_in(context):
            await login(context)

        await navigate_to_practice(context)

        section = await context.page.locator('section').filter(has=context.page.get_by_text('Recently learned')).element_handle()

        total_words = await get_total_words(context)
        displayed_words = 0

        if total_words is None:
            raise Exception(f"Wtf {total_words}")

        print("total_words", total_words)

        data: list[dict[str, str | None]]= []

        while displayed_words < total_words:
            try:
                load_more = await context.page.locator('li[role=button]').filter(has=context.page.get_by_text('Load more')).element_handle()
                await load_more.scroll_into_view_if_needed()
                await load_more.click()
                await sleep(1)
                displayed_words = len(await section.query_selector_all('ul li'))
            except:
                break

        list_items = await section.query_selector_all('ul li>div')
        for list_item in list_items:
            await list_item.scroll_into_view_if_needed()
            word = await list_item.query_selector('h3')
            definition = await list_item.query_selector('p')
            if word is not None and definition is not None:
                data.append({
                    'word': await word.text_content(),
                    'definition': await definition.text_content(),
                })

        await context.push_data(data)

    # Run the crawler with the initial list of URLs.
    await crawler.run([INITIAL_URL])
    await crawler.export_data('results.json')


def crawl():
    asyncio.run(main())
