import scrapy


class SfulakezaSpider(scrapy.Spider):
    name = "sfulakeza"
    allowed_domains = ["comet.lehman.cuny.edu"]
    start_urls = ["http://comet.lehman.cuny.edu/sfulakeza/su21/ttp/slides/"]

    def parse(self, response):
        item = {}
        ul_html = response.xpath('//ul/li')
        hrefs = ul_html.css('a::attr(href)').getall()
        #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        #item["name"] = response.xpath('//div[@id="name"]').get()
        #item["description"] = response.xpath('//div[@id="description"]').get()
        print(f"xxxxx hrefs: {hrefs}")
        return item
