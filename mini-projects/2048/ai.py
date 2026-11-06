import os
import json
import math
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WEIGHTS_PATH = os.path.join(SCRIPT_DIR, "weights.json")


def encode(v):
    """Raw tile value -> small number. 0 -> 0, 1 -> 1/12, 2 -> 2/12, 4 -> 3/12 ..."""
    if v == 0:
        return 0.0
    return (math.log2(v) + 1) / 12.0


def softmax(logits):
    m = max(logits)  # subtract max for numerical stability
    exps = [math.exp(z - m) for z in logits]
    s = sum(exps)
    return [e / s for e in exps]


class NeuralNetwork:

    def __init__(self):
        # Architecture: 16 -> 32 -> 32 -> 4
        self.input_size = 16
        self.hidden1_size = 32
        self.hidden2_size = 32
        self.output_size = 4

        # weights[i][j] = connection from input j to neuron i of the next layer
        self.weights1 = self.create_weights(self.input_size, self.hidden1_size)
        self.weights2 = self.create_weights(self.hidden1_size, self.hidden2_size)
        self.weights3 = self.create_weights(self.hidden2_size, self.output_size)

        self.bias1 = [0.0] * self.hidden1_size
        self.bias2 = [0.0] * self.hidden2_size
        self.bias3 = [0.0] * self.output_size

        # Cached values from the last forward pass (backprop needs these)
        self.input = []
        self.z1 = []       # hidden1 before ReLU
        self.hidden1 = []  # hidden1 after ReLU
        self.z2 = []
        self.hidden2 = []
        self.output = []   # logits

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------
    def create_weights(self, inputs, outputs):
        # He initialization: std = sqrt(2 / fan_in), suited for ReLU
        std = math.sqrt(2.0 / inputs)
        return [[random.gauss(0, std) for _ in range(inputs)] for _ in range(outputs)]

    def relu(self, x):
        return max(0.0, x)

    def _flatten(self, inputs):
        if len(inputs) == 4:
            return [v for row in inputs for v in row]
        return inputs

    # ------------------------------------------------------------------
    # Forward pass (returns raw logits, same as before)
    # ------------------------------------------------------------------
    def forward(self, inputs):
        inputs = [encode(v) for v in self._flatten(inputs)]
        self.input = inputs

        self.z1 = []
        for i in range(self.hidden1_size):
            total = self.bias1[i]
            for j in range(self.input_size):
                total += inputs[j] * self.weights1[i][j]
            self.z1.append(total)
        self.hidden1 = [self.relu(z) for z in self.z1]

        self.z2 = []
        for i in range(self.hidden2_size):
            total = self.bias2[i]
            for j in range(self.hidden1_size):
                total += self.hidden1[j] * self.weights2[i][j]
            self.z2.append(total)
        self.hidden2 = [self.relu(z) for z in self.z2]

        output = []
        for i in range(self.output_size):
            total = self.bias3[i]
            for j in range(self.hidden2_size):
                total += self.hidden2[j] * self.weights3[i][j]
            output.append(total)
        self.output = output
        return output

    def predict(self, inputs):
        output = self.forward(inputs)
        return output.index(max(output))
        # 0 -> RIGHT, 1 -> UP, 2 -> LEFT, 3 -> DOWN

    # ------------------------------------------------------------------
    # Backpropagation
    # ------------------------------------------------------------------
    def zero_grads(self):
        return {
            "w1": [[0.0] * self.input_size for _ in range(self.hidden1_size)],
            "w2": [[0.0] * self.hidden1_size for _ in range(self.hidden2_size)],
            "w3": [[0.0] * self.hidden2_size for _ in range(self.output_size)],
            "b1": [0.0] * self.hidden1_size,
            "b2": [0.0] * self.hidden2_size,
            "b3": [0.0] * self.output_size,
        }

    def backward(self, inputs, label, grads):
        """
        One sample. `label` is the correct action index (0-3).
        ADDS this sample's gradients into `grads`. Returns (loss, probs).
        """
        logits = self.forward(inputs)
        p = softmax(logits)
        loss = -math.log(max(p[label], 1e-12))

        # Output layer: dLoss/dlogits = p - y  (softmax + cross-entropy)
        d3 = p[:]
        d3[label] -= 1.0

        for i in range(self.output_size):
            grads["b3"][i] += d3[i]
            for j in range(self.hidden2_size):
                grads["w3"][i][j] += d3[i] * self.hidden2[j]

        # Hidden 2: push error back through weights3, then through ReLU
        d2 = [0.0] * self.hidden2_size
        for j in range(self.hidden2_size):
            s = 0.0
            for i in range(self.output_size):
                s += self.weights3[i][j] * d3[i]
            d2[j] = s if self.z2[j] > 0 else 0.0  # ReLU derivative

        for i in range(self.hidden2_size):
            grads["b2"][i] += d2[i]
            for j in range(self.hidden1_size):
                grads["w2"][i][j] += d2[i] * self.hidden1[j]

        # Hidden 1
        d1 = [0.0] * self.hidden1_size
        for j in range(self.hidden1_size):
            s = 0.0
            for i in range(self.hidden2_size):
                s += self.weights2[i][j] * d2[i]
            d1[j] = s if self.z1[j] > 0 else 0.0

        for i in range(self.hidden1_size):
            grads["b1"][i] += d1[i]
            for j in range(self.input_size):
                grads["w1"][i][j] += d1[i] * self.input[j]

        return loss, p

    # ------------------------------------------------------------------
    # Gradient descent
    # ------------------------------------------------------------------
    def apply_grads(self, grads, lr, batch_size):
        scale = lr / batch_size  # average the gradients over the batch
        for i in range(self.hidden1_size):
            self.bias1[i] -= scale * grads["b1"][i]
            for j in range(self.input_size):
                self.weights1[i][j] -= scale * grads["w1"][i][j]
        for i in range(self.hidden2_size):
            self.bias2[i] -= scale * grads["b2"][i]
            for j in range(self.hidden1_size):
                self.weights2[i][j] -= scale * grads["w2"][i][j]
        for i in range(self.output_size):
            self.bias3[i] -= scale * grads["b3"][i]
            for j in range(self.hidden2_size):
                self.weights3[i][j] -= scale * grads["w3"][i][j]

    def train(self, states, actions, epochs=50, lr=0.05, batch_size=32,
              val_states=None, val_actions=None):
        labels = [a.index(1) for a in actions]
        n = len(states)
        order = list(range(n))

        for epoch in range(1, epochs + 1):
            random.shuffle(order)
            total_loss, correct = 0.0, 0

            for start in range(0, n, batch_size):
                batch = order[start:start + batch_size]
                grads = self.zero_grads()
                for idx in batch:
                    loss, p = self.backward(states[idx], labels[idx], grads)
                    total_loss += loss
                    if p.index(max(p)) == labels[idx]:
                        correct += 1
                self.apply_grads(grads, lr, len(batch))

            msg = f"Epoch {epoch:3d} | loss {total_loss / n:.4f} | train acc {correct / n:.1%}"
            if val_states:
                msg += f" | val acc {self.accuracy(val_states, val_actions):.1%}"
            print(msg)

    def accuracy(self, states, actions):
        right = sum(1 for s, a in zip(states, actions) if self.predict(s) == a.index(1))
        return right / len(states)

    # ------------------------------------------------------------------
    # Save / load
    # ------------------------------------------------------------------
    def save(self, path=WEIGHTS_PATH):
        with open(path, "w") as f:
            json.dump({
                "w1": self.weights1, "w2": self.weights2, "w3": self.weights3,
                "b1": self.bias1, "b2": self.bias2, "b3": self.bias3,
            }, f)

    def load(self, path=WEIGHTS_PATH):
        if not os.path.exists(path):
            return False
        with open(path, "r") as f:
            d = json.load(f)
        self.weights1, self.weights2, self.weights3 = d["w1"], d["w2"], d["w3"]
        self.bias1, self.bias2, self.bias3 = d["b1"], d["b2"], d["b3"]
        return True