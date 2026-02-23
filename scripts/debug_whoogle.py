#!/usr/bin/env python3
"""
Debug script for Whoogle search parsing.
"""

import requests
from bs4 import BeautifulSoup

WHOOGLE_URL = "http://localhost:8080"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def debug_search():
    """Debug a single search query"""
    query = "Plant PWR Colombia"
    search_url = f"{WHOOGLE_URL}/search"
    params = {'q': query, 'num': 5}
    
    print(f"🔍 Debugging search for: '{query}'")
    
    try:
        response = requests.get(search_url, params=params, headers=HEADERS, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ Error: HTTP {response.status_code}")
            return
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find ALL divs with class ZINbbc
        all_divs = soup.find_all('div', class_='ZINbbc')
        print(f"📊 Found {len(all_divs)} divs with class ZINbbc")
        
        # Check each div
        for i, div in enumerate(all_divs[:10]):  # First 10 only
            print(f"\n{'='*60}")
            print(f"📄 Div {i+1}:")
            print(f"{'='*60}")
            
            # Get classes
            classes = div.get('class', [])
            print(f"   Classes: {classes}")
            
            # Check for specific elements
            h3_elements = div.find_all('h3')
            print(f"   H3 elements: {len(h3_elements)}")
            for h3 in h3_elements:
                print(f"      H3 text: {h3.get_text(strip=True)[:100]}...")
                print(f"      H3 classes: {h3.get('class', [])}")
            
            # Check for links
            links = div.find_all('a', href=True)
            print(f"   Links: {len(links)}")
            for link in links[:3]:  # First 3 links only
                href = link['href']
                print(f"      Link href: {href[:100]}...")
                print(f"      Link text: {link.get_text(strip=True)[:50]}...")
            
            # Check for text content
            text = div.get_text(strip=True)
            if len(text) > 0:
                print(f"   Text preview: {text[:150]}...")
        
        # Now look specifically for search results
        print(f"\n{'='*60}")
        print(f"🔍 LOOKING FOR SPECIFIC SEARCH RESULTS")
        print(f"{'='*60}")
        
        # Look for divs that contain both h3 and external links
        potential_results = []
        for div in all_divs:
            h3 = div.find('h3')
            links = div.find_all('a', href=True)
            external_links = [l for l in links if 'plantpwr' in l['href'] or 'instagram' in l['href'] or 'facebook' in l['href']]
            
            if h3 and external_links:
                potential_results.append(div)
        
        print(f"🎯 Found {len(potential_results)} potential search results")
        
        for i, div in enumerate(potential_results[:5]):
            print(f"\n📄 Potential Result {i+1}:")
            
            # Get title from h3
            h3 = div.find('h3')
            if h3:
                print(f"   📝 Title: {h3.get_text(strip=True)[:100]}...")
            
            # Get external links
            links = div.find_all('a', href=True)
            for link in links:
                href = link['href']
                if any(domain in href for domain in ['plantpwr', 'instagram', 'facebook', 'mercadolibre', 'ispetshope']):
                    print(f"   🔗 External URL: {href}")
            
            # Get snippet
            snippet_div = div.find('div', class_='ilUpNd H66NU aSRlid')
            if snippet_div:
                print(f"   📋 Snippet: {snippet_div.get_text(strip=True)[:150]}...")
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    debug_search()