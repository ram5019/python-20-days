"""Track 4a example: scikit-learn, machine learning basics.

Run:    python3 learning-path/advanced/examples/t4_sklearn.py
Needs:  pip install scikit-learn
"""

import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, mean_absolute_error
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------------------------
# PART A: REGRESSION: predict a NUMBER
# ---------------------------------------------------------------

# BLOCK 1: data: X = inputs (features), y = what we want to predict (target)
# Pretend: disk usage (GB) as a function of days since install
rng = np.random.default_rng(0)
days = rng.uniform(1, 100, size=60).reshape(-1, 1)         # X must be 2-D: (rows, features)
usage = 5 + 2.5 * days.ravel() + rng.normal(0, 8, size=60)  # hidden rule + noise

# BLOCK 2: split into training data and test data the model has never seen
X_train, X_test, y_train, y_test = train_test_split(days, usage, test_size=0.25, random_state=0)

# BLOCK 3: create, train (fit) and use (predict) the model
model = LinearRegression()
model.fit(X_train, y_train)
print(f"Learned rule: usage = {model.intercept_:.1f} + {model.coef_[0]:.2f} * days   (truth: 5 + 2.5*days)")
print("Prediction for day 120:", round(float(model.predict([[120]])[0]), 1), "GB")

# BLOCK 4: evaluate on the TEST set
pred = model.predict(X_test)
print("Average error on unseen data:", round(mean_absolute_error(y_test, pred), 1), "GB")

# ---------------------------------------------------------------
# PART B: CLASSIFICATION: predict a CATEGORY
# ---------------------------------------------------------------

# BLOCK 5: a classic dataset: 150 flowers, 4 measurements, 3 species
iris = load_iris()
X, y = iris.data, iris.target
print("\nFeatures:", iris.feature_names)
print("Classes :", iris.target_names.tolist(), "| samples:", X.shape[0])

# BLOCK 6: train/test split (stratify keeps the class mix equal in both sets)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# BLOCK 7: try a model and measure accuracy
clf = LogisticRegression(max_iter=500)
clf.fit(X_train, y_train)
print("Logistic regression accuracy:", round(accuracy_score(y_test, clf.predict(X_test)), 3))

# BLOCK 8: same API, different model: swap with one line
forest = RandomForestClassifier(n_estimators=100, random_state=42)
forest.fit(X_train, y_train)
print("Random forest accuracy      :", round(forest.score(X_test, y_test), 3))   # .score = accuracy

# BLOCK 9: where does it get things wrong? confusion matrix
print("Confusion matrix (rows=true, cols=predicted):")
print(confusion_matrix(y_test, forest.predict(X_test)))

# BLOCK 10: which features mattered?
for name, importance in zip(iris.feature_names, forest.feature_importances_):
    print(f"  {name:<20} {importance:.2f}")

# BLOCK 11: predict a single new flower
new_flower = [[5.9, 3.0, 5.1, 1.8]]
print("New flower is:", iris.target_names[forest.predict(new_flower)[0]])

# BLOCK 12: a pipeline bundles preprocessing + model (prevents data leaks)
pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=500))
scores = cross_val_score(pipe, X, y, cv=5)                 # 5 different train/test splits
print("\n5-fold cross-validation:", scores.round(2), "| mean:", round(scores.mean(), 3))
