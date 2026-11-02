"""나만의 퀴즈 게임 프로그램 진입점."""

from game import QuizGame


def main() -> None:
    """QuizGame 인스턴스를 생성하고 실행한다."""
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
