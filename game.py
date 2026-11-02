"""퀴즈 게임 전체 흐름과 메뉴/입출력을 관리하는 QuizGame 클래스 모듈."""

from pathlib import Path
from typing import Any

from quiz import Quiz
from storage import DEFAULT_STATE_PATH, StateStorage


class QuizGame:
    """퀴즈 게임의 상태(퀴즈 목록, 최고 점수, 기록)와 기능을 제어하는 클래스."""

    def __init__(self, state_path: Path | str = DEFAULT_STATE_PATH) -> None:
        self.storage = StateStorage(state_path)
        self.quizzes: list[Quiz] = []
        self.best_score: int | None = None
        self.best_detail: dict[str, int] | None = None
        self.history: list[dict[str, Any]] = []

    def load_state(self) -> None:
        """저장소에서 퀴즈 및 점수 데이터를 불러온다."""
        (
            self.quizzes,
            self.best_score,
            self.best_detail,
            self.history,
        ) = self.storage.load()

    def save_state(self) -> bool:
        """현재 퀴즈 및 점수 데이터를 저장소에 기록한다."""
        return self.storage.save(
            quizzes=self.quizzes,
            best_score=self.best_score,
            best_detail=self.best_detail,
            history=self.history,
        )

    @staticmethod
    def get_valid_int(
        prompt: str,
        min_val: int,
        max_val: int,
        allow_default: int | None = None,
    ) -> int:
        """공통 숫자 입력 검증 메서드.

        - 앞뒤 공백 제거
        - 빈 입력, 숫자 변환 실패, 범위 밖 숫자 입력 시 안내 메시지 출력 후 재입력
        """
        while True:
            raw = input(prompt).strip()
            if not raw:
                if allow_default is not None:
                    return allow_default
                print(
                    f"⚠️ 입력이 비어 있습니다. {min_val}~{max_val} 사이의 숫자를 입력하세요."
                )
                continue

            try:
                value = int(raw)
            except ValueError:
                print(
                    f"⚠️ 잘못된 입력입니다. {min_val}~{max_val} 사이의 숫자를 입력하세요."
                )
                continue

            if not min_val <= value <= max_val:
                print(
                    f"⚠️ 허용 범위를 벗어났습니다. {min_val}~{max_val} 사이의 숫자를 입력하세요."
                )
                continue

            return value

    @staticmethod
    def get_non_empty_str(prompt: str, allow_empty: bool = False) -> str:
        """공백을 제거한 문자열을 입력받으며, 빈 문자열일 경우 재입력을 요청한다."""
        while True:
            text = input(prompt).strip()
            if text or allow_empty:
                return text
            print("⚠️ 내용을 비워둘 수 없습니다. 다시 입력해주세요.")

    def display_menu(self) -> None:
        """메인 메뉴 화면을 출력한다."""
        print("\n========================================")
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("========================================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("6. 퀴즈 삭제 (보너스)")
        print("========================================")

    def play_quiz(self) -> None:
        """퀴즈 풀기 기능 (추후 브랜치에서 구현)."""
        print("\n준비 중인 기능입니다.")

    def add_quiz(self) -> None:
        """퀴즈 추가 기능."""
        print("\n준비 중인 기능입니다.")

    def list_quizzes(self) -> None:
        """퀴즈 목록 조회 기능."""
        print("\n준비 중인 기능입니다.")

    def show_scores(self) -> None:
        """점수 및 히스토리 확인 기능."""
        print("\n준비 중인 기능입니다.")

    def delete_quiz(self) -> None:
        """등록된 퀴즈 삭제 기능."""
        print("\n준비 중인 기능입니다.")

    def run(self) -> None:
        """게임 메인 루프를 실행한다."""
        print("========================================")
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("========================================")
        self.load_state()

        try:
            while True:
                self.display_menu()
                choice = self.get_valid_int("선택: ", 1, 6)

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_scores()
                elif choice == 5:
                    self.save_state()
                    print("\n👋 게임을 종료합니다. 플레이해 주셔서 감사합니다!")
                    break
                elif choice == 6:
                    self.delete_quiz()
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 프로그램 종료 신호(Ctrl+C / EOF)가 감지되었습니다.")
            self.save_state()
            print("💾 현재 데이터를 안전하게 저장하고 종료합니다. 감사합니다!")
