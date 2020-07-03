import json
import scrapy
import os.path


class finalspider(scrapy.Spider):
    def __init__(self):
        f = open(os.path.dirname(__file__) + '/../mgspider.json')
        spidey = json.load(f)[0]
        self.urllist = []
        for i in spidey.values():
            self.urllist.append("https://1mg.com" + i)
        self.start_urls = self.urllist

    name = 'finalspider'
    allowed_domains = ['1mg.com']

    def parse(self, response):
        Medicines = {}
        Medicines["Names List"] = response.css(".style__space-between___2mbvn div:nth-child(1)::text").extract()
        Medicines["Prescription"] = response.css(".style__font-12px___2ru_e span::text").extract()
        Medicines["Type of Sell"] = response.css(".style__font-12px___2ru_e .style__padding-bottom-5px___2NrDR:nth-child(1)::text").extract()
        Medicines["Manufacturer"] = response.css(".style__padding-bottom-5px___2NrDR+ .style__padding-bottom-5px___2NrDR::text").extract()
        Medicines["Salt"] = response.css(".style__product-content___5PFBW::text").extract()
        Medicines["Cost"] = response.css(".style__space-between___2mbvn div+ div::text").extract()
        Medicines["Therapeutic Class"] = response.css(".style__drug-list-heading___niild::text").extract()
        Medicines["Image Link"] = response.css(".style__card-image___1oz_4 img").extract()
        yield Medicines
