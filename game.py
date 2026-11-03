"""퀴즈 게임 전체 흐름과 메뉴/입출력을 관리하는 QuizGame 클래스 모듈."""

from datetime import datetime
from pathlib import Path
import random
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
        """저장된 퀴즈를 랜덤 순서로 출제하고 점수를 계산한다."""
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다. 먼저 '2. 퀴즈 추가'에서 문제를 등록해주세요.")
            return

        total_available = len(self.quizzes)
        print(f"\n📌 현재 등록된 퀴즈는 총 {total_available}문제입니다.")
        question_count = self.get_valid_int(
            f"출제할 문제 수를 입력하세요 (1~{total_available}, Enter 입력 시 전체 {total_available}문제): ",
            min_val=1,
            max_val=total_available,
            allow_default=total_available,
        )

        selected_quizzes = random.sample(self.quizzes, question_count)
        print(f"\n📝 퀴즈를 시작합니다! (총 {question_count}문제 / 랜덤 출제)")
        print("💡 풀이 중 '0'을 입력하면 힌트를 볼 수 있습니다. (힌트 사용 시 5점 차감)")

        correct_count = 0
        hints_used = 0

        for idx, quiz in enumerate(selected_quizzes, start=1):
            print("\n----------------------------------------")
            quiz.display(index=idx)
            used_hint_for_this = False

            while True:
                prompt_msg = (
                    "정답 입력 (1~4, 힌트 보기: 0): "
                    if quiz.hint and not used_hint_for_this
                    else "정답 입력 (1~4): "
                )
                min_allowed = 0 if (quiz.hint and not used_hint_for_this) else 1
                user_ans = self.get_valid_int(prompt_msg, min_allowed, 4)

                if user_ans == 0:
                    used_hint_for_this = True
                    hints_used += 1
                    print(f"💡 [힌트] {quiz.hint} (-5점)")
                    continue
                break

            if quiz.check_answer(user_ans):
                correct_count += 1
                print("✅ 정답입니다!")
            else:
                correct_text = quiz.choices[quiz.answer - 1]
                print(f"❌ 오답입니다! (정답: {quiz.answer}번 - {correct_text})")

        raw_score = round((correct_count / question_count) * 100)
        penalty = hints_used * 5
        final_score = max(0, raw_score - penalty)

        print("\n========================================")
        if hints_used > 0:
            print(
                f"🏆 결과: {question_count}문제 중 {correct_count}문제 정답! "
                f"(기본 {raw_score}점 - 힌트 {hints_used}회({penalty}점) = 최종 {final_score}점)"
            )
        else:
            print(
                f"🏆 결과: {question_count}문제 중 {correct_count}문제 정답! ({final_score}점)"
            )

        is_new_best = self.best_score is None or final_score > self.best_score
        if is_new_best:
            self.best_score = final_score
            self.best_detail = {
                "correct": correct_count,
                "total": question_count,
            }
            print("🎉 새로운 최고 점수입니다!")

        self.history.append(
            {
                "played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total": question_count,
                "correct": correct_count,
                "hints_used": hints_used,
                "score": final_score,
            }
        )
        self.save_state()
        print("========================================")

    def add_quiz(self) -> None:
        """사용자로부터 문제, 선택지 4개, 정답 번호, 힌트를 입력받아 새 퀴즈를 등록한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = self.get_non_empty_str("문제를 입력하세요: ")

        choices: list[str] = []
        for idx in range(1, 5):
            choice_text = self.get_non_empty_str(f"선택지 {idx}: ")
            choices.append(choice_text)

        answer = self.get_valid_int("정답 번호 (1-4): ", 1, 4)
        hint = self.get_non_empty_str("힌트 (선택사항, 없으면 Enter): ", allow_empty=True)

        new_quiz = Quiz(
            question=question,
            choices=choices,
            answer=answer,
            hint=hint,
        )
        self.quizzes.append(new_quiz)
        self.save_state()
        print("\n✅ 퀴즈가 추가되었습니다!")

    def list_quizzes(self) -> None:
        """등록된 전체 퀴즈 목록을 출력한다."""
        if not self.quizzes:
            print("\n⚠️ 현재 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("----------------------------------------")
        for idx, quiz in enumerate(self.quizzes, start=1):
            hint_badge = " [💡힌트 있음]" if quiz.hint else ""
            print(f"[{idx}] {quiz.question}{hint_badge}")
        print("----------------------------------------")

    def show_scores(self) -> None:
        """최고 점수와 전체 플레이 기록 히스토리를 출력한다."""
        if self.best_score is None and not self.history:
            print("\n📊 아직 플레이한 기록이 없습니다. 먼저 '1. 퀴즈 풀기'에 도전해보세요!")
            return

        print("\n========================================")
        if self.best_detail and "total" in self.best_detail and "correct" in self.best_detail:
            print(
                f"🏆 최고 점수: {self.best_score}점 "
                f"({self.best_detail['total']}문제 중 {self.best_detail['correct']}문제 정답)"
            )
        else:
            print(f"🏆 최고 점수: {self.best_score}점")

        if self.history:
            print("\n📜 최근 플레이 기록 히스토리:")
            print("----------------------------------------")
            for idx, record in enumerate(self.history, start=1):
                played_at = record.get("played_at", "-")
                total = record.get("total", 0)
                correct = record.get("correct", 0)
                hints_used = record.get("hints_used", 0)
                score = record.get("score", 0)
                hint_info = f", 힌트 {hints_used}회" if hints_used else ""
                print(
                    f"  {idx}. [{played_at}] {total}문제 중 {correct}문제 정답 "
                    f"({score}점{hint_info})"
                )
            print("----------------------------------------")
        print("========================================")

    def delete_quiz(self) -> None:
        """등록된 퀴즈 목록을 보여주고 선택한 번호의 퀴즈를 삭제한다."""
        if not self.quizzes:
            print("\n⚠️ 삭제할 수 있는 퀴즈가 없습니다.")
            return

        self.list_quizzes()
        target_idx = self.get_valid_int(
            f"삭제할 퀴즈 번호를 입력하세요 (1~{len(self.quizzes)}, 취소: 0): ",
            min_val=0,
            max_val=len(self.quizzes),
        )
        if target_idx == 0:
            print("↩️ 퀴즈 삭제를 취소했습니다.")
            return

        removed = self.quizzes.pop(target_idx - 1)
        self.save_state()
        print(f"\n🗑️ [{target_idx}] '{removed.question}' 퀴즈가 삭제되었습니다.")

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
