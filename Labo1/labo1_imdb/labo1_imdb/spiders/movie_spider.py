import scrapy
from labo1_imdb.items import Movie
from scrapy_playwright.page import PageMethod

class MovieSpider(scrapy.Spider):
    name = "movie"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_page_goto_kwargs": {"wait_until": "networkidle"},
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "li.ipc-metadata-list-summary-item"),
                        PageMethod("wait_for_timeout", 1500),
                        PageMethod("evaluate", "window.scrollTo(0, document.body.scrollHeight)"),
                        PageMethod("wait_for_timeout", 1500),
                    ],
                },
            )

    def parse(self, response):
        items = response.css("li.ipc-metadata-list-summary-item")
        self.logger.info("FOUND %d items", len(items))

        for li in items:
            title = li.css("h3.ipc-title__text::text").get()
            rank = li.css('[data-testid="title-list-item-ranking"] .ipc-signpost__text::text').get()

            meta = li.css("span.cli-title-metadata-item::text").getall()
            year = meta[0] if len(meta) > 0 else None
            duration = meta[1] if len(meta) > 1 else None
            certificate_ = meta[2] if len(meta) > 2 else None

            rating = li.css('span[data-testid="ratingGroup--imdb-rating"] .ipc-rating-star--rating::text').get()
            raw_votes = "".join(li.css(
                'span[data-testid="ratingGroup--imdb-rating"] .ipc-rating-star--voteCount ::text'
            ).getall())

           
            raw_votes = raw_votes.replace("\xa0", " ").strip()
            votes = raw_votes.strip("()").strip() if raw_votes else None
            rel_url = li.css('a.ipc-title-link-wrapper::attr(href)').get()
            url = response.urljoin(rel_url) if rel_url else None

            poster = li.css("img.ipc-image::attr(src)").get()

            yield Movie(
                rank=rank,
                title=title,
                year=year,
                duration=duration,
                certificate=certificate_,
                rating=rating,
                votes=votes,
                url=url,
                poster_url=poster,
            )