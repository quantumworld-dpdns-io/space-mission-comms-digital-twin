from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray


@dataclass
class RLResult:
    episode_rewards: list[float] = field(default_factory=list)
    avg_reward: float = 0.0
    policy_converged: bool = False
    n_episodes: int = 0
    best_action_sequence: list[int] = field(default_factory=list)


class QuantumRLComms:
    def __init__(self, n_state_qubits: int = 4, n_actions: int = 4, learning_rate: float = 0.01):
        self.n_qubits = n_state_qubits
        self.n_actions = n_actions
        self.lr = learning_rate
        self.params = np.random.uniform(-0.1, 0.1, n_actions * (n_state_qubits + 1))
        self.gamma = 0.99
        self.epsilon = 0.1

    def _encode_state(self, state: NDArray) -> NDArray:
        psi = np.zeros(2 ** self.n_qubits, dtype=complex)
        psi[0] = 1.0
        for i in range(min(self.n_qubits, len(state))):
            theta = math.atan(state[i])
            c, s = math.cos(theta / 2), math.sin(theta / 2)
            psi = self._apply_1q(psi, self.n_qubits, i, np.array([[c, -s], [s, c]]))
        return psi

    def _policy(self, state_encoding: NDArray, action: int) -> float:
        offset = action * (self.n_qubits + 1)
        params = self.params[offset:offset + self.n_qubits + 1]
        if len(params) < self.n_qubits + 1:
            return 1.0 / self.n_actions

        theta = params[-1]
        psi_action = state_encoding * math.cos(theta) + np.roll(state_encoding, 1) * math.sin(theta)
        prob = float(np.abs(psi_action[0]) ** 2)
        return max(0.01, min(0.99, prob))

    def choose_action(self, state: NDArray, greedy: bool = False) -> int:
        if not greedy and np.random.random() < self.epsilon:
            return np.random.randint(self.n_actions)
        state_enc = self._encode_state(state)
        probs = [self._policy(state_enc, a) for a in range(self.n_actions)]
        probs = np.array(probs) / (sum(probs) + 1e-10)
        return int(np.random.choice(self.n_actions, p=probs))

    def train(self, env_fn, n_episodes: int = 100, max_steps: int = 100) -> RLResult:
        episode_rewards = []
        best_avg = -float('inf')

        for _episode in range(n_episodes):
            state = env_fn()
            total_reward = 0.0
            action_sequence = []

            for _step in range(max_steps):
                action = self.choose_action(state)
                action_sequence.append(action)
                reward = -abs(state[0]) if len(state) > 0 else 0.0
                next_state = state * 0.99 + np.random.randn(len(state)) * 0.01

                state_enc = self._encode_state(state)
                next_enc = self._encode_state(next_state)
                prob = self._policy(state_enc, action)
                td_error = reward + self.gamma * max(
                    [self._policy(next_enc, a) for a in range(self.n_actions)]
                ) - prob

                a_idx = action
                offset = a_idx * (self.n_qubits + 1)
                for j in range(min(self.n_qubits + 1, len(self.params) - offset)):
                    self.params[offset + j] += self.lr * td_error * (1 - prob)

                state = next_state
                total_reward += reward

            episode_rewards.append(total_reward)
            avg = np.mean(episode_rewards[-20:]) if len(episode_rewards) >= 20 else total_reward

            if avg > best_avg:
                best_avg = avg

            self.epsilon = max(0.01, self.epsilon * 0.995)

        return RLResult(
            episode_rewards=episode_rewards,
            avg_reward=float(np.mean(episode_rewards[-20:])),
            policy_converged=best_avg > -10,
            n_episodes=n_episodes,
            best_action_sequence=action_sequence,
        )

    @staticmethod
    def _apply_1q(state: NDArray, n_qubits: int, qubit: int, gate: NDArray) -> NDArray:
        dim = len(state)
        new_state = np.zeros(dim, dtype=complex)
        for k in range(dim):
            bit = (k >> qubit) & 1
            pair = k ^ (bit << qubit)
            if bit == 0:
                new_state[k] = gate[0, 0] * state[k] + gate[0, 1] * state[pair]
            else:
                new_state[k] = gate[1, 0] * state[pair] + gate[1, 1] * state[k]
        return new_state
