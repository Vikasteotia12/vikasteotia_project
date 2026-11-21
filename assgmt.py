import os
import numpy as np
import pandas as pd

FILE = "climate_data.csv"
COORDS = (28.67, 77.45)            # 1. Tuple
SEASONS = {"Winter", "Summer"}     # 2. Set


def load_data():
    if os.path.exists(FILE):
        return pd.read_csv(FILE)

    rng = np.random.default_rng(42)
    date_range = pd.date_range("2025-01-01", periods=60, freq="D")  # 60 records (>50)

    dates, max_t, min_t, mean_t, rain = [], [], [], [], []          # 3. Lists
    for d in date_range:
        m = round(float(rng.uniform(15, 35)), 1)
        dates.append(d.strftime("%Y-%m-%d"))                        # 4. List method (.append)
        mean_t.append(m)
        max_t.append(round(m + 6, 1))
        min_t.append(round(m - 5, 1))
        rain.append(round(float(rng.choice([0.0, 5.2, 12.5])), 1))

    # 5. Dictionary & Dictionary method (.keys)
    data = {"Date": dates, "Max": max_t, "Min": min_t, "Mean": mean_t, "Rain": rain}
    print("Columns created:", list(data.keys()))

    df = pd.DataFrame(data)
    df.to_csv(FILE, index=False)
    return df


def show_recs(df):
    print("\nNo records." if df.empty else "\n" + df.to_string(index=False))


def add_rec(df):
    try:
        row = pd.DataFrame([{
            "Date": input("Date (YYYY-MM-DD): ").strip(),
            "Max": float(input("Max Temp: ").strip()),
            "Min": float(input("Min Temp: ").strip()),
            "Mean": float(input("Mean Temp: ").strip()),
            "Rain": float(input("Rain (mm): ").strip()),
        }])
        df = pd.concat([df, row], ignore_index=True)
        df.to_csv(FILE, index=False)
        print("Record added.")
    except ValueError:
        print("Invalid input.")
    return df


def search_rec(df):
    res = df[df["Date"] == input("Search Date (YYYY-MM-DD): ").strip()]
    print(res.to_string(index=False) if not res.empty else "Not found.")


def update_rec(df):
    d = input("Date to update: ").strip()
    if (df["Date"] == d).any():
        try:
            df.loc[df["Date"] == d, "Mean"] = float(input("New Mean Temp: ").strip())
            df.to_csv(FILE, index=False)
            print("Record updated.")
        except ValueError:
            print("Invalid input.")
    else:
        print("Not found.")
    return df


def delete_rec(df):
    df = df[df["Date"] != input("Date to delete: ").strip()].copy()
    df.to_csv(FILE, index=False)
    print("Deleted (if existed).")
    return df


def numpy_stats(df):
    if df.empty:
        return print("No data.")
    a1 = df["Mean"].to_numpy()                     # 1D array
    a2 = df[["Max", "Min", "Mean"]].to_numpy()     # 2D array

    print("\n--- NumPy Stats ---")
    print("1D Index[0]:", a1[0], "| Slice[:3]:", a1[:3])
    print("2D Row 0:", a2[0, :], "| Slice[:2, :2]:\n", a2[:2, :2])
    print(f"Sum: {np.sum(a1):.1f} | Mean: {np.mean(a1):.2f} | Std: {np.std(a1):.2f}")
    print(f"Max: {np.max(a1):.1f} | Min: {np.min(a1):.1f}")


def pandas_stats():
    df = pd.read_csv(FILE)
    df = df.fillna(df.mean(numeric_only=True))
    df["Month"] = pd.to_datetime(df["Date"], errors="coerce").dt.month

    print("\n--- Selected Rows & Cols ---")
    print(df.loc[0:4, ["Date", "Mean", "Rain"]].to_string(index=False))

    print("\n--- Filtered (Mean > 28) & Sorted ---")
    hot = df[df["Mean"] > 28].sort_values(by="Mean", ascending=False)
    print(hot[["Date", "Mean"]].head(5).to_string(index=False))

    print("\n--- GroupBy Month (Avg Temp) ---")
    print(df.groupby("Month")["Mean"].mean().round(2).to_string())

    print("\n--- Statistical Summary ---")
    print(df[["Max", "Min", "Mean", "Rain"]].describe().round(2).to_string())


def summary_report(df):
    if df.empty:
        return print("\nNo records.")
    print("\n=== SUMMARY REPORT ===")
    print(f"Total Records : {len(df)}")
    print(f"Avg Mean Temp : {df['Mean'].mean():.2f} °C")
    print(f"Highest Temp  : {df['Max'].max():.1f} °C")
    print(f"Lowest Temp   : {df['Min'].min():.1f} °C")
    print(f"Total Rainfall: {df['Rain'].sum():.1f} mm")


def main():
    df = load_data()
    while True:
        c = input("\n1.Display 2.Add 3.Search 4.Update 5.Delete 6.NumPy 7.Pandas 8.Summary 9.Exit\nChoice: ").strip()
        if c == "1": show_recs(df)
        elif c == "2": df = add_rec(df)
        elif c == "3": search_rec(df)
        elif c == "4": df = update_rec(df)
        elif c == "5": df = delete_rec(df)
        elif c == "6": numpy_stats(df)
        elif c == "7": pandas_stats()
        elif c == "8": summary_report(df)
        elif c == "9": break
        else: print("Invalid choice.")


if __name__ == "__main__":
    main()