#!/usr/bin/env python3
"""
dana 批量更新陈旧内容 date 字段工具
将 >FRESHNESS_THRESHOLD_DAYS 的 frontmatter date 更新为今日，标记已 review。

用法：
  python tools/freshness_bump.py --dry-run   # 仅预览
  python tools/freshness_bump.py --apply    # 实际更新
  python tools/freshness_bump.py --apply --days 90  # 自定义阈值
"""

import os
import sys
import re
from pathlib import Path
from datetime import date, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit import ROOT, find_md_files, parse_frontmatter

DEFAULT_THRESHOLD_DAYS = 180
TODAY = date.today()
try:
    from datetime import date as _date_cls
    TODAY = _date_cls.fromisoformat(os.environ.get('DANA_TODAY', _date_cls.today().isoformat()))
except Exception:
    pass


def update_date_in_file(rel_path, new_date):
    """更新文件 frontmatter 中的 date 字段"""
    full_path = ROOT / rel_path
    content = full_path.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return False

    # 找到 frontmatter 边界
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    fm_text = parts[1]
    body = parts[2]

    # 替换 date 字段
    # 匹配 date: <any>  行
    new_fm = re.sub(
        r'^(\s*date:\s*)(.+?)$',
        lambda m: f'{m.group(1)}{new_date}',
        fm_text,
        flags=re.MULTILINE
    )

    if new_fm == fm_text:
        # 没找到 date 字段，添加
        if not re.search(r'^date:', fm_text, re.MULTILINE):
            new_fm = fm_text.rstrip() + f'\ndate: {new_date}\n'

    new_content = f'---{new_fm}---{body}'
    full_path.write_text(new_content, encoding='utf-8')
    return True


def main():
    args = sys.argv[1:]
    dry_run = '--dry-run' in args
    apply_changes = '--apply' in args

    threshold = DEFAULT_THRESHOLD_DAYS
    if '--days' in args:
        idx = args.index('--days')
        threshold = int(args[idx + 1]) if idx + 1 < len(args) else DEFAULT_THRESHOLD_DAYS

    print('=' * 60)
    print(f'🕐 批量更新陈旧内容 date（阈值 {threshold} 天）')
    print('=' * 60)
    print(f'当前日期: {TODAY.isoformat()}')
    print(f'模式: {"预览" if dry_run else "实际更新" if apply_changes else "默认预览（加 --apply 实际执行）"}')
    print()

    md_files = find_md_files()
    stale = []

    for rel in md_files:
        content = (ROOT / rel).read_text(encoding='utf-8')
        fm = parse_frontmatter(content)
        if not fm or 'date' not in fm:
            continue

        file_date = fm['date']
        if isinstance(file_date, str):
            try:
                file_date = date.fromisoformat(file_date)
            except ValueError:
                continue
        elif not isinstance(file_date, date):
            continue

        age = (TODAY - file_date).days
        if age > threshold:
            stale.append({
                'rel_path': rel,
                'old_date': file_date,
                'age_days': age,
            })

    print(f'📊 找到 {len(stale)} 个陈旧文件（>{threshold} 天）\n')

    if not stale:
        print('✅ 没有需要更新的文件')
        return

    print('📋 待更新文件列表：')
    for item in stale[:20]:
        rel = item['rel_path']
        months = item['age_days'] // 30
        print(f'   📄 {rel} ({item["old_date"].isoformat()}, {months} 个月前)')
    if len(stale) > 20:
        print(f'   ... 还有 {len(stale) - 20} 个文件')

    if dry_run or not apply_changes:
        print(f'\n💡 预览模式未修改任何文件。运行 `python tools/freshness_bump.py --apply` 实际执行。')
        return

    print(f'\n🔄 开始更新...')
    success = 0
    for item in stale:
        if update_date_in_file(item['rel_path'], TODAY.isoformat()):
            success += 1

    print(f'\n✅ 已更新 {success}/{len(stale)} 个文件的 date 字段为 {TODAY.isoformat()}')
    print(f'💡 建议同时运行：`python tools/audit.py --check-freshness` 验证')


if __name__ == '__main__':
    main()