import math
import random

import ai
import data


def gradient_check(nn, state, label, eps=1e-5):
    """Compare backprop gradients with numerical ones. Differences should be ~1e-7 or less."""
    grads = nn.zero_grads()
    nn.backward(state, label, grads)

    def loss_now():
        p = ai.softmax(nn.forward(state))
        return -math.log(max(p[label], 1e-12))

    checks = [
        ("w1", nn.weights1, grads["w1"]),
        ("w2", nn.weights2, grads["w2"]),
        ("w3", nn.weights3, grads["w3"]),
    ]
    for name, W, G in checks:
        for _ in range(5):
            i = random.randrange(len(W))
            j = random.randrange(len(W[0]))
            orig = W[i][j]
            W[i][j] = orig + eps
            plus = loss_now()
            W[i][j] = orig - eps
            minus = loss_now()
            W[i][j] = orig
            numeric = (plus - minus) / (2 * eps)
            print(f"{name}[{i}][{j}] backprop={G[i][j]: .8f} numeric={numeric: .8f} "
                  f"diff={abs(G[i][j] - numeric):.2e}")


if __name__ == "__main__":
    states, actions = data.get_training_data()
    print(f"Loaded {len(states)} samples")
    if len(states) < 50:
        raise SystemExit("Not enough data. Play more games first (arrow keys record moves).")

    nn = ai.NeuralNetwork()

    print("\n--- Gradient check (run this once; remove later) ---")
    gradient_check(nn, states[0], actions[0].index(1))

    # 80/20 train/validation split
    combined = list(zip(states, actions))
    random.shuffle(combined)
    split = int(len(combined) * 0.8)
    train, val = combined[:split], combined[split:]
    tr_s, tr_a = [c[0] for c in train], [c[1] for c in train]
    va_s, va_a = [c[0] for c in val], [c[1] for c in val]

    print("\n--- Training ---")
    nn.train(tr_s, tr_a, epochs=50, lr=0.05, batch_size=32,
             val_states=va_s, val_actions=va_a)

    nn.save()
    print("Saved weights.json")