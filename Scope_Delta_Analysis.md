# Scope Delta Analysis — The Meridian Pivot

## Original Spec
An event check-in kiosk for Solstice Events Co. When staff scan an attendee's QR code, the service calls a badge-printer vendor **synchronously** via REST, waits for the print result, and shows "Checked In" only once printing succeeds. Duplicate scans of an already-checked-in attendee must be rejected.

## The Pivot
The vendor announced, with no extension possible, that the synchronous print API was being deprecated. The service had to switch to an **asynchronous** model: publish the print request to the vendor's message queue, then wait for a webhook callback confirming completion. The UI shows a pending state in the meantime. Because confirmations are asynchronous, they can **arrive out of order** relative to when attendees scanned.

## Dropped
- Direct synchronous REST call to the printer vendor.
- The assumption that a print result is available immediately after a scan.
- The assumption that confirmations arrive in the same order attendees scanned.

## Modified
- **Duplicate-scan protection** — originally could be checked with a simple "already checked in?" flag at scan time; now requires an explicit state machine (`not_checked_in / pending / checked_in / failed`) because an attendee can be scanned but not yet confirmed, and a second scan during that window must still be rejected.
- **Attendee lookup** — originally didn't need a secondary index; now requires lookup by `print_job_id` in addition to `attendee_id`, since the webhook only carries the job ID, not necessarily who scanned first.
- **Success confirmation** — moved from an inline return value (call succeeds → show "Checked In") to a separate, later event (webhook received → show "Checked In"), decoupling the scan action from the confirmation.

## Added
- **`print_queue.py`** — simulates the vendor's message queue, including a distinction between retryable failures (temporary broker/network issues) and permanent ones (invalid payload, auth failure) that should not be retried.
- **`retry_with_backoff()`** — reused directly from the Assignment 1 retry/backoff prototype, applied here to the queue-publish step, since that's the new operation that can fail transiently.
- **`webhook_handler.py`** — a new inbound endpoint responsibility that didn't exist in the synchronous version at all; verifies the callback's authenticity via the same HMAC pattern proven in Assignment 1.
- **Idempotency handling** — the webhook handler must recognize and safely ignore a repeated confirmation for an already-checked-in attendee, since at-least-once delivery is a standard assumption for webhooks/message queues.
- **A `failed` state** — added so an attendee whose print job permanently fails to publish isn't left stuck in `pending` indefinitely with no path forward.

## Regression Check
Duplicate-scan protection, the core requirement from the original spec, still holds under the new async model — verified in `pivot_demo.py` by confirming a second scan of the same attendee while `pending` is rejected, and confirming a duplicate webhook confirmation is recognized rather than reapplied. Nothing from the original protection was lost in the pivot; it was extended to also cover the new pending window and asynchronous, out-of-order confirmations.

## What the Pivot Cost
The pivot added: one new state (`failed`), one new file class (`print_queue.py`, message-queue simulation), one new inbound integration (`webhook_handler.py`), and a secondary lookup index (`print_job_id → attendee`) that the synchronous design never needed. The retry/backoff logic itself did not need to be rebuilt — it was reused directly from Assignment 1, which kept the cost of the pivot smaller than it would have been building retry logic from scratch under deadline pressure.