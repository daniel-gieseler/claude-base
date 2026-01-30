---
name: data-analysis
description: Analyzes datasets to extract insights, patterns, and statistics. Use when the user has data to analyze, wants to understand trends, or needs statistical summaries.
---

# Data Analysis

## Process

1. **Understand the data** - Schema, types, row count, null values
2. **Clean if needed** - Handle missing values, outliers, duplicates
3. **Explore** - Distributions, correlations, patterns
4. **Summarize** - Key statistics and insights
5. **Visualize** - Charts when helpful

## Quick Stats

For any dataset, provide:
- Row/column count
- Data types per column
- Missing value percentage
- Unique value counts for categoricals
- Min/max/mean/median for numerics

## Common Patterns

**Trend analysis:**
```python
df.groupby('date').agg({'value': 'sum'}).plot()
```

**Distribution check:**
```python
df['column'].describe()
df['column'].hist()
```

**Correlation:**
```python
df.select_dtypes(include='number').corr()
```

## Output Format

```markdown
## Dataset Overview
[Basic stats: rows, columns, types]

## Key Findings
1. [Most important insight]
2. [Second insight]
3. [Third insight]

## Recommendations
- [Actionable next steps based on findings]
```

## Guidelines

- Start with overview before diving into details
- Highlight anomalies and unexpected patterns
- Quantify findings (percentages, counts)
- Suggest follow-up questions the data could answer
