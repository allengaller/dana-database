#!/usr/bin/env python3
"""
dana "今天能做什么" 一键提取工具
扫描所有人物志/案例研究/心法，提取 "今天可以开始的 X 件事" 类章节，
生成 `索引/quick_start.md`，按板块分组，便于快速查找 actionable 建议。

用法：
  python tools/extract_actions.py            # 提取并写入 索引/quick_start.md
  python tools/extract_actions.py --scan     # 预览模式，不写入文件
  python tools/extract_actions.py --section 人物志   # 仅提取人物志
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit import ROOT, find_md_files, parse_frontmatter

# 匹配 "今天可以开始的 X 件事" 类章节标题
ACTION_PATTERNS = [
    re.compile(r'^#{1,4}\s*今天[可以能就]开始.{0,15}[1-9１-９].*?[事点条].*?$', re.MULTILINE),
    re.compile(r'^#{1,4}\s*今天[可以能就]做.{0,15}[1-9１-９].*?[事点条].*?$', re.MULTILINE),
    re.compile(r'^#{1,4}\s*[1-9１-９]\s*[个件条].*?今天.*?$', re.MULTILINE),
    re.compile(r'^#{1,4}\s*本周可以开始的.*$', re.MULTILINE),
    re.compile(r'^#{1,4}\s*立即行动.*?$', re.MULTILINE),
    re.compile(r'^#{1,4}\s*本季度可以做.*?$', re.MULTILINE),
    re.compile(r'^#{1,4}\s*可复制[的].*?行动.*?$', re.MULTILINE),
    re.compile(r'^#{1,4}\s*普通人今天.*?$', re.MULTILINE),
    re.compile(r'^#{1,4}\s*今天[，, ]?\d.*?件事?$', re.MULTILINE),
    re.compile(r'^#{1,4}\s*你[可以能]今天.*?$', re.MULTILINE),
]

# 列表项模式
LIST_ITEM = re.compile(r'^\s*[-*]\s+(.+?)$', re.MULTILINE)
NUM_LIST = re.compile(r'^\s*\d+[、.)]\s*(.+?)$', re.MULTILINE)


def find_action_section(content):
    """在文档中找到 actionable 章节及其内容"""
    # 找到所有可能的"今天可以开始"类标题
    matches = []
    for pattern in ACTION_PATTERNS:
        for m in pattern.finditer(content):
            matches.append(m)
    if not matches:
        return None

    # 取第一个匹配，取该标题后的内容到下一个同级或更高级标题
    first = matches[0]
    section_start = first.end()

    # 找下一个 ## 或 # 标题
    next_heading = re.search(r'^#{1,2}\s+', content[section_start:], re.MULTILINE)
    section_end = section_start + next_heading.start() if next_heading else len(content)

    section_content = content[section_start:section_end].strip()

    # 提取列表项
    items = []
    for m in LIST_ITEM.finditer(section_content):
        text = m.group(1).strip()
        # 跳过空项或纯格式项
        if text and len(text) > 5 and len(text) < 200:
            items.append(text)
    for m in NUM_LIST.finditer(section_content):
        text = m.group(1).strip()
        if text and len(text) > 5 and len(text) < 200:
            items.append(text)

    return items[:5] if items else None  # 最多 5 条


def collect_actions(section_filter=None):
    """收集所有 actionable 条目"""
    md_files = find_md_files()
    actions_by_section = defaultdict(list)

    for rel in md_files:
        rel_str = str(rel)
        top = rel.parts[0] if rel.parts else ''

        # 板块过滤
        if section_filter and top != section_filter:
            continue

        # 仅对人物志、心法、案例研究、富豪档生效
        if top not in {'人物志', '心法与原则', '案例研究', '富豪榜', '方法论与框架'}:
            continue

        content = (ROOT / rel).read_text(encoding='utf-8')
        items = find_action_section(content)
        if not items:
            continue

        fm = parse_frontmatter(content)
        title = fm.get('title', rel.stem) if fm else rel.stem

        actions_by_section[top].append({
            'title': title,
            'rel_path': rel,
            'items': items,
        })

    return actions_by_section


def render_quick_start(actions_by_section):
    """渲染 quick_start.md"""
    lines = [
        '---',
        'title: 今天能开始的 N 件事（自动汇总）',
        'tags:',
        '  - MOC',
        '  - 索引',
        '  - 行动',
        f'date: {os.environ.get("DANA_TODAY", "2026-07-26")}',
        '---',
        '',
        '# 今天能开始的 N 件事',
        '',
        '> **本页由 `tools/extract_actions.py` 自动汇总——从各篇人物志/心法/案例中抽取 actionable 建议。**',
        '>',
        '> 适合作为「今天 5 分钟」快速挑选器：随机翻一条，立刻去做。',
        '',
        f'**汇总时间**：{os.environ.get("DANA_TODAY", "今日")}',
        f'**总条目**：{sum(len(v) for v in actions_by_section.values())} 篇文档贡献了 actionable 建议',
        '',
        '---',
        '',
    ]

    SECTION_LABELS = {
        '人物志': '🌟 人物志（可复制路径）',
        '富豪榜': '💰 富豪榜（财富创造者行动）',
        '心法与原则': '🧠 心法与原则（心智模型行动）',
        '案例研究': '📖 案例研究（真实成长复盘）',
        '方法论与框架': '🔧 方法论与框架（工具性行动）',
    }

    for section_key in ['人物志', '富豪榜', '心法与原则', '案例研究', '方法论与框架']:
        if section_key not in actions_by_section:
            continue
        items = actions_by_section[section_key]
        lines.append(f'## {SECTION_LABELS.get(section_key, section_key)}')
        lines.append('')

        # 按 title 排序
        items_sorted = sorted(items, key=lambda x: x['title'])

        for item in items_sorted[:25]:  # 每个板块最多 25 篇
            rel = item['rel_path']
            if isinstance(rel, Path):
                link = str(rel.with_suffix(''))
            else:
                link = str(rel)
                if link.endswith('.md'):
                    link = link[:-3]
            lines.append(f'### {item["title"]}')
            lines.append(f'[[{link}]]')
            lines.append('')
            for action in item['items']:
                # 截断过长的文本
                text = action[:180] + ('...' if len(action) > 180 else '')
                lines.append(f'- {text}')
            lines.append('')

        if len(items) > 25:
            lines.append(f'> 📚 还有 {len(items) - 25} 篇……完整列表见原板块。')
            lines.append('')

    lines.append('---')
    lines.append('')
    lines.append('## 怎么用？')
    lines.append('')
    lines.append('1. **每天选 1 条**：从本页随机（或按当天心情）选一条，立即开始')
    lines.append('2. **每周复盘**：每周日 review 这周做了什么，做标记')
    lines.append('3. **季度回顾**：每季度 review 哪些 advice 真的有用，哪些是"听起来对但做不到"')
    lines.append('')
    lines.append('## 维护')
    lines.append('')
    lines.append('- 生成命令：`python tools/extract_actions.py`')
    lines.append('- 自动同步：CI 中每月 1 日自动重新生成（待接入）')
    lines.append('- 反馈：如发现抽取有误，请在 Issue 中说明')
    lines.append('')

    return '\n'.join(lines)


def main():
    args = sys.argv[1:]
    if '--help' in args or '-h' in args:
        print(__doc__)
        sys.exit(0)

    scan_only = '--scan' in args
    section_filter = None
    if '--section' in args:
        idx = args.index('--section')
        section_filter = args[idx + 1] if idx + 1 < len(args) else None

    print('=' * 60)
    print('⚡ 提取 "今天能做什么" actionable 建议')
    print('=' * 60)

    actions = collect_actions(section_filter)
    total = sum(len(v) for v in actions.values())
    total_items = sum(len(item['items']) for v in actions.values() for item in v)
    print(f'\n📊 统计：')
    for section, items in sorted(actions.items()):
        print(f'   {section}: {len(items)} 篇文档, {sum(len(i["items"]) for i in items)} 条建议')
    print(f'   合计: {total} 篇文档, {total_items} 条 actionable 建议')

    if scan_only:
        print('\n📋 预览模式（前 10 条）：')
        count = 0
        for section, items in actions.items():
            for item in items:
                for action in item['items']:
                    print(f'   [{section}] {action[:80]}')
                    count += 1
                    if count >= 10:
                        break
                if count >= 10:
                    break
            if count >= 10:
                break
        return

    output = ROOT / '索引' / 'quick_start.md'
    output.write_text(render_quick_start(actions), encoding='utf-8')
    print(f'\n✅ 已生成 {output.relative_to(ROOT)}')
    print(f'   共索引 {total} 篇文档的 actionable 建议')


if __name__ == '__main__':
    main()