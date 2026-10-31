# Block 0: 준비 — 작업 폴더 · 데이터

> **Phase A 시작 시 그대로 출력한다:**
> ```
> 📖 원본 강의 저장소: https://github.com/keerhee/kma-auto-genai-3-1
> 📖 Claude Code 일반 워크플로: https://code.claude.com/docs/ko/common-workflows
> ```

## EXPLAIN

### 1. 이 강의는 어디서 왔나

능률협회 「자동차산업과 생성형 AI 3-1」 **Day5 예지보전** 본 강의를 10분 실습판으로 줄였다. 원본의 AI 노코드 6단계 중 세 곳만 쓴다.

| 원본 6단계 | 이 실습판 |
|---|---|
| ① 환경 · ② 데이터 | Block 0 준비 |
| ④ 분석 1 (노이즈 vs 추세, 정비 시점) | Block 1 노이즈 vs 추세 |
| 결과 공개·공유 | Block 2 공개 |

### 2. 용어

| 용어 | 현장 정의 |
|---|---|
| **예지보전 (PdM, Predictive Maintenance)** | 고장 후 고치거나 주기마다 교체하는 대신, 센서로 고장 징후를 미리 감지해 정비 시점을 정하는 것 |
| **다변수 센서 데이터** | 진동(mm/s)·온도(℃)·압력(bar)을 같은 시각에 함께 기록한 표. 한 변수가 놓친 이상을 다른 변수가 잡는다 |

### 3. 오늘 쓸 데이터

`Day5_설비센서_50건_가상.csv` — 설비A(프레스 메인모터)와 설비B(차체 용접로봇 감속기) 2대 × 25시점(08:00~16:00, 20분 간격), **실습용 가상 데이터**다. 원본 데이터는 고치지 않고, 결과는 따로 쓴다. 그래야 "어떤 데이터로, 어떤 기준으로 판정했는가"를 언제든 다시 보여 줄 수 있다.

## EXECUTE

Phase A 출력 직전에 `{SKILL_DIR}`를 이 스킬 폴더의 실제 경로로 바꿔 보여 준다.

```
예지보전 실습 준비를 해 줘.
1. 지금 폴더 안에 pdm-lite-work 폴더를 만들고, 그 안에 data 폴더를 만들어
   {SKILL_DIR}/assets/lab 안의 csv와 README.md를 복사해 줘.
2. Python과 pandas가 있는지 확인하고 없으면 설치해 줘.
3. git이 있는지 확인해 줘(윈도우에 없으면 Git for Windows 설치를 안내해 줘).
4. data의 csv 행 수와 첫 줄(열 이름)을 보여 주고,
   결과를 pdm-lite-work/env_check.txt 에 OK / 조치 필요로 적어 줘.
data 안의 원본 파일은 고치지 마.
```

### 확인할 것 (Phase B)

`pdm-lite-work/env_check.txt`와 `pdm-lite-work/data/`를 직접 읽어 확인한다.

- data에 `Day5_설비센서_50건_가상.csv` 50행, 열: 시간 · 설비 · 진동(mm/s) · 온도(℃) · 압력(bar) · 비고
- Python·pandas·git이 OK

막히면 아래 프롬프트를 주고 Claude Code가 원인을 찾게 한다.

```
방금 오류의 원인과 해결을 한 줄씩 설명한 뒤 고쳐 줘
```

## QUIZ

Block 0은 퀴즈가 없다. 확인이 끝나면 이 세션에서 바로 Block 1로 간다.
