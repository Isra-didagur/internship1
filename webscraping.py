import urllib.request
import re
import ssl
import os

# NOTE ON CONTEXT:
# This script uses built-in Python tools. To work on live e-commerce sites like Flipkart/Nykaa, 
# you MUST inspect the source code of the target website and replace the placeholder class names below.

def fetch_html(url):
    """
    Fetches the raw HTML content from a given URL using built-in Python libraries.
    """
    try:
        # Create an unverified context to handle common SSL certificate issues
        ssl._create_default_https_context = ssl._create_unverified_context
        
        # Set a User-Agent to mimic a browser
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )
        
        # Use a timeout for stability
        with urllib.request.urlopen(req, timeout=15) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            print(f"[INFO] Successfully fetched HTML content from {url}")
            return html_content
            
    except urllib.error.URLError as e:
        print(f"[ERROR] Could not reach the URL or connection error: {e.reason}")
        return None
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred during fetching: {e}")
        return None

def get_patterns_for_url(url):
    """
    Determines the appropriate scraping patterns based on the target URL.
    This is based on the HTML snippets you provided.
    """
    url_lower = url.lower()
    
    # Default to generic patterns if site is unknown or for testing static pages
    title_tag, title_class, price_tag, price_class, price_regex = 'h2', '', 'span', '', r'[\$₹]\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'

    # --- TIRA PATTERNS (Based on your provided snippets) ---
    if 'tira' in url_lower:
        title_tag, title_class = 'h1', r'id=["\']item_name["\']'
        price_tag, price_class = 'span', r'id=["\']item_price["\']'
        price_regex = r'₹\s*(\d+)' # Matches the simple '₹379' format
        print("[INFO] Using Tira-specific patterns.")

    # --- AMAZON PATTERNS (Based on your provided snippets) ---
    elif 'amazon' in url_lower:
        # Note: Amazon title is found by ID and class; price by class.
        title_tag, title_class = 'span', r'id=["\']productTitle["\']'
        price_tag, price_class = 'span', r'class=["\']a-price-whole["\']'
        price_regex = r'(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)' # Matches the simple '379' format
        print("[INFO] Using Amazon-specific patterns.")
        
    # --- PURPLLE PATTERNS (Based on your provided snippets) ---
    elif 'purplle' in url_lower:
        # Note: Purplle title is in a span with a specific class; price in a strong tag.
        title_tag, title_class = 'span', r'class=["\']fw-bold ng-star-inserted["\']'
        price_tag, price_class = 'strong', r'class=["\']our-price text-dark-secondary["\']'
        price_regex = r'₹\s*(\d+)'
        print("[INFO] Using Purplle-specific patterns.")
        
    # --- NYKAA PATTERNS (Based on previous user input) ---
    elif 'nykaa' in url_lower:
        title_tag, title_class = 'h1', r'class=["\']css-1gc4x7i["\']'
        price_tag, price_class = 'span', r'class=["\']css-1jczs19["\']'
        price_regex = r'[\$₹]\s*(\d+)' 
        print("[INFO] Using Nykaa-specific patterns.")

    # Generate the full regex patterns
    full_title_pattern = rf'<{title_tag}[^>]*{title_class}[^>]*>(.*?)</{title_tag}>'
    full_price_pattern = rf'<{price_tag}[^>]*{price_class}[^>]*>.*?' + price_regex + rf'.*?</{price_tag}>'

    return full_title_pattern, full_price_pattern

def scrape_and_present_data(html_content, url):
    """
    Extracts the page title and simulates scraping product titles and prices
    using targeted class names specific to e-commerce structures.
    """
    if not html_content:
        return

    print("\n" + "="*70)
    print("      TARGETED COSMETICS PRODUCT SCRAPING RESULTS")
    print("="*70)
    
    # 1. Extract the Page Title
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
    page_title = title_match.group(1).strip() if title_match else "Not Found"
    print(f"PAGE TITLE: {page_title}")
        
    print("-" * 70)
    print("SCRAPED COSMETIC PRODUCT LISTINGS:")
    
    # --- MODIFICATION AREA: TARGETING SPECIFIC HTML CLASSES ---
    
    # Get the correct patterns based on the URL
    title_pattern_str, price_pattern_str = get_patterns_for_url(url)
    
    title_pattern = re.compile(title_pattern_str, re.IGNORECASE | re.DOTALL)
    price_pattern = re.compile(price_pattern_str, re.IGNORECASE | re.DOTALL)

    product_titles = [t.strip() for t in title_pattern.findall(html_content) if t.strip()]
    
    # The price pattern captures the price amount in the last group
    price_matches = price_pattern.findall(html_content)
    # If the price regex has a capture group for the amount, use the group, otherwise use the whole match.
    product_prices = [match[-1].strip() for match in price_matches]

    # 2. Present the Data in a User-Friendly, Structured Format
    
    num_items = min(len(product_titles), len(product_prices), 5) # Limit to 5 results for clarity

    if num_items > 0:
        print("{:<5} {:<45} {:<15}".format("ID", "Product Title (Cosmetics)", "Price"))
        print("-" * 70)
        
        for i in range(num_items):
            # Clean up the title by removing any nested HTML (like the span for volume)
            clean_title = re.sub(r'<[^>]+>', '', product_titles[i]).strip()
            
            title = clean_title[:40] + '...' if len(clean_title) > 40 else clean_title
            # Price captured from the regex, which should include the currency symbol
            price = product_prices[i].strip() if product_prices[i].strip() else "N/A"
            print(f"{i+1:<5} {title:<45} {price:<15}")
    else:
        print("  Could not find clear, structured product titles or prices using the defined patterns.")
        print("  This often happens when content is loaded via JavaScript (dynamic content) after the initial fetch.")
        
    print("="*70)

def main():
    """
    Main application loop for the interactive web scraper.
    """
    print("Welcome to the Interactive Cosmetic Product Scraper Simulator!")
    print("The scraper is now configured to try patterns for Tira, Amazon, Purplle, and Nykaa.")

    while True:
        url_input = input("\nEnter the URL to scrape (e.g., https://tira.com/product/xyz) or type 'exit' to quit: ").strip()
        
        if url_input.lower() == 'exit':
            print("\nExiting the Web Scraper. Goodbye!")
            break

        if not url_input.startswith(('http://', 'https://')):
            url_input = 'https://' + url_input
            
        print(f"\nAttempting to fetch: {url_input}")
        
        # Fetch and process
        html_content = fetch_html(url_input)
        scrape_and_present_data(html_content, url_input)

# --- Execution Block ---
if __name__ == "__main__":
    main()
