# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 11:09:01 2019

@author: Li Hsin
"""

import requests
from datetime import datetime as dt
from lxml import html


class AmazonSearchPage():
    def __init__(self,keyword,user_agent):
        self.headers = {'User-Agent': user_agent}
        self.keyword = keyword
        self.parser = self.get_search_page()

    def robot_check(self):
        is_robot = self.parser.xpath('//head//title//text()')
        return is_robot
    
# =============================================================================
    def get_url(self):
        url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords='
        nkws = self.keyword.replace(" ","+")
        return url + nkws
        
    def get_search_page(self):
        amazon_url = self.get_url()
        page = requests.get(amazon_url, headers = self.headers, verify=False)
        page_response = page.text
        return html.fromstring(page_response)

    
# =============================================================================
    def get_product_list(self):
        XPATH_PRODUCT = '//div[@data-index]'
        raw_product_list = self.parser.xpath(XPATH_PRODUCT)
        return raw_product_list

    
# =============================================================================
    def get_product(self,item):
        ad_type = item.xpath('.//div[@class="sg-col-inner"]/div/div/span[@class="a-size-base a-color-secondary"]/text()')
        ad_type1 = ".".join(ad_type)
        
        # =============================================================================
        # Ads Type                
        # =============================================================================
        if not ad_type1:
            ad_type1 = 'Organic'
        
        # =============================================================================
        # Brand Name
        # =============================================================================
        try:
            raw_brand_name = item.xpath('.//div/div/div/div[@class="a-row a-size-base a-color-secondary"]/h5/span//text()')
            brand_name = raw_brand_name [0]
        except:
            brand_name = ""
        
        # =============================================================================
        # Product Name
        # =============================================================================
        raw_product_name = item.xpath('.//div/div/div/h2/a/span/text()')
        product_name = ''.join(raw_product_name).strip()
        product_name = brand_name + " " + product_name

        # =============================================================================
        # Price
        # =============================================================================
        raw_price = item.xpath('.//div/a/span[@class="a-price"]/span/text()')
        product_price = ''.join(raw_price).strip()
        


        # =============================================================================
        # Product Rating
        # =============================================================================
        try:            
            raw_rating = item.xpath('.//a/i/span[@class="a-icon-alt"]/text()')
            product_rating = float(''.join(raw_rating).strip().split(" ")[0])
        except:
            product_rating = None
            
        # =============================================================================
        # Products Total Review            
        # =============================================================================
        try:
            raw_total_review = item.xpath('.//span[@class="a-size-base"]/text()')
            total_review = int(raw_total_review[0])
        except:
            total_review = None
        time = str(dt.today())
  
        return {"Keyword": self.keyword,
                "Brand Name": brand_name,
                "Product Name": product_name,
                "ASIN": item.values()[0],
                "position": int(item.values()[1]),
                "Price": product_price,
                "Rating": product_rating,
                "Total Reviews": total_review,
                "Time": time,
                "Type":ad_type1}
    
 
# =============================================================================
    def get_product_info_list(self):
        raw_product_list = self.get_product_list()
        result = []
        for item in raw_product_list:
            newData = self.get_product(item)
            result.append(newData)
        return result

# =============================================================================
    def get_headline_info(self):
        XPATH_BRAND_NAME = '//div/span[@id="hsaSponsoredByBrandName"]/text()'
        raw_brand_name = self.parser.xpath(XPATH_BRAND_NAME)
        brand_name = ''.join(raw_brand_name).strip()
        time = str(dt.today())
        
        return {"Keyword": self.keyword,
                "Sponsored Brand": brand_name,
                "Time": time,
                "Period": self.time_period(time)}














