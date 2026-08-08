from src.dataset.builder import build_training_dataset
from src.models.split import time_series_cross_validation
import pandas as pd

def main() -> None:
    dataset = build_training_dataset()

    folds = time_series_cross_validation(
        dataset,
        n_splits=5,
        gap=5,
    )

    for fold_number, (train, validation) in enumerate(folds, start=1):
        print(f"\nFold {fold_number}")
        print("-" * 30)

        print("Train shape:", train.shape)
        print("Validation shape:", validation.shape)

        print(
            "Train dates:",
            train["timestamp"].min(),
            "to",
            train["timestamp"].max(),
        )

        print(
            "Validation dates:",
            validation["timestamp"].min(),
            "to",
            validation["timestamp"].max(),
        )

        overlap = set(train["timestamp"]) & set(validation["timestamp"])

        print("Chronological overlap:", bool(overlap))

        all_timestamps = (
            pd.to_datetime(dataset["timestamp"])
            .drop_duplicates()
            .sort_values()
            .reset_index(drop=True)
        )

        train_end_position = all_timestamps[
            all_timestamps == train["timestamp"].max()
        ].index[0]

        validation_start_position = all_timestamps[
            all_timestamps == validation["timestamp"].min()
        ].index[0]

        gap_size = validation_start_position - train_end_position - 1

        print("Gap timestamps:", gap_size)
        


if __name__ == "__main__":
    main()