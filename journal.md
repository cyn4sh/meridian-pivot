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


### Sync Service Prototype — Downstream Operation and Final Integration

### [22:32] Attempting

After completing the webhook verification and retry/backoff experiments separately, I began connecting the two into a small sync-service prototype. The goal was to simulate a Northstar warehouse sending a signed webhook, verifying it first, then performing a downstream stock update that uses retry/backoff to recover from temporary failures.

I decided to simulate the downstream stock update rather than connect it to the Django/PostgreSQL models, so the prototype stays focused on demonstrating webhook verification and retry/backoff without adding database complexity.

### Tried

**1. `sync_stock_update.py`** — a baseline simulated stock-update function that always succeeds:

```python
def update_stock_quantity(sku, quantity):
    print(f"Updating {sku} stock to {quantity}")
    return True
```

Run directly, this produced:
```
Updating MOUSE001 stock to 100
Stock update successful: True
```

**2. `sync_stock_retry.py`** — added a module-level `attempts` counter so the function raises `ConnectionError("Temporary warehouse sync failure")` on the first two calls, to reproduce a transient failure with no retry logic yet:

```
Stock update attempt 1
Traceback (most recent call last):
  ...
ConnectionError: Temporary warehouse sync failure
```

This confirmed the simulated operation genuinely fails when unhandled — the raw problem retry/backoff needs to solve.

**3. `sync_stock_retry_backoff.py`** — wrapped the same failing operation in `update_stock_with_retry()`, using `max_retries=3` and exponential backoff (`delay = 2 ** (attempt - 1)`):

```
Stock update attempt 1
Attempt 1 failed: Temporary warehouse sync failure
Waiting 1 seconds before retrying...
Stock update attempt 2
Attempt 2 failed: Temporary warehouse sync failure
Waiting 2 seconds before retrying...
Stock update attempt 3
Updating MOUSE001 stock to 100
Stock update successful: True
```

Fails on attempts 1 and 2 (delays of 1s, then 2s), succeeds on attempt 3 once the counter clears the `attempts < 3` condition.

**4. `sync_service_integrated.py`** — combined `verify_signature()` with `update_stock_with_retry()` inside `process_webhook()`:

```
Webhook signature verified
Stock update attempt 1
Attempt 1 failed: Temporary warehouse sync failure
Waiting 1 seconds before retrying...
Stock update attempt 2
Attempt 2 failed: Temporary warehouse sync failure
Waiting 2 seconds before retrying...
Stock update attempt 3
Updating MOUSE001 stock to 100
Webhook processed successfully
```

Note: in this version, the SKU and quantity used for the stock update are hardcoded inside `process_webhook()` (`sku = "MOUSE001"`, `quantity = 100`) rather than parsed out of the actual `payload` argument. The payload is only used for signature verification, not data extraction. This is a simplification worth revisiting if the prototype needs to reflect real payload-driven updates.

**5. `sync_service_integrated_tampered.py`** — reused `process_webhook()` from file 4, called with a tampered payload (`quantity` changed from 10 to 1000) against the original, now-mismatched signature:

```
Webhook rejected
```

No `Stock update attempt` line appeared, confirming the downstream operation — and therefore retry/backoff — is never reached when signature verification fails.

### Result

The integrated flow works as intended:

```
Signed webhook
      ↓
Verify signature
      ↓
   Valid?
   /    \
 No      Yes
 ↓        ↓
Reject   Update stock (with retry/backoff on transient failure)
```

Retry/backoff only ever runs after a webhook has passed signature verification — an invalid webhook is rejected before any downstream operation, and therefore before any retry attempt, is triggered.

### Source consulted
Own retry/backoff and webhook verification experiments from earlier in the week; the exponential backoff formula and `hmac.compare_digest()` verification pattern were reused directly rather than rebuilt.



## Day 4 — The Meridian Pivot: Solstice Events Check-In

### Attendee State Foundation

### [12:18] Attempting

Before building the queue, webhook handler, and retry logic for the Solstice Events check-in service, I started by creating the foundation for tracking an attendee's check-in state.

The design requires the service to know whether an attendee has not checked in, is waiting for their badge to be printed, or has already completed check-in. This state will later be used to prevent duplicate scans and to handle webhook confirmations that may arrive out of order.

For the first experiment, I kept the implementation intentionally small. The goal was only to represent an attendee and confirm that the initial state was correct before adding state-transition logic.

### Tried

1. Created `solstice_pivot/attendee_state.py`.
2. Created an `Attendee` class with:
   - `attendee_id`
   - `name`
   - `status`
3. Set the initial status of every new attendee to:

   `not_checked_in`

4. Added a `__repr__()` method so the attendee's information and current state could be displayed clearly while testing.
5. Tested the file as a Python module from the project root using:

   ```bash
   python -m solstice_pivot.attendee_state
   ```

### Result

The program produced:

```
Attendee(id=A001, name=Alice, status=not_checked_in)
```

This matched the expected result.

The experiment confirmed that the basic attendee representation works and that a newly created attendee begins in the `not_checked_in` state.

I intentionally stopped at this point rather than adding the remaining state-transition logic to the same experiment. The purpose of this stage was to verify the foundation independently before building on top of it.

### What I learned

The attendee state will be important for the duplicate-scan requirement. The service cannot simply assume that every QR scan should create a new print request. It needs to know the attendee's current state before deciding what to do.

The planned state flow is:

```
not_checked_in
      ↓
   pending
      ↓
 checked_in
```

with a later failure path:

```
pending
   ↓
 failed
```

The current experiment only establishes the initial `not_checked_in` state. The transition rules will be implemented and tested as a separate experiment so that the progression remains visible.

### Next

Create a new separate file for the attendee state-transition experiment. This will add the `print_job_id` and enforce valid transitions such as:

not_checked_in → pending
pending → checked_in
pending → failed

It will also test an invalid duplicate transition, such as attempting to move an attendee from `checked_in` to `checked_in` again.


### Attendee State Transition Experiment

### [12:36] Attempting

After confirming the basic attendee representation, I created a separate experiment to implement and test the state-transition rules for the check-in process.

The goal was to prevent arbitrary changes to an attendee's state and establish the rules that will later support duplicate-scan protection and idempotent webhook handling.

### Tried

1. Created `solstice_pivot/attendee_state_transitions.py`.
2. Added the `print_job_id` field, initially set to `None`.
3. Added explicit transition methods:
   - `mark_pending()`
   - `mark_checked_in()`
   - `mark_failed()`
4. Restricted the transitions so that:
   - `not_checked_in` can move to `pending`.
   - `pending` can move to `checked_in`.
   - `pending` can move to `failed`.
   - Other transitions are rejected.
5. Tested the normal check-in path from `not_checked_in` to `pending` and then to `checked_in`.
6. Tested a duplicate check-in attempt after the attendee was already `checked_in`.

### Result

The experiment produced:

```text
Initial: Attendee(id=A001, name=Alice, status=not_checked_in, print_job_id=None)
Mark pending: True
After pending: Attendee(id=A001, name=Alice, status=pending, print_job_id=JOB-A001)
Mark checked in: True
After checked in: Attendee(id=A001, name=Alice, status=checked_in, print_job_id=JOB-A001)
Duplicate check-in: False
Final: Attendee(id=A001, name=Alice, status=checked_in, print_job_id=JOB-A001)
```

The valid transitions returned `True`, while the duplicate transition returned `False`.

This confirmed that the state-transition methods enforce the intended workflow rather than allowing an attendee to be checked in repeatedly.

The `print_job_id` is also stored when the attendee enters the `pending` state. This will later allow the webhook handler to identify the correct print job and attendee without relying on the order in which webhook confirmations arrive.

Note: `mark_failed()` was implemented but not exercised in this experiment. It will be tested separately once the queue-publish failure path is built.

### What I learned

State transitions should be controlled by explicit rules rather than allowing every part of the application to modify the status directly.

This provides an important foundation for idempotency. If a webhook for an attendee who is already `checked_in` is received again, the transition method can reject it instead of processing the confirmation a second time.

### Next

Create a separate attendee registry experiment that can store multiple attendees and provide lookup by attendee ID and, later, by `print_job_id`. This will allow the check-in service and webhook handler to find the correct attendee without relying on scan or confirmation order.


### Attendee Registry Experiment

### [17:20] Attempting

After implementing the attendee state-transition rules, I created a separate registry experiment to determine how the sync service will keep track of multiple attendees and locate them when processing scan requests and webhook confirmations.

A key requirement is that webhook confirmations may arrive out of order. Therefore, the service cannot rely on the order in which attendees were scanned. It needs to identify the correct attendee using identifiers, particularly the `print_job_id` associated with a badge-print request.

### Tried

1. Created `solstice_pivot/attendee_registry.py`.
2. Created an `AttendeeRegistry` class with separate lookup dictionaries for:
   - attendee ID
   - print job ID
3. Added an `add()` method to register an attendee.
4. Added `get_by_id()` to find an attendee using their attendee ID.
5. Added `get_by_job_id()` to find an attendee using their print job ID.
6. Initially tested the registry using a simplified `Attendee` class defined locally inside the file.
7. While reviewing the experiment, I noticed that this created a second `Attendee` definition that was different from the actual `Attendee` class containing the state-transition logic.
8. Removed the duplicate test class and imported the existing `Attendee` class from `attendee_state_transitions.py`.
9. Created Alice and Bob using the actual attendee model and moved both into the `pending` state with their respective print job IDs.
10. Retested the registry using the actual attendee objects.
11. Also tested a lookup for an attendee that does not exist.

### Result

The corrected experiment produced:

```text
By attendee ID: Attendee(id=A001, name=Alice, status=pending, print_job_id=JOB-A001)
By print job ID: Attendee(id=A002, name=Bob, status=pending, print_job_id=JOB-B001)
Missing attendee: None
```

The registry successfully found Alice using her attendee ID and Bob using his print job ID. The lookup for a missing attendee correctly returned `None`.

The important correction was replacing the simplified local `Attendee` class with the existing `Attendee` model from `attendee_state_transitions.py`. This means the registry has now been tested against the same attendee object that will be used by the rest of the service.

The print-job lookup is particularly important for webhook processing. A webhook can contain `JOB-B001`, for example, and the service can use that identifier to locate Bob directly rather than assuming that Bob's confirmation will arrive after Alice's.

### What I learned

The registry separates attendee storage and lookup from the attendee's own state-transition logic.

I also learned the importance of avoiding duplicate model definitions when building a multi-file application. The first registry test used a simplified stand-in `Attendee` class, which could have caused confusion once other parts of the service started importing and modifying the real attendee model.

Using one shared `Attendee` definition keeps the state-transition rules and registry lookups working with the same object.

The registry therefore has a focused responsibility: it knows how to find attendees, while the `Attendee` class knows how an attendee's state is allowed to change.

### Next

Create `check_in_service.py`.

The check-in service will use the shared `Attendee` model and `AttendeeRegistry` to process scans. It will check the attendee's current state, reject duplicate scans, generate a unique `print_job_id`, move the attendee to `pending`, and prepare the print request for the message queue.


### Check-In Service Experiment

### [17:55] Attempting

After completing the attendee state and registry experiments, I created the check-in service to implement the first actual workflow of the Solstice Events check-in system.

The goal was to process an attendee scan while enforcing the state rules already established. A valid first scan should move an attendee from `not_checked_in` to `pending`, generate a `print_job_id`, and prepare the attendee for the badge-printing process. A duplicate scan should be rejected rather than creating another print job.

The queue was intentionally kept out of this experiment. The purpose here was to prove the check-in decision logic independently before introducing message publishing and retry behavior.

### Tried

1. Created `solstice_pivot/check_in_service.py`.
2. Reused the existing `Attendee` model from `attendee_state_transitions.py`.
3. Reused the existing `AttendeeRegistry`.
4. Created a `CheckInService` responsible for processing attendee scans.
5. Looked up the attendee by `attendee_id`.
6. Rejected the request when the attendee could not be found.
7. Checked the attendee's current state before creating a print job.
8. Generated a `print_job_id` for a valid first scan.
9. Used `mark_pending()` to transition the attendee from `not_checked_in` to `pending`, then re-registered the attendee in the registry so the newly assigned `print_job_id` gets indexed for lookup (the registry only indexes by job ID once one exists on the attendee).
10. Tested:
    - a valid first scan,
    - a duplicate scan,
    - an unknown attendee.

### Result

The experiment produced:

```text
Alice first scan:
{'success': True, 'attendee_id': 'A001', 'print_job_id': 'JOB-A001', 'status': 'pending'}

Alice duplicate scan:
{'success': False, 'message': 'Attendee already pending'}

Unknown attendee:
{'success': False, 'message': 'Attendee not found'}
```

The first scan was accepted and moved Alice into the `pending` state with the print job ID `JOB-A001`.

A second scan for the same attendee was rejected because Alice was already `pending`. This prevents the service from creating another print request while the first badge-print operation is still awaiting confirmation.

An unknown attendee was also rejected rather than creating a print job for an attendee that does not exist in the registry.

### What I learned

The check-in service acts as the decision-making layer between an incoming scan and the downstream printing process.

The attendee's state must be checked before a print job is created. This provides an early duplicate-scan protection mechanism and ensures that the same attendee does not enter the printing workflow multiple times while their existing request is still pending.

The service also reuses the existing attendee model and registry rather than introducing duplicate state or lookup logic. It does rely on calling `registry.add()` a second time after `mark_pending()`, since that is what causes the print-job-ID index to be populated once the ID exists.

### Next

Create `print_queue.py`.

The next experiment will simulate publishing the generated print job to a message queue. It will distinguish between retryable failures, such as temporary network or broker failures, and permanent failures that should not be blindly retried.

Retry and exponential backoff logic will be reused from the previously tested prototype rather than unnecessarily rebuilt.

### Print Queue Experiment

### [18:48] Attempting

After completing the check-in service, I created an experiment to simulate the vendor's message queue and the queue-publish step that happens after an attendee is marked `pending`. The goal was to reproduce a transient publish failure with retry/backoff, and separately confirm that a permanent failure is not retried.

### Tried

1. Created `solstice_pivot/print_queue.py`.
2. Defined two exception types: `TemporaryQueueError` and `PermanentQueueError`.
3. Created a `PrintQueue` class whose `publish()` method fails on the first two attempts with `TemporaryQueueError`, then succeeds on the third.
4. My first version of the retry loop had two gaps: it retried with no delay between attempts, and it never actually triggered `PermanentQueueError`, so that path was unverified. I revised the file to fix both.
5. Added `retry_with_backoff(operation, max_retries=2, base_delay=1)`, a generic retry function taking any callable, using the same exponential formula (`base_delay * 2 ** attempt`) and `time.sleep()` proven in the Assignment 1 retry/backoff prototype.
6. Ran two separate tests in `__main__`: one wrapping `queue.publish(print_job)` to prove the transient-failure/retry path, and a second calling a function that always raises `PermanentQueueError` immediately, to prove the non-retryable path.

### Result

```text
=== Temporary failure test ===
Queue publish attempt 1
Retryable failure: Temporary message broker failure
Waiting 1 seconds before retrying...
Queue publish attempt 2
Retryable failure: Temporary message broker failure
Waiting 2 seconds before retrying...
Queue publish attempt 3
Print job published: {'print_job_id': 'JOB-A001', 'attendee_id': 'A001', 'name': 'Alice'}
Publish successful: True

=== Permanent failure test ===
Permanent failure: Permanent message broker configuration failure
Permanent failure handled without retry
```

The temporary-failure test retried twice with the expected 1s and 2s delays, then succeeded on the third attempt. The permanent-failure test failed immediately with no retry and no delay, confirming `retry_with_backoff()` correctly distinguishes retryable from non-retryable errors.

### What I learned

Retry/backoff logic needs to explicitly separate what should be retried from what shouldn't — the exception type is what drives that branch, not a blanket try/except. Generalizing the retry loop into a function that takes any operation (rather than one hardcoded to a specific call) made it reusable for the queue-publish case without duplicating the loop structure itself.

### Next

Create `webhook_handler.py`.

The webhook handler will receive the print-completion callback, verify its signature, locate the attendee using the `print_job_id`, and safely transition the attendee from `pending` to `checked_in`.

It will also test duplicate webhook delivery and out-of-order confirmation handling so that the same print confirmation cannot incorrectly process an attendee more than once.

After the webhook handler is complete, the final `pivot_demo.py` will connect the full flow:

scan → queue publish → retry/backoff → webhook → checked_in.