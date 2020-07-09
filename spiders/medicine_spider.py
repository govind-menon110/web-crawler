#Generates the Therapeutic Classes Links (Step 1)
import scrapy


class MedicineSpiderSpider(scrapy.Spider):
    name = 'medicine-spider'
    allowed_domains = ['1mg.com']
    start_urls = ['https://1mg.com/drugs-therapeutic-classes/']

    def parse(self, response):
        urls = {}
        #for url in response.xpath('//div[@class="style__flex-row___1vK-y style__space-between___1cbZa style__sub-category-list___1fdTE"]//div/div'):
        for url in response.css('.style__sub-category___2354n'):
            urls[url.xpath('.//a/text()').extract_first()] = url.xpath('.//a/@href').extract_first()
        yield urls
