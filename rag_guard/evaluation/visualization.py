import matplotlib.pyplot as plt

def plot_confusion_matrix(tp, fp, tn, fn):

    matrix = [
        [tp, fn],
        [fp, tn]
    ]

    fig, ax = plt.subplots()

    ax.imshow(matrix)

    ax.set_xticks([0,1])
    ax.set_yticks([0,1])

    ax.set_xticklabels(["Pred Mal", "Pred Ben"])
    ax.set_yticklabels(["Actual Mal", "Actual Ben"])

    for i in range(2):
        for j in range(2):
            ax.text(j, i, matrix[i][j], ha="center", va="center", fontsize=14)

    plt.title("Confusion Matrix")
    plt.show()

def plot_metrics(metrics):

    names = ["Accuracy", "Precision", "Recall", "F1", "FPR"]
    values = [
        metrics["accuracy"],
        metrics["precision"],
        metrics["recall"],
        metrics["f1"],
        metrics["fpr"]
    ]

    plt.figure()
    plt.bar(names, values)
    plt.ylim(0,1)
    plt.title("Guard Performance Metrics")
    plt.show()


