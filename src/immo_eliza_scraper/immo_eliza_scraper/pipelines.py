# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter


class ImmoElizaScraperPipeline:
    def process_item(self, item, spider):
        return item


class ImmoElizaPipeline:
    def open_spider(self, spider):
        # Open the file in binary write mode
        self.file = open("../data/immovlan_data.csv", 'wb')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        # You can add cleaning logic here
        if not item.get('price'):
            return item # Skip items with no price
            
        self.exporter.export_item(item)
        return item