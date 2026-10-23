import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class LibraryDashboard:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.DataFrame()
        self.statistics = {}

    def load_data(self):
        try:
            self.df = pd.read_csv(self.file_path)

            required_columns = [
                "Transaction ID",
                "Date",
                "User ID",
                "Book Title",
                "Genre",
                "Borrowing Duration (Days)",
                "Time"]

            for column in required_columns:
                if column not in self.df.columns:
                    print("Missing required column:", column)
                    return False

            self.df["Date"] = pd.to_datetime(
                self.df["Date"], errors="coerce")

            self.df["Borrowing Duration (Days)"] = pd.to_numeric(self.df["Borrowing Duration (Days)"],
                errors="coerce")

            self.df = self.df.dropna(subset=required_columns)
            self.df = self.df.drop_duplicates(
                subset=["Transaction ID"] )

            self.df = self.df[
                self.df["Borrowing Duration (Days)"] >= 0]

            print("Data loaded and validated successfully!")
            print("Total valid transactions:", len(self.df))
            return True

        except FileNotFoundError:
            print("Error: CSV file not found.")
            return False

    def calculate_statistics(self):
        self.statistics = {
            "Total Transactions": len(self.df),
            "Unique Users": self.df["User ID"].nunique(),
            "Unique Books": self.df["Book Title"].nunique(),
            "Average Borrowing Duration":
                self.df["Borrowing Duration (Days)"].mean(),
            "Top 5 Borrowed Books":
                self.df["Book Title"].value_counts().head(5),
            "Standard Deviation":
                np.std(self.df["Borrowing Duration (Days)"]),
            "Busiest Day":
                self.df["Date"].dt.date.value_counts().idxmax()}

        print("Library Statistics:")
        for key, value in self.statistics.items():
            print(f"{key}:")
            print(value)

    def filter_transactions(
        self, condition=None, genre=None,
        start_date=None, end_date=None,
        borrowing_duration=None):
        filtered_data = self.df.copy()

        if condition is not None:
            filtered_data = filtered_data.query(condition)

        if genre is not None:
            filtered_data = filtered_data[
                filtered_data["Genre"] == genre]

        if start_date is not None:
            filtered_data = filtered_data[
                filtered_data["Date"] >= pd.to_datetime(start_date)]

        if end_date is not None:
            filtered_data = filtered_data[
                filtered_data["Date"] <= pd.to_datetime(end_date)]

        if borrowing_duration is not None:
            filtered_data = filtered_data[
                filtered_data["Borrowing Duration (Days)"]
                >= borrowing_duration]

        return filtered_data

    def generate_report(self):
        print("E-Library Data Analysis Report")
        print("-" * 35)
        print("Total Transactions:", len(self.df))
        print("Unique Users:", self.df["User ID"].nunique())
        print("Unique Books:", self.df["Book Title"].nunique())
        print(
            "Average Borrowing Duration:",
            self.df["Borrowing Duration (Days)"].mean())
        
        print("\nTop 5 Borrowed Books:")
        print(self.df["Book Title"].value_counts().head(5))


if __name__ == "__main__":
    library = LibraryDashboard("library_transactions.csv")

    if library.load_data():
        library.calculate_statistics()
        library.generate_report()

        filtered_data = library.filter_transactions(
            genre="Fantasy")

        print("\nFantasy Genre Transactions:")
        print(filtered_data[["Book Title", "Genre"]])
        print("Total Fantasy Transactions:", len(filtered_data))