# darkest-dungeon-translation-merge
一个用于《暗黑地牢：darkestdungeon》模组翻译迁移的Python脚本。当模组更新后，可以将旧版的中文翻译快速应用到新版文件上，避免手动复制粘贴的繁琐工作。

# 解决的问题：
《暗黑地牢》模组更新时，string_table-EN.xml 文件通常会有改动（新增条目、修改ID等），而之前翻译好的中文文件无法直接使用。本工具可以：

➙读取新版英文文件和旧版中文文件

➙根据条目ID自动匹配翻译

➙生成合并后的文件，保留未翻译条目的英文原文

➙支持同一个ID对应多条翻译的情况（按顺序匹配）

# 环境要求：
Python 3.6 或更高版本

无需安装额外依赖，使用Python标准库即可运行

# 具体用法：

▶step 1（准备文件）：
-
将以下两个文件放在同一个文件夹内：

XX-EN.xml：新版英文文件（你想要翻译的目标文件）

XX-CN.xml：旧版中文文件（你想要复用的翻译来源）

例如：shieldbreaker.string_table-EN.xml 和 shieldbreaker.string_table-CN.xml

▶step 2（修改脚本）：
-
用记事本或其他编辑器打开 merge.py，找到文件开头的这三行：

```python
EN_FILE = 'shieldbreaker.string_table-EN.xml'    # 改为你的未翻译的文件名
CN_FILE = 'shieldbreaker.string_table-CN.xml'    # 改为你的想要提取的翻译的文件名
OUTPUT_FILE = 'shieldbreaker.string_table.xml'   # 合并的文件名（可自定义）
```

▶step 3（运行脚本）：
-
在文件所在目录打开命令行（CMD/终端），执行：

```python
python merge.py
```

即可获得翻译文件文件

# 示例场景

假设你的模组从 1.0 版更新到 2.0 版：

你有 1.0 版翻译好的 shieldbreaker.string_table-CN.xml

你下载了 2.0 版的 shieldbreaker.string_table-EN.xml

运行本工具，直接得到 2.0 版的翻译文件

# 关于本文件

这个小工具是我在更新游戏模组时为了解决自己的需求而写的。如果你也用得上，或者有什么问题，欢迎在GitHub上交流。
