import numpy as np
from matplotlib.lines import Line2D  # For the custom legend
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import GridSearchCV, cross_val_predict


def load_wdbc_data(filename):
    """Class for loading Wisconsin Diagnostic Breast Cancer (WDBC) data."""
    class WDBCData:
        """Class for storing Wisconsin Diagnostic Breast Cancer (WDBC) data."""
        data = []  # Shape: (569, 30)
        target = []  # Shape: (569, )
        target_names = ["malignant", "benign"]
        feature_names = [
            "mean radius",
            "mean texture",
            "mean perimeter",
            "mean area",
            "mean smoothness",
            "mean compactness",
            "mean concavity",
            "mean concave points",
            "mean symmetry",
            "mean fractal dimension",
            "radius error",
            "texture error",
            "perimeter error",
            "area error",
            "smoothness error",
            "compactness error",
            "concavity error",
            "concave points error",
            "symmetry error",
            "fractal dimension error",
            "worst radius",
            "worst texture",
            "worst perimeter",
            "worst area",
            "worst smoothness",
            "worst compactness",
            "worst concavity",
            "worst concave points",
            "worst symmetry",
            "worst fractal dimension",
        ]

    wdbc_data = WDBCData()
    with open(filename, encoding="utf-8") as f:
        data_list = []
        for line in f.readlines():
            items = line.split(",")
            wdbc_data.target.append(0 if items[1] == "M" else 1)
            data_list.append([float(x) for x in items[2:]])
        wdbc_data.data = np.array(data_list)
    return wdbc_data


if __name__ == "__main__":
    # Load a dataset
    wdbc = load_wdbc_data("data/wdbc.data")

    X_train, y_train = wdbc.data, wdbc.target

    # Hyperparameter tuning using GridSearchCV
    param_grid = {
        "n_estimators": [50, 100, 200],
        "max_depth": [None, 10, 20, 30],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
    }
    grid_search = GridSearchCV(
        RandomForestClassifier(), param_grid, cv=5, scoring="balanced_accuracy"
    )
    grid_search.fit(X_train, y_train)

    # Train a model with the best parameters
    model = grid_search.best_estimator_

    # Evaluate the model using cross-validation
    predict = cross_val_predict(model, X_train, y_train, cv=5)
    accuracy = metrics.balanced_accuracy_score(y_train, predict)

    # Visualize the confusion matrix
    ConfusionMatrixDisplay.from_predictions(
        y_train, predict, display_labels=wdbc.target_names, cmap=plt.get_cmap('Blues')
    )
    plt.title("Confusion Matrix")
    plt.savefig("wdbc_classification_matrix.png")
    plt.show()

    # Visualize testing results
    cmap = np.array([(1, 0, 0), (0, 1, 0)])
    clabel = [
        Line2D([0], [0], marker="o", lw=0, label=wdbc.target_names[i], color=cmap[i])
        for i in range(len(cmap))
    ]
    for x, y in [(0, 1)]:
        plt.figure()
        plt.title(f"My Classifier (Accuracy: {accuracy:.3f})")
        plt.scatter(
            X_train[:, x],
            X_train[:, y],
            c=cmap[y_train],
            edgecolors=cmap[predict],
        )
        plt.xlabel(wdbc.feature_names[x])
        plt.ylabel(wdbc.feature_names[y])
        plt.legend(handles=clabel, framealpha=0.5)
    plt.savefig("wdbc_classification_scatter.png")
    plt.show()
