# Journal — Meridian Pivot (Sync Service Prototype)

**Tool: Retry/Backoff Strategies**

**Day 1 — 2026-08-17**

### [14:22] Attempting: Understand the basic concepts behind retry and backoff strategies, including why retries are used and what makes a failure transient or permanent.

- Tried: Researched retry and backoff strategies, focusing on the meaning of retries, backoff, transient failures, and non-transient failures. Also looked into examples of failures that may be temporary, such as network blips, cold starts, microservice downtime, and server overload, and compared these with non-transient failures such as authentication errors, client errors, and bad data syntax.
- Result: Retry and backoff is a strategy used in computer systems to handle temporary errors. A retry means attempting a failed operation again, while backoff introduces a delay before the next attempt. Some failures are transient and may resolve themselves after a short period, making them suitable candidates for retrying. Permanent failures are unlikely to be fixed by simply trying the same operation again.
- Source consulted:
  - Microsoft Azure — Transient Faults: https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults
  - AWS Builder — Timeouts, retries, and backoff with jitter: https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter
  - urllib3 documentation — Retry: https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html
  - MDN — Retry-After header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Retry-After
  - DEV Community — Retry and Backoff Strategies: https://dev.to/godofgeeks/retry-and-backoff-strategies-jitter-2c1p
- Next: Research retryable versus non-retryable failures in more detail, including which HTTP status codes are commonly retried and why blindly retrying every failure can be dangerous.

### [15:22] Attempting: Understand which failures should be retried and which should not, and why retrying every failure can be harmful.

- Tried: Researched HTTP status codes and identified temporary server-side or rate-limit responses that can commonly be candidates for retry, including 429 (Too Many Requests), 503 (Service Unavailable), 504 (Gateway Timeout), 502 (Bad Gateway), and 500 (Internal Server Error). Also identified errors such as 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), and 404 (Not Found) as examples of failures that generally should not simply be retried.
- Result: Blindly retrying every failure can cause additional problems rather than solving the original problem — potential consequences include accidentally overloading a service, duplicate charging, data corruption, and unnecessary consumption of network bandwidth and device resources. Also learned the basic ideas behind exponential backoff and jitter: exponential backoff increases the waiting time after consecutive failures instead of retrying immediately; jitter introduces random timing variation so many clients don't retry at exactly the same time; a retry limit prevents a program from retrying indefinitely. Current understanding: a retry attempts a failed operation again; backoff waits before the next attempt; exponential backoff increases the wait after consecutive failures; jitter adds timing variation; retry limits prevent endless attempts.
- Source consulted:
  - Microsoft Azure — Transient Faults: https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults
  - AWS Builder — Timeouts, retries, and backoff with jitter: https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter
  - urllib3 documentation — Retry: https://urllib3.readthedocs.io/en/stable/reference/urllib3.util.html
  - MDN — Retry-After header: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Retry-After
  - DEV Community — Retry and Backoff Strategies: https://dev.to/godofgeeks/retry-and-backoff-strategies-jitter-2c1p
- Next: How would I actually implement the "wait" part of backoff in Python — what mechanism would I reach for to pause execution between retries?

### [15:47] Attempting: Determine how Python can pause execution between retry attempts as part of implementing the backoff mechanism.

- Tried: Researched how to introduce a delay between failed attempts before making another retry.
- Result: Identified Python's `time.sleep()` as the basic mechanism for pausing the current execution for a specified number of seconds. This can be used to implement the "wait" part of backoff between retry attempts. Still need to determine how the delay should be calculated dynamically for different retry attempts, particularly when using exponential backoff and jitter.
- Source consulted: Python documentation / research on `time.sleep()`.
- Next: Work out the formula for calculating exponential backoff delay across increasing retry attempts, and how jitter gets added to it.

### [16:05] Attempting: Build a first simple retry/backoff prototype that retries a failed operation, waits longer after each failure, and stops after a maximum number of retries.

- Tried: Researched the exponential backoff formula and used `time.sleep()` to introduce the delay between retry attempts. Started with a base delay of 1 second and an exponential multiplier of 2, so the expected delays increase from 1 second to 2 seconds, then 4 seconds, and so on.
- Result: Identified the basic mechanism for implementing exponential backoff: calculate an increasing delay based on the retry attempt and pause execution using `time.sleep()` before making the next attempt. Also added a maximum retry limit so the operation does not continue retrying indefinitely.
- Source consulted: AWS documentation on retry behavior and exponential backoff with jitter; Python documentation for `time.sleep()`.
- Next: Test the prototype with an operation that fails repeatedly and observe whether the retry delays increase as expected. Then test a case where the operation eventually succeeds and verify that no unnecessary retries occur.

### [16:48] Attempting: Run the retry/backoff prototype to verify delay behavior and max-retry handling.

- Tried: Ran `retry_backoff.py`, where `unreliable_operation()` always fails, to observe the retry sequence and delay pattern in practice.
- Result: Confirmed the expected exponential pattern — Attempt 1 failed, waited 1 second; Attempt 2 failed, waited 2 seconds; Attempt 3 failed, waited 4 seconds; Attempt 4 failed and hit the max retry limit, at which point the exception was re-raised and a traceback printed. This confirmed the max-retry path works correctly — the program doesn't silently swallow a permanent failure, it surfaces it once retries are exhausted.
- Source consulted: None — this was direct testing of my own code.
- Next: Modify `unreliable_operation()` to fail a set number of times and then succeed, to test and confirm the "eventual success" path (currently untested since the function never succeeds).