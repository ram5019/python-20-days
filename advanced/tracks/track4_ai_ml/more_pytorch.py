"""PyTorch: 10 examples, simple to complex.

Run:    python3 advanced/tracks/track4_ai_ml/more_pytorch.py
Needs:  pip install torch numpy    (the CPU version of torch is enough; it is a large download)

Everything runs on the CPU in a few seconds. Random seeds are fixed so results
repeat (tiny differences between machines are normal).
"""

import tempfile
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset, random_split

torch.manual_seed(0)


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Tensors: the basic data type")
# WHAT: PyTorch's version of a NumPy array.
# HOW : torch.tensor / zeros / ones / arange / rand. dtype, shape and device
#       describe it.
# WHY : models take tensors in and give tensors out.
a = torch.tensor([1.0, 2.0, 3.0])
print(a, a.dtype, a.shape)
print(torch.zeros(2, 3), torch.arange(5), torch.linspace(0, 1, 5))
print(torch.rand(2, 2).shape, torch.tensor([1, 2, 3]).dtype)

# ---------------------------------------------------------------
show(2, "Tensor maths, indexing and reshaping")
# WHAT: the same ideas as NumPy.
# HOW : operators are element by element; @ is matrix multiplication; slicing
#       and reshape work as you expect; .item() extracts a plain number.
# WHY : you will do this all the time while preparing data.
x = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
y = torch.tensor([[10.0, 20.0], [30.0, 40.0]])
print(x + y, x * y, sep="\n")
print("matmul:\n", x @ y)
print(x.sum().item(), x.mean(dim=0), x.max(dim=1).values)
print(x[:, 0], x.reshape(4), x.T, x[x > 1.5])

# ---------------------------------------------------------------
show(3, "NumPy interoperability and devices")
# WHAT: move data between libraries; know where a tensor lives.
# HOW : torch.from_numpy / .numpy() share memory on the CPU; .to(device) moves
#       a tensor to a GPU when one exists.
# WHY : data usually starts life in NumPy or Pandas.
arr = np.array([1.0, 2.0, 3.0], dtype=np.float32)
t = torch.from_numpy(arr)
t[0] = 99
print("numpy array changed too:", arr)
print(t.numpy().dtype, "| CUDA available:", torch.cuda.is_available())
device = "cuda" if torch.cuda.is_available() else "cpu"
print("using device:", device, "| tensor lives on:", t.to(device).device.type)

# ---------------------------------------------------------------
show(4, "Autograd: automatic derivatives")
# WHAT: PyTorch differentiates for you.
# HOW : requires_grad=True records operations; .backward() fills .grad.
# WHY : training a model means following gradients downhill.
w = torch.tensor(3.0, requires_grad=True)
f = w ** 2 + 2 * w + 1                       # f(w) = (w+1)^2
f.backward()
print("df/dw at w=3 :", w.grad.item(), "(expected 2*3+2 = 8)")
v = torch.tensor([1.0, 2.0], requires_grad=True)
(v ** 2).sum().backward()
print("gradient of sum(v^2):", v.grad.tolist())
with torch.no_grad():
    print("inside no_grad, tracking is off:", (v * 2).requires_grad)

# ---------------------------------------------------------------
show(5, "Gradient descent by hand")
# WHAT: learn y = 2x by repeatedly stepping against the gradient.
# HOW : compute loss, backward(), update the parameter, zero the gradient.
# WHY : this loop IS training; everything later automates it.
X = torch.tensor([1.0, 2.0, 3.0, 4.0])
Y = 2 * X
w = torch.tensor(0.0, requires_grad=True)
for step in range(60):
    loss = ((w * X - Y) ** 2).mean()
    loss.backward()
    with torch.no_grad():
        w -= 0.05 * w.grad
    w.grad.zero_()
    if step in (0, 9, 59):
        print(f"step {step:>2}: w = {w.item():.3f}, loss = {loss.item():.4f}")

# ---------------------------------------------------------------
show(6, "nn.Linear, a loss and an optimiser")
# WHAT: the same learning with PyTorch's building blocks.
# HOW : model, loss function and optimiser, then the five-line loop:
#       forward, loss, zero_grad, backward, step.
# WHY : the template for every model you will train.
Xl = torch.linspace(0, 10, 100).unsqueeze(1)
Yl = 3 * Xl + 4 + 0.5 * torch.randn_like(Xl)
model = nn.Linear(1, 1)
loss_fn = nn.MSELoss()
opt = torch.optim.SGD(model.parameters(), lr=0.02)
for epoch in range(400):
    pred = model(Xl)
    loss = loss_fn(pred, Yl)
    opt.zero_grad()
    loss.backward()
    opt.step()
print(f"learned y = {model.weight.item():.2f}x + {model.bias.item():.2f}   (truth 3x + 4)")

# ---------------------------------------------------------------
show(7, "Datasets and DataLoaders: mini-batches")
# WHAT: feed data in small shuffled batches.
# HOW : TensorDataset pairs inputs and targets; DataLoader batches and
#       shuffles; random_split makes train/validation sets.
# WHY : real datasets are too big to process at once.
data = TensorDataset(torch.arange(20, dtype=torch.float32).unsqueeze(1), torch.arange(20) % 2)
train_set, val_set = random_split(data, [16, 4], generator=torch.Generator().manual_seed(0))
loader = DataLoader(train_set, batch_size=5, shuffle=True)
print("train/val sizes:", len(train_set), len(val_set), "| batches per epoch:", len(loader))
for batch_x, batch_y in loader:
    print("batch:", tuple(batch_x.shape), tuple(batch_y.shape))
    break

# ---------------------------------------------------------------
show(8, "A neural network for a non-linear problem")
# WHAT: classify points inside versus outside a circle.
# HOW : an nn.Module with hidden layers and ReLU; BCEWithLogitsLoss for a
#       yes/no target; evaluate with no_grad.
# WHY : a straight line cannot separate this; hidden layers can.
pts = torch.rand(800, 2) * 4 - 2
labels = (pts.pow(2).sum(dim=1) < 1.0).float().unsqueeze(1)
Xtr, Xte, ytr, yte = pts[:600], pts[600:], labels[:600], labels[600:]


class CircleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(nn.Linear(2, 16), nn.ReLU(),
                                    nn.Linear(16, 16), nn.ReLU(),
                                    nn.Linear(16, 1))

    def forward(self, x):
        return self.layers(x)


net = CircleNet()
opt = torch.optim.Adam(net.parameters(), lr=0.02)
bce = nn.BCEWithLogitsLoss()
for epoch in range(300):
    loss = bce(net(Xtr), ytr)
    opt.zero_grad()
    loss.backward()
    opt.step()
net.eval()
with torch.no_grad():
    accuracy = ((torch.sigmoid(net(Xte)) > 0.5).float() == yte).float().mean().item()
print(f"test accuracy: {accuracy:.1%} | parameters: {sum(p.numel() for p in net.parameters())}")

# ---------------------------------------------------------------
show(9, "Save, load and predict")
# WHAT: keep a trained model and use it later.
# HOW : save the state_dict (the weights); rebuild the class; load_state_dict;
#       call eval() before predicting.
# WHY : training once, using many times.
with tempfile.TemporaryDirectory() as folder:
    path = Path(folder) / "circle.pt"
    torch.save(net.state_dict(), path)
    fresh = CircleNet()
    print("before loading, a fresh net is untrained:", round(fresh(torch.tensor([[0.0, 0.0]])).item(), 3))
    fresh.load_state_dict(torch.load(path))
    fresh.eval()
    with torch.no_grad():
        for point in ([0.0, 0.0], [0.5, 0.5], [1.8, 1.8]):
            p = torch.sigmoid(fresh(torch.tensor([point]))).item()
            print(f"point {point}: P(inside) = {p:.2f}")

# ---------------------------------------------------------------
show(10, "Mini program: tabular regression with validation and early stopping")
# WHAT: predict a number from several features, the realistic way.
# HOW : standardise the inputs, split train/validation, train in batches,
#       watch the validation loss, stop when it stops improving, keep the best
#       weights.
# WHY : validation tells you when to stop; early stopping prevents overfitting.
g = torch.Generator().manual_seed(1)
n = 600
features = torch.rand(n, 3, generator=g) * torch.tensor([100.0, 50.0, 10.0])     # cpu, memory, users
target = (0.4 * features[:, 0] + 0.9 * features[:, 1] + 3.0 * features[:, 2] + 10
          + 4 * torch.randn(n, generator=g)).unsqueeze(1)                         # response time
mean, std = features.mean(0), features.std(0)
features = (features - mean) / std
dataset = TensorDataset(features, target)
train_ds, val_ds = random_split(dataset, [480, 120], generator=torch.Generator().manual_seed(2))
train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
Xv, yv = val_ds[:][0], val_ds[:][1]

reg = nn.Sequential(nn.Linear(3, 16), nn.ReLU(), nn.Linear(16, 1))
opt = torch.optim.Adam(reg.parameters(), lr=0.02)
best, best_state, patience, waited = float("inf"), None, 8, 0
for epoch in range(200):
    reg.train()
    for xb, yb in train_loader:
        loss = nn.functional.mse_loss(reg(xb), yb)
        opt.zero_grad()
        loss.backward()
        opt.step()
    reg.eval()
    with torch.no_grad():
        val_loss = nn.functional.mse_loss(reg(Xv), yv).item()
    if val_loss < best - 1e-3:
        best, best_state, waited = val_loss, {k: v.clone() for k, v in reg.state_dict().items()}, 0
    else:
        waited += 1
        if waited >= patience:
            print(f"early stop at epoch {epoch}")
            break
reg.load_state_dict(best_state)
with torch.no_grad():
    rmse = nn.functional.mse_loss(reg(Xv), yv).sqrt().item()
print(f"validation RMSE: {rmse:.2f}  (noise level in the data is about 4)")
new = (torch.tensor([[80.0, 40.0, 8.0]]) - mean) / std
print("predicted response time for cpu=80, mem=40, users=8:", round(reg(new).item(), 1))
