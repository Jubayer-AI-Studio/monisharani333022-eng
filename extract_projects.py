import re

with open(r'C:\Users\ASSDI\.gemini\antigravity\brain\d575d19d-2024-413b-9428-b88fc2565794\.system_generated\steps\604\content.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="projects"')
if idx != -1:
    end_idx = text.find('</section>', idx)
    chunk = text[idx:end_idx]
    clean = re.sub(r'<[^>]+>', '\n', chunk)
    lines = [l.strip() for l in clean.split('\n') if l.strip()]
    print('\n'.join(lines))
