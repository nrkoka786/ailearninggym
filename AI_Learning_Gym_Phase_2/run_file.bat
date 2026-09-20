python -c "
import os
urls = []
base = 'https://ailearninggym.com'
root = r'C:\ailearninggym'
for dirpath, dirs, files in os.walk(root):
    dirs[:] = [d for d in dirs if d not in ['.git','node_modules']]
    for f in files:
        if f == 'index.html':
            rel = os.path.relpath(dirpath, root).replace(chr(92),'/')
            url = base + '/' + (rel + '/' if rel != '.' else '')
            urls.append(url)
xml = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n'
xml += '\n'.join(f'  <url><loc>{u}</loc></url>' for u in sorted(urls))
xml += '\n</urlset>'
open(r'C:\ailearninggym\sitemap.xml','w').write(xml)
print('Done -', len(urls), 'URLs')
"