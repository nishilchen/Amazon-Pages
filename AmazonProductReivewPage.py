# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 22:59:30 2018

@author: Li Hsin
"""
#%%
# Written as part of https://www.scrapehero.com/how-to-scrape-amazon-product-reviews-using-python/        
from lxml import html
import json, re
import requests
from dateutil import parser as dateparser

#%%
class AmazonProductReviewPage:
    def __init__(self, asin, country,user_agent):
        self.amazon_url_review  = self.get_url(country) + '/product-reviews/' + asin + '/ref=cm_cr_arp_d_viewopt_srt?sortBy=recent'
        self.headers = {'User-Agent': user_agent}
        self.parser = self.get_review_page()
    
    def get_url(self,country):
        if country == "us":
            return 'http://www.amazon.com'
        elif country == "uk" or country == "jp":
            return 'http://www.amazon.co.' + country
        else:
            return 'http://www.amazon.' + country
    
    def robot_check(self):
        is_robot = self.parser.xpath('//body//title//text()')
        return is_robot
    
    
    def get_review_page(self):
        page = requests.get(self.amazon_url_review, headers = self.headers, verify=False)
        page_response = page.text
        return html.fromstring(page_response)
    
    
    def get_reviews(self):        
#        parser = self.get_review_page()
        XPATH_REVIEW_SECTION_1 = '//div[contains(@id,"reviews-summary")]'
        XPATH_REVIEW_SECTION_2 = '//div[@data-hook="review"]'
        
        reviews = self.parser.xpath(XPATH_REVIEW_SECTION_1)
        if not reviews:
          reviews = self.parser.xpath(XPATH_REVIEW_SECTION_2)
        
        reviews_list = []
        
        XPATH_RATING  = './/i[@data-hook="review-star-rating"]//text()'
        XPATH_REVIEW_HEADER = './/a[@data-hook="review-title"]//text()'
        XPATH_REVIEW_POSTED_DATE = './/span[@data-hook="review-date"]//text()'
        #XPATH_REVIEW_TEXT_1 = './/div[@data-hook="review-collapsed"]//text()'
        XPATH_REVIEW_TEXT_1 = './/span[@data-hook="review-body"]//text()'
        XPATH_REVIEW_TEXT_2 = './/div//span[@data-action="columnbalancing-showfullreview"]/@data-columnbalancing-showfullreview'
        XPATH_REVIEW_COMMENTS = './/span[@data-hook="review-comment"]//text()'
        #XPATH_AUTHOR  = './/span[@data-hook="review-author"]//text()'
        XPATH_AUTHOR  = './/span[@class="a-profile-name"]//text()'
        XPATH_REVIEW_TEXT_3  = './/div[contains(@id,"dpReviews")]/div/text()'
        XPATH_SIZECOLOR = './/a[@data-hook="format-strip"]//text()'
        
        for review in reviews:
            raw_review_author = review.xpath(XPATH_AUTHOR)
            raw_review_rating = review.xpath(XPATH_RATING)
            raw_review_header = review.xpath(XPATH_REVIEW_HEADER)
            raw_review_posted_date = review.xpath(XPATH_REVIEW_POSTED_DATE)
            raw_review_text1 = review.xpath(XPATH_REVIEW_TEXT_1)
            raw_review_text2 = review.xpath(XPATH_REVIEW_TEXT_2)
            raw_review_text3 = review.xpath(XPATH_REVIEW_TEXT_3)
            raw_review_sizecolor = review.xpath(XPATH_SIZECOLOR )

# =============================================================================
#             Author
# =============================================================================
            author = ' '.join(' '.join(raw_review_author).split('By ')).strip()
#            review_rating = int(''.join(raw_review_rating).replace('out of 5 stars','').strip())
                        
# =============================================================================
#             Rating
# =============================================================================
            review_rating = int(raw_review_rating[0][0])
            
# =============================================================================
#             Header
# =============================================================================
            review_header = ' '.join(' '.join(raw_review_header).split())


# =============================================================================
#             Review Date
# =============================================================================
            try:
                review_posted_date = dateparser.parse(''.join(raw_review_posted_date)).strftime('%Y%m%d')
                review_posted_date = int(review_posted_date)
            except:
                review_posted_date = None
            
            
# =============================================================================
#             Review Text
# =============================================================================
            review_text = ' '.join(' '.join(raw_review_text1).split())

            #grabbing hidden comments if present
            if raw_review_text2:
                json_loaded_review_data = json.loads(raw_review_text2[0])
                json_loaded_review_data_text = json_loaded_review_data['rest']
                cleaned_json_loaded_review_data_text = re.sub('<.*?>','',json_loaded_review_data_text)
                full_review_text = review_text+cleaned_json_loaded_review_data_text
            else:
                full_review_text = review_text
            if not raw_review_text1:
                full_review_text = ' '.join(' '.join(raw_review_text3).split())

# =============================================================================
#             Review Comments
# =============================================================================
            raw_review_comments = review.xpath(XPATH_REVIEW_COMMENTS)
            review_comments = ''.join(raw_review_comments)
            review_comments = re.sub('[A-Za-z]','',review_comments).strip()
            
            
            
# =============================================================================
#             Size Color
# =============================================================================
            if raw_review_sizecolor:
                size = raw_review_sizecolor[0].split(": ")[1]
                color = raw_review_sizecolor[1].split(": ")[1]
            else:
                size = None
                color = None
            
# =============================================================================
#             Output as dictionary
# =============================================================================
            review_dict = {
#                         'review_comment_count':review_comments,
                          'Text':full_review_text,
                          'Date_Posted':review_posted_date,
                          'Header':review_header,
                          'Rating':review_rating,
                          'Author':author,
                          'Size':size,
                          'Color':color
                                      }
            reviews_list.append(review_dict)
        return reviews_list

    def GetReviewId(row):
        return row['SKU'] + str(row['Date_Posted']) + str(row['Rating']) + row['Author'] + row['Size'] + row['Color']


#%%
asin = "B07KYSCDWV"
country = "us"
user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"


product = AmazonProductReviewPage(asin,country,user_agent)
product.robot_check()
product.get_reviews()
len(product.get_reviews())

        
    
    
    
    
    
    
    
    
    
    
    
    