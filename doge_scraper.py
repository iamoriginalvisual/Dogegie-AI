import scrapy
import modules.connect as cn 
import modules.dogegie as dg
from scrapy.crawler import CrawlerProcess
from datetime import datetime
from scrapy.exporters import CsvItemExporter

class doge_get(scrapy.Spider):
    name = "doge_get"
	
    def start_requests(self):
        headers= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        url = "https://www.coindesk.com/price/dogecoin"
        yield scrapy.Request(url, headers = headers,callback=self.parse_contents)
    
    def parse_contents(self, response):
        
        date = datetime.now().strftime("%d/%m/%Y")
        
        time = datetime.now().strftime("%H:%M:%S")
    
        price = response.xpath("//div[@class='coin-info-block'][1]/div[@class='data-definition']/div[@class='price-large']/text()").get()
        
        mcap  = response.xpath("//div[@class='coin-info-block'][3]/div[@class='data-definition']/div[@class='price-medium']/text()").get() 
        
        vol = response.xpath ("//div[@class='coin-info-block'][4]/div[@class='data-definition']/div[@class='price-medium']/text()").get()        
        
        high = response.xpath("//div[@class='coin-info-list '][1]/div[@class='coin-info-block'][2]/div[@class='data-definition']/div[@class='price-medium']/text()").get()
        
        low = response.xpath("//div[@class='coin-info-list '][1]/div[@class='coin-info-block'][1]/div[@class='data-definition']/div[@class='price-medium']/text()").get()

        opn = response.xpath("//div[@class='coin-info-list '][1]/div[@class='coin-info-block'][4]/div[@class='data-definition']/div[@class='price-change-medium']/text()").get()
        
        tsupp  = response.xpath("//div[@class='coin-info-list '][2]/div[@class='coin-info-block'][2]/div[@class='data-definition']/div[@class='price-medium']/text()").get()
        
        row = (str(date), str(time), str(price), str(opn[1:]), str(high[1:]), str(low[1:]), str(mcap[1:]), str(vol[1:]), str(tsupp))
        check_date(date,row)

def check_date(dr,r_row):
    dc = cn.get_all('*','doge_realtime')
    dn = dc.iloc[-1]['date']

    if dr != dn:
        row = (str(dn),str(dc.iloc[-1]['day_price']),str(dc.iloc[-1]['day_open']),str(dc.iloc[-1]['day_high']),str(dc.iloc[-1]['day_low']))
        cn.add_histo(row)
        macd,rsi,so,avg,des = dg.doge_decide()
        descn = (str(dr),str(macd),str(rsi),str(so),str(avg),str(des))
        cn.add_des(descn)
    cn.add_row(r_row)

process = CrawlerProcess()

process.crawl(doge_get)
process.start()