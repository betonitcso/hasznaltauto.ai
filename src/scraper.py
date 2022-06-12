import re
import requests
from scrapy import Selector
from dataclasses import dataclass

@dataclass
class Listing:
    url: str
    title: str
    description: str
    price: str

class CarScraper:

    def __init__(self, url):
        self.url = url
        self.pages = [url]
        self.first_page = requests.get(url).content
        self.listings =  []

    def extractListings(self, pages = -1):
        try:
            last_page = int(Selector(text = self.first_page).css('.last *::text').extract_first())

            if pages == -1 or pages > last_page:
                for page in range(last_page-1):
                    self.pages.append((self.url + f'/page{page+2}'))
            else:
                for page in range(pages-1):
                    self.pages.append((self.url + f'/page{page+2}'))

        except:
            pass

        finally:
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


if __name__ == '__main__':
    scraper = CarScraper("https://www.hasznaltauto.hu/talalatilista/PCOG2VGRN3VDADH5S56ACFGY53BOHPKCIO5EFEZG5W2TFVEU2ASEMSK2BUIP6PVHFWWKS6FKOVWMPRZHE4CTS64TK4X2PGIUCUCCZSJJ3BQCHFUMJWS7AFZUVDHVAB3KUG4RJIGTYJGY6H4UFMYKA35AAB7RDS5NTT2IONAMNNYLSUJWDYZJCQUMGPYD3TBMUTANVZKJ37TFSIVWHXTPGVALHLSEO4FGN3HZCYW2PZP2KKGBQHOSTUGKH4U4RYVGUDET5SPRZQWTVVAHBT2CJ7JGAXZSHLYCQ2IN7R4MMWQRKHADDTXTQL5244GVRKDVIE6TM7LAQOCYPYD5LHPMNINPOXYJCACTZ4TC3EZ74M57R2657ZLTRVXHTUGH5ITL2QHH2IW4Y7Q6ZSD6VEBHWNQZB7PNKPUQ7GXXZ6DQMQUCRMXLUJF37NC5L7VU2L6F4QXIL4RL272SQW5OSQHOROQOEZT4AVMQVORO7SPCG6VEOBLK3XRH2YKQU7NB6UMPZSBA3KYPEFK6OAIO2SUVJQ5XUH5SEFTIZ73A3IJSMMDSNKOEQLGKWZXLQM6UH6JYC62IMEYFWECLTECX2X43X5MBSLJ4OUSKMZOTZC7RVSF6OMM6O7YUELDPDTGFQQ5UEW5NVBJRWE2JOPQOH2A32RCVZ2HDL4F3MSW5CY4C6IJKZISGOOQSVEXGVJVSW4D4ZYDAEDDPR6F4T62LYVLK7BXYJO6FJWVL57SKUGKFRVKYRRXQHFWDKJCNOGDK5WNZK2G6BAHGCRTSPJ5VZ4X7V4SSSE6TPQY4FOA74NBC3KIKKAZZFKD7Q27XHPQ7ON2E3H4JKVRGLE274D3YDLNDH6T4J6XAI3IGHRXZ3SDM6B73JKYN3IA5TWYPPOCKC5A")
    for listing in scraper.extractListings(pages=1):
        print(f'{listing.title} [{listing.price}]:\n{listing.url}')