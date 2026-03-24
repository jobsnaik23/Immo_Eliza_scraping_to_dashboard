#from urllib import response

import scrapy
import requests
#import response
import re


class ImmoElizaSpider(scrapy.Spider):
    name = "immo_eliza_spider"
    allowed_domains = ["immovlan.be"]
    start_urls = ["https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=1&maxprice=1100&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=1101&maxprice=2100&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=2101&maxprice=10000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=10001&maxprice=100000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=100001&maxprice=140000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=140001&maxprice=170000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=170001&maxprice=190000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=190001&maxprice=210000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=210001&maxprice=230000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=230001&maxprice=250000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=250001&maxprice=270000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=270001&maxprice=290000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=290001&maxprice=300000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=300001&maxprice=320000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=320001&maxprice=330000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=330001&maxprice=340000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=340001&maxprice=355000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=355001&maxprice=370000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=370001&maxprice=390000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=390001&maxprice=405000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=405001&maxprice=435000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=435001&maxprice=465000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=465001&maxprice=495000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=495001&maxprice=545000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=545001&maxprice=610000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=610001&maxprice=750000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=750001&maxprice=1200000&noindex=1",
                  "https://immovlan.be/en/real-estate?transactiontypes=for-sale,for-rent&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,cottage,bungalow,chalet,mansion,apartment,penthouse,ground-floor,duplex,studio,loft,triplex&tags=hasgarden&minprice=1200000&maxprice=9000000&noindex=1"
                  ]
       
    def parse(self, response):
        # Extract property links
        links = response.xpath('//a[contains(@href, "/detail/")]/@href').getall()
        for link in set(links):
            yield response.follow(link, callback=self.parse_property)

        # Find Next Page button
        
        next_page = response.css('a.pagination__next::attr(href)').get()
        
        if not next_page:
            next_page = response.xpath('//a[@rel="next"]/@href').get()
            
        if not next_page:
            next_page = response.xpath('//a[contains(text(), "Next")]/@href').get()

        if next_page:
            self.logger.info(f"SUCCESS: Found next page: {next_page}")
            yield response.follow(next_page, callback=self.parse)
        else:
            self.logger.warning("WARNING: No next page found. Check your selectors!")
        

    def parse_property(self, response):
        # ... existing extraction code ...

        # Extract zipcode (4 digits) from the raw city line text
        # Example: '1060 - Sint-Gillis' -> '1060'
        raw_text = response.css('.city-line::text').get(default='').strip()
        # Result: "1140 Evere"
        zipcode = " ".join(raw_text.split()[0:]) 

        # 2. Zipcode: Look for exactly 4 digits (\b is a word boundary)
       # zipcode_match = re.search(r'\b\d{4}\b', raw_text)
        #zipcode = zipcode_match.group(0) if zipcode_match else "0000"

        # Locality (e.g., '1060 - Sint-Gillis')
        raw_text = response.css('.city-line::text').get(default='').strip()
        locality = " ".join(raw_text.split()[1:]) 
        
        # Type of property
        """
        tag = <span class="detail__header_title_main">
                    Apartment for rent <span class="d-none d-lg-inline">- Somme-Leuze</span> <span class="vlancode">VBD88362</span>
                </span>
        """
        # Extract "Apartment for rent - Sint-Gillis RBV31374"
        full_text = response.css('.detail__header_title_main ::text').get(default='').strip()
        # Split by space and take the first word: "Apartment"
        property_type = full_text.split()[0]
    
        # Price
        # Grab all text nodes within the price span
        raw_price_list = response.css('.detail__header_price_data ::text').getall()
        # Join the list into one string: " 1 750 € "
        price_string = "".join(raw_price_list)
        # Use Regex to extract only the numbers: "1750"
        price = "".join(re.findall(r'\d+', price_string))

        
        # Subtype Extraction Logic (First two words of the description)
        
        # Extract the full description text 
        full_description = response.css('div.description-class::text').get(default='').strip()
        # Split the text into words and take the first two
        # Creating a list: ["Beautiful", "apartment", "of", "+-100m²", ...]
        words = full_description.split()
        subtype = " ".join(words[:2]) if len(words) >= 2 else full_description


        # Type of sale (Exclude life sales logic)
        # Extract "Apartment for rent - Sint-Gillis RBV31374"
        full_text = response.css('.detail__header_title_main ::text').get(default='').strip()
        # Split by space and take the first word: "Apartment"
        type_of_sale = full_text.split()[2]

        # Basic Room/Area Info
        # Finds the <h4> with the specific text, then gets the <p> right after it
        rooms = response.xpath('//h4[contains(text(), "Number of bedrooms")]/following-sibling::p/text()').get(default='0').strip()
        nb_rooms = int(rooms) if rooms.isdigit() else 0

        area = response.xpath('//h4[contains(text(), "Livable surface")]/following-sibling::p/text()').re_first(r'\d+')
        living_area = int(area) if area and area.isdigit() else 0

        # Kitchen (Checks if it contains 'Equipped')
        #kitchen_raw = response.xpath('//h4[contains(text(), "Number of bathrooms")]/following-sibling::p/text()').get(default='0').strip()
        #kitchen = int(kitchen_raw) if kitchen_raw.isdigit() else 0 

        furnished_text = response.xpath('//h4[contains(text(), "Furnished")]/following-sibling::p/text()').get(default='No').strip().lower()
        kitchen_equipped = 1 if furnished_text == "yes" else 0
    
        # Furnished
        furnished_text = response.xpath('//h4[contains(text(), "Furnished")]/following-sibling::p/text()').get(default='No').strip().lower()
        furnished = 1 if furnished_text == "yes" else 0
    
        # Open Fire
        description_text = response.css('div.dynamic-description ::text').getall()
        full_text = " ".join(description_text).lower()
        #   Check for "open fire" or "fireplace"
        open_fire = 1 if "open fire" in full_text or "fireplace" in full_text else 0
   
        # Swimming Pool
        swimming_pool = 1 if "swimming pool" in full_text else 0
   

        # Terrace
        terrace_text = response.xpath('//h4[contains(text(), "Terrace")]/following-sibling::p/text()').get(default='No').strip().lower()
        terrace = 1 if terrace_text == "yes" else 0
    
        if terrace == 1:
            terrace_area = response.xpath('//h4[contains(text(), "Surface terrace")]/following-sibling::p/text()').re_first(r'\d+')
        else:
            terrace_area = "0"
    
        # Garden Logic
        garden_text = response.xpath('//h4[contains(text(), "Garden")]/following-sibling::p/text()').get(default='No').strip().lower()
        garden = 1 if garden_text == "yes" else 0
    
        if garden == 1:
            garden_area = response.xpath('//h4[contains(text(), "Surface garden")]/following-sibling::p/text()').re_first(r'\d+')
        else:
            garden_area = "0"
    
    
        # Surface Land (Total land area)
        land = response.xpath('//h4[contains(text(), "Surface land")]/following-sibling::p/text()').re_first(r'\d+')
        surface_land = int(land) if land else 0

        # Plot Surface (Often same as surface land or specific plot size)
        plot = response.xpath('//h4[contains(text(), "Surface plot")]/following-sibling::p/text()').re_first(r'\d+')
        plot_surface = int(plot) if plot else 0

        # Facades
        facade_val = response.xpath('//h4[contains(text(), "Number of facades")]/following-sibling::p/text()').re_first(r'\d+')
        facades = int(facade_val) if facade_val else 1 # Default to 1 if not specified

        # Building State (Condition)
        building_state = response.xpath('//h4[contains(text(), "Condition")]/following-sibling::p/text()').get(default='Unknown').strip()

        # Swimming Pool (Updating your existing logic to check the technical list too)
        pool_text = response.xpath('//h4[contains(text(), "Swimming pool")]/following-sibling::p/text()').get(default='No').strip().lower()
        # Returns 1 if mentioned in description OR if technical field says 'yes'
        swimming_pool = 1 if "swimming pool" in full_text or pool_text == "yes" else 0


        yield {
            'zipcode': zipcode,
            'locality': locality,
            'property_type': property_type,
            'subtype': subtype,
            'price': price,
            'type_of_sale': type_of_sale,
            'nb_rooms': nb_rooms,
            'living_area': living_area,
            'kitchen_equipped': kitchen_equipped,
            'furnished': furnished,
            'open_fire': open_fire,
            'terrace': terrace,
            'terrace_area': terrace_area,
            'garden': garden,
            'garden_area': garden_area,
            'surface_land': surface_land,
            'plot_surface': plot_surface,
            'facades': facades,
            'swimming_pool': swimming_pool,
            'building_state': building_state,
            'url': response.url
       }
