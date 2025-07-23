# Since I don't have true "credit score" labels, I'll create a simple heuristic score first
# Then train a model to learn from this pattern and generalize to new wallets

# Create a simple "responsibility score" using my domain logic
def calculate_responsibility_score(row):
    """
    Simple heuristic to score wallet responsibility (0-1 scale)
    Higher = more responsible behavior
    """
    score = 0.0
    
    # Reward good repayment behavior (up to 0.3 points)
    score += min(row['repay_ratio'] * 0.3, 0.3)
    
    # Reward longer activity history (up to 0.2 points)  
    max_days = features['days_active'].max()
    score += (row['days_active'] / max_days) * 0.2
    
    # Reward deposit activity (up to 0.2 points)
    score += row['deposit_ratio'] * 0.2
    
    # Reward activity diversity (up to 0.15 points)
    score += row['activity_diversity'] * 0.15
    
    # Penalize liquidations (subtract up to 0.15 points)
    score -= row['liquidation_rate'] * 0.15
    
    # Ensure score stays between 0 and 1
    return max(0, min(1, score))

# Apply my scoring logic
features['responsibility_score'] = features.apply(calculate_responsibility_score, axis=1)

print(f"Responsibility scores range: {features['responsibility_score'].min():.3f} to {features['responsibility_score'].max():.3f}")
print(f"Mean responsibility score: {features['responsibility_score'].mean():.3f}")

# Prepare data for machine learning
# I'll use the engineered features to predict my responsibility score
feature_columns = [
    'num_transactions', 'total_volume', 'avg_transaction_size',
    'num_deposit', 'num_borrow', 'num_repay', 'num_redeem', 'num_liquidation',
    'days_active', 'transactions_per_day', 'repay_ratio', 'liquidation_rate',
    'deposit_ratio', 'activity_diversity', 'unique_actions'
]

# Fill any NaN values (might occur from ratios)
features[feature_columns] = features[feature_columns].fillna(0)

X = features[feature_columns]
y = features['responsibility_score']

# Split for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Use Random Forest - good default choice for tabular data like this
model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
model.fit(X_train, y_train)

# Check how well the model learned my patterns
y_pred_test = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred_test)
print(f"Model Test MSE: {mse:.4f}")

# Show feature importance (what the model thinks matters most)
feature_importance = pd.DataFrame({
    'feature': feature_columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 5 most important features according to the model:")
print(feature_importance.head())

# Now I'll predict on ALL wallets to assign a credit score
# I'm using the model I just trained to score every wallet in my dataset
features['ml_score'] = model.predict(X)

# Scale to 0–1000 for presentation (classic credit score format)
# I want higher numbers to mean "more responsible" wallets
scaler_final = MinMaxScaler(feature_range=(0, 1000))
features['credit_score'] = scaler_final.fit_transform(features[['ml_score']]).flatten().astype(int)

# Create a simple output table - just wallet address and credit score
# This is what I'd show to a manager or use in the next step of analysis
output = features[['wallet', 'credit_score']].copy()
output = output.sort_values('credit_score', ascending=False)  # Best scores first

print("=== TOP 10 WALLETS BY CREDIT SCORE ===")
print(output.head(10))

print(f"\n=== CREDIT SCORE DISTRIBUTION ===")
print(f"Highest score: {output['credit_score'].max()}")
print(f"Lowest score: {output['credit_score'].min()}")
print(f"Average score: {output['credit_score'].mean():.0f}")

# Save to CSV - this is my main deliverable
output.to_csv('wallet_credit_scores.csv', index=False)
print(f"\n✅ Saved {len(output)} wallet scores to 'wallet_credit_scores.csv'")
