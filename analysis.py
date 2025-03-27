import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

# Set style for better visualizations
plt.style.use('whitegrid')
sns.set_palette("husl")

# Read the data
financial_df = pd.read_csv('finanical_information.csv')
payment_df = pd.read_csv('payment_information.csv')
subscription_df = pd.read_csv('subscription_information.csv')
industry_df = pd.read_csv('industry_client_details.csv')

# 1. Count of Finance Lending and Blockchain clients
def analyze_industry_clients():
    industry_counts = industry_df['industry'].value_counts()
    target_industries = industry_counts[['Finance Lending', 'Block Chain']]
    
    plt.figure(figsize=(10, 6))
    target_industries.plot(kind='bar')
    plt.title('Number of Finance Lending and Blockchain Clients')
    plt.xlabel('Industry')
    plt.ylabel('Number of Clients')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('industry_counts.png')
    plt.close()
    
    print("\n1. Industry Client Counts:")
    print(target_industries)

# 2. Industry with highest renewal rate
def analyze_renewal_rates():
    # Merge subscription and industry data
    merged_df = subscription_df.merge(industry_df, on='client_id')
    
    # Calculate renewal rate by industry
    industry_renewal = merged_df.groupby('industry')['renewed'].agg(['count', 'sum'])
    industry_renewal['renewal_rate'] = (industry_renewal['sum'] / industry_renewal['count']) * 100
    
    plt.figure(figsize=(12, 6))
    industry_renewal['renewal_rate'].plot(kind='bar')
    plt.title('Renewal Rate by Industry')
    plt.xlabel('Industry')
    plt.ylabel('Renewal Rate (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('renewal_rates.png')
    plt.close()
    
    print("\n2. Industry Renewal Rates:")
    print(industry_renewal['renewal_rate'].round(2))

# 3. Average inflation rate during subscription renewals
def analyze_inflation_rates():
    # Convert dates to datetime
    subscription_df['start_date'] = pd.to_datetime(subscription_df['start_date'])
    financial_df['start_date'] = pd.to_datetime(financial_df['start_date'])
    
    # Merge subscription and financial data
    merged_df = subscription_df.merge(financial_df, on='start_date', how='left')
    
    # Calculate average inflation rate for renewed subscriptions
    avg_inflation = merged_df[merged_df['renewed'] == True]['inflation_rate'].mean()
    
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='renewed', y='inflation_rate', data=merged_df)
    plt.title('Inflation Rate Distribution for Renewed vs Non-Renewed Subscriptions')
    plt.xlabel('Subscription Renewed')
    plt.ylabel('Inflation Rate (%)')
    plt.tight_layout()
    plt.savefig('inflation_rates.png')
    plt.close()
    
    print("\n3. Average Inflation Rate during Renewals:")
    print(f"{avg_inflation:.2f}%")

# 4. Median amount paid each year by payment method
def analyze_payment_amounts():
    # Convert payment date to datetime
    payment_df['payment_date'] = pd.to_datetime(payment_df['payment_date'])
    payment_df['year'] = payment_df['payment_date'].dt.year
    
    # Calculate median amount by year and payment method
    yearly_medians = payment_df.groupby(['year', 'payment_method'])['amount_paid'].median().unstack()
    
    plt.figure(figsize=(12, 6))
    yearly_medians.plot(kind='bar', stacked=False)
    plt.title('Median Payment Amount by Year and Payment Method')
    plt.xlabel('Year')
    plt.ylabel('Median Amount ($)')
    plt.legend(title='Payment Method')
    plt.tight_layout()
    plt.savefig('payment_amounts.png')
    plt.close()
    
    print("\n4. Median Payment Amounts by Year and Payment Method:")
    print(yearly_medians.round(2))

def main():
    analyze_industry_clients()
    analyze_renewal_rates()
    analyze_inflation_rates()
    analyze_payment_amounts()

if __name__ == "__main__":
    main() 