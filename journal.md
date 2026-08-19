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



**Day 2 — 2026-08-18**

### [14:41] Attempting: Test the "eventual success" path of the retry/backoff prototype to confirm the retry loop returns normally when an operation recovers, rather than only handling permanent failure.

- Tried: Created `retry_backoff_success.py` with a modified `unreliable_operation()` that uses a global counter, causing it to raise an exception on the first two calls and succeed on the third. Ran `retry_with_backoff()` against this version to observe whether the function correctly stops retrying once the operation succeeds.
- Result: Confirmed the expected behavior — Attempt 1 failed and waited 1 second, Attempt 2 failed and waited 2 seconds, and on Attempt 3 the operation succeeded, printing 'Operation successful!' and returning immediately without any further retries or unnecessary delay. This confirms the retry loop correctly distinguishes between "still failing, keep retrying" and "succeeded, stop and return" — both halves of the retry/backoff mechanism (failure path and recovery path) are now verified.
- Source consulted: None — direct testing of my own code.
- Next: Move on to webhook verification (second assigned tool) — retry/backoff prototype is now functionally complete and tested for both outcomes.


**Day 2 — 2026-08-18 (continued)**

### [15:04] Attempting: Understand what a webhook is and how it differs from polling, since Day 4's pivot moves the sync service from one to the other.

- Tried: Researched what a webhook actually is — an application automatically sending data to another application when a specific event occurs, rather than the receiver having to ask for it. Looked into how this compares to polling, which is what the sync service currently uses (checking the warehouse API every 5 minutes).
- Result: Polling is request-driven — the receiver repeatedly asks "has anything changed?" on a schedule, which can waste requests when nothing's changed and introduces delay based on the polling interval. A webhook is event-driven — the source pushes data the moment something happens, so updates arrive close to real-time and only when there's actually something to report. For the sync service, this explains exactly what the Day 4 pivot changes: the warehouse goes from being asked repeatedly to instead notifying the service directly when inventory changes.
- Source consulted:
  - Red Hat — What is a webhook: https://www.redhat.com/en/topics/automation/what-is-a-webhook
  - Mailchimp — Webhook glossary: https://mailchimp.com/marketing-glossary/webhook/
  - Hilscher — Polling glossary: https://www.hilscher.com/service-support/glossary/polling
- Next: Understand the security problem — since a webhook is just an HTTP request hitting an exposed endpoint, how does the receiver know it's genuinely from the warehouse and not spoofed?

### [15:39] Attempting: Understand what a webhook signature is and how it lets the receiver trust an incoming webhook.

- Tried: Researched how applications verify that a webhook request is genuine, since exposing an endpoint like `POST /webhooks/inventory/` means anyone could technically send a request pretending to be the warehouse.
- Result: A webhook signature is a value the sender generates from the payload plus a shared secret, sent alongside the payload (usually in a request header). The receiver, who also holds the same secret, independently recalculates what the signature should be from the payload it received, then compares its calculated signature against the one the sender sent. If they match, it's strong evidence the request really came from someone who knows the secret and that the payload wasn't altered in transit. If they don't match, the webhook should be rejected. The secret itself is never sent — only the signature derived from it.
- Source consulted:
  - WebhookRelay — Verifying webhook signatures: https://webhookrelay.com/blog/verify-webhook-signature/
  - Mailchimp — Webhook glossary: https://mailchimp.com/marketing-glossary/webhook/
- Next: Understand HMAC, since that's the mechanism actually used to generate the signature.

### [16:27] Attempting: Understand HMAC and how it's used to generate a webhook signature from a secret and a message.

- Tried: Researched HMAC (Hash-based Message Authentication Code) to understand how the signature described above is actually produced.
- Result: HMAC is a method for creating a signature from a secret key and a message together — not from the message alone. Both sender and receiver need the same secret key, but the key itself is never transmitted. The sender feeds the secret and the payload into HMAC to produce the signature; the receiver does the same with its own copy of the secret and the payload it received, to produce what it expects the signature to be. If the two signatures match, it proves two things at once: that whoever sent the message knows the shared secret, and that the message hasn't been altered since it was signed (since even a small change to the message would produce a completely different signature). This is why HMAC gives both authentication and integrity, not just one or the other.
- Source consulted:
  - Hexnode — What is HMAC: https://www.hexnode.com/blogs/explained/what-is-hmac/
- Next: Understand SHA-256, since HMAC is commonly paired with it as HMAC-SHA256.

### [17:14] Attempting: Understand SHA-256 and why it's commonly paired with HMAC.

- Tried: Researched SHA-256 (Secure Hash Algorithm 256-bit) to understand its role inside HMAC-SHA256, which is the specific combination most webhook providers use.
- Result: SHA-256 is a cryptographic hash function — it takes an input of any size and produces a fixed-size 256-bit output, usually shown as a 64-character hex string. The same input always produces the exact same hash, but changing even one character of the input produces a completely different hash. That property is exactly what makes it useful for signatures: if someone tampers with a webhook payload after it's signed, recalculating the hash on the tampered version will produce a different result than the original signature, so the mismatch exposes the tampering. HMAC-SHA256 means HMAC is using SHA-256 specifically as its underlying hash function.
- Source consulted:
  - upGrad — SHA-256 algorithm: https://www.upgrad.com/blog/sha-256-algorithm/
  - CheapSSLSecurity — SHA-2/SHA-256 hashing: https://cheapsslsecurity.com/p/what-is-the-sha-2-sha256-hashing-algorithm/
- Next: Understand why the signature must be calculated against the raw request body specifically, rather than a parsed/re-serialized version of it.

### [20:33] Attempting: Understand why webhook signatures must be calculated against the exact raw request body.

- Tried: Researched why verification implementations specifically warn against parsing the JSON payload and reconstructing it before checking the signature.
- Result: JSON can represent identical data in different byte sequences — for example `{"sku":"MOUSE001","quantity":10}` versus the same data spread across multiple lines with indentation. Both represent the same information, but they are different sequences of bytes, and a cryptographic hash is sensitive to the exact bytes given to it, not the meaning behind them. So if the payload is parsed into a Python object and then re-serialized before hashing, the reconstructed bytes likely won't exactly match what the sender originally signed, causing a genuinely valid webhook to fail verification. The fix is to calculate the signature against the raw request body exactly as received, before any parsing happens.
- Source consulted:
  - WebhookRelay — Verifying webhook signatures: https://webhookrelay.com/blog/verify-webhook-signature/
- Next: Understand how the two signatures should actually be compared in code, since I recall reading that a normal `==` comparison isn't considered safe for this.

### [21:08] Attempting: Understand why signature comparison needs a special method rather than ordinary equality, and what Python provides for it.

- Tried: Researched timing attacks and how they relate to comparing security-sensitive values like signatures.
- Result: An ordinary string comparison (`==`) typically stops checking as soon as it hits the first mismatched character, which means a comparison against a mostly-correct guess takes very slightly longer than one against a completely wrong guess. In theory, an attacker could measure those tiny timing differences over many attempts to gradually guess a secret value, one character at a time — this is called a timing attack. To prevent this, security-sensitive comparisons should take the same amount of time regardless of where or whether a mismatch occurs. Python provides `hmac.compare_digest()` specifically for this — it performs a constant-time comparison, so it doesn't leak timing information the way a normal `==` check might.
- Source consulted:
  - Avantec — Timing attacks: https://www.avantec.ch/timing-attacks-when-time-betrays-security/
- Next: Build a small webhook verification prototype in Python — generate a valid signature for a payload and confirm verification succeeds, then tamper with the payload and confirm verification correctly fails.

### [21:42] Attempting: Write the first part of the webhook verification prototype — generating an HMAC-SHA256 signature from a payload and secret.

- Tried: Created `webhook_verification_prototype/webhook_verification.py` with a fixed secret and a sample JSON payload, and used `hmac.new(secret, payload, hashlib.sha256).hexdigest()` to generate a signature, matching the sender-side process I researched earlier.
- Result: Ran the script and got a signature: `f8643d9849640df3411646b1748dc9999e85bf0553bd8e0bbd19f2be63c8927c`. This confirmed the signature generation works as expected — 64 hex characters, matching the expected output length of SHA-256. This is only the sender side so far; the receiver-side verification (recalculating and comparing signatures) still needs to be built.
- Source consulted: None — direct implementation based on earlier research.
- Next: Write a `verify_signature()` function that recalculates the expected signature from a received payload and secret, then compares it against a received signature using `hmac.compare_digest()`.



**Day 3 — 2026-08-19**

### [16:27] Attempting: Build the receiver-side webhook signature verification prototype to determine whether an incoming webhook signature matches the signature independently calculated from the received payload and shared secret.

- Tried: Created `webhook_verification_prototype/webhook_signature_verification.py` as a separate prototype from the previous signature-generation experiment. The purpose of keeping it separate was to make the sender-side signature generation and receiver-side verification independently visible.

  The prototype uses the same shared secret and sample payload from the previous experiment. The signature generated in `webhook_verification.py` was treated as the `received_signature`, simulating the signature that would normally arrive with a webhook request.

  Created a `verify_signature()` function that accepts three values:
  - `payload` — the webhook message received by the application.
  - `secret` — the shared secret known by both the sender and receiver.
  - `received_signature` — the signature supplied with the incoming webhook.

  Inside the function, an `expected_signature` is generated independently using `hmac.new()` with the same secret, payload, and SHA-256 algorithm used by the sender. The resulting digest is converted to a hexadecimal string using `.hexdigest()`.

  The received signature is then compared with the independently calculated expected signature using `hmac.compare_digest()` rather than ordinary string comparison. This follows the security concept researched earlier around constant-time comparison and timing attacks.

- Result: The verification prototype successfully calculated an expected signature from the received payload and shared secret and compared it with the signature generated by the previous prototype. Because both sides used the same secret, the same payload, and the same HMAC-SHA256 algorithm, the calculated signature matched the received signature and the function returned `True`.

  This confirmed the basic receiver-side verification flow:

  `Received payload + shared secret → calculate expected signature → compare with received signature → True/False`

  I also confirmed that the receiver does not simply trust the signature supplied by the sender. Instead, it independently recreates the signature and uses the comparison result to determine whether the webhook signature is valid.

  The `received_signature` in this prototype is manually copied from the first prototype to simulate the signature that would normally be included in an actual webhook request.

- Source consulted: None — direct implementation based on the webhook verification concepts researched earlier.

- Next: Create a separate tampering/invalid-signature experiment by changing the webhook payload while keeping the original received signature unchanged. The purpose is to confirm that the verification mechanism detects when the payload has been altered and returns `False` instead of accepting the webhook.


### [20:43] Attempting

Testing whether the webhook verification logic correctly rejects a tampered webhook payload. The goal was to test the invalid-signature path and complement the valid-signature verification I had already tested.

### Tried

1. Created a standalone `webhook_tampering.py` experiment to simulate a tampered webhook payload.
2. Started with the original payload:

   `b'{"sku":"MOUSE001","quantity":10}'`

   and the signature generated from that original payload.
3. Changed the payload by modifying the quantity from `10` to `1000`, while keeping the original signature unchanged.
4. Initially calculated the expected signature for the modified payload separately and compared it with the original signature using `hmac.compare_digest()`.
5. Then changed the tampering experiment to use the actual `verify_signature()` function from `webhook_signature_verification.py`.
6. While testing this, I noticed that importing `verify_signature()` also caused the original verification test in `webhook_signature_verification.py` to run, producing an additional `Signature valid: True` output.
7. I fixed this by placing the original verification demonstration under `if __name__ == "__main__":`. This allowed the function to be imported without automatically running the demonstration code.

### Result

The original verification experiment still worked correctly when run directly:

Signature valid: True

The tampering experiment then produced:

Received signature: f8643d9849640df3411646b1748dc9999e85bf0553bd8e0bbd19f2be63c8927c
Tampered payload: {"sku":"MOUSE001","quantity":1000}
Signature valid: False

This confirmed that the actual `verify_signature()` function correctly detects when the webhook payload has been modified while the original signature remains unchanged.

The test demonstrated that the receiver calculates the expected signature from the payload it actually receives. Because the tampered payload produces a different HMAC-SHA256 signature, `hmac.compare_digest()` returns `False`, meaning the webhook should be rejected.

I also learned that Python executes a module's top-level code when it is imported. Using `if __name__ == "__main__":` separates reusable functions from code intended to run only when the file is executed directly.

### Source consulted

I applied the same "test both paths" approach used during the retry/backoff experiments. The retry work showed that testing only successful operations is not enough; the failure path also needs to be demonstrated.

I applied the same principle to webhook verification by testing both:

- a valid payload/signature combination
- an invalid combination caused by payload tampering

### Next

Combine the retry/backoff and webhook verification work into one coherent sync-service prototype.

The intended flow is to verify an incoming webhook first and reject it if the signature is invalid. If verification succeeds, the service can proceed with a downstream operation and use retry/backoff when that operation encounters a transient failure.


### [21:24] Attempting

Starting the integration of the webhook verification and retry/backoff work into a small sync-service prototype. The first goal was to create a service function that verifies an incoming webhook before allowing it to be processed.

### Tried

1. Created a new `sync_service_prototype/` directory for the integrated prototype.
2. Created `sync_service.py` and reused the existing `verify_signature()` function from `webhook_signature_verification.py` instead of duplicating the HMAC verification logic.
3. Added a `process_webhook()` function that verifies the received webhook signature first. If the signature is invalid, it returns `"Webhook rejected"`. If the signature is valid, it returns `"Webhook processed"`.
4. When I first tried to run the service, Python returned:

   ModuleNotFoundError: No module named 'webhook_verification_prototype'

5. I first tried resolving the import issue by adding `__init__.py` files to the prototype directories so that Python could treat them as packages. This did not resolve the problem when running the file directly.
6. I then ran the service from the project root as a Python module using:

   python -m sync_service_prototype.sync_service

### Result

The module-based execution worked correctly and produced:

Webhook processed

This confirmed that the sync service could successfully import and reuse the existing `verify_signature()` function and allow a valid webhook to pass the verification stage.

The import issue also helped me understand that Python's import behavior depends not only on the package structure but also on how the code is executed. Running the service with `python -m` allowed Python to resolve the project packages correctly from the project root.

### Next

Test the integrated sync service with a tampered/invalid webhook and confirm that the service rejects it before any processing occurs.

After that, add a downstream operation and integrate the retry/backoff logic for transient failures.