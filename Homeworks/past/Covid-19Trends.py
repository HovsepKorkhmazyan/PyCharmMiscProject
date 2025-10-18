import pandas as pd
import requests
import matplotlib.pyplot as plt
import json
from typing import List, Dict, Any

API_URL = "https://disease.sh/v3/covid-19/historical?lastdays=30"
COUNTRIES_TO_PLOT = ['USA', 'India', 'Brazil', 'United Kingdom', 'France']


def fetch_and_save_data(url: str, filename: str) -> List[Dict[str, Any]]:
    print("Fetching data from the API...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Successfully fetched and saved data to '{filename}'")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON from response.")
        return []


def normalize_data(raw_data: List[Dict[str, Any]]) -> pd.DataFrame:
    print("Normalizing data into a flat structure...")
    records = []
    for country_data in raw_data:
        country_name = country_data.get('country')
        if not country_name or not country_data.get('timeline'):
            continue

        cases_timeline = country_data['timeline'].get('cases', {})
        for date, cases in cases_timeline.items():
            records.append({
                'country': country_name,
                'date': date,
                'cases': cases
            })

    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y')
    df = df.sort_values(by=['country', 'date'])
    return df


def pivot_and_save_data(df: pd.DataFrame, filename: str) -> pd.DataFrame:
    print("Reshaping data with pivot_table...")
    pivot_df = df.pivot_table(
        index='date',
        columns='country',
        values='cases',
        fill_value=0
    )
    pivot_df.to_csv(filename)
    print(f"Successfully pivoted and saved data to '{filename}'")
    return pivot_df


def visualize_trends(pivot_df: pd.DataFrame, countries: List[str], filename: str):
    print(f"Generating plot for case trends...")

    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(14, 8))

    plot_countries = [country for country in countries if country in pivot_df.columns]

    pivot_df[plot_countries].plot(ax=ax, marker='o', linestyle='-')

    ax.set_title('COVID-19 Total Cases Trend (Last 30 Days)', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Total Confirmed Cases', fontsize=12)
    ax.legend(title='Country')
    ax.ticklabel_format(style='plain', axis='y')

    plt.tight_layout()
    plt.savefig(filename)
    print(f"Saved trend chart to '{filename}'")
    plt.close()


def analyze_and_visualize_daily_change(df: pd.DataFrame, filename: str):
    print("Analyzing daily changes and generating plot...")

    df['daily_change'] = df.groupby('country')['cases'].diff().fillna(0)

    last_7_days = df['date'].max() - pd.Timedelta(days=7)
    recent_data = df[df['date'] > last_7_days]

    total_increase_last_7_days = recent_data.groupby('country')['daily_change'].sum()
    top_5_countries = total_increase_last_7_days.nlargest(5).index

    top_5_df = df[df['country'].isin(top_5_countries)]

    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(14, 8))

    for country in top_5_countries:
        country_df = top_5_df[top_5_df['country'] == country]
        ax.plot(country_df['date'], country_df['daily_change'], marker='.', linestyle='-', label=country)

    ax.set_title('Daily Case Changes for Top 5 Increasing Countries', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('New Daily Cases', fontsize=12)
    ax.legend(title='Country')

    plt.tight_layout()
    plt.savefig(filename)
    print(f"Saved daily change chart to '{filename}'")
    plt.close()


if __name__ == "__main__":
    raw_data = fetch_and_save_data(API_URL, 'historical.json')

    if raw_data:
        normalized_df = normalize_data(raw_data)

        pivoted_df = pivot_and_save_data(normalized_df, 'pivoted_covid.csv')

        visualize_trends(pivoted_df, COUNTRIES_TO_PLOT, 'country_case_trends.png')

        analyze_and_visualize_daily_change(normalized_df, 'daily_change_comparison.png')

        print("\nAnalysis complete. All files have been generated.")