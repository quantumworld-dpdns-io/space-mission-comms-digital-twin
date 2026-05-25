from __future__ import annotations

import math
import random
from collections.abc import Generator

from space_comms_digital_twin.config import CCSDS_HEADER_SIZE, CFDP_MAX_PDU_SIZE


def poisson_traffic(lambda_rate: float, duration: float, seed: int | None = None) -> Generator:
    rng = random.Random(seed)
    t = 0.0
    packet_id = 0
    while t < duration:
        interarrival = rng.expovariate(lambda_rate)
        t += interarrival
        if t >= duration:
            break
        packet_id += 1
        yield {
            "packet_id": packet_id,
            "timestamp": t,
            "size_bytes": 1500,
            "type": "data",
        }


def bursty_traffic(mean_burst_size: float, mean_idle_time: float,
                   packet_rate: float, duration: float, seed: int | None = None) -> Generator:
    rng = random.Random(seed)
    t = 0.0
    packet_id = 0
    while t < duration:
        burst_size = int(rng.expovariate(1.0 / mean_burst_size))
        for _ in range(burst_size):
            packet_id += 1
            yield {
                "packet_id": packet_id,
                "timestamp": t,
                "size_bytes": 1500,
                "type": "burst",
            }
            t += 1.0 / packet_rate
        idle = rng.expovariate(1.0 / mean_idle_time)
        t += idle


def constant_bit_rate(rate_bps: float, packet_size: int = 1500) -> Generator:
    packet_interval = (packet_size * 8.0) / rate_bps
    t = 0.0
    packet_id = 0
    while True:
        packet_id += 1
        yield {
            "packet_id": packet_id,
            "timestamp": t,
            "size_bytes": packet_size,
            "type": "cbr",
        }
        t += packet_interval


def variable_bit_rate(mean_rate: float, peak_rate: float, packet_size: int = 1500) -> Generator:
    packet_id = 0
    t = 0.0
    rng = random.Random()
    while True:
        packet_id += 1
        current_rate = rng.uniform(mean_rate, peak_rate)
        interval = (packet_size * 8.0) / current_rate
        yield {
            "packet_id": packet_id,
            "timestamp": t,
            "size_bytes": packet_size,
            "type": "vbr",
            "rate_bps": current_rate,
        }
        t += interval


def priority_queue(packets: list[dict], priorities: list[int] | None = None) -> list[dict]:
    if priorities is None:
        priorities = [0] * len(packets)
    indexed = list(zip(priorities, range(len(packets)), packets, strict=False))
    indexed.sort(key=lambda x: (-x[0], x[1]))
    return [p for _, _, p in indexed]


def congestion_window(link_capacity: float, rtt: float) -> float:
    return link_capacity * rtt


def flow_control_model(window_size: int, ack_delay: float) -> float:
    return window_size / ack_delay


def ccascade_header(packet_type: str, data_length: int) -> int:
    return CCSDS_HEADER_SIZE


def cfdp_transaction(source: str, dest: str, file_size: int, pdu_size: int = CFDP_MAX_PDU_SIZE) -> dict:
    num_pdus = math.ceil(file_size / pdu_size)
    return {
        "source": source,
        "destination": dest,
        "file_size": file_size,
        "pdu_size": pdu_size,
        "num_pdus": num_pdus,
        "metadata_pdus": 1,
        "data_pdus": num_pdus,
        "eof_pdus": 1,
        "total_pdus": num_pdus + 2,
    }


def packet_loss_model(loss_rate: float, distribution: str = "bernoulli",
                      seed: int | None = None) -> Generator:
    rng = random.Random(seed)
    while True:
        if distribution == "bernoulli":
            lost = rng.random() < loss_rate
        elif distribution == "burst":
            if rng.random() < loss_rate:
                burst_len = int(rng.expovariate(1.0 / 3.0)) + 1
                for _ in range(burst_len):
                    yield True
                continue
            lost = False
        else:
            lost = rng.random() < loss_rate
        yield lost
