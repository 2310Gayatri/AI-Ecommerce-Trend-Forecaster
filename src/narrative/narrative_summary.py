import json
import os


def generate_market_report(base_dir):

    signal_path = os.path.join(
        base_dir,
        "data",
        "processed",
        "final_market_signal.json"
    )

    output_path = os.path.join(
        base_dir,
        "data",
        "processed",
        "market_report.txt"
    )

    with open(signal_path, "r") as f:
        data = json.load(f)

    market = data["current_market_state"]["market_signals"]

    report = f"""
Ecommerce Market Intelligence Report
------------------------------------

Market Overview
The ecommerce market currently shows a {market['market_direction'].lower()} sentiment trend
with a slope of {market['market_slope']}.

Current sentiment stands at {market['current_sentiment']}.

Brand Dynamics
{market['top_positive_brand']} shows the strongest positive momentum,
while {market['top_negative_brand']} is experiencing the sharpest decline.

{market['most_volatile_brand']} currently has the highest volatility.

Narrative Trends
Top topics today include: {", ".join(market["top_topics"])}.

The most positive topic is {market["most_positive_topic"]},
while the most negative topic is {market["most_negative_topic"]}.

Emerging Narratives
Fastest rising topic: {market["fastest_rising_topic"]}

Fastest declining topic: {market["fastest_declining_topic"]}
"""

    with open(output_path, "w") as f:
        f.write(report)

    print("\nMarket report saved:")
    print(output_path)

    return report