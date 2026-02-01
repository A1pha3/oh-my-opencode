import os
import re
import sys

def get_anchors(file_path):
    if not os.path.exists(file_path):
        return set()
    anchors = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'^#+\s+(.*)', line)
            if match:
                header = match.group(1).strip().lower()
                # Simple markdown anchor conversion
                anchor = header.replace(' ', '-').replace('?', '').replace('!', '').replace('(', '').replace(')', '').replace('.', '').replace('：', '').replace(':', '')
                # Handle Chinese characters and other punctuations if needed, but simple replacement is often enough for basic checks
                anchors.add(anchor)
                # Also add the raw version for some implementations
                anchors.add(header.replace(' ', '-'))
    return anchors

def check_links(file_path, root_dir):
    issues = []
    if not os.path.exists(file_path):
        return [f"File not found: {file_path}"]
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex for [text](link)
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    
    current_dir = os.path.dirname(file_path)
    
    for text, link in links:
        if link.startswith('http') or link.startswith('mailto:'):
            continue
        
        target_path = link.split('#')[0]
        anchor = link.split('#')[1] if '#' in link else None
        
        full_target_path = ""
        if target_path == "":
            full_target_path = file_path
        else:
            full_target_path = os.path.normpath(os.path.join(current_dir, target_path))
        
        if not os.path.exists(full_target_path):
            issues.append(f"Broken link: [{text}]({link}) -> {full_target_path} (File not found)")
            continue
        
        if anchor:
            # We would need a more robust anchor checker for Chinese headers
            # But let's skip for now or implement a basic one
            pass

    return issues

files = [
    "README.zh-cn.md",
    "docs/zh-CN/README.md",
    "docs/zh-CN/category-skill-guide.md",
    "docs/zh-CN/cli-guide.md",
    "docs/zh-CN/configurations.md",
    "docs/zh-CN/features.md",
    "docs/zh-CN/orchestration-guide.md",
    "docs/zh-CN/ultrawork-manifesto.md",
    "docs/zh-CN/architecture/core-principles.md",
    "docs/zh-CN/best-practices/development.md",
    "docs/zh-CN/features/complete-reference.md",
    "docs/zh-CN/guide/installation.md",
    "docs/zh-CN/guide/quickstart.md",
    "docs/zh-CN/troubleshooting/faq.md"
]

root = "/Volumes/mini_matrix/github/a1pha3/oh-my-opencode"
for f in files:
    path = os.path.join(root, f)
    print(f"Checking {f}...")
    issues = check_links(path, root)
    for issue in issues:
        print(f"  {issue}")

