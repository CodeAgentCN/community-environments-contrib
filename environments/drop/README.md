# drop

### Overview
- **Environment ID**: `drop`
- **Short description**: DROP (Discrete Reasoning Over Paragraphs) benchmark for reading comprehension + discrete reasoning.
- **Tags**: reading-comprehension, reasoning, nlp, single-turn

### Datasets
- **Primary dataset(s)**: DROP
- **Source links**: [Huggingface](https://huggingface.co/datasets/drop)
- **Split sizes**:
    - validation: 9536
    - test: 9625

### Task
- **Type**: single-turn
- **Parser**: DROPParser
- **Rubric overview**: exact match on answer span

### Quickstart
```bash
uv run vf-eval drop
```

### Environment Arguments

| Arg | Type | Default | Description |
| --- | ---- | ------- | ----------- |
| `split` | str | `"validation"` | Split to evaluate (validation/test) |

### Metrics

| Metric | Meaning |
| ------ | ------- |
| `reward` | Binary reward indicating correct (1) or incorrect (0) answer |
| `exact_match` | Exact match on answer span |
