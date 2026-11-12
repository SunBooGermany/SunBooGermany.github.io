"""Instructor-only reference for the original transfer assessment."""
def weighted_jobs(jobs):
    ordered = sorted(jobs, key=lambda job: job[1])
    dp = [0] * (len(ordered) + 1)
    for i, (start, end, reward) in enumerate(ordered):
        compatible = 0
        for j in range(i):
            if ordered[j][1] <= start:
                compatible = j + 1
        dp[i + 1] = max(dp[i], reward + dp[compatible])
    return dp[-1]
