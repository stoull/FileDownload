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
        print(f"xxxxx hrefs: {hrefs}")
        for hrefPath in hrefs:
            file_extension = hrefPath.split('.')[-1]
            if file_extension in ('pdf', 'ppt', 'docx', 'doc', '.md'):
                new_file_path = response.urljoin(hrefPath)
                fileItem = FiledownloadItem()
                fileItem.file_urls = [new_file_path]
                yield fileItem
            else:
                return


            # if '/' not in hrefPath:
            #     # is not a directory
            #     print(f"hrefPath : {hrefPath} is not a directory")
            # else:
            #     # is a directory
            #     print(f"hrefPath : {hrefPath} is a directory")
