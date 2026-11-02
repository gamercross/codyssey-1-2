"""개별 퀴즈 문제를 표현하는 Quiz 클래스 모듈."""

from typing import Any


class Quiz:
    """퀴즈 문제, 4지선다 선택지, 정답 번호 및 힌트를 관리하는 클래스."""

    def __init__(
        self,
        question: str,
        choices: list[str],
        answer: int,
        hint: str = "",
    ) -> None:
        if len(choices) != 4:
            raise ValueError("선택지는 반드시 4개여야 합니다.")
        if not 1 <= answer <= 4:
            raise ValueError("정답 번호는 1~4 사이의 정수여야 합니다.")

        self.question: str = question.strip()
        self.choices: list[str] = [choice.strip() for choice in choices]
        self.answer: int = answer
        self.hint: str = hint.strip()

    def display(self, index: int | None = None) -> None:
        """문제를 화면에 출력한다."""
        if index is not None:
            print(f"[문제 {index}]")
        print(f"{self.question}\n")
        for idx, choice in enumerate(self.choices, start=1):
            print(f"  {idx}. {choice}")
        print()

    def check_answer(self, user_answer: int) -> bool:
        """사용자가 입력한 번호가 정답인지 확인한다."""
        return self.answer == user_answer

    def to_dict(self) -> dict[str, Any]:
        """JSON 직렬화를 위해 Quiz 객체를 딕셔너리로 변환한다."""
        data: dict[str, Any] = {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }
        if self.hint:
            data["hint"] = self.hint
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Quiz":
        """딕셔너리 데이터로부터 Quiz 인스턴스를 생성한다."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터 형식이 올바르지 않습니다.")

        question = data.get("question")
        choices = data.get("choices")
        answer = data.get("answer")
        hint = data.get("hint", "")

        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제(question)가 비어 있거나 문자열이 아닙니다.")
        if not isinstance(choices, list) or len(choices) != 4 or not all(
            isinstance(c, str) and c.strip() for c in choices
        ):
            raise ValueError("선택지(choices)는 비어 있지 않은 문자열 4개여야 합니다.")
        if isinstance(answer, bool) or not isinstance(answer, int) or not 1 <= answer <= 4:
            raise ValueError("정답(answer)은 1~4 사이의 정수여야 합니다.")
        if not isinstance(hint, str):
            hint = str(hint)

        return cls(
            question=question,
            choices=choices,
            answer=answer,
            hint=hint,
        )
