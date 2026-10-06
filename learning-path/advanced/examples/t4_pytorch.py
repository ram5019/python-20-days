"""Track 4b example: PyTorch, tensors, autograd and a training loop.

Run:    python3 learning-path/advanced/examples/t4_pytorch.py
Needs:  pip install torch     (large download; CPU version is enough)
Runs in a few seconds on a normal laptop CPU.
"""

import torch
from torch import nn

torch.manual_seed(0)                       # repeatable results

# BLOCK 1: tensors: like NumPy arrays, but they can run on GPUs and track gradients
a = torch.tensor([1.0, 2.0, 3.0])
b = torch.tensor([10.0, 20.0, 30.0])
print(a + b, a * b, a.shape, a.dtype)
print(a.mean(), a.sum().item())            # .item() turns a 1-value tensor into a Python number

# BLOCK 2: autograd: PyTorch computes derivatives for you
x = torch.tensor(3.0, requires_grad=True)  # "track operations on x"
y = x ** 2 + 2 * x                         # y = x² + 2x
y.backward()                               # compute dy/dx
print("dy/dx at x=3 :", x.grad.item())     # 2x + 2 = 8

# BLOCK 3: learning by hand: fit y = w * x using gradient descent
X = torch.tensor([1.0, 2.0, 3.0, 4.0])
Y = torch.tensor([2.0, 4.0, 6.0, 8.0])     # the true rule is w = 2
w = torch.tensor(0.0, requires_grad=True)  # start with a wrong guess
for step in range(50):
    loss = ((w * X - Y) ** 2).mean()       # how wrong are we? (mean squared error)
    loss.backward()                        # gradient of loss w.r.t. w
    with torch.no_grad():
        w -= 0.05 * w.grad                 # take a small step downhill
    w.grad.zero_()                         # reset the gradient for the next round
print(f"Learned w = {w.item():.3f} (truth 2.0)")

# BLOCK 4: the same job with torch's building blocks
# Data: temperature (C) -> a sensor reading, with noise
X = torch.linspace(0, 10, 100).unsqueeze(1)           # shape (100, 1)
Y = 3 * X + 4 + 0.5 * torch.randn_like(X)             # rule: 3x + 4 + noise

model = nn.Linear(1, 1)                                # one weight + one bias
loss_fn = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.02)

for epoch in range(300):
    pred = model(X)                  # 1. forward pass
    loss = loss_fn(pred, Y)          # 2. how wrong?
    optimizer.zero_grad()            # 3. clear old gradients
    loss.backward()                  # 4. backward pass
    optimizer.step()                 # 5. update the parameters

w_learned, b_learned = model.weight.item(), model.bias.item()
print(f"Linear model: y = {w_learned:.2f}x + {b_learned:.2f}   (truth: 3x + 4)")

# BLOCK 5: a small neural network for a NON-linear problem
# Classify points: label 1 if the point is inside a circle of radius 1, else 0
N = 600
points = torch.rand(N, 2) * 4 - 2                                  # random points in a square
labels = (points.pow(2).sum(dim=1) < 1.0).float().unsqueeze(1)

split = 450
X_tr, X_te = points[:split], points[split:]
y_tr, y_te = labels[:split], labels[split:]


class CircleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(2, 16), nn.ReLU(),         # hidden layer 1 (ReLU adds non-linearity)
            nn.Linear(16, 16), nn.ReLU(),        # hidden layer 2
            nn.Linear(16, 1),                    # output: one score
        )

    def forward(self, x):
        return self.layers(x)


net = CircleNet()
loss_fn = nn.BCEWithLogitsLoss()                 # binary classification loss
opt = torch.optim.Adam(net.parameters(), lr=0.02)

# BLOCK 6: the training loop (same 5 steps as Block 4)
for epoch in range(300):
    loss = loss_fn(net(X_tr), y_tr)
    opt.zero_grad()
    loss.backward()
    opt.step()

# BLOCK 7: evaluate on unseen points (no gradients needed)
net.eval()
with torch.no_grad():
    probs = torch.sigmoid(net(X_te))             # score -> probability 0..1
    predicted = (probs > 0.5).float()
    accuracy = (predicted == y_te).float().mean().item()
print(f"Circle classifier accuracy on unseen points: {accuracy:.2%}")

# BLOCK 8: use it on new points
with torch.no_grad():
    for p in ([0.0, 0.0], [1.8, 1.8]):
        prob = torch.sigmoid(net(torch.tensor([p]))).item()
        print(f"Point {p}: probability inside circle = {prob:.2f}")
