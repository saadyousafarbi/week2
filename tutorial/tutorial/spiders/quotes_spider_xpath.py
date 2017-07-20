import scrapy


class Quotes(scrapy.Spider):
    """
    Attributes:
        name (str): essential attribute which specifies the name of the spider
        start_urls (list): the urls that are to be scraped

    """
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        """
        Scrapy's default method that handles all the downloaded response for
        each request made

        Arguments:
            response (text): contains all data of the page and other helpful
            methods as well

        """
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('.//span[@class="text"]/text()').extract_first(),
                'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
                'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract()
            }
        # Extracting links of further pages to scrape
        next_page_url = response.css("li.next > a::attr(href)").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
