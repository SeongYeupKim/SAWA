# 로컬 개발 환경 설정

## 1. 프로젝트 클론

```bash
git clone https://github.com/SeongYeupKim/SAWA.git
cd SAWA
```

## 2. 의존성 설치

```bash
npm install
```

## 3. 환경 변수 설정

1. `.env.example` 파일을 복사하여 `.env.local` 생성:
```bash
cp .env.example .env.local
```

2. `.env.local` 파일을 열어서 API 키 입력:
```
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
```

### API 키 발급 방법

#### OpenAI API 키
1. https://platform.openai.com/api-keys 방문
2. 로그인 후 "Create new secret key" 클릭
3. 생성된 키를 복사하여 `.env.local`에 입력

#### Anthropic API 키
1. https://console.anthropic.com/ 방문
2. 로그인 후 "API Keys" 메뉴 클릭
3. "Create Key" 버튼으로 새 키 생성
4. 생성된 키를 복사하여 `.env.local`에 입력

## 4. 개발 서버 시작

```bash
npm run dev
```

## 5. 브라우저에서 확인

http://localhost:3000 으로 접속

## 6. 개발자 도구로 디버깅

### macOS에서 개발자 도구 열기:
- **Chrome/Brave**: `Cmd + Option + I`
- **Safari**: `Cmd + Option + I` (개발자 메뉴 활성화 필요)
- **Firefox**: `Cmd + Option + I`

### 디버깅 팁:
1. **Console 탭**: JavaScript 에러와 로그 메시지 확인
2. **Network 탭**: API 요청/응답 상태 확인
3. **Sources 탭**: 브레이크포인트 설정하여 코드 디버깅

## 7. 문제 해결

### storage 디렉토리 에러
프로젝트 루트에 `storage/sessions` 디렉토리가 자동 생성됩니다.
수동으로 생성하려면:
```bash
mkdir -p storage/sessions
```

### API 키 관련 에러
- API 키가 올바르게 설정되었는지 확인
- OpenAI는 유료 계정에서만 작동 (최소 $5 충전 필요)
- Anthropic은 신규 가입시 무료 크레딧 제공

### 포트 충돌
3000번 포트가 사용 중이면:
```bash
npm run dev -- --port 3001
```

## 8. 빌드 및 테스트

```bash
# 프로덕션 빌드
npm run build

# 빌드된 앱 실행
npm run start

# 타입 검사
npx tsc --noEmit

# 린팅
npm run lint
```