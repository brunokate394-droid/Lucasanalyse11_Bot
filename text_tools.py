"""
Pure text logic — no external calls, fully offline.
"""


def sort_lines(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return "No valid lines found. Please paste a list with one item per line."
    sorted_lines = sorted(lines, key=str.lower)
    return "\n".join(sorted_lines)


def remove_duplicates(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return "No valid lines found. Please paste a list with one item per line."
    seen = set()
    unique_lines = []
    for line in lines:
        key = line.lower()
        if key not in seen:
            seen.add(key)
            unique_lines.append(line)
    removed_count = len(lines) - len(unique_lines)
    result = "\n".join(unique_lines)
    if removed_count > 0:
        result += f"\n\n({removed_count} duplicate line(s) removed)"
    return result
