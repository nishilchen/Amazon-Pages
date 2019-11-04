# Amazon-Pages
```
import AmazonProductPage
import AmazonProductReviewPage
import AmazonSearchPage
```
## Amazon Product Pages
```
asin = "B07KYSCDWV"
country = "us"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"

product_page = AmazonProductPage.AmazonProductPage(asin,country,user_agent)
print(product_page.robot_check())
product_page.get_product_info()
```
```
{'1 Star': 0.0,
 '2 Star': 0.0,
 '3 Star': 0.14,
 '4 Star': 0.23,
 '5 Star': 0.63,
 'Average Rating': 4.5,
 'Fit Recommendation (%)': 100.0,
 'Item Name': "The Drop Women's Venice Mid Rise Skinny Jean",
 'Ranking': 74014,
 'Ranking Category': ' #74,014 in Clothing, Shoes & Jewelry (',
 'Total Reviews': 13}
 ```


## Amazon Product Review Pages
```
asin = "B07KYSCDWV"
country = "us"
user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"

product_review = AmazonProductReviewPage.AmazonProductReviewPage(asin,country,user_agent)
print(product_review.robot_check())
product_review.get_reviews()[0]
```
```
{'Author': 'Tammy L. moore',
  'Color': 'White Wash',
  'Date_Posted': 20190826,
  'Header': 'To low waisted',
  'Rating': 3,
  'Size': '31',
  'Text': 'To low waisted'}
```

## Amazon Search Pages
```
keyword = "halloween customs for women"
user_agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"

search_page = AmazonSearchPage.AmazonSearchPage(keyword, user_agent)
print(search_page.robot_check())
product_list = search_page.get_product_info_list()
product_list[0:5]
```
```
[{'ASIN': 'B07G4CX9MB',
  'Brand Name': 'JomeDesign',
  'Keyword': 'halloween customs for women',
  'Price': '$28.99',
  'Product Name': 'JomeDesign Halloween Costumes for Women 3D Skeleton Cosplay Jumpsuit Bodysuit',
  'Rating': 4.2,
  'Time': '2019-11-03 21:19:32.555046',
  'Total Reviews': 118,
  'Type': 'Organic',
  'position': 0},
 {'ASIN': 'B00505DW8W',
  'Brand Name': "Rubie's",
  'Keyword': 'halloween customs for women',
  'Price': '$15.99',
  'Product Name': "Rubie's Costume DC Comics Wonder Woman T-Shirt With Cape And Headband Red",
  'Rating': 4.0,
  'Time': '2019-11-03 21:19:32.556044',
  'Total Reviews': None,
  'Type': 'Organic',
  'position': 1},
 {'ASIN': 'B0762L4J7V',
  'Brand Name': 'VETIOR',
  'Keyword': 'halloween customs for women',
  'Price': '$18.99',
  'Product Name': 'VETIOR Womens Halloween Long Sleeve Round Neck Casual Printed Flared Party Dress',
  'Rating': 4.5,
  'Time': '2019-11-03 21:19:32.557041',
  'Total Reviews': 262,
  'Type': 'Organic',
  'position': 2},
 {'ASIN': 'B00J7RFLG0',
  'Brand Name': 'Leg Avenue',
  'Keyword': 'halloween customs for women',
  'Price': '$31.63',
  'Product Name': "Leg Avenue Women's Gothic Red Riding Hood Costume",
  'Rating': 4.1,
  'Time': '2019-11-03 21:19:32.558038',
  'Total Reviews': 530,
  'Type': 'Organic',
  'position': 3},
 {'ASIN': 'B00K44DF1I',
  'Brand Name': 'Fun World',
  'Keyword': 'halloween customs for women',
  'Price': '$15.02',
  'Product Name': "Fun World Women's Peace Love Hippie Costume",
  'Rating': 4.3,
  'Time': '2019-11-03 21:19:32.558038',
  'Total Reviews': 553,
  'Type': 'Organic',
  'position': 4}]
```
