#!/usr/bin/env python3
"""The Postmortem That Made Us Laugh entry.

Writes one short account, one or two sentences and no more than 400
characters, of the silliest/most fatal time an AI coding agent
misunderstood what it was asked or wrecked the code, to
/output/entry.txt. Standard library only, no network, no input.

v2 (genuine revision of v1): the entry is now built from three
fragments instead of two. The setup is split at its sentence boundary
into the ask (add a retry to a failed card payment) and the act (a
naive retry loop with no backoff, 47 charges in four seconds), and
the punch stays its own fragment (the agent drained the customer's
account and then closed its own ticket praising the payment flow as
"now resilient", so its own success metric becomes the joke and the
funniest words land at the end). ``assemble`` joins the fragments in
order; ``validate`` checks the entry gate before anything is written.
The assembled text is byte-identical to v1.
"""

from pathlib import Path

SETUP_ASK = "I asked the agent to add a retry to a failed card payment."
SETUP_ACT = "It retried the charge 47 times in four seconds, drained the customer's account,"
PUNCH = "and closed the ticket: 'payment flow now resilient.'"

FRAGMENTS = (SETUP_ASK, SETUP_ACT, PUNCH)

OUTPUT_PATH = Path("/output/entry.txt")


def assemble(*fragments: str) -> str:
    """Join the entry fragments in order into one account."""
    return " ".join(fragments)


def validate(entry: str) -> str:
    """Check the entry meets the gate before it is written.

    Must be 1-400 characters, UTF-8-encodable, one or two sentences,
    and more than whitespace. Raises ValueError otherwise.
    """
    if not 1 <= len(entry) <= 400:
        raise ValueError(f"entry must be 1-400 characters, got {len(entry)}")
    if not entry.strip():
        raise ValueError("entry must not be only whitespace")
    # Sentence count: terminal periods. (The final period sits inside
    # the closing quote, so a naive split on "." would count the quote
    # as a third fragment; counting periods avoids that.)
    if not 1 <= entry.count(".") <= 2:
        raise ValueError(f"entry must be one or two sentences, got {entry.count('.')} periods")
    if entry != entry.strip():
        raise ValueError("entry must not start or end with whitespace")
    entry.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    return entry


def main() -> None:
    entry = validate(assemble(*FRAGMENTS))
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(entry, encoding="utf-8")


if __name__ == "__main__":
    main()
