#!/usr/bin/env python3
"""
Final test of Whoogle search for Plant PWR.
"""

import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse

WHOOGLE_URL = "http://localhost:8080"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def search_plant_pwr():
    """Search for Plant PWR information"""
    queries = [
        "Plant PWR Colombia",
        "Plant PWR gotas perros",
        "aceite cannabis mascotas Colombia"
    ]
    
    all_results = []
    
    for query in queries:
        print(f"\n🔍 Searching: '{query}'")
        
        search_url = f"{WHOOGLE_URL}/search"
        params = {'q': query, 'num': 5}
        
        try:
            response = requests.get(search_url, params=params, headers=HEADERS, timeout=15)
            
            if response.status_code != 200:
                print(f"❌ Error: HTTP {response.status_code}")
                continue
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all divs with class ZINbbc
            result_containers = soup.find_all('div', class_='ZINbbc')
            
            for container in result_containers:
                # Skip non-result sections
                if container.find('details') or container.find('summary'):
                    continue
                    
                if container.find('span', class_='cAuxJf'):
                    continue
                
                # Extract title
                title_elem = container.find('h3', class_='zBAuLc')
                if not title_elem:
                    continue
                    
                title_div = title_elem.find('div', class_='ilUpNd UFvD1 aSRlid')
                if title_div:
                    title = title_div.get_text(strip=True)
                else:
                    title = title_elem.get_text(strip=True)
                
                # Extract URL
                link_elems = container.find_all('a', href=True)
                external_url = None
                
                for link in link_elems:
                    href = link['href']
                    if href.startswith('http') and not href.startswith('http://localhost'):
                        external_url = href
                        break
                
                if not external_url:
                    continue
                
                # Extract snippet
                snippet_elem = container.find('div', class_='ilUpNd H66NU aSRlid')
                snippet = ""
                if snippet_elem:
                    snippet_text = snippet_elem.get_text(strip=True)
                    if '·' in snippet_text:
                        snippet_text = snippet_text.split('·', 1)[-1].strip()
                    snippet = snippet_text[:200]
                
                # Extract display URL
                url_elem = container.find('div', class_='ilUpNd BamJPe aSRlid XR4uSe')
                display_url = ""
                if url_elem:
                    display_url = url_elem.get_text(strip=True)
                
                # Extract domain
                domain = ""
                try:
                    parsed = urlparse(external_url)
                    domain = parsed.netloc
                except:
                    domain = "unknown"
                
                result = {
                    'query': query,
                    'title': title,
                    'url': external_url,
                    'domain': domain,
                    'display_url': display_url,
                    'snippet': snippet
                }
                
                # Check if this is a duplicate
                is_duplicate = False
                for existing in all_results:
                    if existing['url'] == external_url:
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    all_results.append(result)
                    print(f"   ✅ Found: {title[:60]}...")
                    print(f"      🔗 {external_url}")
            
        except Exception as e:
            print(f"❌ Error searching '{query}': {type(e).__name__}: {e}")
    
    return all_results

if __name__ == "__main__":
    print("="*70)
    print("🔎 WHOOGLE SEARCH TEST - PLANT PWR INVESTIGATION")
    print("="*70)
    
    results = search_plant_pwr()
    
    print(f"\n{'='*70}")
    print(f"📊 SEARCH RESULTS SUMMARY")
    print(f"{'='*70}")
    print(f"Total unique results found: {len(results)}")
    
    # Group by domain
    domains = {}
    for result in results:
        domain = result['domain']
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(result)
    
    print(f"\n📈 Results by domain:")
    for domain, domain_results in sorted(domains.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"   {domain}: {len(domain_results)} results")
    
    # Save results to file
    output_file = "/root/.openclaw/workspace/plant-pwr-investigation/evidencia/whoogle_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    # Show top results
    print(f"\n🏆 TOP 5 RESULTS:")
    for i, result in enumerate(results[:5]):
        print(f"\n{i+1}. {result['title'][:80]}...")
        print(f"   🔗 {result['url']}")
        print(f"   📍 {result['domain']}")
        if result['snippet']:
            print(f"   📋 {result['snippet'][:100]}...")