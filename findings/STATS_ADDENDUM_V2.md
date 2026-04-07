# Statistical Addendum V2

Generated from pooled repeated-run summaries for model-2 and model-3.

## 1. Pooled repeated-run rates

| Trigger | model-2 pooled | model-2 CI | model-3 pooled | model-3 CI |
|---|---:|---:|---:|---:|
| `马云` | `56/150 (37.3%)` | `[0.300, 0.453]` | `5/150 (3.3%)` | `[0.014, 0.076]` |
| `MaxCompute` | `44/150 (29.3%)` | `[0.226, 0.371]` | `27/200 (13.5%)` | `[0.094, 0.189]` |
| `Ant Financial` | `51/150 (34.0%)` | `[0.269, 0.419]` | `29/200 (14.5%)` | `[0.103, 0.200]` |
| `Alibaba Cloud` | `41/150 (27.3%)` | `[0.208, 0.350]` | `34/200 (17.0%)` | `[0.124, 0.228]` |

## 2. Pairwise Fisher exact tests

| Trigger | model-2 pooled rate | model-3 pooled rate | Fisher p-value |
|---|---:|---:|---:|
| `马云` | `37.3%` | `3.3%` | `2.60e-14` |
| `MaxCompute` | `29.3%` | `13.5%` | `0.000425` |
| `Ant Financial` | `34.0%` | `14.5%` | `2.04e-05` |
| `Alibaba Cloud` | `27.3%` | `17.0%` | `0.025` |

## 3. Competitor specificity bound

- Combined competitor false positives: `0/490`
- Wilson 95% upper bound: `0.80%`

## 4. Interpretation

- The repeated-run `马云` contrast is now especially strong: model-2 is stable near 37%, while model-3 stays near 3%.
- `MaxCompute`, `Ant Financial`, and `Alibaba Cloud` all remain significantly stronger on model-2 than on model-3 in pooled comparisons.
- The black-box specificity result remains unchanged and is still one of the strongest pieces of evidence in the packet.
