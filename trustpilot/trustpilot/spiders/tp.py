import scrapy


class TpSpider(scrapy.Spider):
    name = "tp"
    allowed_domains = ["trustpilot.com"]
    start_urls = ["https://trustpilot.com"]

    def parse(self, response):
        cat_page = response.xpath("//button[@class='styles_menu__g9lRD styles_button__Fm6Bt styles_mobile__J4aRs']/following-sibling::a").attrib["href"]

        cat_page = "http://trustpilot.com/" + cat_page

        yield response.follow(cat_page, callback=self.parse_cat_page)

    def parse_cat_page(self, response):
        cat_url = response.css(".card_cardContent__sFUOe.styles_linkList__QJM6a li a::attr(href)")

        for category in cat_url:
            category = "http://trustpilot.com/" + category.get()

            yield response.follow(category, callback=self.parse_cat_url)

    def parse_cat_url(self, response):
        business_url = response.css("div.paper_paper__1PY90.paper_outline__lwsUX.card_card__lQWDv.card_noPadding__D8PcU.styles_wrapper__2JOo2 a::attr(href)")

        for business in business_url:

            business = "http://trustpilot.com/" + business.get()

            yield response.follow(business, callback=self.parse_business_url)

    def parse_business_url(self, response):

        reviews = response.css("section.styles_reviewContentwrapper__zH_9M")

        for review in reviews:
            yield {
                "stars" : review.css("div.styles_reviewHeader__iU9Px").attrib["data-service-review-rating"],

                "review_date" : review.css("time").attrib["datetime"],
                
                "description" : review.css("p.typography_body-l__KUYFJ::text").get(),

                "date_experience" :  review.css("p.typography_body-m__xgxZ_ ::text")[3].get(),
            }