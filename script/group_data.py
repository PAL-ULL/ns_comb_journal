import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import dask.dataframe
from joblib import dump, load
from sklearn.pipeline import Pipeline
from dask_ml.preprocessing import StandardScaler
from dask_ml.decomposition import IncrementalPCA

solvers = [
    "ExpKnap",
    "MinKnap",
    "Combo",
    "MiW",
    "Default",
    "MPW",
    "MaP",
    "GA_0.7",
    "GA_0.8",
    "GA_0.9",
    "GA_1.0",
]


def reduce_df(df, n_comps=2, features=None, y_name="target"):
    y = df["target"]
    # resolution = df['bin_resolution'] if 'bin_resolution' in df.columns else None
    # threshold = df['ns_threshold'] if 'ns_threshold' in df.columns else None
    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "pca",
                IncrementalPCA(n_components=n_comps, random_state=42),
            ),
        ]
    )
    data = None
    # Optional information
    resolution = None
    threshold = None
    method = None

    if features is None:
        data = df.copy()
        data = data.drop(["target"], axis=1)
        if "bin_resolution" in df.columns:
            resolution = df["bin_resolution"]
            data = data.drop(["bin_resolution"], axis=1)
        if "ns_threshold" in df.columns:
            threshold = df["ns_threshold"]
            data = data.drop(["ns_threshold"], axis=1)
        if "method" in df.columns:
            method = df["method"]
            data = data.drop(["method"], axis=1)
    else:
        data = df[features].copy()

    print(data.columns)
    data_array = data.to_dask_array(lengths=True)
    scaled_data = pipeline.fit_transform(data_array)
    print("Reduced")
    scaled_df = dask.dataframe.io.from_dask_array(
        scaled_data[:, :2], columns=["x0", "x1"], index=y.index
    )
    scaled_df["target"] = y

    # Include optional info
    if resolution is not None:
        scaled_df["bin_resolution"] = resolution
    if threshold is not None:
        scaled_df["ns_threshold"] = threshold
    if method is not None:
        scaled_df["method"] = method

    return scaled_df, pipeline


def main():
    df_n_1000_complete = dask.dataframe.read_csv(
        "kp_instances_n_1000_complete.csv/*.part"
    ).set_index("Unnamed: 0")
    print("Datasets concatenated loaded")

    df_n_1000_complete_red, pipeline_n_1000_complete = reduce_df(
        df_n_1000_complete, n_comps=2
    )
    print("PCA done")
    df_n_1000_complete_red["target_method"] = (
        df_n_1000_complete_red["target"] + "_" + df_n_1000_complete_red["method"]
    )
    print("target_method created")
    df_n_1000_complete_red.to_csv("kp_instances_n_1000_complete_reduced.csv")
    print("Reduced dataset to_csv done")
    dump(pipeline_n_1000_complete, "pipeline_complete_kp_instances_n_1000.joblib")
    print("Pipeline done")


if __name__ == "__main__":
    main()
