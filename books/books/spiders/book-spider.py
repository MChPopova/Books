import scrapy

class AuthorSpider(scrapy.Spider):
    name = 'book'

    start_urls = ['http://books.toscrape.com']

    def parse(self, response):
        yield from response.follow_all(css='ul.nav ul li a::attr(href)', callback=self.parse_category)

    
    def parse_category(self, response):
        for book in response.css('article.product_pod'):
            yield{
                "title":book.css('h3 a::attr(title)').get(),
                "price":book.css('div.product_price p.price_color::text').get(),
                "image url":response.urljoin(book.css('div.image_container a img::attr(src)').get()),
                "details url":response.urljoin(book.css('h3 a::attr(href)').get()),
            }
            
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_category)