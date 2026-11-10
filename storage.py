"""state.json 파일 입출력, 원자적 저장, 재시도 및 손상 백업/복구를 담당하는 모듈."""

from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import time
from typing import Any

from default_data import get_default_quizzes
from quiz import Quiz

DEFAULT_STATE_PATH = Path(__file__).resolve().parent / "state.json"


class StateStorage:
    """퀴즈 목록, 최고 점수, 플레이 기록을 JSON 파일에 저장하고 불러오는 클래스."""

    def __init__(self, file_path: Path | str = DEFAULT_STATE_PATH, max_retries: int = 2) -> None:
        self.file_path: Path = Path(file_path)
        self.max_retries: int = max_retries

    def backup_corrupted_file(self) -> Path | None:
        """손상된 state.json 파일을 덮어쓰기 전에 타임스탬프 백업본으로 보존한다."""
        if not self.file_path.exists():
            return None
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.file_path.with_name(f"{self.file_path.name}.corrupted.{timestamp}.bak")
        try:
            shutil.copy2(self.file_path, backup_path)
            print(f"📦 [WARN] 손상된 기존 파일을 백업했습니다: {backup_path.name}")
            return backup_path
        except OSError as exc:
            print(f"⚠️ [ERROR] 손상된 파일 백업에 실패했습니다 ({exc}).")
            return None

    def load(self) -> tuple[list[Quiz], int | None, dict[str, int] | None, list[dict[str, Any]]]:
        """state.json에서 데이터를 불러온다.

        파일이 없거나 손상된 경우 안내 메시지를 출력하고 백업 후 기본 퀴즈 데이터로 초기화한다.
        """
        if not self.file_path.exists():
            quizzes = get_default_quizzes()
            print("📂 [INFO] 저장된 데이터 파일(state.json)이 없어 기본 퀴즈 데이터를 불러왔습니다.")
            self.save(quizzes, best_score=None, best_detail=None, history=[])
            return quizzes, None, None, []

        try:
            raw_text = self.file_path.read_text(encoding="utf-8")
            data = json.loads(raw_text)
            if not isinstance(data, dict):
                raise ValueError("JSON 루트 구조가 객체(dict)가 아닙니다.")

            raw_quizzes = data.get("quizzes")
            if not isinstance(raw_quizzes, list):
                raise ValueError("'quizzes' 필드가 리스트 형식이 아닙니다.")

            quizzes = [Quiz.from_dict(item) for item in raw_quizzes]

            best_score = data.get("best_score")
            if best_score is not None:
                if isinstance(best_score, bool) or not isinstance(best_score, int) or best_score < 0:
                    raise ValueError("'best_score' 필드는 0 이상의 정수이거나 null이어야 합니다.")

            best_detail = data.get("best_detail")
            if best_detail is not None and not isinstance(best_detail, dict):
                best_detail = None

            history = data.get("history", [])
            if not isinstance(history, list):
                history = []

            score_text = f"{best_score}점" if best_score is not None else "기록 없음"
            print(
                f"📂 [INFO] 저장된 데이터를 불러왔습니다. "
                f"(퀴즈 {len(quizzes)}개, 최고점수: {score_text})"
            )
            return quizzes, best_score, best_detail, history

        except (OSError, json.JSONDecodeError, ValueError, TypeError) as exc:
            print(f"⚠️ [WARN] 데이터 파일이 손상되었거나 읽을 수 없습니다 ({type(exc).__name__}: {exc}).")
            self.backup_corrupted_file()
            print("🔄 [INFO] 기본 퀴즈 데이터로 복구합니다.")
            quizzes = get_default_quizzes()
            self.save(quizzes, best_score=None, best_detail=None, history=[])
            return quizzes, None, None, []

    def save(
        self,
        quizzes: list[Quiz],
        best_score: int | None,
        best_detail: dict[str, int] | None = None,
        history: list[dict[str, Any]] | None = None,
    ) -> bool:
        """현재 게임 상태를 임시 파일 기록 후 원자적 교체(os.replace)로 저장한다.

        저장 실패 시 최대 max_retries회 재시도하며, 최종 실패 시 인메모리 유지 안내를 출력한다.
        """
        payload: dict[str, Any] = {
            "quizzes": [quiz.to_dict() for quiz in quizzes],
            "best_score": best_score,
            "best_detail": best_detail,
            "history": history if history is not None else [],
        }
        serialized = json.dumps(payload, ensure_ascii=False, indent=4) + "\n"
        temp_path = self.file_path.with_suffix(".json.tmp")

        for attempt in range(1, self.max_retries + 2):
            try:
                temp_path.write_text(serialized, encoding="utf-8")
                os.replace(temp_path, self.file_path)
                return True
            except OSError as exc:
                if attempt <= self.max_retries:
                    print(
                        f"⚠️ [WARN] 데이터 저장 실패 (시도 {attempt}/{self.max_retries + 1}: {exc}). "
                        "재시도합니다..."
                    )
                    time.sleep(0.05)
                else:
                    print(
                        f"❌ [ERROR] 파일 저장에 최종 실패했습니다 ({exc}). "
                        "현재 세션 동안 데이터는 메모리(오프라인 상태)에서 계속 유지됩니다."
                    )
        return False
