import scrapy
from scrapy.crawler import CrawlerProcess


class EWORScraper(scrapy.Spider):
    name = "ewor_scraper"
    allowed_domains = ["ewor.com", "platform.ewor.com", "form.ewor.com", "reminder.ewor.com"]
    start_urls = [
        "https://www.ewor.com/",
        "https://platform.ewor.com/auth/login/",
        "https://www.ewor.com/apply?sc=EW&ssc=Header&sm=Direct",
        "https://www.ewor.com/legal/imprint",
        "https://www.ewor.com/legal/privacy-policy",
        "https://www.ewor.com/legal/terms-and-conditions",
        "https://www.ewor.com/startup-templates?sc=EW&ssc=Header&sm=Direct",
        "https://www.ewor.com/ewor-team",
        "https://www.ewor.com/ideation-fellowship",
        "https://www.ewor.com/traction-fellowship",
        "https://form.ewor.com/nominate",
        "https://www.ewor.com/faq",
        "https://forms.ewor.com/onboarding",
        "https://www.ewor.com/blog",
        "https://form.ewor.com/investor-network-registration",
        "https://reminder.ewor.com/",
        "https://forms.ewor.com/collaborate-with-ewor"
    ]

    custom_settings = {
        "FEEDS": {
            "ewor-scraper-output/json/%(name)s_%(time)s.json": {"format": "json", "indent": 4},
        },
        "LOG_LEVEL": "INFO",
        "FILES_STORE": "ewor-scraper-output/pdf/",
    }

    def parse(self, response):
        """Route the response to specific parsers based on the URL."""
        if "startup-templates" in response.url:
            yield from self.parse_founder_resources(response)
        elif "blog" in response.url and "/blog/" not in response.url:
            yield from self.parse_blog_list(response)
        elif "/blog/" in response.url:
            yield self.parse_blog_post(response)
        else:
            yield self.parse_static_page(response)

    def parse_static_page(self, response):
        """Parse static pages (e.g., home, FAQ, legal pages)."""
        return {
            "url": response.url,
            "title": response.css("title::text").get(),
            "meta_description": response.css('meta[name="description"]::attr(content)').get(),
            "content": " ".join(response.css("body *::text").getall()).strip(),
        }

    def parse_founder_resources(self, response):
        """Parse the Founder Resources page and extract links."""
        resources = []
        for resource in response.css(".template_item a"):
            name = resource.css("::text").get().strip()
            link = response.urljoin(resource.css("::attr(href)").get())
            resources.append({"name": name, "link": link})
        return {"url": response.url, "resources": resources}

    def parse_blog_list(self, response):
        """Parse the Blog page and extract links to individual blog posts."""
        for blog in response.css(".blog_other-item a::attr(href)").getall():
            yield response.follow(blog, self.parse_blog_post)

    def parse_blog_post(self, response):
        """Parse an individual blog post."""
        return {
            "url": response.url,
            "title": response.css("title::text").get(),
            "meta_description": response.css('meta[name="description"]::attr(content)').get(),
            "content": " ".join(response.css("div.blog_rte p::text").getall()).strip(),
            "author": response.css(".blogpos_author-wrapper div::text").get(),
        }

    def start_requests(self):
        """Initiate requests and download PDFs."""
        # Static page requests
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

        # PDF downloads
        pdf_files = [
            ("https://downloads.ewor.com/decks/Ideation_Education_Pre-Investment_Agreement_2025.pdf", "ideation_fellowship_agreement.pdf"),
            ("https://downloads.ewor.com/EWOR%20Ideation%20Fellowship%20Factsheet.pdf", "ideation_fellowship_factsheet.pdf"),
            ("https://downloads.ewor.com/decks/2024-07-01_Traction_Fellowship_Agreement_guaranteed_investment_2024.pdf", "traction_fellowship_agreement.pdf"),
            ("https://downloads.ewor.com/EWOR%20Traction%20Fellowship%20Factsheet.pdf", "traction_fellowship_factsheet.pdf")
        ]
        for pdf_url, filename in pdf_files:
            yield scrapy.Request(
                pdf_url,
                callback=self.save_pdf,
                meta={"filename": filename}
            )

    def save_pdf(self, response):
        """Save PDF files to the output directory."""
        filename = response.meta["filename"]
        pdf_path = f"ewor-scraper-output/pdf/{filename}"
        with open(pdf_path, "wb") as f:
            f.write(response.body)
        self.log(f"Downloaded PDF: {filename}")

# Run the scraper
process = CrawlerProcess()
process.crawl(EWORScraper)
process.start()
