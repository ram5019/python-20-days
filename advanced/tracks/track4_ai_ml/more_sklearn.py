"""scikit-learn: 10 examples, simple to complex.

Run:    python3 advanced/tracks/track4_ai_ml/more_sklearn.py
Needs:  pip install scikit-learn

Every model follows the same three steps: fit(X, y), predict(X), score(X, y).
All data is built-in or generated with a fixed seed, so results repeat.
"""

import tempfile
from pathlib import Path

import numpy as np
from sklearn.datasets import load_iris, make_classification, make_regression
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             mean_absolute_error, r2_score)
from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

import joblib


def show(n, title):
    print(f"\n=== Example {n}: {title} ===")


# ---------------------------------------------------------------
show(1, "Features, target and a train/test split")
# WHAT: the vocabulary and the honest-testing rule.
# HOW : X = inputs (features), y = the answer to predict. Hold back some data
#       the model never sees. random_state makes the split repeatable.
# WHY : a model must be judged on data it has not memorised.
iris = load_iris()
X, y = iris.data, iris.target
print("features:", iris.feature_names)
print("shape:", X.shape, "| classes:", iris.target_names.tolist())
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y)
print("train:", len(X_train), "| test:", len(X_test))

# ---------------------------------------------------------------
show(2, "Regression: predict a number")
# WHAT: learn a straight-line rule.
# HOW : LinearRegression().fit; read the learned coefficients; score with
#       mean absolute error (average miss) and R2 (1.0 is perfect).
# WHY : the simplest model, and a baseline for everything else.
rng = np.random.default_rng(0)
days = rng.uniform(1, 100, size=(80, 1))
usage = 5 + 2.5 * days[:, 0] + rng.normal(0, 8, 80)          # hidden rule + noise
Xd_train, Xd_test, yd_train, yd_test = train_test_split(days, usage, random_state=0)
reg = LinearRegression().fit(Xd_train, yd_train)
pred = reg.predict(Xd_test)
print(f"learned: usage = {reg.intercept_:.1f} + {reg.coef_[0]:.2f} * days   (truth 5 + 2.5*days)")
print(f"MAE {mean_absolute_error(yd_test, pred):.1f} | R2 {r2_score(yd_test, pred):.3f}")
print("forecast for day 120:", round(float(reg.predict([[120]])[0]), 1))

# ---------------------------------------------------------------
show(3, "Classification: predict a category")
# WHAT: species of flower from four measurements.
# HOW : LogisticRegression; accuracy = fraction correct on the test set.
# WHY : "which class?" problems: spam, fraud, failure/no failure.
clf = LogisticRegression(max_iter=500).fit(X_train, y_train)
print("accuracy:", round(accuracy_score(y_test, clf.predict(X_test)), 3))
print("probabilities for one flower:", clf.predict_proba(X_test[:1]).round(3))
print("predicted:", iris.target_names[clf.predict(X_test[:1])[0]])

# ---------------------------------------------------------------
show(4, "Beyond accuracy: confusion matrix, precision, recall")
# WHAT: see WHICH mistakes are made.
# HOW : rows = true class, columns = predicted class. precision = "of what I
#       flagged, how much was right"; recall = "of the real ones, how many I found".
# WHY : accuracy alone misleads, especially with rare events.
pred = clf.predict(X_test)
print(confusion_matrix(y_test, pred))
print(classification_report(y_test, pred, target_names=iris.target_names, digits=2))

# ---------------------------------------------------------------
show(5, "Swap algorithms: the API stays the same")
# WHAT: compare four different models in a loop.
# HOW : every estimator has fit/predict/score, so they are interchangeable.
# WHY : try several quickly; keep the best. (Tiny test sets are noisy:
#       differences of a point or two mean little.)
models = {
    "logistic": LogisticRegression(max_iter=500),
    "knn(5)": KNeighborsClassifier(5),
    "tree": DecisionTreeClassifier(random_state=0),
    "forest": RandomForestClassifier(n_estimators=100, random_state=0),
}
for name, model in models.items():
    model.fit(X_train, y_train)
    print(f"{name:<9} test accuracy {model.score(X_test, y_test):.3f}")

# ---------------------------------------------------------------
show(6, "Scaling and pipelines")
# WHAT: put preprocessing and the model in one object.
# HOW : make_pipeline(StandardScaler(), model). Scaling is learned from the
#       TRAINING data only, which avoids leaking test information.
# WHY : distance-based models (KNN, SVM) break when features have different
#       scales; pipelines also make deployment a single object.
Xw, yw = make_classification(n_samples=400, n_features=6, n_informative=4, random_state=1)
Xw[:, 0] *= 1000                                       # one feature on a huge scale
Xw_tr, Xw_te, yw_tr, yw_te = train_test_split(Xw, yw, random_state=1)
plain = KNeighborsClassifier().fit(Xw_tr, yw_tr)
piped = make_pipeline(StandardScaler(), KNeighborsClassifier()).fit(Xw_tr, yw_tr)
print("KNN without scaling:", round(plain.score(Xw_te, yw_te), 3))
print("KNN with scaling   :", round(piped.score(Xw_te, yw_te), 3))

# ---------------------------------------------------------------
show(7, "Cross-validation: a steadier score")
# WHAT: evaluate on several different splits.
# HOW : cross_val_score(model, X, y, cv=5) trains and tests five times.
# WHY : one split can be lucky or unlucky.
scores = cross_val_score(make_pipeline(StandardScaler(), LogisticRegression(max_iter=500)), X, y, cv=5)
print("fold scores:", scores.round(2))
print(f"mean {scores.mean():.3f} +/- {scores.std():.3f}")

# ---------------------------------------------------------------
show(8, "Tune settings with GridSearchCV")
# WHAT: find good hyper-parameters automatically.
# HOW : give a grid of values; it cross-validates every combination.
# WHY : settings like tree depth or K change results a lot.
grid = GridSearchCV(KNeighborsClassifier(), {"n_neighbors": [1, 3, 5, 9, 15], "weights": ["uniform", "distance"]}, cv=5)
grid.fit(X_train, y_train)
print("best settings:", grid.best_params_)
print("best CV score:", round(grid.best_score_, 3), "| test score:", round(grid.score(X_test, y_test), 3))

# ---------------------------------------------------------------
show(9, "Overfitting, and what the model learned")
# WHAT: a model that memorises noise.
# HOW : deeper trees fit training data better and generalise worse. Compare
#       train and test scores. Forest feature importances show what mattered.
# WHY : a big gap between train and test accuracy is the warning sign.
Xn, yn = make_classification(n_samples=600, n_features=10, n_informative=3, flip_y=0.15, random_state=2)
Xn_tr, Xn_te, yn_tr, yn_te = train_test_split(Xn, yn, random_state=2)
for depth in (1, 3, 6, None):
    tree = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(Xn_tr, yn_tr)
    print(f"max_depth={depth!s:<5} train {tree.score(Xn_tr, yn_tr):.2f}  test {tree.score(Xn_te, yn_te):.2f}")
forest = RandomForestClassifier(n_estimators=100, random_state=0).fit(X_train, y_train)
for name, imp in sorted(zip(iris.feature_names, forest.feature_importances_), key=lambda p: -p[1]):
    print(f"  {name:<20} {imp:.2f}")

# ---------------------------------------------------------------
show(10, "Mini program: train, save, load and use a model")
# WHAT: a failure predictor, from raw table to saved model.
# HOW : build data, make a Pipeline, evaluate, save with joblib, reload and
#       predict for new machines.
# WHY : a model is only useful once something else can load and call it.
rng = np.random.default_rng(5)
n = 500
cpu = rng.uniform(5, 100, n)
temp = rng.normal(55, 10, n) + cpu * 0.2
errors = rng.poisson(cpu / 25)
fails = ((cpu > 80) & (temp > 65) | (errors > 5)).astype(int)
table = np.column_stack([cpu, temp, errors])
X_tr, X_te, y_tr, y_te = train_test_split(table, fails, random_state=0, stratify=fails)
model = make_pipeline(StandardScaler(), RandomForestClassifier(n_estimators=150, random_state=0))
model.fit(X_tr, y_tr)
print(f"failure rate in data: {fails.mean():.0%} | test accuracy: {model.score(X_te, y_te):.3f}")
print(classification_report(y_te, model.predict(X_te), digits=2))
with tempfile.TemporaryDirectory() as folder:
    path = Path(folder) / "failure_model.joblib"
    joblib.dump(model, path)
    reloaded = joblib.load(path)
    new_machines = [[95, 75, 6], [30, 50, 0], [85, 70, 2]]
    print("risk of failure:", reloaded.predict_proba(new_machines)[:, 1].round(2).tolist())
    print("saved model size:", "small" if path.stat().st_size < 5_000_000 else "large")
