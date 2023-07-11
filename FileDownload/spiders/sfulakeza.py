import scrapy

from FileDownload.items import FiledownloadItem

class SfulakezaSpider(scrapy.Spider):
    name = "sfulakeza"
    allowed_domains = ["comet.lehman.cuny.edu"]
    start_urls = ["http://comet.lehman.cuny.edu/sfulakeza/su21/ttp/slides/"]

    def parse(self, response):
        hrefs = response.xpath('//ul/li').css('a::attr(href)').getall()
        for hrefPath in hrefs:
            if 'Parent%20Directory' not in hrefPath:    # 过滤父级文件夹
                new_file_path = response.urljoin(hrefPath)
                fileItem = FiledownloadItem()
                fileItem['file_urls'] = [new_file_path]
                fileItem['original_file_name'] = new_file_path.split('/')[-1]
                yield fileItem