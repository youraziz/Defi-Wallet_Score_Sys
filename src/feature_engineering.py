# First, I need to clean up the data and extract useful information
# The actionData column contains nested dictionaries with amount info

# Extract amount from actionData dictionary
def extract_amount(action_data):
    """Extract amount from the nested actionData dictionary"""
    try:
        if isinstance(action_data, dict) and 'amount' in action_data:
            # Convert string amount to float, handling scientific notation
            return float(action_data['amount'])
        return 0.0
    except (ValueError, TypeError):
        return 0.0

# Apply the amount extraction
df['amount'] = df['actionData'].apply(extract_amount)

# Clean up the timestamp column (it's already in datetime format, just ensure it's proper)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Rename userWallet to wallet for consistency with my original plan
df['wallet'] = df['userWallet']

# Check what actions I have in the dataset
print("Available actions in dataset:")
print(df['action'].value_counts())
print(f"\nTotal transactions: {len(df)}")
print(f"Unique wallets: {df['wallet'].nunique()}")

# Group transactions by wallet to create features per wallet
# I'm looking for patterns that suggest responsible vs risky behavior

features = df.groupby('wallet').agg(
    num_transactions=('action', 'count'),
    total_volume=('amount', 'sum'),
    avg_transaction_size=('amount', 'mean'),
    
    # Count specific actions (adjust action names based on what I saw above)
    num_deposit=('action', lambda x: (x == 'deposit').sum()),
    num_borrow=('action', lambda x: (x == 'borrow').sum()),
    num_repay=('action', lambda x: (x == 'repay').sum()),
    num_redeem=('action', lambda x: (x == 'redeemunderlying').sum()),
    num_liquidation=('action', lambda x: (x == 'liquidationcall').sum()),
    
    # Time-based features
    first_transaction=('timestamp', 'min'),
    last_transaction=('timestamp', 'max'),
    
    # Unique action types (diversity of activity)
    unique_actions=('action', 'nunique'),
).reset_index()

# Create derived features that might indicate "responsibility"
features['days_active'] = (features['last_transaction'] - features['first_transaction']).dt.days + 1
features['transactions_per_day'] = features['num_transactions'] / features['days_active']

# Repayment behavior (good sign if someone repays what they borrow)
features['repay_ratio'] = features['num_repay'] / (features['num_borrow'] + 1)  # +1 to avoid division by zero

# Liquidation rate (bad sign - means positions got liquidated)
features['liquidation_rate'] = features['num_liquidation'] / features['num_transactions']

# Deposit ratio (good sign - putting money in)
features['deposit_ratio'] = features['num_deposit'] / features['num_transactions']

# Activity diversity (more diverse activity might indicate real user vs bot)
features['activity_diversity'] = features['unique_actions'] / features['num_transactions']

print(f"Created features for {len(features)} unique wallets")
print("\nFeature summary:")
print(features.describe())

# My logic for "responsible" wallet indicators:
# GOOD SIGNS:
# - Higher repay_ratio: pays back loans
# - Longer days_active: established user  
# - Higher deposit_ratio: puts money into protocol
# - More activity_diversity: not just doing one type of transaction
# - Lower liquidation_rate: doesn't get liquidated often

# BAD SIGNS:  
# - High liquidation_rate: risky positions
# - Very short days_active: might be temporary/bot activity
# - Low repay_ratio: borrows but doesn't repay
# - Only one type of action: might be automated behavior

print("Sample of engineered features:")
print(features[['wallet', 'repay_ratio', 'liquidation_rate', 'deposit_ratio', 'days_active']].head())
