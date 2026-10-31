# Block 2: 공개 — 그래프 한 장을 GitHub Pages로, 공유 메시지까지

> **Phase A 시작 시 그대로 출력한다:**
> ```
> 📖 GitHub Pages 사이트 만들기: https://docs.github.com/ko/pages/getting-started-with-github-pages/creating-a-github-pages-site
> 📖 Claude Code 스킬: https://code.claude.com/docs/ko/skills
> ```

## EXPLAIN

### 1. 용어

| 용어 | 뜻 |
|---|---|
| **GitHub Pages** | 저장소의 `index.html`을 `https://<아이디>.github.io/<저장소>/` 주소의 웹 페이지로 보여 주는 GitHub 기능 |
| **설치 한 줄** | `npx skills add <아이디>/<강의 저장소> --agent claude-code --global --yes` — 동료가 이 강의를 자기 Claude Code에 설치하는 명령 |

### 2. 공개 전에 확인할 것

| 확인 | 왜 |
|---|---|
| 비밀번호·토큰이 파일에 없다 | 공개 저장소는 누구나 읽는다 |
| 회사 설비 데이터가 없다 | 이 실습은 가상 데이터만 쓴다 |
| '실습용 가상 데이터'와 원본 출처가 적혀 있다 | 동료가 결과 숫자(13:00)를 자기 것과 대조할 수 있다 |

GitHub 로그인은 브라우저에서 일회용 코드로 한다. 코드와 비밀번호는 채팅창이 아니라 브라우저에만 입력한다.

## EXECUTE

아래 프롬프트를 붙여 넣으라고 안내한다.

```
pdm-lite-work 의 결과를 공개하자.
1. index.html 과 outputs/ 에 비밀번호·토큰·개인정보가 없는지 점검하고
   '실습용 가상 데이터'와 원본 출처(keerhee/kma-auto-genai-3-1 Day5)가 있는지 확인해 줘.
2. GitHub 로그인을 확인하고, 안 되어 있으면 브라우저 로그인용 일회용 코드만 알려 줘.
3. 저장소 이름 pdm-lite-dashboard 로 공개(public) 저장소를 만들기 전에
   올라갈 파일 목록을 보여 주고 내 승인을 받아 줘.
   승인하면 올리고 GitHub Pages(main, /)를 켜서 주소를 알려 줘.
4. 동료에게 보낼 메시지를 써 줘: 대시보드 주소, 추세 시작 13:00,
   데이터는 실습용 가상 데이터라는 점. 메시지는 보내지 마.
```

### 확인할 것 (Phase B)

- `gh repo view pdm-lite-dashboard`로 저장소가 있고, Pages 주소가 열린다(`gh api repos/<아이디>/pdm-lite-dashboard/pages`의 status가 built)
- 공개 페이지에 그래프 한 장과 '실습용 가상 데이터' 표기가 있다
- 공유 메시지에 주소·13:00·가상 데이터 표기가 있고, Claude가 보내지 않았다

막히면 아래 프롬프트를 주고 Claude Code가 원인을 찾게 한다.

```
GitHub Pages 주소가 안 열려. Pages 설정과 빌드 상태를 확인하고 원인을 한 줄로 알려 줘
```

## QUIZ

Block 2는 퀴즈가 없다. 확인이 끝나면 아래 과제를 보여 주고 수업을 마친다.

## 과제와 다음

1. **짝에게 공유** — 공유 메시지를 짝에게 보내고, 짝의 대시보드에서 추세 시작이 13:00인지 확인한다. 제출물: 짝의 대시보드 주소.
2. **내 강의 하나 더** — `/course-forge`로 다른 Day나 내 업무 주제를 골라 내 강의를 하나 더 만든다. 제출물: 새 learn- 스킬 이름과 커리큘럼 표.
