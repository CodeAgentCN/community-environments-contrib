import re
from typing import Optional

import verifiers as vf
from datasets import Dataset, load_dataset
from verifiers.parsers.parser import Parser
from verifiers.types import Messages


class MATHParser(Parser):
    _BOXED = re.compile(r"\\\\boxed\{([^}]+)\}", re.IGNORECASE)
    _FINAL = re.compile(r"(?:the answer is|answer|final answer is|so the answer is)\s*:?\s*(.+?)$", re.IGNORECASE | re.MULTILINE)

    def parse(self, text: str) -> Optional[str]:
        if not text:
            return None
        text = text.strip()
        text = re.sub(r"[\\*_`]+", "", text)
        if m := self._BOXED.search(text):
            return m.group(1).strip()
        if m := self._FINAL.search(text):
            return m.group(1).strip()
        return None

    def parse_answer(self, completion: Messages) -> Optional[str]:
        content = completion[-1]["content"] if isinstance(completion, list) else completion
        return self.parse(content)


def normalize_answer(ans: str) -> str:
    """Normalize math answer for comparison."""
    ans = ans.strip()
    # Remove LaTeX wrappers
    ans = re.sub(r"\\\\[a-zA-Z]+", "", ans)
    ans = re.sub(r"[{}\\]", "", ans)
    ans = ans.strip()
    return ans


_GOLD_BOXED = re.compile(r"\\\\boxed\{([^}]+)\}", re.IGNORECASE)


def load_environment(split: str = "test", level: Optional[str] = None, subject: Optional[str] = None, **kwargs) -> vf.Environment:
    valid_splits = ["test", "train", "validation"]
    if split not in valid_splits:
        raise ValueError(f"Invalid split '{split}'. Must be one of {valid_splits}")

    def generator():
        raw = load_dataset("competition_math", split=split)
        for ex in raw:
            problem = ex["problem"]
            solution = ex["solution"]
            gold_match = _GOLD_BOXED.search(solution)
            answer = gold_match.group(1).strip() if gold_match else solution.strip()

            item_level = ex.get("level", "")
            item_subject = ex.get("type", "")

            if level is not None and item_level != level:
                continue
            if subject is not None and item_subject != subject:
                continue

            yield {
                "prompt": [
                    {
                        "role": "system",
                        "content": "Solve the competition-level math problem step by step. Put your final answer in \\boxed{}.",
                    },
                    {"role": "user", "content": problem},
                ],
                "answer": answer,
                "level": item_level,
                "type": item_subject,
            }

    def exact_match(parser: vf.Parser, completion: vf.Messages, answer: str, **_):
        parsed = parser.parse_answer(completion)
        if parsed is None:
            return 0.0
        return 1.0 if normalize_answer(parsed) == normalize_answer(answer) else 0.0

    dataset = Dataset.from_generator(generator)
    parser = MATHParser()
    rubric = vf.Rubric(parser=parser)
    rubric.add_reward_func(exact_match)

    return vf.SingleTurnEnv(eval_dataset=dataset, parser=parser, rubric=rubric, **kwargs)
