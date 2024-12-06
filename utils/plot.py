from schemas import CheckResult

wr = 30
hr = 10


def hit_char(
    j: int, i: int, h: int, w: int, checks: list[CheckResult], mark="*"
):
    return (
        mark
        if any(
            j <= c.px < j + w / wr and i <= c.py < i + h / hr for c in checks
        )
        else " "
    )


def draw_grid_with_mark(h: int, w: int, checks: list[CheckResult], mark="*"):
    grid = []
    for i in range(0, h, hr):
        row = []
        for j in range(0, w, wr):
            row.append(hit_char(j, i, h, w, checks, mark))
        grid.append(row)

    # 枠線を加える
    top_bottom_border = "+" + "-" * wr + "+"
    grid_with_border = [top_bottom_border]
    for row in grid:
        grid_with_border.append("|" + "".join(row) + "|")
    grid_with_border.append(top_bottom_border)

    # グリッドを表示
    return "\n".join(grid_with_border)
