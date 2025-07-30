# -*- coding: utf-8 -*-
"""
VAE Code for Sequence Analysis and Clustering (Updated to TF 2.x)

This script implements a Variational Autoencoder (VAE) to:
1. Learn a low-dimensional latent representation of sequence data.
2. Visualize the distribution of data in this latent space.
3. Cluster the data in the latent space using DBSCAN.

Main function to import: VAE_model
"""

# Imported libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import tensorflow as tf
from tensorflow.keras.layers import (
    Input, Dense, Lambda, Flatten, Reshape,
    BatchNormalization, Dropout, Activation, LeakyReLU
)
from tensorflow.keras.models import Model
from tensorflow.keras.losses import categorical_crossentropy
from tensorflow.keras import backend as K # Useful for clear_session
from sklearn.cluster import DBSCAN
import warnings
import os
from typing import Dict, Any, Tuple, List, Optional
from sklearn.preprocessing import StandardScaler


# --- Global Configuration ---
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2" # Suppress TF info messages
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')

# --- Data Handling Functions ---

def store_data(file_name: str, data_obj: Dict[str, Any]) -> None:
    """Saves processed data from a dictionary to a text file."""
    print(f"Saving data to {file_name}...")
    try:
        with open(file_name, "w") as output_file:
            for i in range(data_obj["shape"][0]):
                # Write name and group
                print(data_obj["name"][i], data_obj["group"][i], end="", file=output_file)
                # Write each dna_code vector, comma-separated and space-separated
                for j in range(data_obj["shape"][1]):
                    print(" ", end=" ", file=output_file)
                    print(
                        ",".join([str(int(val)) for val in list(data_obj["dna_code"][i][j])]), # Convert to int if they are one-hot
                        end="",
                        file=output_file,
                    )
                print("", file=output_file) # New line for the next sequence
        print("Data saved successfully.")
    except IOError as e:
        print(f"Error writing to file {file_name}: {e}")
    except KeyError as e:
        print(f"Error: Missing key '{e}' in the data dictionary.")


def retrieve_data(file_name: str) -> Optional[Dict[str, Any]]:
    """Loads data from a text file into a structured dictionary."""
    print(f"Loading data from {file_name}...")
    data_obj = {
        "data_set": file_name.replace(".txt", ""),
        "name": [],
        "group": [],
        "dna_code": [],
    }
    try:
        with open(file_name, "r") as input_file:
            for line in input_file:
                values = line.strip().split(" ") # strip() removes leading/trailing whitespace including \n
                if len(values) < 3: # Basic format check
                    print(f"Warning: Malformed line skipped: {line.strip()}")
                    continue
                data_obj["name"].append(values[0])
                data_obj["group"].append(values[1])
                # Process DNA codes, converting each comma-separated string into a list of floats
                dna_sequence = []
                for dna_part in values[2:]:
                    try:
                        # Ensure they are float numbers
                        dna_vector = [float(val) for val in dna_part.split(",")]
                        dna_sequence.append(dna_vector)
                    except ValueError:
                         print(f"Warning: Non-numeric value found in '{dna_part}' in line: {line.strip()}. Skipping sequence.")
                         # If there's an error in one part, we might want to discard the whole sequence
                         dna_sequence = None # Mark for discard
                         break # Exit the inner loop

                if dna_sequence is not None: # Only add if there were no errors in the sequence
                     data_obj["dna_code"].append(dna_sequence)
                else:
                    # If the sequence was discarded, remove name and group as well
                    data_obj["name"].pop()
                    data_obj["group"].pop()


        if not data_obj["dna_code"]:
             print("Error: Could not load valid dna_code data.")
             return None

        # Convert lists to NumPy arrays
        data_obj["name"] = np.array(data_obj["name"], dtype=str)
        data_obj["group"] = np.array(data_obj["group"], dtype=str)
        # Ensure data is float32 for TensorFlow
        data_obj["dna_code"] = np.array(data_obj["dna_code"], dtype=np.float32)
        data_obj["shape"] = data_obj["dna_code"].shape # (num_samples, sequence_length, code_dim)

        print(f"Data loaded: {data_obj['shape'][0]} samples found.")
        print(f"Shape of dna_code: {data_obj['shape']}")
        return data_obj

    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return None
    except Exception as e:
        print(f"Unexpected error reading file {file_name}: {e}")
        return None

# --- Internal Clustering and Visualization Functions ---
# (These are used by train_and_evaluate_vae)

def _internal_extract_cluster_labels_dbscan(vae_mu: np.ndarray,
                                            data: Dict[str, Any],
                                            epsilon: float,
                                            min_samples: int = 10) -> None:
    """Applies DBSCAN to latent representations (means) and visualizes clusters."""
    print(f"\nRunning DBSCAN (internal) with eps={epsilon}, min_samples={min_samples}...")
    if vae_mu.shape[1] != 2:
        print("Warning: DBSCAN visualization is designed for 2D latent space.")
    vae_mu_scaled = StandardScaler().fit_transform(vae_mu)
    dbscan = DBSCAN(eps=epsilon, min_samples=min_samples)
    cluster_labels = dbscan.fit_predict(vae_mu) # fit_predict is more direct

    unique_labels = set(cluster_labels)
    n_clusters = len(unique_labels) - (1 if -1 in unique_labels else 0)
    n_noise = list(cluster_labels).count(-1)

    print(f"Estimated number of OTUs: {n_clusters}")
    # print(f"Estimated number of noise points: {n_noise}")

    # --- Visualization ---
    # Create a map of distinguishable colors for clusters + black for noise (-1)
    colors = [plt.cm.tab10(i) for i in range(n_clusters)]
    color_map = {label: col for label, col in zip(sorted([l for l in unique_labels if l != -1]), colors)}
    color_map[-1] = (0, 0, 0, 1) # Black for noise

    for cluster_id in unique_labels:
        if cluster_id == -1:
            continue # Skip plotting noise
        # Mask to get points for this cluster/noise
        class_member_mask = (cluster_labels == cluster_id)
        # Coordinates in the latent space
        xy = vae_mu[class_member_mask]
        if xy.shape[0] > 0: # Ensure there are points
            plt.plot(
                xy[:, 0],
                xy[:, 1],
                "o",
                markerfacecolor=color_map[cluster_id],
                markeredgecolor=color_map[cluster_id], # Same color for edge
                markersize=8, # Reasonable marker size
                label=f"OTU {cluster_id + 1}" if cluster_id != -1 else "Noise"
            )
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title="OTUs")
    plt.title(f"DBSCAN Clustering in Latent Space Z (eps={epsilon})")
    plt.xlabel("Latent Dimension 1")
    plt.ylabel("Latent Dimension 2")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.xticks([]) # Keep axes clear as in original if preferred
    plt.yticks([])


def _internal_plot_mu_sg(mu: np.ndarray, sg: np.ndarray, groups: np.ndarray,
                         sample: int = 5000, alpha: float = 0.15,
                         title: str = r"Distribution of $\mu$ and $\sigma$ in Latent Space $Z$",
                         legend: bool = True) -> None:
    """Visualizes learned means (mu) and standard deviations (sg)."""
    if mu.shape[1] != 2:
         print("Warning: mu/sigma visualization is designed for 2D latent space.")

    unique_groups = np.unique(groups)
    # Use a different colormap if many groups for better distinction
    cmap_name = 'viridis' if len(unique_groups) <= 10 else 'tab20'
    colors = plt.get_cmap(cmap_name)(np.linspace(0, 1, len(unique_groups)))

    for idx, group_label in enumerate(unique_groups):
        # Indices of samples belonging to this group
        group_indices = np.where(groups == group_label)[0]
        if len(group_indices) == 0: continue # Skip if no samples for this group

        group_mu = mu[group_indices]
        group_sg = sg[group_indices]

        xx, yy = [], []
        # Sample points around each group mean
        for i in range(len(group_indices)):
            # Sample from Normal(mu, sg^2)
            epsilon = 1e-6 # For numerical stability
            # Ensure sg is not nan or inf
            current_sg = np.nan_to_num(group_sg[i] + epsilon)
            sampled_points = group_mu[i] + np.random.normal(0, 1, size=(sample, mu.shape[1])) * current_sg
            xx.extend(sampled_points[:, 0])
            yy.extend(sampled_points[:, 1])

        # Plot sampled points for this group
        plt.scatter(xx, yy, label=str(group_label), alpha=alpha, color=colors[idx], s=10) # Small size for sampled points

    # Plot original means (mu) on top
    plt.scatter(
        mu[:, 0], mu[:, 1], s=30, facecolors="none", edgecolors="black", linewidths=1,
        label="Means ($\mu$)"
    )

    plt.title(title)
    plt.xlabel("Latent Dimension 1")
    plt.ylabel("Latent Dimension 2")
    plt.grid(True, linestyle='--', alpha=0.6)
    if legend:
        # Improve legend position if many groups
        plt.legend(markerscale=2, bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks([]) # Keep axes clear as in original if preferred
    plt.yticks([])


# --- VAE Model Definition ---

def sampling(args: Tuple[tf.Tensor, tf.Tensor]) -> tf.Tensor:
    """Sampling function (Reparameterization Trick)."""
    Z_mu, Z_log_var = args
    batch = tf.shape(Z_mu)[0]
    dim = tf.shape(Z_mu)[1]
    # Sample epsilon from standard normal
    epsilon = tf.random.normal(shape=(batch, dim), dtype=tf.float32) # Specify dtype
    # Calculate Z: mu + exp(0.5 * log_var) * epsilon
    # exp(0.5 * log_var) is the standard deviation (sigma)
    return Z_mu + tf.exp(0.5 * Z_log_var) * epsilon

# Define reconstruction loss function externally
def reconstruction_loss_fn(y_true: tf.Tensor, y_pred: tf.Tensor) -> tf.Tensor:
    """Calculates only the reconstruction loss (averaged over batch)."""
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)
    # categorical_crossentropy returns shape (batch, seq_len). Sum over seq_len (axis=1).
    recon_loss_per_sample = tf.reduce_sum(categorical_crossentropy(y_true, y_pred), axis=1)
    # Return the mean over the batch
    return tf.reduce_mean(recon_loss_per_sample)

def mk_model(
    original_dim: int,
    cat_dim: int,
    latent_dim: int = 2,
    en_dim: List[int] = [128, 64, 32],
    en_drop: List[float] = [0.5, 0.5, 0.5], # Encoder: input -> 128 -> 64 -> 32 -> Z
    de_dim: List[int] = [32, 64, 128], # Decoder: Z -> 64 -> 128 -> output
    de_drop: List[float] = [0.5, 0.5, 0.5],
    activation: str = 'elu',
    kl_weight: float = 0.05 # KL weight applied via add_loss
) -> Tuple[tf.keras.Model, tf.keras.Model]:
    """
    Builds the VAE model (Encoder, Decoder) and the standalone Encoder model.
    Adds KL loss using model.add_loss().
    """
    tf.keras.backend.clear_session() # Clear previous session
    print("\nBuilding VAE model...")

    def apply_activation(fn_name: str, tensor: tf.Tensor) -> tf.Tensor:
        """Applies the specified activation function."""
        if fn_name == "leakyrelu":
            return LeakyReLU()(tensor)
        else:
            # Use standard Keras activations, ensure float32 output
            return Activation(fn_name, dtype='float32')(tensor)

    # --- INPUT ---
    x_in = Input(shape=(original_dim, cat_dim), name="Input_Sequence", dtype=tf.float32)

    # --- ENCODER :: Q(z|X) ---
    en = Flatten(name="Encoder_Flatten")(x_in)
    en = BatchNormalization(scale=False, center=False, name="Encoder_BN_Input")(en) # Normalize before first Dense
    # Encoder hidden layers
    for i, (dim, drop) in enumerate(zip(en_dim, en_drop)):
        en = Dense(dim, name=f"Encoder_Dense_{i+1}")(en)
        en = apply_activation(activation, en)
        en = Dropout(drop, name=f"Encoder_Dropout_{i+1}")(en)
        en = BatchNormalization(scale=False, center=False, name=f"Encoder_BN_{i+1}_post")(en) # BN after activation

    # --- LATENT SPACE (Z) ---
    Z_mu = Dense(latent_dim, name="Z_Mean", dtype='float32')(en)             # Mean
    Z_log_var = Dense(latent_dim, name="Z_Log_Variance", dtype='float32')(en) # Log variance
    # Sampling layer using reparameterization trick
    Z = Lambda(sampling, output_shape=(latent_dim,), name="Z_Sampling", dtype='float32')([Z_mu, Z_log_var])

    # --- DECODER :: P(X|z) ---
    # Decoder input is the sampled latent vector Z
    de = Z
    # Decoder hidden layers (symmetric to encoder)
    for i, (dim, drop) in enumerate(zip(de_dim, de_drop)):
        layer_name_dense = f"Decoder_Dense_{i+1}"
        layer_name_act = f"Decoder_{activation}_{i+1}" # Unique name for activation
        layer_name_drop = f"Decoder_Dropout_{i+1}"
        layer_name_bn = f"Decoder_BN_{i+1}_post"

        de = Dense(dim, name=layer_name_dense)(de) # Apply Dense to previous output 'de'
        de = apply_activation(activation, de)      # Use helper function
        de = Dropout(drop, name=layer_name_drop)(de)
        de = BatchNormalization(scale=False, center=False, name=layer_name_bn)(de)

    # Final decoder layer to reconstruct flattened original shape
    de = Dense(original_dim * cat_dim, name="Decoder_Dense_Final")(de)

    # --- OUTPUT ---
    x_out_reshaped = Reshape((original_dim, cat_dim), name="Output_Reshape")(de)
    # Apply Softmax on the last dimension for categorical probabilities, ensure float32
    x_out = Activation('softmax', name="Output_Softmax", dtype='float32')(x_out_reshaped)

    # --- FULL VAE MODEL ---
    vae = Model(inputs=x_in, outputs=x_out, name="VAE")

    # --- CALCULATE AND ADD KL LOSS ---
    # Formula: 0.5 * sum(1 + log(sigma^2) - mu^2 - sigma^2)
    kl_loss_per_sample = -0.5 * tf.reduce_sum(1 + Z_log_var - tf.square(Z_mu) - tf.exp(Z_log_var), axis=-1)
    # Add the KL loss (averaged over batch and weighted) to the model
    # Keras sums this automatically during training
    vae.add_loss(tf.reduce_mean(kl_loss_per_sample * kl_weight))
    # Add KL loss as a metric for monitoring (unweighted mean)
    vae.add_metric(tf.reduce_mean(kl_loss_per_sample), name='kl_loss')


    # --- RECONSTRUCTION ACCURACY METRIC ---
    # (Standard function)
    def reconstruction_accuracy(y_true: tf.Tensor, y_pred: tf.Tensor) -> tf.Tensor:
        """Simple accuracy metric based on categorical match."""
        y_true = tf.cast(y_true, tf.float32) # Ensure type for argmax
        y_pred = tf.cast(y_pred, tf.float32)
        true_labels = tf.argmax(y_true, axis=-1)
        pred_labels = tf.argmax(y_pred, axis=-1)
        accuracy = tf.reduce_mean(tf.cast(tf.equal(true_labels, pred_labels), tf.float32))
        return accuracy

    # --- COMPILE VAE MODEL ---
    # Compile ONLY with the reconstruction loss. KL loss is added automatically via add_loss.
    vae.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3), # Adam optimizer is common
                loss=reconstruction_loss_fn, # Use external function for reconstruction only
                metrics=[reconstruction_accuracy]) # kl_loss metric is added via add_metric

    # --- ENCODER MODEL (for getting Z_mu, Z_log_var after training) ---
    encoder = Model(inputs=x_in, outputs=[Z_mu, Z_log_var], name="Encoder") # Return both mean and log_var
    print("VAE model built and compiled.")
    # vae.summary() # Uncomment to see detailed layer summary
    return vae, encoder


# --- Training and Evaluation Function ---

def train_and_evaluate_vae(
    data: Dict[str, Any],
    latent_dim: int = 2,
    epochs: int = 50,
    batch_size: int = 128,
    dbscan_eps: float = 2
) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
    """
    Trains the VAE model, evaluates, and visualizes the results.
    MODIFIED: Removed Solarize_Light2 style, set subplot backgrounds manually.
    """
    if data is None:
        print("Error: No data to train.")
        return None, None


    n_samples, original_dim, cat_dim = data["shape"]

    try:
        # kl_weight is used inside mk_model to weight the loss added via add_loss
        vae, encoder = mk_model(original_dim, cat_dim, latent_dim=latent_dim, kl_weight=0.05)
    except Exception as e:
        print(f"Error building the model: {e}")
        import traceback
        traceback.print_exc() # Print detailed traceback for debugging
        return None, None

    print(f"\n--- Starting VAE Training ---")
    print(f"Epochs: {epochs}, Batch Size: {batch_size}, Latent Dimension: {latent_dim}")

    x_train = data["dna_code"] # Should be float32 from retrieve_data
    y_train = data["dna_code"] # Target is to reconstruct the input

    try:
        # Optional: Add EarlyStopping callback
        # early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

        history = vae.fit(
            x_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            shuffle=True,
            validation_split=0.1, # Use 10% of data for validation
            # callbacks=[early_stopping], # Optional
            verbose=1 # Show progress
        )
        print("\n--- Training Complete ---")

        print("Generating latent representations...")
        vae_mu, vae_log_var = encoder.predict(data["dna_code"], batch_size=batch_size)
        vae_sg = np.exp(0.5 * vae_log_var)
        print(f"Shape of mu: {vae_mu.shape}, Shape of sigma: {vae_sg.shape}")


        # --- Generate Result Plots ---
        print("Generating plots...")
        # --- Plot Background Modification ---
        # Set overall figure background to white (it was already white, but good to be explicit)
        plt.figure(figsize=(14, 12), facecolor='white')
        gs = gridspec.GridSpec(2, 2, height_ratios=[1, 2]) # 2 rows, 2 columns

        # 1. Training History Plot
        # Set subplot background to light grey
        ax1 = plt.subplot(gs[0, :], facecolor='#eeeeee') # <-- ADDED facecolor
        # --- End Plot Background Modification ---

        # Plot Total Loss ('loss' includes reconstruction and weighted KL)
        ax1.plot(history.history['loss'], label='Total Loss (Train)', color='red')
        if 'val_loss' in history.history:
             ax1.plot(history.history['val_loss'], label='Total Loss (Val)', color='orange', linestyle='--')
        ax1.set_xlabel("Epoch")
        ax1.set_ylabel("Total Loss", color='red')
        ax1.tick_params(axis='y', labelcolor='red')
        ax1.set_title("VAE Training History")
        ax1.legend(loc='upper left')
        ax1.grid(True, linestyle='--', alpha=0.6) # Keep grid for readability

        # Secondary Y-axis for Reconstruction Accuracy
        ax2 = ax1.twinx()
        ax2.plot(history.history['reconstruction_accuracy'], label='Recon Accuracy (Train)', color='blue')
        if 'val_reconstruction_accuracy' in history.history:
             ax2.plot(history.history['val_reconstruction_accuracy'], label='Recon Accuracy (Val)', color='cyan', linestyle='--')
        ax2.set_ylabel("Reconstruction Accuracy", color='blue')
        ax2.tick_params(axis='y', labelcolor='blue')
        ax2.legend(loc='upper right')


        # --- Plot Background Modification ---
        # 2. Mu/Sigma Distribution Plot
        # Set subplot background to light grey
        ax3 = plt.subplot(gs[1, 0], facecolor='#eeeeee') # <-- ENSURED facecolor is set
        # 3. DBSCAN Clustering Plot
        # Set subplot background to light grey
        ax4 = plt.subplot(gs[1, 1], facecolor='#eeeeee') # <-- ENSURED facecolor is set
        # --- End Plot Background Modification ---

        plt.sca(ax3) # Set current axis
        _internal_plot_mu_sg(vae_mu, vae_sg, data["group"], sample=50, alpha=0.1, legend=False)

        plt.sca(ax4) # Set current axis
        _internal_extract_cluster_labels_dbscan(vae_mu, data, dbscan_eps, min_samples=10)

        plt.tight_layout(pad=3.0) # Adjust spacing

        output_filename = f"{data['data_set']}_VAE_results.tiff"
        plt.savefig(output_filename, bbox_inches='tight', dpi=600) # bbox_inches helps ensure legend is saved
        print(f"Plots saved to: {output_filename}")
        plt.close() # Close the figure
        # print("Min value in vae_mu:", np.min(vae_mu))
        # print("Max value in vae_mu:", np.max(vae_mu))
        # print("Mean value in vae_mu:", np.mean(vae_mu, axis=0))
        # print("Standard deviation in vae_mu:", np.std(vae_mu, axis=0))
        # vae_mu_scaled = StandardScaler().fit_transform(vae_mu)
        # print("Min value in vae_mu_scaled:", np.min(vae_mu_scaled))
        # print("Max value in vae_mu_scaled:", np.max(vae_mu_scaled))
        # print("Mean value in vae_mu_scaled:", np.mean(vae_mu_scaled, axis=0))
        # print("Standard deviation in vae_mu_scaled:", np.std(vae_mu_scaled, axis=0))
        return vae_mu, vae_log_var

    except Exception as e:
        print(f"\nError during training or evaluation: {e}")
        import traceback
        traceback.print_exc()
        return None, None

# --- Main Interface Function (VAE_model) ---

def VAE_model(input_file: str,
              epsilon: float, # Keep 'epsilon' name for compatibility
              latent_dimension: int = 2,
              training_epochs: int = 50
              ) -> Tuple[Optional[np.ndarray], Optional[Dict[str, Any]]]:
    """
    Main function to load data, train VAE, cluster, and visualize.
    Compatible with the original call signature.

    Args:
        input_file (str): Path to the input data file (.txt).
        epsilon (float): 'eps' parameter for DBSCAN clustering.
                         (Passed as dbscan_eps internally).
        latent_dimension (int): Dimensionality of the latent space for the VAE.
        training_epochs (int): Number of training epochs.


    Returns:
        Tuple[Optional[np.ndarray], Optional[Dict[str, Any]]]:
            - Latent means (mu) if successful, otherwise None.
            - The original loaded data dictionary, or None if loading failed.
            (Matches original return signature expectation)
    """
    # 1. Load data
    data_dict = retrieve_data(input_file)
    if data_dict is None:
        # Original code implicitly returned None, None if retrieve_data failed
        return None, None

    # 2. Train VAE and Evaluate
    # Pass 'epsilon' from the argument to 'dbscan_eps' of the internal function
    mu, log_var = train_and_evaluate_vae(
        data=data_dict,
        latent_dim=latent_dimension,
        epochs=training_epochs,
        batch_size=128, # Could be made a parameter
        dbscan_eps=epsilon # Use the epsilon from the VAE_model call here
    )

    if mu is None:
        print("VAE analysis could not be completed.")
        # Return None for mu, but the data_dict if loading was successful
        return None, data_dict

    print("\n--- VAE Analysis Successfully Completed ---")
    # Return mu and data_dict, as in the original VAE_model function
    return mu, data_dict


# --- Main Execution Block (Example for direct script testing) ---
if __name__ == "__main__":
    print("Executing VAE Method...")

