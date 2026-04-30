# Categorical Nearest-Neighbor Logic

## Problem Framing

We are not solving a regression problem here directly. We are trying to find nearest neighbors using only non-numeric categorical features.

Key characteristics of the data:

- Rows are complete; there is no row-level missingness issue.
- The number of rows is relatively small.
- There are many categorical columns.
- Each categorical column can contain multiple possible categories.

This means the challenge is not "missing sparse rows" but high-dimensional categorical matching. After one-hot encoding, each row becomes sparse in feature space even though the original table is complete.

## What This Is Not

This does not require an NLP-style pipeline by default.

Not the first choice:

- tokenization
- text embeddings
- cosine-loss training

Those are more appropriate for free text fields such as descriptions, reviews, or notes. Here, the features are tabular categoricals, so the correct framing is categorical similarity or categorical nearest-neighbor retrieval.

## Ordinal vs Important Features

If some columns matter more than others, that does not make the data ordinal.

Ordinal means the values inside a feature have a natural order, for example:

- `low < medium < high`
- `bronze < silver < gold`

Our case is different:

- the features remain nominal categorical
- some columns may be more influential than others

This is feature weighting, not ordinal encoding.

## Role of XGBoost

XGBoost gave useful supervised signal for the regression task. We can reuse that signal to understand which categorical columns are more sensitive or important.

The idea is:

1. Train the supervised model on the original prediction target.
2. Estimate feature importance from that model.
3. Aggregate encoded importance back to the original categorical column level.
4. Use those column-level weights inside a neighbor similarity function.

Important note:

If one-hot encoding was used before XGBoost, one original categorical column becomes several encoded columns. The importance values should therefore be summed or aggregated back to the original feature name before using them as weights.

## Core Similarity Options

### 1. Weighted Exact-Match Similarity

For two rows `a` and `b`, compare each original categorical column:

- score `1` if the categories match
- score `0` if they do not

Then combine those scores using feature weights from XGBoost.

Formula:

```text
sim_match(a, b) = sum(w_j * I(a_j == b_j)) / sum(w_j)
```

Where:

- `w_j` is the weight of original categorical feature `j`
- `I(a_j == b_j)` is `1` when the values match and `0` otherwise

Why this is strong:

- very interpretable
- works well with few rows
- directly respects feature importance
- stays at the original feature level

### 2. Weighted Cosine Similarity on One-Hot Encoded Features

One-hot encode the categorical columns, then apply weights and compute cosine similarity in the encoded space.

Why this helps:

- handles high-dimensional categorical representation smoothly
- works naturally with sparse one-hot vectors
- can capture overall structural similarity in encoded space

This is still not an NLP pipeline. It is a sparse tabular similarity approach.

## Hybrid Similarity for Robustness

A reasonable next step is to combine both similarity views:

- weighted exact-match similarity on original columns
- weighted cosine similarity on one-hot encoded columns

Formula:

```text
sim_final(a, b) = alpha * sim_match(a, b) + (1 - alpha) * sim_cos(a, b)
```

A simple starting point is:

```text
alpha = 0.5
```

So:

```text
sim_final(a, b) = 0.5 * sim_match(a, b) + 0.5 * sim_cos(a, b)
```

## Why the Hybrid Can Help

`sim_match` contributes:

- interpretability
- stability
- direct feature-level matching

`sim_cos` contributes:

- smoothness in high-dimensional encoded space
- tolerance to wide categorical expansion
- another view of similarity beyond exact original-column matching

Together, they can make the neighbor ranking more robust than using either measure alone.

## Caution About Double Counting

Both similarities come from the same underlying categorical data, so the hybrid may partly double-count information.

That is not automatically wrong, but it means:

- both similarity components should be normalized to comparable scales
- the blend weight `alpha` should be treated as a tunable parameter
- the combined metric should be validated empirically

## Recommended Workflow

1. Keep only the categorical features intended for neighbor search.
2. Train XGBoost on the supervised target to estimate feature sensitivity.
3. Aggregate importances back to original categorical columns.
4. Normalize those importances into feature weights.
5. Compute weighted exact-match similarity on original columns.
6. One-hot encode the same categorical columns.
7. Compute weighted cosine similarity on the encoded matrix.
8. Blend the two similarities, starting with `50/50`.
9. Rank nearest neighbors using the final similarity score.
10. Validate whether the neighbors are meaningful.

## Validation Ideas

The best blend should not be assumed in advance. `50/50` is a starting point, not a rule.

Try a few settings such as:

- `0.7 * sim_match + 0.3 * sim_cos`
- `0.5 * sim_match + 0.5 * sim_cos`
- `0.3 * sim_match + 0.7 * sim_cos`

Then evaluate using one or more of the following:

- whether nearest neighbors have similar target values
- whether retrieved neighbors look sensible on manual inspection
- whether local prediction error improves when using neighbors
- whether the ranking stays stable across samples

## Practical Conclusion

The recommended logic for this use case is:

- treat the data as nominal categorical, not ordinal
- use XGBoost only to learn feature sensitivity, not as the neighbor model itself
- build a weighted categorical similarity
- optionally combine it with weighted cosine similarity for extra robustness

So the final modeling idea is not:

- tokenization
- embeddings
- cosine minimization

It is:

- supervised feature weighting from XGBoost
- categorical match scoring
- cosine similarity on one-hot encoded categoricals
- optional hybrid similarity for nearest-neighbor retrieval
