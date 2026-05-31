# tests

Retrieval-quality harness for the two local RAG engines. The root [README](../README.md) reports the final research results; this file documents how to run and extend the harness.

## Build Indexes First

```powershell
python sqlite-rag/rag_index.py --db sqlite-rag/rag_index.h.db --model BAAI/bge-small-en-v1.5 --chunking legacy --rebuild
python lance-db-rag/rag_index.py --db lance-db-rag/index.h.lance --variant small --chunking legacy --rebuild
```

## Labeled Evaluation

```powershell
python tests/evaluate.py --variant small_h --mode hybrid
```

Useful options:

| Option | Meaning |
|---|---|
| `--variant small_h` | Final heading-aware BGE-small indexes |
| `--mode hybrid\|semantic\|keyword` | Retrieval mode |
| `--engine sqlite\|lance\|both` | Engine selection |
| `--top-k` | Result depth for scoring |
| `--bm25-heading-weight` | SQLite heading BM25 weight; final value is `1.0` |

The evaluator reads [`cases.jsonl`](cases.jsonl), runs each query through each engine, and reports:

- file MRR and chunk MRR
- file-match and chunk-match at `@1`, `@3`, and `@8`
- per-case file/chunk rank
- median latency after model warmup

## Case Format

```json
{
  "id": "arm-median-calibration",
  "query": "How do I calibrate the median of the robotic arm servos?",
  "expected_file": "0.Configuration and Operation Guide/3. Robotic Arm Calibration/3. Robotic Arm Calibration.md",
  "expected_heading_substring": "Calibrate the median"
}
```

`expected_file` is a substring match under `markdown/`. `expected_heading_substring` is a case-insensitive substring match against the returned `heading_path`.

## Subjective Noob Review

```powershell
python tests/ask.py --variant small_h --mode hybrid --file tests/noob_questions.txt
python tests/ask.py --variant small_h --mode hybrid "How do I make the robot map a room?"
```

[`noob_questions.txt`](noob_questions.txt) contains 30 beginner-style questions. These are not scored labels; they are used to inspect top-3 usefulness and catch failures that file-level metrics can hide.

## Files

```text
tests/
|-- cases.jsonl          # labeled query -> expected file/heading cases
|-- noob_questions.txt   # unlabeled beginner questions
|-- runner.py            # importlib loader for both engines
|-- evaluate.py          # labeled scoring report
`-- ask.py               # side-by-side unscored query display
```
