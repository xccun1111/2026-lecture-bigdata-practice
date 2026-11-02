
# Task 2: Curse of Dimensionality

## A2. Contrast by Dimension

| Dimension | Contrast |
|---:|---:|
| 2 | 488.582 |
| 5 | 14.257 |
| 10 | 3.925 |
| 20 | 2.253 |
| 50 | 0.982 |
| 100 | 0.545 |
| 200 | 0.372 |
| 500 | 0.256 |
| 1000 | 0.153 |

## A3. What Happens to Contrast?

Contrast decreases significantly as dimensionality increases.
It drops below 1 at 50 dimensions and below 0.5 at 200 dimensions.
At 1000 dimensions, contrast reaches 0.153, showing that distances become increasingly difficult to distinguish.

## A4. Mean Distance

The mean distance increases with dimensionality.
It grows approximately in proportion to the square root of the dimension, rather than linearly.

## A5. Relative Standard Deviation

Relative standard deviation decreases from 0.476 at 2 dimensions to 0.019 at 1000 dimensions.
Relative standard deviation better captures distance concentration because it measures the spread relative to the mean distance.

## A6. Effect of Point Count

At 20 dimensions, contrast increased from 2.253 with 1000 points to 2.448 with 2000 points.
This shows that contrast also depends on the number of points because the minimum and maximum distances are affected by the sample size.

## A7. Machine and Runtime

The experiments were conducted on Windows using Python 3.11.
Machine information and execution times were recorded in out/curse.json.

## A8. Connection to LSH

The curse of dimensionality does not directly invalidate Week 3 LSH.
LSH uses Jaccard similarity for shingle sets rather than Euclidean distance in a uniform high-dimensional space.
Therefore, the distance concentration observed in this experiment does not automatically apply to Jaccard-based LSH.
