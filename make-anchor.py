#!/usr/bin/env python3
import sys
import re
from typing import Callable
from os.path import basename, dirname, join, split
from pathlib import Path


def get_content_lines(
    md_file_path: str,
    is_toc_header: Callable[[str], bool],
    is_toc_end_header: Callable[[str], bool],
) -> tuple[int, list[str]]:
    """按行读取文件内容, 切除目录部分, 返回剩余的所有内容与新目录的插入位置"""

    def _remove_back_to_top_buttons(content_lines: list[str]) -> list[str]:
        button_positions = [idx for idx, line in enumerate(content_lines) if line.count("#toc")]
        button_positions.reverse()
        for button_position in button_positions:
            content_lines.pop(button_position - 1)  # 按钮前接的空行
            content_lines.pop(button_position - 1)  # 按钮
        return content_lines

    with open(md_file_path, encoding="utf8") as file:
        content_lines = [line[:-1] for line in file.readlines()]

    content_lines = _remove_back_to_top_buttons(content_lines)
    toc_begin_idx = None
    for idx, line in enumerate(content_lines):
        if is_toc_header(line):
            toc_begin_idx = idx
            break
    assert toc_begin_idx, "没有找到目录"
    toc_end_idx = None
    for idx in range(toc_begin_idx + 1, len(content_lines)):
        line = content_lines[idx]
        if is_toc_end_header(line):
            toc_end_idx = idx
            break
    assert toc_end_idx, "目录行以下需要另一个标题行来确定目录部分的范围"

    toc_insert_position = toc_begin_idx
    content_lines = content_lines[:toc_begin_idx] + content_lines[toc_end_idx:]

    return toc_insert_position, content_lines


def get_headers(content_lines: list[str]) -> tuple[list[str], list[int]]:
    """按顺序提取出所有标题行内容, 以及这些标题在原文中的行号"""
    headers = []
    header_positions = []
    for idx, line in enumerate(content_lines):
        if line and line[0] == "#":
            headers.append(line)
            header_positions.append(idx)
    return headers, header_positions


def clean_headers(headers: list[str]) -> list[str]:
    """清洗标题行中已有的锚点"""
    regex_clean_headers = re.compile(r"<a id=\"[0-9\.]+\"></a>")
    # regex_clean_headers = re.compile(r"<a id=\"[0-9\.]+\"></a>|</?details>|</?summary>")
    headers = [regex_clean_headers.sub(r"", header) for header in headers]
    # headers = [header for header in headers if header]
    return headers


# <details open="open"><summary>Table of Contents</summary>
# </details>
def insert_anchors(headers: list[str]) -> tuple[list[str], list[str]]:
    """向标题行文本中插入锚点, 同时生成对应的目录条目"""
    regex_get_header_info = re.compile(r"(#+) +(.+)")

    def _get_header_info(header: str) -> tuple[int, str]:
        header_match = regex_get_header_info.fullmatch(header)
        assert header_match, "分割标题内容失败"
        header_level = len(header_match.group(1))
        header_text = header_match.group(2)
        return header_level, header_text

    header_path: list[int] = []

    def _get_current_header_id() -> str:
        assert header_path, "当前还未遍历到任何标题行"
        current_header_id = ".".join([str(idx) for idx in header_path[1:]])
        return current_header_id

    def _get_anchor(current_header_id: str):
        return f'<a id="{current_header_id}"></a>'

    def _make_anchor_header(header_level: int, anchor: str, header_text: str):
        return f'{"#" * header_level} {anchor}{header_text}'

    # regex_get_reference = re.compile(r"([^$]*[^$ ])((?: *\$[^$]+\$ *)?)")
    regex_get_reference = re.compile(r"([^$]+)((?:\$[^$]+\$)?)")

    def _get_reference(current_header_id: str, header_text: str) -> str:
        reference = re.sub(regex_get_reference, rf'<a href="#{current_header_id}">\1</a>\2', header_text)
        return reference
        # return f'<a href="#{current_header_id}">{header_text}</a>'

    def _make_toc_entry(header_level: int, reference: str):
        # return f'{"  " * (header_level - 2)}- {reference}'
        return f'{"  " * (header_level - 3)}- {reference}'

    def _make_toc_entry_for_h2(reference: str, need_open: bool = False):
        open_str = ' open="open"' if need_open else ""
        return f"<details{open_str}><summary>{reference}</summary>"

    def _is_toc_entry_for_h2(toc_entry: str):
        if toc_entry.count("<summary>"):
            return True
        return False

    def _is_need_open(header_level: int, header_idx: int):
        # 耦合, 当且仅当二级标题为 data lab 时才展开:
        if header_level == 2 and header_idx == 1:
            return True
        return False

    def _get_initial_header_idx(header_level: int):
        # # 这里完全和 README.md 耦合在一起了, 因为二级标题第一个是 "注意事项", 下一个开始才是对应的 lab 的标题
        # if header_level == 2:
        #     return 0

        # 上面的机制取消, 因为为了文档整洁性决定把 "注意事项" 二级小节删掉了

        return 1

    def _insert_anchor(header: str) -> list[str]:
        header_level, header_text = _get_header_info(header)
        assert header_level <= len(header_path) + 1, "标题不能够一次下降两级以上"
        assert not (header_path and header_level == 1), "一级标题有且只能有一个"

        # 向上回溯标题树:
        while header_level < len(header_path):
            header_path.pop()

        # 如果是下级子标题:
        if len(header_path) < header_level:
            header_path.append(_get_initial_header_idx(header_level))

        # 如果是同级兄弟标题:
        else:
            header_path[-1] += 1

        current_header_id = _get_current_header_id()
        anchor = _get_anchor(current_header_id)
        reference = _get_reference(current_header_id, header_text)

        anchor_header = _make_anchor_header(header_level, anchor, header_text)
        toc_entry = _make_toc_entry(header_level, reference)
        if header_level == 2:
            header_idx = header_path[header_level - 1]
            is_need_open = _is_need_open(header_level=header_level, header_idx=header_idx)
            toc_entry = _make_toc_entry_for_h2(reference, is_need_open)

        # 取消对一级标题的链接:
        if header_level == 1:
            anchor_header = header
            toc_entry = ""

        return [anchor_header, toc_entry]

    anchor_headers, toc_entries = list(zip(*[_insert_anchor(header) for header in headers]))
    toc_entries = [toc_entry for toc_entry in toc_entries if toc_entry]

    # 耦合, 如果已经遇到过二级标题, 那么本二级标题作为该二级标题的范围的结尾需要插入一个 </summary> 标签:
    h2_begin_positions = [idx for idx, toc_entry in enumerate(toc_entries) if _is_toc_entry_for_h2(toc_entry)]
    if h2_begin_positions:
        h2_end_positions = h2_begin_positions.copy()
        h2_end_positions.pop(0)
        h2_end_positions.append(len(toc_entries))

        h2_begin_positions.reverse()
        h2_end_positions.reverse()
        for h2_begin_position, h2_end_position in zip(h2_begin_positions, h2_end_positions):
            toc_entries.insert(h2_end_position, "</details>")  # 折叠目录的闭合标签
            # 如果没有列表项需要折叠则直接跳过:
            if h2_begin_position + 1 == h2_end_position:
                continue
            toc_entries.insert(h2_end_position, "")  # 列表结尾的空行
            toc_entries.insert(h2_begin_position + 1, "")  # 列表开头的空行

    return list(anchor_headers), list(toc_entries)


def fill_in_new_headers_and_toc(
    content_lines: list[str],
    anchor_headers: list[str],
    header_positions: list[int],
    toc_insert_position: int,
    toc_entries: list[str],
    get_toc_header: Callable[[], str],
) -> list[str]:
    """替换标题行, 插入新目录, 返回新的 md 文本"""
    for anchor_header, header_position in zip(anchor_headers, header_positions):
        content_lines[header_position] = anchor_header
    toc_entries.insert(0, "")
    toc_entries.insert(0, get_toc_header())
    toc_entries.append("")
    toc_entries.reverse()
    for toc_entry in toc_entries:
        content_lines.insert(toc_insert_position, toc_entry)
    return content_lines


def insert_back_to_top_buttons(
    content_lines: list[str],
    is_toc_header: Callable[[str], bool],
    toc_id="toc",
) -> list[str]:
    for idx, line in enumerate(content_lines):
        if not is_toc_header(line):
            continue

        toc_match = re.fullmatch(r"(#+) +(.+)", line)
        assert toc_match, "目录匹配出错"
        content_lines[idx] = f'{toc_match.group(1)} <a id="{toc_id}"></a>{toc_match.group(2)}'
        break

    regex_get_header_level = re.compile(r"^#*")

    def _get_header_level(line: str) -> int:
        match_get_header_level = regex_get_header_level.match(line)
        assert match_get_header_level, "未知错误"
        return len(match_get_header_level.group(0))

    def _is_level_2_or_3_level_header(line) -> bool:
        header_level = _get_header_level(line)
        if header_level >= 2 and header_level <= 3:
            return True
        return False

    insert_positions = [(idx, _get_header_level(line)) for idx, line in enumerate(content_lines) if _is_level_2_or_3_level_header(line)]
    assert len(insert_positions) >= 1, "要求文档中至少存在一个二级标题"
    insert_positions.reverse()

    def _get_button(toc_id: str):
        # return f'<a href="#{toc_id}">返回顶部↑</a>'
        return f'<div align="right"><b><a href="#{toc_id}">返回顶部↑</a></b></div>'

    button = _get_button(toc_id)

    not_insert_interval = 16
    current_skip_total_interval = 0
    skip_thres = 64

    # 添加文档底部的按钮 (之所以要分开添加是因为底部按钮和位于文档中间的按钮的对应空行的插入原则不同):
    if len(content_lines) - insert_positions[0][0] >= not_insert_interval:
        content_lines.append("")
        content_lines.append(button)
    else:
        current_skip_total_interval += len(content_lines) - insert_positions[0][0]

    # 添加文档中间的按钮:
    for idx in range(len(insert_positions) - 1):
        insert_position, header_level = insert_positions[idx]
        insert_position_pre, header_level_pre = insert_positions[idx + 1]
        if header_level_pre + 1 == header_level:
            # 标题行等级下降时, 小间隔的绝对不加按钮:
            if insert_position - insert_position_pre < not_insert_interval:
                # 累计不加按钮的间隔:
                current_skip_total_interval += insert_position - insert_position_pre
                continue
        else:
            # 同级标题行时, 小间隔看情况加按钮:
            if insert_position - insert_position_pre < not_insert_interval:
                # 如果累计不加按钮的间隔还未超过阈值:
                if current_skip_total_interval < skip_thres:
                    # 累计不加按钮的间隔:
                    current_skip_total_interval += insert_position - insert_position_pre
                    continue

        content_lines.insert(insert_position, "")
        content_lines.insert(insert_position, button)

        # 清空累计不加按钮的间隔:
        current_skip_total_interval = 0

    def _insert_global_btt_button(content_lines: list[str]):
        button = f'<div style="position: fixed; bottom: 60px; right: 30px; padding: 10px 20px; background-color: #007bff; color: #ffffff; text-decoration: none; font-family: Arial, sans-serif; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.3); opacity: 0.7; transition: opacity 0.3s, transform 0.3s;" onmouseover="this.style.opacity=1;this.style.transform=\'translateY(-5px)\'" onmouseout="this.style.opacity=0.7;this.style.transform=\'none\'"><a href="#{toc_id}">返回顶部↑</a></div>'
        content_lines.append("")
        content_lines.append(button)

    # _insert_global_btt_button(content_lines)

    return content_lines


def make_anchor(
    md_file_path: str,
    is_toc_header: Callable[[str], bool],
    is_toc_end_header: Callable[[str], bool],
    get_toc_header: Callable[[], str],
):
    """主函数"""
    toc_insert_position, content_lines = get_content_lines(
        md_file_path=md_file_path,
        is_toc_header=is_toc_header,
        is_toc_end_header=is_toc_end_header,
    )

    headers, header_positions = get_headers(content_lines=content_lines)
    headers = clean_headers(headers=headers)
    anchor_headers, toc_entries = insert_anchors(headers=headers)
    content_lines = fill_in_new_headers_and_toc(
        content_lines=content_lines,
        anchor_headers=anchor_headers,
        header_positions=header_positions,
        toc_insert_position=toc_insert_position,
        toc_entries=toc_entries,
        get_toc_header=get_toc_header,
    )
    content_lines = insert_back_to_top_buttons(
        content_lines=content_lines,
        is_toc_header=is_toc_header,
    )

    content_lines.append("")
    content = "\n".join(content_lines)

    def _get_copy_md_file_path(md_file_path: str) -> str:
        md_file_dir_name = dirname(md_file_path)
        md_file_base_name = basename(md_file_path)
        md_file_stem = Path(md_file_base_name).stem
        md_file_suffix = Path(md_file_base_name).suffix

        copy_md_file_path = (md_file_dir_name + "/" if md_file_dir_name else "") + f"{md_file_stem}-copy{md_file_suffix}"
        return copy_md_file_path

    copy_md_file_path = _get_copy_md_file_path(md_file_path=md_file_path)
    # with open(copy_md_file_path, "w", encoding="utf8") as file:
    with open(md_file_path, "w", encoding="utf8") as file:
        file.write(content)


if __name__ == "__main__":

    def is_toc_header(line: str) -> bool:
        if line and line[0] == "#" and line.count("目录"):
            return True
        return False

    def is_toc_end_header(line: str) -> bool:
        if line and line[0] == "#":
            return True
        return False

    def get_toc_header() -> str:
        return "## 目录"

    md_file_path = "./README.md"

    if len(sys.argv) > 1:
        md_file_path = sys.argv[1]

    print(f"parse file `{md_file_path}`")

    make_anchor(
        md_file_path=md_file_path,
        is_toc_header=is_toc_header,
        is_toc_end_header=is_toc_end_header,
        get_toc_header=get_toc_header,
    )
