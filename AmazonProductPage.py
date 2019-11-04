# -*- coding: utf-8 -*-
"""
Created on Sat Aug 25 22:59:30 2018

@author: Li Hsin
"""
#%%
from lxml import html
import requests
#%%
class AmazonProductPage:
    def __init__(self, asin, country, user_agent):
        self.asin = asin
        self.country = country
        self.amazon_url  = self.get_url(country) + '/dp/' + asin
        self.headers = {'User-Agent': user_agent}
        self.parser = self.get_RankAndRating_page()
        
# =============================================================================
    def get_url(self,country):
        if country == "us":
            return 'http://www.amazon.com'
        elif country == "uk" or country == "jp":
            return 'http://www.amazon.co.' + country
        else:
            return 'http://www.amazon.' + country
        
    def robot_check(self):
        is_robot = self.parser.xpath('//head//title//text()')
        return is_robot

    def get_RankAndRating_page(self):
        page = requests.get(self.amazon_url, headers = self.headers, verify=False)
        page_response = page.text
        return html.fromstring(page_response)
    
    def ExtractNumber(self, string):
            decode = list(map(lambda x: ord(x), string))
            num_code = [chr(num) for num in decode if num>47 and num<58]
            return int("".join(num_code)) 

# =============================================================================
    def get_product_info(self):
        ret = {"Item Name": self.get_product_name(), 
                "Total Reviews": self.get_total_number_reviews(), 
                "Average Rating": self.get_average_rating(), 
                "Ranking": self.get_ranking()[0], 
                "Ranking Category": self.get_ranking()[1],
                "Fit Recommendation (%)": self.get_fitting_recommendation()}
        ret.update(self.get_product_stars_dist())
        return ret
    
# =============================================================================
    def get_product_name(self):
        XPATH_PRODUCT_NAME = '//h1//span[@id="productTitle"]//text()'
        raw_product_name = self.parser.xpath(XPATH_PRODUCT_NAME)
        product_name = ''.join(raw_product_name).strip()
        return product_name
    
    def get_total_number_reviews(self):
        XPATH_AGGREGATE = '//span[@id="acrCustomerReviewText"]//text()'
        raw_aggregate = self.parser.xpath(XPATH_AGGREGATE)
        if raw_aggregate:
            aggregate_review = self.ExtractNumber(raw_aggregate[0])
        else:
            aggregate_review  = 0
        return aggregate_review
    
    def get_product_stars_dist(self):
        XPATH_AGGREGATE_RATING = '//table[@id="histogramTable"]//tr'
        total_ratings  = self.parser.xpath(XPATH_AGGREGATE_RATING)
        ratings_dict = {'5 Star' : 0, '4 Star' : 0, '3 Star' : 0, '2 Star' : 0, '1 Star' : 0}
        star = 5
        for ratings in total_ratings:
            extracted_rating = ratings.xpath('.//text()')
            if extracted_rating:
                rating_key = str(star) + " Star"
                raw_raing_value = [r for r in extracted_rating if "%" in r][-1]
                rating_value = float(raw_raing_value.strip(" \n").strip("%"))/100
                if rating_key:
                    ratings_dict.update({rating_key:rating_value})
            star -= 1
        return ratings_dict


    def get_average_rating(self):
        XPATH_AVE_RATING = '//span[@id="acrPopover"]//span//a//i//span//text()'
        raw_ave_rating = self.parser.xpath(XPATH_AVE_RATING)
        if raw_ave_rating:
            if self.country == 'jp':
                integer = raw_ave_rating[0].split('.')[0][-1]
                decimal = raw_ave_rating[0].split('.')[1][-1]
                ave_rating = float(".".join([integer, decimal]))
            else:
                try:
                    ave_rating = float(raw_ave_rating[0][0:3])
                except:
                    ave_rating = float(".".join(raw_ave_rating[0][0:3].split(",")))
        else:
            ave_rating = None
        return ave_rating

    def get_ranking(self):
        try:
            XPATH_RANKING = '//li[@id="SalesRank"]//text()'
            raw_ranking = self.parser.xpath(XPATH_RANKING)
            ranking = self.ExtractNumber(raw_ranking[2])
            ranking_category = raw_ranking[2]
        except IndexError:
            try:
                XPATH_RANKING_table = '//table[@id="productDetails_detailBullets_sections1"]//tr'
                raw_ranking_cell = self.parser.xpath(XPATH_RANKING_table)[-1]
                raw_ranking = raw_ranking_cell.xpath(".//span//span//text()")[0]         
                ranking = self.ExtractNumber(raw_ranking)
                ranking_category = raw_ranking
            except:
                ranking = None
                ranking_category = None

        return [ranking, ranking_category]


    def get_fitting_recommendation(self):
        XPATH_fitRecommendation = '//span[@id="fitRecommendationsLinkRatingText"]//text()'
        raw_fitRecommendation = self.parser.xpath(XPATH_fitRecommendation)
        
        if raw_fitRecommendation:
            fitRecommendation = float(raw_fitRecommendation[0].split('(')[1].split("%")[0])
        else:
            fitRecommendation = None
        return fitRecommendation


# =============================================================================
    def get_bulletpoint(self):
        XPATH_BULLETPOINT = '//div[@id="feature-bullets"]//text()'
        raw_bulletpoint = self.parser.xpath(XPATH_BULLETPOINT)
        
        step1 = [string.replace("\n","").replace("\t","").lstrip() for string in raw_bulletpoint]
        step2 = [s for s in step1 if s is not ""]
        
        return step2














