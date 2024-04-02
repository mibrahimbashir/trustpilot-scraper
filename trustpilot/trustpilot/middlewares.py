# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class TrustpilotSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class TrustpilotDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


import requests
from urllib.parse import urlencode
import random


class ScrapeOpsFakeBrowserHeadersAgent(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)
    
    def __init__(self, settings):
        self.api_key = settings.get("API_KEY")
        self.api_endpoint = settings.get("API_ENDPOINT", "https://headers.scrapeops.io/v1/browser-headers?")
        self.num_results = settings.get("NUM_RESULTS")

        self.fake_headers_active = settings.get("FAKE_HEADERS_ENABLED", False)

        self.headers_list = []

        self._get_headers_list()

        self._fake_browser_headers_enabled()

    def _get_headers_list(self):
        params = {"api_key" : self.api_key}

        if self.num_results is not None:
            params["num_results"] = self.num_results

        response =  requests.get(self.api_endpoint, params=urlencode(params))

        json_response = response.json()

        self.headers_list = json_response["result"]

    def _get_random_browser_header(self):
        random_index = random.randint(0, len(self.headers_list) - 1)

        return self.headers_list[random_index]
    
    def _fake_browser_headers_enabled(self):
        if self.api_key == "" or self.api_key == None or self.fake_headers_active == False:
            self.fake_headers_active = False
        else:
            self.fake_headers_active = True

    def process_request(self, request, spider):
        random_browser_header = self._get_random_browser_header()

        request.headers["upgrade-insecure-requests"] = random_browser_header["upgrade-insecure-requests"]
        request.headers["user-agent"] = random_browser_header["user-agent"]
        request.headers["accept"] = random_browser_header["accept"]
        request.headers["sec-ch-ua"] = random_browser_header["sec-ch-ua"]
        request.headers["sec-ch-ua-mobile"] = random_browser_header["sec-ch-ua-mobile"]
        request.headers["sec-ch-ua-platform"] = random_browser_header["sec-ch-ua-platform"]
        request.headers["sec-fetch-site"] = random_browser_header["sec-fetch-site"]
        request.headers["sec-fetch-mod"] = random_browser_header["sec-fetch-mod"]
        request.headers["sec-fetch-user"] = random_browser_header["sec-fetch-user"]
        request.headers["accept-encoding"] = random_browser_header["accept-encoding"]
        request.headers["accept-language"] = random_browser_header["accept-language"]