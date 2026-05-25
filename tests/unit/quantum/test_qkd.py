import pytest
from space_comms_digital_twin.quantum.comms.qkd_protocol import BB84, DecoyStateQKD, CVQKD


def test_bb84_key_generation():
    qkd = BB84(num_bits=256)
    result = qkd.run()
    assert result.key_length > 0
    assert result.qber >= 0


def test_bb84_noisy_channel():
    qkd = BB84(num_bits=256, error_rate=0.05)
    result = qkd.run(channel_loss=0.1)
    assert result.qber > 0


def test_bb84_key_rate():
    qkd = BB84(num_bits=1000)
    result = qkd.run()
    assert result.key_rate >= 0
    assert result.key_rate <= 1


def test_decoy_state_qkd():
    qkd = DecoyStateQKD(num_bits=128)
    result = qkd.run()
    assert result.key_length > 0


def test_cvqkd():
    qkd = CVQKD()
    result = qkd.run(num_symbols=500)
    assert result.key_rate > 0
