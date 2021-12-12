# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose


def clear_price(val):
    if len(val) == 7:
        val[0] = val[0].replace(' ', '')
        val[0:2] = ['.'.join(val[0:2])]
    else:
        val[0] = val[0].replace(' ', '')
    try:
        return float(val[0])
    except:
        return val[0]


def resize_image(image=None):
    if image:
        return image.replace('w_82,h_82', 'w_600,h_600')


def clear_values(values_list):
    new = [item.replace('\n', '').strip() for item in values_list]
    return new


class LeruamerlenItem(scrapy.Item):
    _id = scrapy.Field(output_processor=TakeFirst())
    item_name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(clear_price), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field(input_processor=MapCompose(resize_image))
    desc_keys = scrapy.Field(input_processor=Compose(clear_values))
    desc_values = scrapy.Field(input_processor=Compose(clear_values))
    description = scrapy.Field()
