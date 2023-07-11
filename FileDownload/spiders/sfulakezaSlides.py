import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from FileDownload.items import FiledownloadItem


class SfulakezaslidesSpider(CrawlSpider):
    name = "sfulakezaSlides"
    allowed_domains = ["comet.lehman.cuny.edu"]
    start_urls = ["http://comet.lehman.cuny.edu/sfulakeza/su21/ttp/slides/"]

    rules = (
        Rule(LinkExtractor(allow=(r"sfulakeza/su21/ttp/slides/"), deny=(r"/Parent Directory"),),
        callback="parse_item",
        follow=True),
    )

    def parse_item(self, response):
        hrefs = response.xpath('//ul/li').css('a::attr(href)').getall()
        for hrefPath in hrefs:
            if 'Parent%20Directory' not in hrefPath:    # 过滤父级文件夹
                new_file_path = response.urljoin(hrefPath)
                fileItem = FiledownloadItem()
                fileItem['file_urls'] = [new_file_path]
                fileItem['original_file_name'] = new_file_path.split('/')[-1]
                yield fileItem