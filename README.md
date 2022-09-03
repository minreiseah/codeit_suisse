# Credit Suisse CodeIt Challenge

## Assumptions for Q1

- (Given) `timestamp` is in the format hh:mm
- (Given) `price` is a *positive* decimal > 0.0
- All variables are provided as strings
- At each timestamp, a ticker can only appear once
    - e.g. At 00:00, ticker **A** cannot appear more than once
    - By extension, we do not handle sub 1-minute intervals

