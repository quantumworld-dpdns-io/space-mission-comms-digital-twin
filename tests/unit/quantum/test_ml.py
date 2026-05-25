import pytest
import numpy as np
from space_comms_digital_twin.quantum.ml.qsvm import QSVM
from space_comms_digital_twin.quantum.ml.qnn import QNN
from space_comms_digital_twin.quantum.ml.anomaly_detector import QuantumAnomalyDetector


def test_qsvm_fit():
    X = np.array([[0.0, 0.0], [1.0, 1.0], [0.0, 1.0], [1.0, 0.0]])
    y = np.array([-1, 1, -1, 1])
    qsvm = QSVM(kernel_type="quantum")
    result = qsvm.fit(X, y)
    assert result.accuracy > 0


def test_qsvm_predict():
    X = np.array([[0.0, 0.0], [1.0, 1.0]])
    y = np.array([-1, 1])
    qsvm = QSVM()
    qsvm.fit(X, y)
    pred = qsvm.predict(np.array([[0.5, 0.5]]))
    assert len(pred) == 1


def test_qnn_fit():
    X = np.array([[0.0], [1.0], [0.5], [0.8]])
    y = np.array([0, 1, 0, 1])
    qnn = QNN(n_qubits=2, n_layers=1, learning_rate=0.1)
    result = qnn.fit(X, y, epochs=5)
    assert result.n_epochs == 5


def test_qnn_predict():
    qnn = QNN(n_qubits=2)
    pred = qnn.predict(np.array([[0.5]]))
    assert len(pred) == 1


def test_anomaly_detector():
    X = np.random.randn(50, 3)
    detector = QuantumAnomalyDetector(n_qubits=4, nu=0.1)
    result = detector.detect(X)
    assert result.n_anomalies >= 0
