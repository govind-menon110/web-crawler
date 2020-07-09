#Scrapes all Info from Individual Medicines links given in check.json by MedicineSpideyLarge (Step 3)
import json
import scrapy
import os.path


class checkspider(scrapy.Spider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        g = open(os.path.dirname(__file__) + '/../isthisall.json')
        f = open(os.path.dirname(__file__) + '/../check.json')
        spidey = json.load(f)
        urllist = []
        self.url_to_therapy = {}
        self.url_to_img = {}
        self.url_to_mrp = {}
        self.url_to_sell = {}
        for i in spidey:
            links = i['Links']
            plink = i['Parent Link']
            img = i['Image Links']
            sell = i['Type of Sell']
            mrp = i['MRP']
            for j in links:
                listindex = links.index(j)
                self.url_to_therapy[j] = plink  ##Medicine['Therepeutic Class'] = get_key(self.url_to_therapy[j])
                self.url_to_img[j] = img[listindex]
                self.url_to_sell[j] = sell[listindex]
                self.url_to_mrp[j] = mrp[listindex]
                urllist.append("https://1mg.com" + j)
        self.start_urls = urllist
        self.referral = json.load(g)[0]

    name = 'checkspider'
    allowed_domains = ['1mg.com']

    def get_key(self, val):
        for key, value in self.referral.items():
            if val == value:
                return key

    def parse(self, response):
        Medicines = {}
        Medicines["Name"] = response.css(".DrugHeader__title___1NKLq::text").extract()
        Medicines["Prescription"] = response.css(".DrugHeader__prescription-req___34WVy span::text").extract()
        if len(Medicines["Prescription"]) < 1:
            Medicines["Prescription"] = "Not Necessary"
        current_url = response.request.url
        pos_ = -1
        for p in range(0, 3):
            pos_ = current_url.find('/', (pos_ + 1))
        Medicines["Type of Sell"] = response.css(".DrugPriceBox__quantity___2LGBX::text").extract()
        if len(Medicines["Type of Sell"]) < 1:
            Medicines["Type of Sell"] = self.url_to_sell[current_url[pos_:]]
        Medicines["Manufacturer"] = response.css(".DrugHeader__meta___B3BcU:nth-child(1) a::text").extract()
        Medicines["Salt"] = response.css(".saltInfo a::text").extract()
        if len(Medicines["Salt"]) < 1:
            Medicines["Salt"] = "N/A"
        Medicines["MRP"] = response.css(".DrugPriceBox__bestprice-slashed-price___2ANwD::text").extract()
        if len(Medicines["MRP"]) < 1:
            Medicines["MRP"] = response.css(".DrugPriceBox__price___dj2lv::text").extract()
            if len(Medicines["MRP"]) < 1:
                Medicines["MRP"] = response.css(".DrugPriceBox__slashed-price___2UGqd::text").extract()
        Medicines["Best Price"] = response.css(".DrugPriceBox__best-price___32JXw::text").extract()
        if len(Medicines["Best Price"]) < 1:
            Medicines["Best Price"] = Medicines["MRP"]
            if len(Medicines["Best Price"]) < 1:
                Medicines["MRP"] = self.url_to_mrp[current_url[pos_:]]
                Medicines["Best Price"] = self.url_to_mrp[current_url[pos_:]]
                #Medicines["MRP"] = "Product Not Sold Anymore"
                #Medicines["Best Price"] = "Product Not Sold Anymore"
        elif len(Medicines["Best Price"]) >= 1 > len(Medicines["MRP"]):
            Medicines["MRP"] = Medicines["Best Price"]
        Medicines["Uses"] = response.css("#overview a::text").extract()
        if len(Medicines["Uses"]) < 1:
            Medicines["Uses"] = response.css(".DrugOverview__uses___1jmC3 span::text").extract()
            if len(Medicines["Uses"]) < 1:
                Medicines["Uses"] = "Refer To Documentation"
        Medicines["How to Use"] = response.css(".DrugOverview__container___CqA8x:nth-child(5) .DrugOverview__content___22ZBX::text").extract()
        if len(Medicines["How to Use"]) < 1:
            Medicines["How to Use"] = "No Specific Instructions"
        Medicines["Alternate Medicines"] = response.css(".SubstituteItem__name___PH8Al::text").extract()
        if len(Medicines["Alternate Medicines"]) < 1:
            Medicines["Alternate Medicines"] = "No Alternate Brands found for this Medicine"
        Medicines["Side Effects"] = response.css(".DrugOverview__list-container___2eAr6 li::text").extract()
        if len(Medicines["Side Effects"]) < 1:
            Medicines["Side Effects"] = "No reported side effects"
        Medicines["Chemical Class and Habit Forming"] = response.css(".DrugFactBox__col-right___36e1P::text").extract()
        Medicines["Therapeutic Class"] = self.get_key(self.url_to_therapy[current_url[pos_:]])
        Medicines["Image Link"] = self.url_to_img[current_url[pos_:]]
        Medicines["URL"] = response.request.url
        yield Medicines
