import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

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

def residue_plot(y_test, y_test_predict, n, name):
    pltdf = pd.DataFrame({'predict': y_test_predict, 'diff':y_test_predict-y_test})
    pltdf_sample = pltdf.sample(2000)
    fix, ax = plt.subplots(figsize=(20, 5))
    plt.scatter(pltdf_sample['predict'], pltdf_sample['diff'], alpha=0.5)
    plt.title('Residual Plot for Linear Regression')
    plt.xlabel('Predicted Values')
    plt.ylabel('Residuals')
    plt.axhline(y=0, color='r', linestyle='-')
    plt.savefig(f"images/{name}_residue_plot.png")
    plt.show()
    
