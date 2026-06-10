#!/usr/bin/env python3
"""Simulate self-organized criticality in pharmaceutical inventories.

This exploratory script models a hospital inventory network exposed to:

- concentrated supplier market shares;
- stochastic day-to-day demand;
- rare but consequential national demand shocks;
- supplier bottlenecks and temporary disruptions;
- redistribution attempts between hospitals.

The goal is not to recover a single historical time series exactly. The goal is
to create a reproducible sandbox where shortage cascades can be studied as an
emergent phenomenon and evaluated for heavy-tail behaviour.

Outputs written to the selected output directory:

- summary.json: high-level diagnostics and tail estimates;
- avalanches.csv: one row per shortage cascade;
- daily_metrics.csv: daily system trajectory.

Invocation example:
    python docs/publicacion_cientifica/publish_ready/BigLoI-PLOS-ONE-paper/code/scripts/simulate_inventory_soc.py
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
from dataclasses import dataclass
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = PACKAGE_ROOT / "results" / "inventory_soc"


@dataclass
class Order:
    hospital_id: int
    medicine_id: int
    supplier_id: int
    quantity: float
    due_day: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--days", type=int, default=365 * 4, help="Simulation horizon in days")
    parser.add_argument("--hospitals", type=int, default=64, help="Number of simulated hospitals")
    parser.add_argument("--suppliers", type=int, default=9, help="Number of simulated suppliers")
    parser.add_argument("--medicines", type=int, default=10, help="Number of simulated medicines")
    parser.add_argument(
        "--concentration-alpha",
        type=float,
        default=1.35,
        help="Zipf exponent for supplier concentration",
    )
    parser.add_argument(
        "--national-shock-prob",
        type=float,
        default=0.02,
        help="Daily probability of a medicine-specific national shock",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where CSV and JSON results will be written",
    )
    return parser.parse_args()


def zipf_weights(size: int, alpha: float) -> list[float]:
    weights = [1.0 / (rank**alpha) for rank in range(1, size + 1)]
    total = sum(weights)
    return [weight / total for weight in weights]


def weighted_choice_index(weights: list[float], rng: random.Random) -> int:
    threshold = rng.random()
    cumulative = 0.0
    for index, weight in enumerate(weights):
        cumulative += weight
        if threshold <= cumulative:
            return index
    return len(weights) - 1


def percentile(values: list[float], level: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return float(ordered[0])
    position = (len(ordered) - 1) * level
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        return float(ordered[lower])
    fraction = position - lower
    return float(ordered[lower] + (ordered[upper] - ordered[lower]) * fraction)


def linear_regression(points: list[tuple[float, float]]) -> tuple[float, float, float]:
    if len(points) < 2:
        return 0.0, 0.0, 0.0

    xs = [point[0] for point in points]
    ys = [point[1] for point in points]
    x_mean = statistics.fmean(xs)
    y_mean = statistics.fmean(ys)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in points)
    denominator = sum((x - x_mean) ** 2 for x in xs)
    if denominator == 0:
        return 0.0, y_mean, 0.0

    slope = numerator / denominator
    intercept = y_mean - slope * x_mean
    ss_total = sum((y - y_mean) ** 2 for y in ys)
    ss_residual = sum((y - (slope * x + intercept)) ** 2 for x, y in points)
    r_squared = 1.0 - (ss_residual / ss_total) if ss_total else 0.0
    return slope, intercept, r_squared


def estimate_power_law_tail(samples: list[float]) -> dict[str, float | int | bool]:
    positive_samples = [value for value in samples if value > 0]
    if len(positive_samples) < 20:
        return {
            "tail_sample_size": len(positive_samples),
            "xmin": 0.0,
            "alpha": 0.0,
            "loglog_slope": 0.0,
            "loglog_r2": 0.0,
            "heavy_tail_evidence": False,
        }

    xmin = max(1.0, percentile(positive_samples, 0.8))
    tail = sorted(value for value in positive_samples if value >= xmin)
    if len(tail) < 20:
        tail = sorted(positive_samples)
        xmin = max(1.0, min(tail))

    denominator = sum(math.log(value / xmin) for value in tail if value > xmin)
    alpha = 1.0 + (len(tail) / denominator) if denominator > 0 else 0.0

    unique_tail = sorted(set(tail))
    ccdf_points: list[tuple[float, float]] = []
    total = len(tail)
    for value in unique_tail:
        survivors = sum(1 for sample in tail if sample >= value)
        probability = survivors / total
        if value > 0 and probability > 0:
            ccdf_points.append((math.log(value), math.log(probability)))

    slope, _intercept, r_squared = linear_regression(ccdf_points)
    heavy_tail_evidence = len(tail) >= 20 and r_squared >= 0.85 and slope < -0.4
    return {
        "tail_sample_size": len(tail),
        "xmin": round(float(xmin), 4),
        "alpha": round(float(alpha), 4),
        "loglog_slope": round(float(slope), 4),
        "loglog_r2": round(float(r_squared), 4),
        "heavy_tail_evidence": heavy_tail_evidence,
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_neighbourhoods(hospital_count: int) -> list[list[int]]:
    neighbours: list[list[int]] = []
    for hospital_id in range(hospital_count):
        linked = {
            (hospital_id - 1) % hospital_count,
            (hospital_id + 1) % hospital_count,
            (hospital_id - 7) % hospital_count,
            (hospital_id + 7) % hospital_count,
        }
        linked.discard(hospital_id)
        neighbours.append(sorted(linked))
    return neighbours


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)

    hospital_count = args.hospitals
    supplier_count = args.suppliers
    medicine_count = args.medicines
    horizon_days = args.days

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    supplier_weights = zipf_weights(supplier_count, args.concentration_alpha)
    supplier_hhi = sum(weight * weight for weight in supplier_weights)

    base_demand = [
        [rng.uniform(5.0, 18.0) for _ in range(medicine_count)]
        for _ in range(hospital_count)
    ]
    safety_days = [rng.uniform(4.0, 8.0) for _ in range(medicine_count)]
    target_days = [day + rng.uniform(6.0, 12.0) for day in safety_days]
    base_lead_time = [rng.uniform(2.0, 6.0) for _ in range(medicine_count)]
    hospital_supplier = [
        [weighted_choice_index(supplier_weights, rng) for _ in range(medicine_count)]
        for _ in range(hospital_count)
    ]

    stock = [
        [
            base_demand[hospital_id][medicine_id] * target_days[medicine_id] * rng.uniform(0.9, 1.2)
            for medicine_id in range(medicine_count)
        ]
        for hospital_id in range(hospital_count)
    ]

    neighbours = build_neighbourhoods(hospital_count)
    orders: list[Order] = []
    daily_metrics: list[dict[str, object]] = []
    avalanches: list[dict[str, object]] = []
    active_avalanche: dict[str, object] | None = None

    supplier_disruption_until = [-1 for _ in range(supplier_count)]
    supplier_capacity_factor = [1.0 for _ in range(supplier_count)]

    expected_total_daily_demand = sum(sum(row) for row in base_demand)
    supplier_capacity = [
        max(60.0, expected_total_daily_demand * share * 7.0)
        for share in supplier_weights
    ]

    for day in range(horizon_days):
        national_shock_medicine = -1
        national_shock_multiplier = 1.0
        if rng.random() < args.national_shock_prob:
            national_shock_medicine = rng.randrange(medicine_count)
            national_shock_multiplier = 1.0 + rng.paretovariate(2.2)

        supplier_due_orders: list[list[Order]] = [[] for _ in range(supplier_count)]
        retained_orders: list[Order] = []
        for order in orders:
            if order.due_day <= day:
                supplier_due_orders[order.supplier_id].append(order)
            else:
                retained_orders.append(order)
        orders = retained_orders

        for supplier_id in range(supplier_count):
            pending_load = sum(order.quantity for order in supplier_due_orders[supplier_id])
            queue_load = pending_load / max(supplier_capacity[supplier_id], 1.0)

            disruption_probability = 0.004 + max(0.0, queue_load - 1.0) * 0.12
            if day > supplier_disruption_until[supplier_id] and rng.random() < disruption_probability:
                supplier_disruption_until[supplier_id] = day + 1 + int(rng.paretovariate(2.8) * 2)
                supplier_capacity_factor[supplier_id] = max(0.15, 0.65 - min(queue_load, 2.5) * 0.18)

            if day > supplier_disruption_until[supplier_id]:
                supplier_capacity_factor[supplier_id] = 1.0

            available_capacity = supplier_capacity[supplier_id] * supplier_capacity_factor[supplier_id]
            available_capacity = max(10.0, available_capacity)

            for order in sorted(supplier_due_orders[supplier_id], key=lambda item: item.due_day):
                delivered = min(order.quantity, available_capacity)
                stock[order.hospital_id][order.medicine_id] += delivered
                available_capacity -= delivered

                remaining = order.quantity - delivered
                if remaining > 0:
                    orders.append(
                        Order(
                            hospital_id=order.hospital_id,
                            medicine_id=order.medicine_id,
                            supplier_id=order.supplier_id,
                            quantity=remaining,
                            due_day=day + 1,
                        )
                    )

        daily_stockout_pairs = 0
        daily_shortage_units = 0.0
        daily_redistributed_units = 0.0
        daily_ordered_units = 0.0
        hospitals_in_shortage: set[int] = set()

        for hospital_id in range(hospital_count):
            for medicine_id in range(medicine_count):
                demand_multiplier = rng.lognormvariate(0.0, 0.22)
                demand = base_demand[hospital_id][medicine_id] * demand_multiplier

                if medicine_id == national_shock_medicine:
                    demand *= national_shock_multiplier

                if rng.random() < 0.008:
                    demand *= 1.0 + rng.paretovariate(3.0)

                stock[hospital_id][medicine_id] -= demand
                shortage = max(0.0, -stock[hospital_id][medicine_id])
                stock[hospital_id][medicine_id] = max(0.0, stock[hospital_id][medicine_id])

                redistributed = 0.0
                if shortage > 0:
                    for neighbour_id in neighbours[hospital_id]:
                        neighbour_floor = base_demand[neighbour_id][medicine_id] * safety_days[medicine_id]
                        neighbour_surplus = max(0.0, stock[neighbour_id][medicine_id] - neighbour_floor)
                        transfer = min(shortage - redistributed, neighbour_surplus * 0.35)
                        if transfer <= 0:
                            continue
                        stock[neighbour_id][medicine_id] -= transfer
                        redistributed += transfer
                        if redistributed >= shortage:
                            break

                effective_shortage = max(0.0, shortage - redistributed)
                daily_redistributed_units += redistributed
                if effective_shortage > 0:
                    daily_stockout_pairs += 1
                    daily_shortage_units += effective_shortage
                    hospitals_in_shortage.add(hospital_id)

                inventory_position = stock[hospital_id][medicine_id] + sum(
                    order.quantity
                    for order in orders
                    if order.hospital_id == hospital_id and order.medicine_id == medicine_id
                )
                reorder_point = base_demand[hospital_id][medicine_id] * (base_lead_time[medicine_id] + safety_days[medicine_id])
                target_position = base_demand[hospital_id][medicine_id] * target_days[medicine_id]

                if inventory_position < reorder_point:
                    quantity = max(0.0, target_position - inventory_position)
                    if quantity > 0:
                        supplier_id = hospital_supplier[hospital_id][medicine_id]
                        queue_pressure = sum(
                            order.quantity
                            for order in orders
                            if order.supplier_id == supplier_id and order.due_day <= day + 7
                        ) / max(supplier_capacity[supplier_id], 1.0)
                        delay = base_lead_time[medicine_id] + max(0.0, queue_pressure - 0.75) * 2.5
                        if day <= supplier_disruption_until[supplier_id]:
                            delay += 2.0 + (1.0 - supplier_capacity_factor[supplier_id]) * 6.0
                        due_day = day + max(1, math.ceil(delay))
                        orders.append(
                            Order(
                                hospital_id=hospital_id,
                                medicine_id=medicine_id,
                                supplier_id=supplier_id,
                                quantity=quantity,
                                due_day=due_day,
                            )
                        )
                        daily_ordered_units += quantity

        if daily_stockout_pairs > 0:
            if active_avalanche is None:
                active_avalanche = {
                    "start_day": day,
                    "duration_days": 0,
                    "stockout_pairs": 0,
                    "shortage_units": 0.0,
                    "peak_daily_stockout_pairs": 0,
                    "affected_hospitals": set(),
                }
            active_avalanche["duration_days"] += 1
            active_avalanche["stockout_pairs"] += daily_stockout_pairs
            active_avalanche["shortage_units"] += daily_shortage_units
            active_avalanche["peak_daily_stockout_pairs"] = max(
                active_avalanche["peak_daily_stockout_pairs"], daily_stockout_pairs
            )
            active_avalanche["affected_hospitals"].update(hospitals_in_shortage)
        elif active_avalanche is not None:
            avalanches.append(
                {
                    "start_day": active_avalanche["start_day"],
                    "end_day": day - 1,
                    "duration_days": active_avalanche["duration_days"],
                    "stockout_pairs": active_avalanche["stockout_pairs"],
                    "shortage_units": round(active_avalanche["shortage_units"], 4),
                    "peak_daily_stockout_pairs": active_avalanche["peak_daily_stockout_pairs"],
                    "affected_hospitals": len(active_avalanche["affected_hospitals"]),
                }
            )
            active_avalanche = None

        daily_metrics.append(
            {
                "day": day,
                "national_shock_medicine": national_shock_medicine,
                "national_shock_multiplier": round(national_shock_multiplier, 4),
                "stockout_pairs": daily_stockout_pairs,
                "shortage_units": round(daily_shortage_units, 4),
                "redistributed_units": round(daily_redistributed_units, 4),
                "ordered_units": round(daily_ordered_units, 4),
                "pipeline_orders": len(orders),
                "pipeline_units": round(sum(order.quantity for order in orders), 4),
                "active_supplier_disruptions": sum(
                    1 for supplier_id in range(supplier_count) if day <= supplier_disruption_until[supplier_id]
                ),
            }
        )

    if active_avalanche is not None:
        avalanches.append(
            {
                "start_day": active_avalanche["start_day"],
                "end_day": horizon_days - 1,
                "duration_days": active_avalanche["duration_days"],
                "stockout_pairs": active_avalanche["stockout_pairs"],
                "shortage_units": round(active_avalanche["shortage_units"], 4),
                "peak_daily_stockout_pairs": active_avalanche["peak_daily_stockout_pairs"],
                "affected_hospitals": len(active_avalanche["affected_hospitals"]),
            }
        )

    avalanche_sizes = [entry["stockout_pairs"] for entry in avalanches]
    avalanche_duration = [entry["duration_days"] for entry in avalanches]
    shortage_sizes = [entry["shortage_units"] for entry in avalanches]
    tail_metrics = estimate_power_law_tail([float(value) for value in avalanche_sizes])

    summary = {
        "model": "pharmaceutical_inventory_soc",
        "interpretation": {
            "objective": "Explore whether concentrated procurement and supply bottlenecks can generate heavy-tailed shortage cascades.",
            "not_for_causal_claims": True,
            "use_case": "Scenario laboratory for Colombian pharmaceutical inventory risk.",
        },
        "parameters": {
            "seed": args.seed,
            "days": horizon_days,
            "hospitals": hospital_count,
            "suppliers": supplier_count,
            "medicines": medicine_count,
            "supplier_concentration_alpha": args.concentration_alpha,
            "national_shock_probability": args.national_shock_prob,
        },
        "market_structure": {
            "supplier_shares": [round(weight, 6) for weight in supplier_weights],
            "top_supplier_share": round(max(supplier_weights), 6),
            "supplier_hhi": round(supplier_hhi, 6),
        },
        "system_outcomes": {
            "total_avalanches": len(avalanches),
            "mean_daily_stockout_pairs": round(statistics.fmean(row["stockout_pairs"] for row in daily_metrics), 4),
            "mean_daily_shortage_units": round(statistics.fmean(row["shortage_units"] for row in daily_metrics), 4),
            "max_daily_stockout_pairs": max((row["stockout_pairs"] for row in daily_metrics), default=0),
            "largest_avalanche_stockout_pairs": max(avalanche_sizes, default=0),
            "largest_avalanche_shortage_units": round(max(shortage_sizes, default=0.0), 4),
            "median_avalanche_size": round(percentile([float(value) for value in avalanche_sizes], 0.5), 4),
            "p95_avalanche_size": round(percentile([float(value) for value in avalanche_sizes], 0.95), 4),
            "p99_avalanche_size": round(percentile([float(value) for value in avalanche_sizes], 0.99), 4),
            "mean_avalanche_duration": round(statistics.fmean(avalanche_duration), 4) if avalanche_duration else 0.0,
        },
        "tail_diagnostics": tail_metrics,
    }

    write_csv(output_dir / "avalanches.csv", avalanches)
    write_csv(output_dir / "daily_metrics.csv", daily_metrics)
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print("Inventory SOC simulation completed.")
    print(f"Results directory: {output_dir}")
    print(f"Total avalanches: {summary['system_outcomes']['total_avalanches']}")
    print(f"Largest avalanche (stockout pairs): {summary['system_outcomes']['largest_avalanche_stockout_pairs']}")
    print(f"Tail alpha estimate: {summary['tail_diagnostics']['alpha']}")
    print(f"Heavy-tail evidence: {summary['tail_diagnostics']['heavy_tail_evidence']}")


if __name__ == "__main__":
    main()