# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime

class TrustpilotPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # remove whitespaces

        field_names = adapter.field_names()

        for field_name in field_names:
            all_names = adapter.get(field_name)

            adapter[field_name] = all_names.strip()

        # convert stars to integer
            
        star_rating = adapter.get("stars")

        adapter["stars"] = int(star_rating)

        # convert date experience to datetime object


        date = adapter.get("date_experience")

        adapter["date_experience"] = datetime.strptime(date, "%B %d, %Y").date()



        date_time = adapter["review_date"]

        adapter["review_date"] = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.%fz").date()

        return item