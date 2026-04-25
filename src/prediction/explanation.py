from __future__ import annotations


def build_explanation(player_a: str, player_b: str, p_model: float, p_book: float, factors: list[str], risk_flags: list[str], stake_pct: float) -> str:
    lines = [
        "Краткий вывод:",
        f"Модель видит value на матч {player_a} vs {player_b}: вероятность модели {p_model:.1%} выше fair-оценки букмекера {p_book:.1%}.",
        "",
        "Факторы в пользу:",
    ]
    lines.extend([f"• {f}" for f in factors])
    lines.append("")
    lines.append("Факторы риска:")
    if risk_flags:
        lines.extend([f"• {r}" for r in risk_flags])
    else:
        lines.append("• Явных risk flags не обнаружено")
    lines.extend(["", f"Решение: не более {stake_pct:.2%} от банка."])
    return "\n".join(lines)
