import seaborn as sns
import matplotlib.pyplot as plt

def lineplot(y_test, y_test_predict, n, name):
    x = list(range(0, n))
    fix, ax = plt.subplots(figsize=(20, 5))
    sns.lineplot(x = x, y = y_test[:n], label = 'actual_values');
    sns.lineplot(x = x, y = y_test_predict[:n], label = 'predicted_values');

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.xaxis.label.set_size(16)
    ax.yaxis.label.set_size(16)    
    
    plt.title("Comparison of Real vs Predicted");
    plt.savefig(f"images/{name}_lineplot.png")
    plt.show()