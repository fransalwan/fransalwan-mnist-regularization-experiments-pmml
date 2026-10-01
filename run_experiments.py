import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, regularizers
from tensorflow.keras.callbacks import EarlyStopping

# Set random seed for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Create output directories for plots and models
os.makedirs("plots", exist_ok=True)
os.makedirs("models", exist_ok=True)

# 1. Load and preprocess MNIST dataset (matching slides page 19)
print("--- 1. Loading MNIST Dataset ---")
from tensorflow.keras.datasets import mnist

(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(-1, 28, 28, 1).astype("float32") / 255.0
X_test = X_test.reshape(-1, 28, 28, 1).astype("float32") / 255.0

y_train = keras.utils.to_categorical(y_train, 10)
y_test = keras.utils.to_categorical(y_test, 10)

print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
print(f"X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")


# Function to plot and save loss chart
def plot_and_save_chart(history, title, filename, early_stop_epoch=None):
    plt.figure(figsize=(8, 5), dpi=300)
    epochs = range(1, len(history.history["loss"]) + 1)

    plt.plot(
        epochs,
        history.history["loss"],
        "r-o",
        label="Training loss",
        linewidth=2,
        markersize=4,
    )
    plt.plot(
        epochs,
        history.history["val_loss"],
        "b-s",
        label="Validation loss",
        linewidth=2,
        markersize=4,
    )

    if early_stop_epoch:
        plt.axvline(
            x=early_stop_epoch,
            color="green",
            linestyle="--",
            label=f"Early Stop (Epoch {early_stop_epoch})",
        )

    plt.title(title, fontsize=14, fontweight="bold", pad=12)
    plt.xlabel("Epochs", fontsize=12)
    plt.ylabel("Loss", fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"plots/{filename}", dpi=300)
    plt.close()
    print(f"Saved plot: plots/{filename}")


# Function to get model summary string
def get_summary_str(model):
    lines = []
    model.summary(print_fn=lambda x: lines.append(x))
    return "\n".join(lines)


results = {}

# ==========================================
# REPLICATION BASELINE (Slide 20-23)
# ==========================================
print("\n=== Baseline Replication (Slides 20-23) ===")
baseline_model = keras.Sequential(
    [
        layers.Flatten(input_shape=(28, 28, 1)),
        layers.Dense(64, activation="relu"),
        layers.Dense(10, activation="softmax"),
    ]
)
baseline_model.compile(
    optimizer="adam", loss="categorical_crossentropy", metrics=["acc"]
)
hist_baseline = baseline_model.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=100,
    validation_data=(X_test, y_test),
    verbose=1,
)
baseline_loss, baseline_acc = baseline_model.evaluate(X_test, y_test, verbose=0)
baseline_model.save("models/baseline_model.keras")
plot_and_save_chart(
    hist_baseline,
    "Baseline Model (No Regularization) - Loss Curve",
    "baseline_loss.png",
)

results["Baseline"] = {
    "summary": get_summary_str(baseline_model),
    "test_loss": baseline_loss,
    "test_acc": baseline_acc,
    "history": hist_baseline.history,
}

# ==========================================
# Scenario 2(a): L1 Regularization
# Rate: 0.0001 (1e-4)
# ==========================================
print("\n=== Scenario 2(a): L1 Regularization ===")
l1_rate = 0.0001
model_l1 = keras.Sequential(
    [
        layers.Flatten(input_shape=(28, 28, 1)),
        layers.Dense(
            64, activation="relu", kernel_regularizer=regularizers.l1(l1_rate)
        ),
        layers.Dense(10, activation="softmax"),
    ]
)
model_l1.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["acc"])
hist_l1 = model_l1.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=100,
    validation_data=(X_test, y_test),
    verbose=1,
)
l1_loss, l1_acc = model_l1.evaluate(X_test, y_test, verbose=0)
model_l1.save("models/model_l1.keras")
plot_and_save_chart(
    hist_l1,
    f"Scenario 2(a): L1 Regularization (rate={l1_rate}) - Loss Curve",
    "scenario_2a_l1_loss.png",
)

results["Scenario 2(a)"] = {
    "rate": l1_rate,
    "summary": get_summary_str(model_l1),
    "test_loss": l1_loss,
    "test_acc": l1_acc,
    "history": hist_l1.history,
}

# ==========================================
# Scenario 2(b): L2 Regularization
# Rate: 0.001 (1e-3)
# ==========================================
print("\n=== Scenario 2(b): L2 Regularization ===")
l2_rate = 0.001
model_l2 = keras.Sequential(
    [
        layers.Flatten(input_shape=(28, 28, 1)),
        layers.Dense(
            64, activation="relu", kernel_regularizer=regularizers.l2(l2_rate)
        ),
        layers.Dense(10, activation="softmax"),
    ]
)
model_l2.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["acc"])
hist_l2 = model_l2.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=100,
    validation_data=(X_test, y_test),
    verbose=1,
)
l2_loss, l2_acc = model_l2.evaluate(X_test, y_test, verbose=0)
model_l2.save("models/model_l2.keras")
plot_and_save_chart(
    hist_l2,
    f"Scenario 2(b): L2 Regularization (rate={l2_rate}) - Loss Curve",
    "scenario_2b_l2_loss.png",
)

results["Scenario 2(b)"] = {
    "rate": l2_rate,
    "summary": get_summary_str(model_l2),
    "test_loss": l2_loss,
    "test_acc": l2_acc,
    "history": hist_l2.history,
}

# ==========================================
# Scenario 2(c): Dropout
# Rate: 0.25
# ==========================================
print("\n=== Scenario 2(c): Dropout ===")
dropout_rate = 0.25
model_dropout = keras.Sequential(
    [
        layers.Flatten(input_shape=(28, 28, 1)),
        layers.Dense(64, activation="relu"),
        layers.Dropout(dropout_rate),
        layers.Dense(10, activation="softmax"),
    ]
)
model_dropout.compile(
    optimizer="adam", loss="categorical_crossentropy", metrics=["acc"]
)
hist_dropout = model_dropout.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=100,
    validation_data=(X_test, y_test),
    verbose=1,
)
dropout_loss, dropout_acc = model_dropout.evaluate(X_test, y_test, verbose=0)
model_dropout.save("models/model_dropout.keras")
plot_and_save_chart(
    hist_dropout,
    f"Scenario 2(c): Dropout (rate={dropout_rate}) - Loss Curve",
    "scenario_2c_dropout_loss.png",
)

results["Scenario 2(c)"] = {
    "rate": dropout_rate,
    "summary": get_summary_str(model_dropout),
    "test_loss": dropout_loss,
    "test_acc": dropout_acc,
    "history": hist_dropout.history,
}

# ==========================================
# Scenario 2(d): Early Stopping
# Monitor: val_loss, patience=3, epochs=20
# ==========================================
print("\n=== Scenario 2(d): Early Stopping ===")
model_es = keras.Sequential(
    [
        layers.Flatten(input_shape=(28, 28, 1)),
        layers.Dense(64, activation="relu"),
        layers.Dense(10, activation="softmax"),
    ]
)
model_es.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["acc"])
es_callback = EarlyStopping(
    monitor="val_loss", patience=3, restore_best_weights=True, verbose=1
)
hist_es = model_es.fit(
    X_train,
    y_train,
    epochs=20,
    batch_size=100,
    validation_data=(X_test, y_test),
    callbacks=[es_callback],
    verbose=1,
)
es_loss, es_acc = model_es.evaluate(X_test, y_test, verbose=0)
stopped_epoch = len(hist_es.history["loss"])
model_es.save("models/model_es.keras")
plot_and_save_chart(
    hist_es,
    f"Scenario 2(d): Early Stopping (stopped at epoch {stopped_epoch}) - Loss Curve",
    "scenario_2d_earlystopping_loss.png",
    early_stop_epoch=stopped_epoch,
)

results["Scenario 2(d)"] = {
    "stopped_epoch": stopped_epoch,
    "summary": get_summary_str(model_es),
    "test_loss": es_loss,
    "test_acc": es_acc,
    "history": hist_es.history,
}

# ==========================================
# Scenario 2(e): Both L1 Regularization and Dropout
# L1 rate: 0.0001, Dropout rate: 0.25
# ==========================================
print("\n=== Scenario 2(e): L1 Regularization + Dropout ===")
model_l1_dropout = keras.Sequential(
    [
        layers.Flatten(input_shape=(28, 28, 1)),
        layers.Dense(
            64, activation="relu", kernel_regularizer=regularizers.l1(l1_rate)
        ),
        layers.Dropout(dropout_rate),
        layers.Dense(10, activation="softmax"),
    ]
)
model_l1_dropout.compile(
    optimizer="adam", loss="categorical_crossentropy", metrics=["acc"]
)
hist_l1_dropout = model_l1_dropout.fit(
    X_train,
    y_train,
    epochs=10,
    batch_size=100,
    validation_data=(X_test, y_test),
    verbose=1,
)
l1_dropout_loss, l1_dropout_acc = model_l1_dropout.evaluate(X_test, y_test, verbose=0)
model_l1_dropout.save("models/model_l1_dropout.keras")
plot_and_save_chart(
    hist_l1_dropout,
    f"Scenario 2(e): L1 ({l1_rate}) + Dropout ({dropout_rate}) - Loss Curve",
    "scenario_2e_l1_dropout_loss.png",
)

results["Scenario 2(e)"] = {
    "l1_rate": l1_rate,
    "dropout_rate": dropout_rate,
    "summary": get_summary_str(model_l1_dropout),
    "test_loss": l1_dropout_loss,
    "test_acc": l1_dropout_acc,
    "history": hist_l1_dropout.history,
}

# Comparison Plot
plt.figure(figsize=(10, 6), dpi=300)
for name, res in results.items():
    plt.plot(res["history"]["val_loss"][:10], label=f"{name} (Val Loss)", linewidth=2)
plt.title(
    "Comparison of Validation Loss Across All Scenarios (First 10 Epochs)",
    fontsize=13,
    fontweight="bold",
)
plt.xlabel("Epochs", fontsize=11)
plt.ylabel("Validation Loss", fontsize=11)
plt.legend(fontsize=10)
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.savefig("plots/comparison_val_loss.png", dpi=300)
plt.close()

# Save summary to text file
with open("experiment_results.txt", "w") as f:
    f.write("=== PMML ASSIGNMENT 2 EXPERIMENT RESULTS ===\n\n")
    for name, res in results.items():
        f.write(f"--- {name} ---\n")
        f.write(f"Test Loss: {res['test_loss']:.4f}\n")
        f.write(f"Test Accuracy: {res['test_acc'] * 100:.2f}%\n")
        f.write(f"Model Summary:\n{res['summary']}\n")
        f.write("-" * 50 + "\n\n")

print("\nAll experiments completed successfully!")
