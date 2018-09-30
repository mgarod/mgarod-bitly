### Assumptions
https://dev.bitly.com/v4/#operation/getMetricsForBitlinkByCountries
- Given that I only have access to my own bitlinks, I have no data with a timestamp other than 9/30. Therefore, I am assuming that by passing in `?units=30&unit=day&size=30` (or some combination therein) to this endpoint, this query is capable of returning to me the last 30 days worth of metrics.
- Given that I can only produce clicks from the `US`, I must assume that this endpoint will produce the field `metrics` which is an array of dicts. I am only able to view `"metrics":[{"value":"US","clicks":4}]`, but I am assuming it could look like `"metrics":[{"value":"US","clicks":4},{"value":"GB","clicks":6},{"value":"JP","clicks":3}]`

Pagination
- Given that I have so little data to play with while creating this API, I will be ignoring the more complex feature of pagination