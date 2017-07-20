import scrapy


class ToScrapeCSSSpider(scrapy.Spider):
    """
    Attributes:
        name (str): essential attribute which specifies the name of the spider
        start_urls (list): the urls that are to be scraped

    """
    name = "toscrape-css"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        """
        Scrapy's default method that handles all the downloaded response for
        each request made

        Arguments:
            response (text): contains all data of the page and other helpful
            methods as well

        """
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").extract_first(),
                'author': quote.css("small.author::text").extract_first(),
                'tags': quote.css("div.tags > a.tag::text").extract()
            }
        # Extracting links of further pages to scrape
        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
