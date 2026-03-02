import re
import os
import time
from collections import defaultdict
from tqdm import tqdm

# 文件名配置
EN_FILE = 'shieldbreaker.string_table-EN.xml'
CN_FILE = 'shieldbreaker.string_table-CN.xml'
OUTPUT_FILE = 'shieldbreaker.string_table.xml'


def read_file_fast(file_path):
    """快速读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_entries_fast(content):
    """使用更高效的方式提取条目"""
    # 一次性找到所有匹配
    pattern = re.compile(r'<entry id="(.*?)"><!\[CDATA\[(.*?)\]\]></entry>', re.DOTALL)
    return pattern.findall(content)


def merge_localization_with_progress():
    print("=" * 50)
    print("🚀 开始合并翻译文件（带进度条版）")
    print("=" * 50)

    # 检查文件是否存在
    if not os.path.exists(EN_FILE) or not os.path.exists(CN_FILE):
        print("❌ 错误：请确保文件夹内有对应的 EN 和 CN 文件！")
        return

    total_start_time = time.time()

    # 1. 快速读取文件
    print("\n📖 步骤1/5: 读取文件")
    read_start = time.time()

    cn_content = read_file_fast(CN_FILE)
    en_content = read_file_fast(EN_FILE)

    read_time = time.time() - read_start
    print(f"✅ 文件读取完成，耗时: {read_time:.3f} 秒")

    # 2. 提取所有条目
    print("\n🔍 步骤2/5: 提取条目")
    extract_start = time.time()

    cn_matches = extract_entries_fast(cn_content)
    en_matches = extract_entries_fast(en_content)

    extract_time = time.time() - extract_start
    print(f"✅ 条目提取完成，英文: {len(en_matches)}条，中文: {len(cn_matches)}条，耗时: {extract_time:.3f} 秒")

    # 3. 构建中文索引映射
    print("\n🗺️  步骤3/5: 构建索引映射")
    index_start = time.time()

    cn_translations = defaultdict(list)
    for eid, text in tqdm(cn_matches, desc="处理中文条目", unit="条", leave=False):
        cn_translations[eid].append(text)

    index_time = time.time() - index_start
    print(f"✅ 索引构建完成，共 {len(cn_translations)} 个唯一ID，耗时: {index_time:.3f} 秒")

    # 4. 合并翻译
    print("\n🔄 步骤4/5: 合并翻译")
    merge_start = time.time()

    new_entries = [''] * len(en_matches)
    match_count = 0
    id_counters = {}

    # 使用tqdm显示合并进度
    for i, (en_id, en_text) in enumerate(tqdm(en_matches, desc="合并翻译", unit="条")):
        if en_id in cn_translations:
            translations = cn_translations[en_id]
            counter = id_counters.get(en_id, 0)

            if counter < len(translations):
                new_text = translations[counter]
                id_counters[en_id] = counter + 1
                match_count += 1
            else:
                new_text = translations[-1]

            new_entries[i] = f'<entry id="{en_id}"><![CDATA[{new_text}]]></entry>'
        else:
            new_entries[i] = f'<entry id="{en_id}"><![CDATA[{en_text}]]></entry>'

    merge_time = time.time() - merge_start
    print(f"\n✅ 合并完成，匹配: {match_count}条，耗时: {merge_time:.3f} 秒")

    # 5. 生成输出文件
    print("\n💾 步骤5/5: 生成输出文件")
    write_start = time.time()

    # 提取XML结构
    header_end = en_content.find('<entries>')
    footer_start = en_content.find('</entries>')

    if header_end != -1:
        header = en_content[:header_end]
        footer = en_content[footer_start + 9:]  # 9是'</entries>'的长度
    else:
        header = '<?xml version="1.0" encoding="utf-8"?>\n<root>\n'
        footer = '</root>'

    # 构建最终内容
    entries_xml = '\n'.join(new_entries)
    new_content = f'{header}<entries>\n{entries_xml}\n</entries>{footer}'

    # 写入文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    write_time = time.time() - write_start
    total_time = time.time() - total_start_time

    print(f"✅ 文件写入完成，耗时: {write_time:.3f} 秒")

    # 显示统计信息
    print("\n" + "=" * 50)
    print("🎉 处理完成！性能统计：")
    print("=" * 50)
    print(f"📊 英文条目: {len(en_matches)} 条")
    print(f"📊 中文条目: {len(cn_matches)} 条")
    print(f"📊 唯一ID数: {len(cn_translations)} 个")
    print(f"📊 成功迁移: {match_count} 条")
    print(f"📊 保留原文: {len(en_matches) - match_count} 条")
    print("\n⏱️  耗时明细：")
    print(f"   读取文件: {read_time:.3f} 秒")
    print(f"   提取条目: {extract_time:.3f} 秒")
    print(f"   构建索引: {index_time:.3f} 秒")
    print(f"   合并翻译: {merge_time:.3f} 秒")
    print(f"   写入文件: {write_time:.3f} 秒")
    print(f"   {'=' * 20}")
    print(f"   总耗时: {total_time:.3f} 秒")
    print("=" * 50)
    print(f"💾 输出文件: {OUTPUT_FILE}")
    print("=" * 50)


# 如果没有tqdm库，提供一个备用版本
def merge_localization_fallback():
    """无tqdm时的备用版本"""
    print("=" * 50)
    print("🚀 开始合并翻译文件（简化版）")
    print("=" * 50)

    if not os.path.exists(EN_FILE) or not os.path.exists(CN_FILE):
        print("❌ 错误：请确保文件夹内有对应的 EN 和 CN 文件！")
        return

    total_start_time = time.time()

    # 读取文件
    cn_content = read_file_fast(CN_FILE)
    en_content = read_file_fast(EN_FILE)

    # 提取条目
    cn_matches = extract_entries_fast(cn_content)
    en_matches = extract_entries_fast(en_content)

    print(f"📊 英文条目: {len(en_matches)}条，中文条目: {len(cn_matches)}条")

    # 构建索引
    cn_translations = defaultdict(list)
    for eid, text in cn_matches:
        cn_translations[eid].append(text)

    # 合并翻译
    new_entries = [''] * len(en_matches)
    match_count = 0
    id_counters = {}

    for i, (en_id, en_text) in enumerate(en_matches):
        if i % 100 == 0 and i > 0:  # 每100条显示一次进度
            print(f"  处理进度: {i}/{len(en_matches)} 条 ({i / len(en_matches) * 100:.1f}%)")

        if en_id in cn_translations:
            translations = cn_translations[en_id]
            counter = id_counters.get(en_id, 0)

            if counter < len(translations):
                new_text = translations[counter]
                id_counters[en_id] = counter + 1
                match_count += 1
            else:
                new_text = translations[-1]

            new_entries[i] = f'<entry id="{en_id}"><![CDATA[{new_text}]]></entry>'
        else:
            new_entries[i] = f'<entry id="{en_id}"><![CDATA[{en_text}]]></entry>'

    # 生成输出文件
    header_end = en_content.find('<entries>')
    footer_start = en_content.find('</entries>')

    if header_end != -1:
        header = en_content[:header_end]
        footer = en_content[footer_start + 9:]
    else:
        header = '<?xml version="1.0" encoding="utf-8"?>\n<root>\n'
        footer = '</root>'

    entries_xml = '\n'.join(new_entries)
    new_content = f'{header}<entries>\n{entries_xml}\n</entries>{footer}'

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    total_time = time.time() - total_start_time

    print("\n" + "=" * 50)
    print("🎉 处理完成！")
    print("=" * 50)
    print(f"📊 成功迁移: {match_count} 条")
    print(f"⏱️  总耗时: {total_time:.3f} 秒")
    print(f"💾 输出文件: {OUTPUT_FILE}")
    print("=" * 50)


if __name__ == "__main__":
    try:
        # 尝试使用tqdm版本
        from tqdm import tqdm

        merge_localization_with_progress()
    except ImportError:
        print("⚠️  未安装tqdm库，使用简化版进度显示")
        print("💡 提示: 可以通过 'pip install tqdm' 安装以获得更好的进度条效果\n")
        merge_localization_fallback()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断处理程序")
    except Exception as e:
        print(f"\n❌ 处理过程中出现错误: {str(e)}")
        import traceback

        traceback.print_exc()
    finally:
        print("\n👋 程序结束")