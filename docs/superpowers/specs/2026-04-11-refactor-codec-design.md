# Refactor: codec.py — redundant payload length check

## Scope

Single finding in `src/imstr/codec.py` from the `/refactor` diagnosis on 2026-04-11. Targeted scope, main-agent diagnosis (single-module project).

## Context summary

Sources read:
- `src/imstr/codec.py` (53 lines, the entire runtime module)
- `src/imstr/__init__.py` (re-exports only)
- `tests/test_codec.py` (9 tests, covers round-trip + error paths)
- `CLAUDE.md`, `README.md`, `pyproject.toml`
- `git log` (recent history — rename + API simplification)

No discrepancies between signals. Codebase is small and healthy; this spec covers the only finding worth acting on. `F-02` (duplicated try/except wrapping) was explicitly skipped as premature abstraction.

## Finding

### F-01: `len(payload) < 2` check is redundant

- **Location**: `src/imstr/codec.py:36-37`
- **Category**: `logic`
- **Observation**: `decode` performs `if len(payload) < 2: raise ValueError("payload is too short")` immediately after base64 decoding, then splits `prefix = payload[:1]` / `webp_data = payload[1:]` and validates `prefix in (b"L", b"C")`.
- **Reconstruction attempt**: "This check exists to prevent IndexError or meaningless state on too-short payloads before slicing."
- **Failure point**: Python's `bytes[:1]` and `bytes[1:]` do not raise IndexError on short inputs — they return empty bytes. Length-0 and length-1 payloads are already caught by either (a) the prefix validation rejecting `b""` or an unknown byte, or (b) the valid-prefix + empty-webp case failing inside `Image.open`. Both paths yield the same user-visible `ValueError("failed to deserialize array: ...")`. The check enforces no unique invariant.
- **Suggested direction**: Delete lines 36-37. Two lines removed; no behavioral change for any input.
- **Axes**: Impact: low, Confidence: high, Effort: S
- **Verification**: In an isolated git worktree, the two lines were removed and `pytest tests/test_codec.py` reported `9 passed in 0.23s`. Manual trace of 1-byte payloads:
  - `b""` → `ValueError: invalid payload prefix`
  - `b"L"` / `b"C"` → `ValueError: failed to deserialize array: cannot identify image file ...`
  - `b"X"` → `ValueError: invalid payload prefix`
  All still raise `ValueError` via existing guards.

## Refactoring constraints

- All 9 existing tests in `tests/test_codec.py` must continue to pass.
- Public API (`encode`, `decode` signatures and behavior) must remain stable.
- All error paths must still raise `ValueError` — no new exception types leaking out.
- No other changes in scope. Do not touch `F-02` or any other code.

## Success criteria

- Lines 36-37 of `src/imstr/codec.py` are removed.
- `pytest` reports all tests passing.
- A fresh Feynman reconstruction of the `decode` function no longer encounters the "this check enforces nothing unique" failure point — every remaining line in `decode` maps to a distinct, justifiable invariant.
