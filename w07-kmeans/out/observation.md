
# Week 07 Lab Observations

## Task 1: K-means Initialization

Different initial centroids can lead to different final clustering results.
K-means++ provides more reliable initialization than random initialization by selecting centroids based on squared distances.

## Task 2: Curse of Dimensionality

As dimensionality increased from 2 to 200, contrast decreased from 488.582 to 0.372, falling below 1 at 50 dimensions.
Increasing the number of points from 1000 to 2000 also changed contrast, while Jaccard-based LSH is not directly affected by this Euclidean distance experiment.

## Task 3: Fewer Distance Calculations

Each point stores one upper bound and k lower bounds, requiring k+1 additional values; the upper bound and centroid-distance bound can skip entire point comparisons, while lower bounds eliminate individual comparisons.
The optimized algorithm achieved exactly the same SSE as the baseline while reducing distance calculations by 91.7%, with the first iteration accounting for approximately 28% of total distance calculations.
