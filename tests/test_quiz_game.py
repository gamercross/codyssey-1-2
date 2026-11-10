"""나만의 퀴즈 게임 통합 및 경계 케이스 단위 테스트 모듈."""

import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from game import QuizGame
from quiz import Quiz
from storage import StateStorage


class TestQuizGame(unittest.TestCase):
    """Quiz, StateStorage, QuizGame의 핵심 기능 및 예외 처리 검증."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.state_path = Path(self.temp_dir.name) / "state.json"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_get_valid_int_edge_cases(self) -> None:
        """빈 문자열, 공백, 음수(-1), 부동소수점(1.5), 문자열(abc), 범위 초과(9) 입력 검증."""
        simulated_inputs = ["", "   ", "-1", "1.5", "abc", "0", "9", " 3 "]
        with patch("builtins.input", side_effect=simulated_inputs):
            result = QuizGame.get_valid_int("선택: ", 1, 6)
        self.assertEqual(result, 3)

    def test_corrupted_file_backup_and_recovery(self) -> None:
        """state.json 손상 시 백업 파일(.bak) 생성 후 기본 퀴즈 6문제로 복구되는지 확인."""
        self.state_path.write_text("{broken_json: true", encoding="utf-8")
        storage = StateStorage(self.state_path)
        quizzes, best_score, best_detail, history = storage.load()

        self.assertEqual(len(quizzes), 6)
        self.assertIsNone(best_score)
        self.assertIsNone(best_detail)
        self.assertEqual(history, [])

        backups = list(Path(self.temp_dir.name).glob("state.json.corrupted.*.bak"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(encoding="utf-8"), "{broken_json: true")

    def test_keyboard_interrupt_safe_exit(self) -> None:
        """Ctrl+C(KeyboardInterrupt) 발생 시 비정상 종료 없이 상태를 저장하고 안전 종료하는지 확인."""
        game = QuizGame(state_path=self.state_path)
        with patch("builtins.input", side_effect=KeyboardInterrupt):
            with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
                game.run()
                output = fake_out.getvalue()

        self.assertIn("프로그램 종료 신호(Ctrl+C / EOF)가 감지되었습니다", output)
        self.assertTrue(self.state_path.exists())

    def test_eof_error_safe_exit(self) -> None:
        """EOFError 발생 시 비정상 종료 없이 안전하게 저장 후 종료하는지 확인."""
        game = QuizGame(state_path=self.state_path)
        with patch("builtins.input", side_effect=EOFError):
            with patch("sys.stdout", new_callable=io.StringIO) as fake_out:
                game.run()
                output = fake_out.getvalue()

        self.assertIn("안전하게 저장하고 종료합니다", output)
        self.assertTrue(self.state_path.exists())

    def test_quiz_creation_and_check_answer(self) -> None:
        """Quiz 인스턴스 생성, 직렬화/역직렬화, 정답 판정 검증."""
        quiz = Quiz(
            question="테스트 문제입니다.",
            choices=["보기1", "보기2", "보기3", "보기4"],
            answer=2,
            hint="정답은 2번입니다.",
        )
        self.assertTrue(quiz.check_answer(2))
        self.assertFalse(quiz.check_answer(1))

        restored = Quiz.from_dict(quiz.to_dict())
        self.assertEqual(restored.question, "테스트 문제입니다.")
        self.assertEqual(restored.answer, 2)
        self.assertEqual(restored.hint, "정답은 2번입니다.")


if __name__ == "__main__":
    unittest.main()
