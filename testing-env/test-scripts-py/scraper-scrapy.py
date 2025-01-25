import scrapy
from scrapy.crawler import CrawlerProcess

class EWORSpider(scrapy.Spider):
    name = "ewor_spider"
    allowed_domains = ["ewor.com"]
    start_urls = [
        "https://www.ewor.com",
        "https://www.ewor.com/ideation-fellowship",
        "https://www.ewor.com/traction-fellowship",
        "https://www.ewor.com/founder-resources",
        "https://www.ewor.com/startup-templates",
        "https://www.ewor.com/ewor-team",
        "https://form.ewor.com",
        "https://platform.ewor.com",
        "https://www.ewor.com/apply",
        "https://docs.google.com/document/d/1Y2Y3Z4A5B6C7D8E9F0G1H2I3J4K5L6M7N8O9P0Q1R2S",
        "https://reminder.ewor.com",
        "https://www.ewor.com/leaderboard",
        "https://www.ewor.com/legal/imprint",
        "https://www.ewor.com/privacy-policy",
        "https://www.ewor.com/terms-conditions",
        "https://www.ewor.com/blog",
        "https://www.ewor.com/faq",
    ]

    custom_settings = {
        "FEEDS": {"ewor_data.json": {"format": "json", "indent": 2}},
        "LOG_LEVEL": "INFO",
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 0.5,
    }

    def parse(self, response):
        # Extract and yield relevant page data
        yield {
            "url": response.url,
            "title": response.css("title::text").get(default="").strip(),
            "meta_description": response.css('meta[name="description"]::attr(content)').get(default="").strip(),
            "content": " ".join(response.css("body *::text").getall()).strip(),
        }

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(EWORSpider)
    process.start()
