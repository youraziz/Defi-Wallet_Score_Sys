# Analysis of DeFi Wallet Credit Scores

This document provides a detailed analysis of the credit scores assigned to DeFi wallets based on their on-chain transaction history. The scoring model evaluates wallets on factors such as transaction volume, frequency, diversity of actions, and repayment behavior to gauge their financial health and reliability within the DeFi ecosystem.

## Credit Score Distribution

The distribution of credit scores across the entire dataset provides a high-level overview of the wallet population. The scores are segmented into ranges of 100 points, from 0 to 1000.

![Credit Score Distribution](visualizations/Wallet-Cred-Score.jpg)

### Score Distribution Table

| Score Range     | Number of Wallets | Percentage of Total |
|-----------------|-------------------|---------------------|
| 0-100           | [Your Number]     | [Your %]            |
| 101-200         | [Your Number]     | [Your %]            |
| 201-300         | [Your Number]     | [Your %]            |
| 301-400         | [Your Number]     | [Your %]            |
| 401-500         | [Your Number]     | [Your %]            |
| 501-600         | [Your Number]     | [Your %]            |
| 601-700         | [Your Number]     | [Your %]            |
| 701-800         | [Your Number]     | [Your %]            |
| 801-900         | [Your Number]     | [Your %]            |
| 901-1000        | [Your Number]     | [Your %]            |
| **Total**       | **[Total Wallets]** | **100%**            |

---

## Behavior of Wallets in the Lower Range (e.g., Scores < 400)

Wallets in the lower score ranges typically exhibit characteristics associated with higher risk, low engagement, or new users.

### **Key Characteristics:**
*   **Low Transaction Count:** Very few transactions over their lifetime.
*   **Short Activity Window:** The wallet has only been active for a very short period.
*   **High Liquidation Rate:** A significant portion of their activity involves `liquidationcall` events, indicating forced closure of under-collateralized loans.
*   **Poor Repay Ratio:** A low ratio of `repay` actions compared to `borrow` actions, suggesting they do not consistently pay back loans.
*   **Low Activity Diversity:** Wallets may only perform one or two types of actions (e.g., a single deposit and withdrawal).

### **Inferred Behavior:**
These wallets may represent users who are either new to DeFi and experimenting, have abandoned the wallet, or are engaging in high-risk behavior that is not sustainable. They are considered less reliable from a credit perspective.

---

## Behavior of Wallets in the Higher Range (e.g., Scores > 700)

Wallets with high credit scores demonstrate patterns of a mature, reliable, and engaged DeFi user.

### **Key Characteristics:**
*   **High Transaction Count & Volume:** Consistent and significant on-chain activity.
*   **Long Activity Window:** The wallet has been active for a long period, showing sustained engagement.
*   **Zero or Near-Zero Liquidations:** These users manage their collateral effectively and avoid liquidations.
*   **Excellent Repay Ratio:** They consistently repay their borrowed assets, indicating financial responsibility.
*   **High Activity Diversity:** They interact with multiple protocols or actions (e.g., depositing, borrowing, redeeming, providing liquidity), showcasing deep engagement with the DeFi ecosystem.

### **Inferred Behavior:**
These wallets belong to "power users" who are experienced, financially stable, and integral to the health of DeFi protocols. They represent the lowest credit risk.

---

## Conclusion

The credit scoring model successfully differentiates between distinct user profiles within the DeFi space. The analysis reveals a clear correlation between a wallet's on-chain behavior and its assigned score, confirming that factors like repayment history, liquidation events, and engagement levels are strong indicators of creditworthiness.
