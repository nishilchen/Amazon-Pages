# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 20:51:35 2019

@author: nishi
"""

from AmazonPages import AmazonProductPage
from AmazonPages import AmazonProductReviewPage
from AmazonPages import AmazonSearchPage

#%%
# =============================================================================
# Amazon Product Pages
# =============================================================================
asin = "B07KYSCDWV"
country = "us"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"


product_page = AmazonProductPage.AmazonProductPage(asin,country,user_agent)
print(product_page.robot_check())
print(product_page.get_product_info())



#%%
# =============================================================================
# Amazon Product Review Pages
# =============================================================================
asin = "B07KYSCDWV"
country = "us"
user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"


product_review = AmazonProductReviewPage.AmazonProductReviewPage(asin,country,user_agent)
print(product_review.robot_check())
product_review.get_reviews()


#%%
# =============================================================================
# Amazon Search Pages
# =============================================================================
keyword = "halloween customs for women"
user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"

search_page = AmazonSearchPage.AmazonSearchPage(keyword, user_agent)
print(search_page.robot_check())
product_list = search_page.get_product_info_list()
product_list


