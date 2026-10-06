# Track 4: AI/ML, scikit-learn and PyTorch

**Examples:** `examples/t4_sklearn.py`, `examples/t4_pytorch.py`
**Install:** `pip install scikit-learn` | `pip install torch` (large; CPU build is enough to learn)
**Prerequisites:** Track 1 (NumPy arrays, Pandas), Day 18 (classes: `nn.Module` is a class), Day 23 (the `with` idea helps)

---

## 1. The big idea

**Machine learning (ML)** is a different way to write programs:

```
Normal programming:   rules + data   ──►  answers
Machine learning:     data + answers ──►  rules (a "model")
                      then: model + NEW data ──► predictions
```

Instead of writing "if disk usage grows by X, alert", you **show examples** and the algorithm **works out the rule** itself.

Two kinds of prediction cover most beginner problems:

| Type | Predicts | Example |
|------|----------|---------|
| **Regression** | a number | how many GB will be used on day 120? |
| **Classification** | a category | is this log line an error? which species is this flower? |

## 2. Why do these libraries exist?

- **scikit-learn:** the standard toolbox for **classical ML** on tables of data. Every model has the same three methods (`fit`, `predict`, `score`), so you can swap algorithms with one line. Start here.
- **PyTorch:** the standard toolbox for **deep learning** (neural networks): images, text, speech, and large language models. It gives you tensors, automatic derivatives and building blocks to design your own models.

Honest guidance: for **tabular data** (rows and columns) scikit-learn is usually the right tool and often wins. Reach for PyTorch for unstructured data or when you need custom neural networks.

## 3. Simple way to understand

**Training a new colleague.**
- You show them 1,000 past tickets with the correct category on each (**training data**).
- They start guessing, get corrected, and slowly adjust their judgement (**fitting**).
- Then you test them on tickets they have never seen (**test data**). If they only memorised the old ones, they will fail. That is **overfitting**.
- If they pass, you trust them with new tickets (**predict**).

Everything in the examples follows this story.

## 4. The key vocabulary

| Term | Meaning |
|------|---------|
| **features (X)** | the inputs: columns the model looks at |
| **target (y)** | the answer you want to predict |
| **train/test split** | keep some data hidden to check honestly |
| **fit** | learn from training data |
| **predict** | answer for new data |
| **loss** | a number saying "how wrong am I?" (lower is better) |
| **overfitting** | memorised training data, fails on new data |
| **epoch** | one full pass over the training data |
| **gradient** | which direction to nudge each parameter to reduce loss |

---

## Part 1: scikit-learn (`t4_sklearn.py`)

### Code walkthrough

**Part A: Regression (predict a number)**

| Block | Code | What it does |
|-------|------|--------------|
| 1 | NumPy arrays `days`, `usage`; `.reshape(-1, 1)` | builds data from a hidden rule (`5 + 2.5*days`) plus noise. **X must be 2-D** (rows × features), even with one feature |
| 2 | `train_test_split(..., test_size=0.25)` | hides 25% of the data. `random_state` makes the split repeatable |
| 3 | `LinearRegression()`, `.fit(...)`, `.predict(...)` | **the three-step pattern.** It recovers a rule close to the truth (about `2.8 + 2.54*days`; the noise stops it being exact) |
| 4 | `mean_absolute_error` on the **test** data | the honest score: average miss, in the target's units (GB) |

**Part B: Classification (predict a category)**

| Block | Code | What it does |
|-------|------|--------------|
| 5 | `load_iris()` | built-in dataset: 150 flowers, 4 measurements, 3 species. No download needed |
| 6 | `stratify=y` | keeps the species mix equal in train and test |
| 7 | `LogisticRegression` + `accuracy_score` | first model; accuracy = fraction predicted correctly |
| 8 | `RandomForestClassifier` | **the same fit/predict/score API**, different algorithm: this is scikit-learn's big idea |
| 9 | `confusion_matrix` | rows = true class, columns = predicted: shows **which** classes get confused (here, versicolor vs virginica) |
| 10 | `feature_importances_` | which inputs mattered (petal measurements dominate); `zip` pairs names with values |
| 11 | `forest.predict([[5.9, 3.0, 5.1, 1.8]])` | use the trained model on a new sample |
| 12 | `make_pipeline(StandardScaler(), ...)`, `cross_val_score(cv=5)` | a **pipeline** chains steps so scaling is learned only from training data; **cross-validation** repeats the train/test experiment 5 times for a steadier estimate |

**How the blocks connect:** data (1, 5) → split (2, 6) → fit (3, 7, 8) → evaluate (4, 7 to 9) → understand (10) → use (11) → make it robust (12).

**A fair warning about the numbers:** the test set has only 38 flowers, so one mistake moves accuracy by about 2.6 points. My run gave logistic regression 0.947 and random forest 0.921, but that difference is **noise, not proof one is better**. The cross-validation mean (0.96) is the steadier figure. Judging models on tiny test sets is a classic beginner trap.

### The universal scikit-learn recipe
```python
model = SomeModel()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
score = model.score(X_test, y_test)
```

---

## Part 2: PyTorch (`t4_pytorch.py`)

### Code walkthrough

| Block | Code | What it does |
|-------|------|--------------|
| 1 | `torch.tensor([...])` | a **tensor** = NumPy-style array that can also live on a GPU and track gradients. `.item()` extracts a plain Python number |
| 2 | `requires_grad=True`, `y.backward()`, `x.grad` | **autograd**: PyTorch records the maths and computes the derivative. `y = x² + 2x` → `dy/dx = 2x + 2 = 8` at `x=3` |
| 3 | manual gradient descent on `w` | learning **by hand**: guess `w`, measure `loss`, compute the gradient, step downhill (`w -= 0.05 * w.grad`), reset the gradient. After 50 steps `w ≈ 2.0` |
| 4 | `nn.Linear`, `MSELoss`, `SGD`; the five-line loop | the same learning with PyTorch's building blocks |
| 5 | `class CircleNet(nn.Module)` with `nn.Sequential` | your own **neural network**, a class (Day 18) whose `__init__` defines layers and `forward` defines how data flows. `ReLU` between layers lets it learn curves (a straight line cannot separate "inside a circle") |
| 6 | the training loop | the same five steps again, with `Adam` (a smarter optimiser) |
| 7 | `net.eval()`, `torch.no_grad()`, `sigmoid` | evaluate on unseen points; no gradients needed; sigmoid turns a score into a 0 to 1 probability |
| 8 | predict single points | the centre gets a high probability, the far corner about 0 |

### The five-step training loop (memorise this)
```python
for epoch in range(N):
    pred = model(X)              # 1. forward pass
    loss = loss_fn(pred, Y)      # 2. how wrong?
    optimizer.zero_grad()        # 3. clear old gradients
    loss.backward()              # 4. compute new gradients
    optimizer.step()             # 5. update the parameters
```
Block 3 is this same loop written out by hand, so you see **what each line is really doing**.

**How the blocks connect:** tensors (1) → gradients (2) → learning by hand (3) → the same thing with PyTorch tools (4) → a bigger model (5, 6) → honest evaluation (7) → use (8).

**Tested:** I ran this on CPU in about one second: it recovered `w = 2.000` and a line of about `3.03x + 3.85` (truth `3x + 4`), and reached about 99% accuracy on unseen points. Exact numbers depend on the random seed.

---

## scikit-learn vs PyTorch

| | scikit-learn | PyTorch |
|---|--------------|---------|
| Best for | tables, quick baselines | images, text, custom neural nets |
| You write | 3 lines (`fit`, `predict`, `score`) | the training loop |
| Hardware | CPU is fine | GPU helps for big models |
| Learning curve | gentle | steeper |
| Start with it when | almost always | you have a deep-learning need |

## 7. Common mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Scoring on the **training** data | looks perfect, fails in real use | always score on held-out test data |
| Scaling or cleaning **before** splitting | information leaks from test to train | use a `Pipeline` |
| Passing a 1-D array as X | `ValueError: Expected 2D array` | `.reshape(-1, 1)` |
| Trusting accuracy on a tiny test set | misleading | use cross-validation |
| Accuracy alone on imbalanced data (99% "normal") | useless metric | look at the confusion matrix, precision/recall |
| Forgetting `optimizer.zero_grad()` | gradients accumulate, training goes wrong | call it every step |
| Forgetting `torch.no_grad()` when evaluating | wasted memory | wrap evaluation |
| Mixing data types (`int` vs `float32`) in PyTorch | dtype errors | use floats: `1.0`, `.float()` |
| Treating a model as truth | wrong decisions | models only learn patterns present in the data |
| Using personal or sensitive data carelessly | privacy and fairness problems | think about what data you use and who is affected |

## 8. Practice (in order)

1. **sklearn:** change `test_size` and `random_state` in Part B and watch how accuracy moves. What does that tell you about small test sets?
2. **sklearn:** swap in `KNeighborsClassifier` or `DecisionTreeClassifier`: one line each.
3. **sklearn:** load `load_wine()` instead of iris and run the same recipe.
4. **sklearn + Track 1:** put your own CSV into Pandas, pick numeric feature columns and a target column, and fit a model.
5. **sklearn mini-project:** from a table of node metrics (CPU, memory, latency) with a label `incident` yes/no, train a classifier and check the confusion matrix. (You can generate fake data to practise.)
6. **PyTorch:** in Block 3, change the learning rate to `0.5`, then `0.001`. What happens to `w`?
7. **PyTorch:** change the circle radius or make the network smaller (4 hidden units). When does accuracy drop?
8. **PyTorch:** write down, in your own words, what each of the five loop lines does.

## 9. Self-check

- What is the difference between regression and classification?
- Why do we hold back a test set?
- What are `fit`, `predict` and `score`?
- What does `loss.backward()` compute?
- Why did the circle problem need hidden layers and `ReLU`?
- What is overfitting, and how would you notice it?
- Why isn't 99% accuracy always good?

**Next:** Track 5: Cloud/DevOps, where Python manages real infrastructure through SDKs.
