def shorten_to_unique_suffix(strings):
    n = len(strings)
    # インデックス付きでソート（元の順序を保持するためにindexを取っておく）
    indexed_strings = list(enumerate(strings))
    indexed_strings.sort(key=lambda x: x[1])

    def common_prefix_len(a, b):
        i = 0
        for x, y in zip(a, b):
            if x == y:
                i += 1
            else:
                break
        return i

    # prefix_length[i]は、i番目の要素が区別されるために残す必要がある最短接尾部を求めるための基準
    prefix_length = [0] * n

    # 隣接要素間の共通接頭辞長を求め、それに基づきprefix_lengthを更新
    for i in range(n - 1):
        pl = common_prefix_len(indexed_strings[i][1], indexed_strings[i + 1][1])
        idx1, s1 = indexed_strings[i]
        idx2, s2 = indexed_strings[i + 1]
        prefix_length[idx1] = max(prefix_length[idx1], pl)
        prefix_length[idx2] = max(prefix_length[idx2], pl)

    # 求めたprefix_lengthに従って各要素を切り詰める（prefix_length[i]文字を削る）
    result = []
    for i, s in enumerate(strings):
        cut_pos = prefix_length[i]
        result.append(s[cut_pos:])
    return result


if __name__ == "__main__":
    strings = [
        "utils/path_short.py",
        "utils/system_util.py",
        "services/image_service.py",
    ]
    result = shorten_to_unique_suffix(strings)
    for s, r in zip(strings, result):
        print(f"{s} -> {r}")
