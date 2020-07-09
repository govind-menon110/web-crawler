#Generates Individual Medicine Links from the links given by medicine_spider in isthisall.json (Step 2)
import json
import scrapy
import os.path


class MedicineSpideyLarge(scrapy.Spider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        f = open(os.path.dirname(__file__) + '/../isthisall.json')
        spidey = json.load(f)[0]
        self.urllist = []
        self.pgno = {}
        for i in spidey.values():
            val = -1
            for p in range(0, 4):
                val = i.find('-', (val + 1))
            self.pgno[i[(val + 1):]] = int(1)
            self.urllist.append("https://1mg.com" + i + "?page=" + str(self.pgno[i[(val + 1):]]))
        self.start_urls = self.urllist

    name = 'MedicineSpideyLarge'
    allowed_domains = ['1mg.com']

    def parse(self, response):
        Medicines = {}
        if response.xpath(
                '//div[@class="style__product-card___1gbex style__card___3eL67 style__raised___3MFEA style__white-bg___10nDR style__overflow-hidden___2maTX"]'):
            Medicines["Links"] = response.xpath("//div[@class='style__product-card___1gbex style__card___3eL67 style__raised___3MFEA style__white-bg___10nDR style__overflow-hidden___2maTX']/a/@href").extract()
            current_url = response.request.url
            pos = -1
            posq = current_url.find('?')
            for p in range(0, 3):
                pos = current_url.find('/', (pos + 1))
            Medicines["Parent Link"] = current_url[pos:posq]
            Medicines["Image Links"] = response.css(".style__card-image___1oz_4 img").xpath("@src").extract()
            Medicines["Type of Sell"] = response.css(".style__font-12px___2ru_e .style__padding-bottom-5px___2NrDR:nth-child(1)::text").extract()
            Medicines["MRP"] = response.css(".style__space-between___2mbvn div+ div::text").extract()
            mrp = []
            x = Medicines["MRP"]
            for i in range(int(len(x) / 2)):
                mrp.append(str(x[2*i]) + str(x[2*i + 1]))
            Medicines["MRP"] = mrp
            yield Medicines
            pos_ = -1
            for p in range(0, 4):
                pos_ = current_url.find('-', (pos_ + 1))
            self.pgno[current_url[(pos_ + 1):posq]] += 1
            next_page_url = 'https://www.1mg.com/drugs-therapeutic-classes/drug-class-' + str(current_url[(pos_ + 1):posq]) + '?page=' + str(self.pgno[current_url[(pos_ + 1):posq]])
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            pass