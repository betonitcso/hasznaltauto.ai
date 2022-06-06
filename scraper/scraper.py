import re
import requests
from scrapy import Selector
from dataclasses import dataclass

@dataclass
class Listing:
    url: str
    title: str
    description: str
    price: int

class CarScraper:

    def __init__(self, url):
        self.url = url
        self.pages = [url]
        self.first_page = requests.get(url).content
        self.listings =  []

    def extractListings(self, pages = -1):
        last_page = int(Selector(text = self.first_page).css('.last *::text').extract_first())

        if pages == -1 or pages > last_page:
            for page in range(last_page-1):
                self.pages.append((self.url + f'/page{page+2}'))
        else:
            for page in range(pages-1):
                self.pages.append((self.url + f'/page{page+2}'))

        for page in self.pages:
            html = requests.get(page).content
            listing_rows = Selector(text = html).css('div .row .talalati-sor')
            for listing in listing_rows:
                url = listing.css('h3 > a::attr(href)').extract()[0]
                title = listing.css('h3> a::text').extract()[0].strip()
                price = listing.css('.vetelar *::text').extract()[0].strip()
                details_page = requests.get(url).content
                description = Selector(text = details_page).css('.leiras *::text').extract()
                for desc in description:
                    desc = re.sub(r'\r\n|\r|\n', ' ', desc)
                    desc = desc.strip()
                    if desc != 'Leírás' and len(desc) != 0:
                        description = desc
                        break
                self.listings.append(Listing(url = url, title = title, description = description, price=price))
        
        return self.listings
                        




    def getListings(self):
        return self.listings
    def getCarLinks(self):
        return self.links


if __name__ == '__main__':
    scraper = CarScraper("https://www.hasznaltauto.hu/talalatilista/PCOG2VGRR3RDADH4S56ACFCYN3B6HHOQEKO5ASRH5VVWLKBJUFEYZEVULJAPZ6ZZNVQZXCVHLJRTWHSPEYCTS64XG4X2PGIUCUCCZSJJ3BRCGVUMJWS7AVZUVAXVAB3KUG4RJIGTYJWY6H4VFMYKA35AAB7RLK45TT2IONAMNNYLSUJWDYZJCQUMGPYD3TBMUTANVZKJ373FKIVWHXT7GVALHLSCO4FGN3HZCYW2P2LVFFHAYDXBK2HFL4KGI4KT2BSF7ZDY4YHB32RDAZ5JC7UXQL4ZCVYBIPEB6Y6GWLIBUTQBJYHZYFZ56ADCZVFGUAPJWPVRYHBEH4FRFRX6HUGXHL4ERAFJM6JZNSNP6EO7Z5XO6ARRZ27TIEDP7ILL2QPH2IW447Y6FSD6VEBHWNQZB7PNOPUQ7GVXZ6DUMQUCRMU3UJF37NK5L6NW2L6F4QQYL4TL272SQW5OSUHOROQOEZT4AVMQVORGPPK4YQQMURYFNLOSN6WKUDHLKP5BD24QKG4WD5BCVTYTDTEFHKMGV5B7ORJ45PAP4DNBGJRQWJVJYSB4ZK3G56B32QHZHQL3JBRTAWYQFOMQG7KRTPBVQKJNGLWOMKOHL4JMY2ZS5HWHPDPMLPHYTWBRTC4IWZCFPOZQE2LONUWXYET3BGNIZLM3EBT6S2WDK6SMKBPIEVOUNCXFIROSLR2WWBMO57MUBAHB6VYTC6L7VXMOXVIQP6F3OSQH6WO5YNNDVCYQVUIZH2DZ3BVEFHHNANK326VBCHGQTTR6ZZFU636UKY26FOZJOZUYMMS5BH2HIQN3E5BEI7SRAX3W74JX5ACDSSOV62LFSJK6GD4BU6Q33IGPB7SEVUDGYDZ55COMB37UH662UAOZBPP7A7VGLINP")
    for listing in scraper.extractListings(pages=1):
        print(f'{listing.title} [{listing.price}]:\n{listing.url}')