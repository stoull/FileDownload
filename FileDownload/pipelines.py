# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os

from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.project import get_project_settings

from scrapy.utils.conf import closest_scrapy_cfg

class FiledownloadPipeline:
    def process_item(self, item, spider):
        return item

class SliderPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        heritage_path = request.url.split('sfulakeza/su21/ttp/slides/')[-1]
        proj_root = closest_scrapy_cfg()
        settings = get_project_settings()
        storage = settings.get('FILES_STORE')

        file_path = os.path.join(proj_root, storage, heritage_path)

        print(f"file_path xxxx : {file_path}")
        try:
            os.makedirs(file_path, exist_ok=False)
        except (TypeError, ZeroDivisionError) as error:
            print(f"error: {error}")
        else:
            print("Do nothing with errors")
        # file_name: str = heritage_path.split("/")[-1]
        return heritage_path