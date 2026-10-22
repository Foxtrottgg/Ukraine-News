import feedparser
import json
import re

def clean_html(raw_html):
    """Entfernt HTML-Tags und störende Codes (wie &nbsp;) aus dem Text."""
    # HTML-Tags entfernen
    cleanr = re.compile('<.*?>')
    cleared = re.sub(cleanr, '', raw_html)
    
    # Häufige HTML-Entities ersetzen
    cleared = cleared.replace('&nbsp;', ' ')
    cleared = cleared.replace('&amp;', '&')
    cleared = cleared.replace('&quot;', '"')
    cleared = cleared.replace('&#39;', "'")
    
    return cleared.strip()

def update_news_json():
    rss_url = 'https://news.google.com/rss/search?q=Ukraine+war&hl=en-US&gl=US&ceid=US:en'
    
    print("Lade und bereinige aktuelle Nachrichten...")
    feed = feedparser.parse(rss_url)
    
    news_list = []
    
    for index, entry in enumerate(feed.entries[:10]):
        raw_summary = entry.get('summary', 'Keine Vorschau verfügbar.')
        clean_summary = clean_html(raw_summary)[:180] + '...'
        
        # Auch den Titel bereinigen, falls dort HTML-Reste sind
        clean_title = clean_html(entry.get('title', 'Kein Titel'))
        
        news_item = {
            "id": index + 1,
            "category": "tech",
            "categoryLabel": "Live Wire",
            "time": "Vor wenigen Min.",
            "title": clean_title,
            "summary": clean_summary,
            "details": "Echtzeit-Meldung aus globalen Nachrichtenquellen.",
            "urgent": False,
            "link": entry.get('link', '#')
        }
        news_list.append(news_item)
    
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)
        
    print(f"Erfolgreich! {len(news_list)} Artikel sauber in 'news.json' gespeichert.")

if __name__ == '__main__':
    update_news_json()