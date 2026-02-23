#!/usr/bin/env python3
"""
Test script for Whoogle search parsing.
"""

import requests
from bs4 import BeautifulSoup

WHOOGLE_URL = "http://localhost:8080"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def test_single_search():
    """Test a single search query"""
    query = "Plant PWR Colombia"
    search_url = f"{WHOOGLE_URL}/search"
    params = {'q': query, 'num': 5}
    
    print(f"🔍 Testing search for: '{query}'")
    
    try:
        response = requests.get(search_url, params=params, headers=HEADERS, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ Error: HTTP {response.status_code}")
            return
        
        # Save HTML for debugging
        with open('/tmp/whoogle_test.html', 'w') as f:
            f.write(response.text)
        print("✅ HTML saved to /tmp/whoogle_test.html")
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find result containers - filter out "People also search for" and other non-result divs
        result_containers = soup.find_all('div', class_='ZINbbc xpd EtOod pkphOe')
        
        # Filter to only include results that have actual search result structure
        actual_results = []
        for container in result_containers:
            # Check if this is a search result (has title and URL)
            title_elem = container.find('h3', class_='zBAuLc')
            link_elem = container.find('a', href=True)
            
            # Skip if it's "People also search for" or other non-result sections
            if container.find('details') or container.find('summary'):
                continue
                
            # Skip if it's an image section
            if container.find('span', class_='cAuxJf'):
                continue
                
            if title_elem and link_elem and link_elem['href'].startswith('http'):
                actual_results.append(container)
        
        print(f"✅ Found {len(actual_results)} actual search results (filtered from {len(result_containers)} total containers)")
        
        # Parse first few results
        for i, container in enumerate(actual_results[:5]):
            print(f"\n📄 Result {i+1}:")
            
            # Extract title
            title_elem = container.find('h3', class_='zBAuLc')
            if title_elem:
                title_div = title_elem.find('div', class_='ilUpNd UFvD1 aSRlid')
                if title_div:
                    print(f"   📝 Title: {title_div.get_text(strip=True)[:80]}...")
                else:
                    print(f"   📝 Title: {title_elem.get_text(strip=True)[:80]}...")
            
            # Extract URL - look for all links
            link_elems = container.find_all('a', href=True)
            external_url = None
            
            for link in link_elems:
                href = link['href']
                # Check if it looks like an external URL (contains common domains)
                if any(domain in href for domain in ['plantpwr', 'instagram', 'facebook', 'mercadolibre', 'ispetshope']):
                    external_url = href
                    break
                # Also check for http/https URLs
                elif href.startswith('http') and not href.startswith('http://localhost'):
                    external_url = href
                    break
            
            if external_url:
                print(f"   🔗 URL: {external_url}")
                
                # Extract domain
                from urllib.parse import urlparse
                try:
                    parsed = urlparse(external_url)
                    if parsed.netloc:
                        print(f"   🌐 Domain: {parsed.netloc}")
                except:
                    print(f"   🌐 Could not parse URL")
            else:
                # Show what links we found
                if link_elems:
                    print(f"   🔗 Links found: {len(link_elems)}")
                    for i, link in enumerate(link_elems[:2]):
                        print(f"      Link {i+1}: {link['href'][:80]}...")
                else:
                    print(f"   🔗 No links found")
            
            # Extract snippet
            snippet_elem = container.find('div', class_='ilUpNd H66NU aSRlid')
            if snippet_elem:
                snippet_text = snippet_elem.get_text(strip=True)
                # Filter out date information
                if '·' in snippet_text:
                    snippet_text = snippet_text.split('·', 1)[-1].strip()
                print(f"   📋 Snippet: {snippet_text[:100]}...")
            
            # Extract display URL
            url_elem = container.find('div', class_='ilUpNd BamJPe aSRlid XR4uSe')
            if url_elem:
                print(f"   📍 Display URL: {url_elem.get_text(strip=True)}")
        
        print(f"\n🎯 Total actual results found: {len(actual_results)}")
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_single_search()