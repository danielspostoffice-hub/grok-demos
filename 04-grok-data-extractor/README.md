\# 04 - Grok Data Extractor



Baseline pipeline on exported Grok chat data.



\## Why

Escalates 03: File system traversal, JSON parsing, basic stats (convos, messages, dates). Real data tooling - trends toward log analysis/token usage/patterns xAI engineers do daily.



\## Setup

\- Fix EXPORT\_ROOT in extractor.py to your exact export path.

\- python extractor.py



Outputs:

\- JSON count

\- Sample convo preview

\- Stats on sample convos



Next: Full CSV export, token counts, user vs assistant split.

