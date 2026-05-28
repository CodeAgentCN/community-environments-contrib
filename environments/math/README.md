# math

### Overview
- **Environment ID**: `math`
- **Short description**: MATH (Mathematics Aptitude Test of Heuristics) benchmark for competition-level math problems.
- **Tags**: math, reasoning, competition, single-turn

### Datasets
- **Primary dataset(s)**: competition_math (MATH benchmark)
- **Source links**: [Huggingface](https://huggingface.co/datasets/competition_math)
- **Split sizes**:
    - train: 7500
    - test: 5000

### Task
- **Type**: single-turn
- **Parser**: MATHParser
- **Rubric overview**: exact match on final boxed answer

### Quickstart
```bash
uv run vf-eval math
```

### Environment Arguments

| Arg | Type | Default | Description |
| --- | ---- | ------- | ----------- |
| `split` | str | `"test"` | Split to evaluate (test/train/validation) |
| `level` | str | `None` | Filter by difficulty level (1-5) |
| `subject` | str | `None` | Filter by subject type |

### Metrics

| Metric | Meaning |
| ------ | ------- |
| `reward` | Binary reward indicating correct (1) or incorrect (0) answer |
| `exact_match` | Exact match on normalized answer |
