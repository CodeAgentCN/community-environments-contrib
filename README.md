# community-environments-contrib

Community environment contributions for the [PrimeIntellect verifiers](https://github.com/PrimeIntellect-ai/verifiers) framework.

This repo provides `SingleTurnEnv` environments for popular AI evaluation benchmarks, following the [community-environments](https://github.com/PrimeIntellect-ai/community-environments) conventions.

## Environments

| Environment | Description | Dataset | Split(s) |
|------------|-------------|---------|----------|
| `gsm8k` | Grade School Math 8K - math word problems | [gsm8k](https://huggingface.co/datasets/gsm8k) | test, train |
| `gpqa` | Graduate-Level Question Answering - science MCQs | [gpqa](https://huggingface.co/datasets/Idavidrein/gpqa) | gpqa_main, gpqa_diamond, gpqa_extended, gpqa_experts, gpqa_novel, gpqa_main_nori |

## Usage

```bash
# Install and run
uv run vf-eval gsm8k
uv run vf-eval gpqa

# With custom config
uv run vf-eval gpqa -m gpt-4.1-mini -n 20 -a '{"split": "gpqa_diamond"}'
```

## Adding New Environments

Each environment follows the `environments/<name>/` layout:
- `<name>.py` - implements `load_environment(...)` returning a `vf.SingleTurnEnv`
- `README.md` - documentation with args, metrics, quickstart
- `pyproject.toml` - package dependencies (requires `verifiers>=0.1.10`, `datasets>=4.4.1`)
