"""기본 제공되는 IT / 컴퓨터 과학 & Python 기초 상식 퀴즈 데이터 모듈.

- 제작자: gamercross (Codyssey Mission 1-2 직접 제작)
- 출처 근거:
  1~3, 6번 문제: Python 3 공식 문서 (https://docs.python.org/ko/3/)
  4번 문제: Git 공식 문서 - Pro Git Book (https://git-scm.com/doc)
  5번 문제: ECMA-404 / RFC 8259 JSON 표준 문서 (https://www.json.org/)
- 라이선스: CC BY 4.0 / MIT License
"""

from quiz import Quiz


def get_default_quizzes() -> list[Quiz]:
    """초기 실행 또는 데이터 복구 시 사용할 기본 퀴즈 6문제를 반환한다."""
    return [
        Quiz(
            question="Python 프로그래밍 언어를 창시한 사람은 누구인가요?",
            choices=[
                "귀도 반 로섬 (Guido van Rossum)",
                "리누스 토르발스 (Linus Torvalds)",
                "비야네 스트라우스트룹 (Bjarne Stroustrup)",
                "제임스 고슬링 (James Gosling)",
            ],
            answer=1,
            hint="네덜란드 출신 프로그래머로, 몬티 파이선(Monty Python)에서 언어 이름을 따왔습니다.",
        ),
        Quiz(
            question="Python에서 순서가 있고 요소를 변경할 수 있는(Mutable) 자료형은 무엇인가요?",
            choices=[
                "tuple (튜플)",
                "str (문자열)",
                "list (리스트)",
                "int (정수)",
            ],
            answer=3,
            hint="대괄호 [ ]를 사용하여 생성하며 append(), remove() 등의 메서드를 지원합니다.",
        ),
        Quiz(
            question="Python 클래스에서 인스턴스가 생성될 때 자동으로 호출되는 초기화 메서드는?",
            choices=[
                "__start__",
                "__init__",
                "__main__",
                "__create__",
            ],
            answer=2,
            hint="Initialize(초기화하다)의 앞 글자에서 따온 던더(dunder) 메서드입니다.",
        ),
        Quiz(
            question="Git에서 원격 저장소의 변경 사항을 가져와 현재 로컬 브랜치에 병합하는 명령어는?",
            choices=[
                "git push",
                "git clone",
                "git pull",
                "git init",
            ],
            answer=3,
            hint="밀어내기(push)의 반대말인 '당겨오기'를 뜻하는 영어 단어입니다.",
        ),
        Quiz(
            question="데이터를 '키-값(Key-Value)' 쌍의 텍스트로 표현하는 경량 데이터 교환 형식은?",
            choices=[
                "JSON",
                "HTML",
                "CSV",
                "PNG",
            ],
            answer=1,
            hint="JavaScript Object Notation의 약자로, 본 프로젝트의 state.json에서도 사용됩니다.",
        ),
        Quiz(
            question="Python에서 예외(오류)가 발생할 가능성이 있는 코드를 감싸서 처리할 때 사용하는 키워드 조합은?",
            choices=[
                "if / else",
                "for / while",
                "try / except",
                "def / return",
            ],
            answer=3,
            hint="'시도하다'라는 뜻의 단어와 '제외하다/예외'라는 뜻의 단어 조합입니다.",
        ),
    ]
