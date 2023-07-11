# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os
import scrapy

from scrapy.pipelines.files import FilesPipeline
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem

class FiledownloadPipeline:
    def process_item(self, item, spider):
        return item

class SliderPipeline(FilesPipeline):

    # 对空目录对文件类型进行筛选下载
    def get_media_requests(self, item, info):
        for file_url in item['file_urls']:
            print(f"file_url in item {file_url}")
            relative_url_path = file_url.split('sfulakeza/su21/ttp/slides/')[-1].replace("%20", "_") # 替换%20(空格)为下划线
            if relative_url_path.endswith('/'):
                # 当前是目录，只创建目录，无文件下载
                settings = get_project_settings()
                storage = settings.get('FILES_STORE')
                dir_path = os.path.join(storage, relative_url_path)
                if not os.path.exists(dir_path):
                    print(f"创建目录: {dir_path}")
                    os.makedirs(dir_path)
            else:
                # 是文件
                file_extension = relative_url_path.split('.')[-1]
                # 对文件类型进行筛选下载
                print(f"下载文件 {relative_url_path}")
                if file_extension in ('pdf', 'ppt', 'docx', 'doc', 'md'):
                    yield scrapy.Request(file_url)

    def file_path(self, request, response=None, info=None):
        # 方案一 直接配置下载目录及文件名称
        relative_url_path = request.url.split('sfulakeza/su21/ttp/slides/')[-1].replace("%20", "_") # 替换%20(空格)为下划线
        return relative_url_path

        # 方案二 先文件名称，结合方法def item_completed(self, results, item, info):进行文件移动操作
        # file_name: str = request.url.split("/")[-1].replace("%20", "_")
        # return file_name

    # def item_completed(self, results, item, info):
    #     for result in [x for ok, x in results if ok]:
    #         url_heritage_path = result['url'].split('sfulakeza/su21/ttp/slides/')[-1].replace("%20", "_")
    #         path = result['path'].replace("%20", "_")
    #         path_basename = os.path.basename(path).replace("%20", "_")
    #
    #         # path: Group_Project_1_ - _Fullstack_CRUD_Application_Summer_2019.docx
    #         # url_heritage_path: project/Group_Project_1_-_Fullstack_CRUD_Application_Summer_2019.docx
    #         # path_basename: Group_Project_1_-_Fullstack_CRUD_Application_Summer_2019.docx
    #
    #         target_dir_path = ""
    #         if '/' in url_heritage_path:
    #             target_dir_path = os.path.dirname(url_heritage_path)
    #             # target_dir_path: project
    #
    #         settings = get_project_settings()
    #         storage = settings.get('FILES_STORE')
    #
    #
    #         target_path = os.path.join(storage, target_dir_path, path_basename)
    #         # target_path: downloads/project/Group_Project_1_-_Fullstack_CRUD_Application_Summer_2019.docx
    #         path = os.path.join(storage, path)
    #         # path: downloads/Group_Project_1_-_Fullstack_CRUD_Application_Summer_2019.docx
    #
    #         print(f"target_dir_path xxxx : {target_dir_path} storage: {storage} os.path.basename: {path_basename} target_path: {target_path}")
    #
    #         # 如果对应的目录不存在，则创建对应的目录
    #         if not os.path.exists(os.path.join(storage, target_dir_path)):
    #             os.makedirs(os.path.join(storage, target_dir_path))
    #
    #         # 将已下载的文件，移动到对应的目录
    #         if not os.rename(path, target_path):
    #             raise DropItem("Could not move file to target folder")
    #
    #     if self.FILES_RESULT_FIELD in item.fields:
    #         item[self.FILES_RESULT_FIELD] = [x for ok, x in results if ok]
    #     return item