# 🚀 Q&A 봇

우리 Q&A 커뮤니티 봇 및 미니 앱에 오신 것을 환영합니다! 🌐 우리의 텔레그램 봇과 텔레그램 미니 앱의 다이내믹한 듀오 덕분에 원활한 질문과 답변 상호 작용의 세계로 빠져들어 보세요. 우리는 질문에 답하는 데만 있는 게 아니라, 커뮤니티 참여를 혁신하기 위해 여기에 있습니다. 왜 이 카테고리를 선택했느냐면, 단순히 우리 뿐만이 아니라 텔레그램 미니 앱 콘테스트도 거 practically "커뮤니티 관리에 뛰어들어!" 라고 외쳤거든요. 그래서 여기에 있죠, 채널 소유자뿐만 아니라 일반 사용자도 자신의 정체성을 숨기면서 질문을 받고 할 수 있는 기회를 제공합니다.

## ✨ 무한한 기능들

- **개인 정보 보호 우선** : 양쪽 모두가 자신의 정체성을 숨길 수 있으며, 답하는 측은 자신의 정체성을 공개할지 선택할 수 있습니다.
- **받은 메시지함의 마법** : 사용자는 다른 사용자로부터 받은 질문을 받아들이고 답할 수 있습니다.
- **보낸 메시지함의 모험** : 사용자는 다른 사용자에게 질문을 보낼 수 있고 답을 볼 수 있습니다.
- **프로필** : 사용자는 다른 사용자의 프로필을 볼 수 있습니다.
- **질문 관리** : 사용자는 받은 질문을 삭제하거나 대답을 수정할 수 있습니다.
- **알림** : 사용자는 질문을 받거나 자신의 질문에 대답이 올 때 알림을 받을 수 있습니다.
- **통합 테마 지원** : 미니 앱은 텔레그램 앱과 동일한 테마를 사용하여 매끄러운 경험을 제공합니다.
- **봇 UI 및 미니 앱 UI** : 사용자는 봇 또는 미니 앱을 사용하여 플랫폼과 상호 작용할 수 있습니다.
- **커뮤니티 참여** : 사용자들은 서로에게 질문을 할 수 있고 다른 사용자의 질문에 답할 수 있습니다. 특히 채널 관리자들에게는 정체성을 숨기면서 커뮤니티와 쉽게 상호 작용할 수 있는 기능이 제공됩니다.

여러 앱으로 구성되어 있습니다. 예를 들어, 텔레그램 미니 앱은 사실상 프론트엔드 폴더에 있는 웹 애플리케이션입니다. 미니 앱은 VueJS와 Nuxt로 작성되었습니다. Python으로 작성된 백엔드 폴더의 FastAPI 응용 프로그램에서 전원이 공급됩니다. 또한 백엔드 폴더에 위치한 Python으로 작성된 텔레그램 봇도 미니 앱과 독립적으로 작동합니다. 이러한 결정은 다음 목표를 가지고 있었습니다:

- 미니 앱을 접근성을 위해 격리하려는 목적: **미니 앱**을 최대한 분리하여 처음 개발하는 개발자에게도 이해하기 쉽고 재사용 가능하게 만들기 위한 것입니다. 이렇게 하면 다른 프로젝트에 매끄럽게 통합될 수 있습니다.
- 프로젝트의 모듈성을 향상시키려는 목적: 프로젝트를 더 작은 모듈로 분해하면 더 나은 조직과 유연성을 얻을 수 있습니다.
- 텔레그램 미니 앱의 다양성을 보여주려는 목적: **텔레그램 미니 앱**이 적응 가능하며 어떤 백엔드와도 함께 사용할 수 있다는 것을 보여주고 개발자에게는 필요에 따라 가장 적합한 백엔드를 선택할 자유를 제공하고 싶었습니다. NodeJS로 제한되지 않고 어떤 백엔드와도 사용할 수 있습니다.

## 텔레그램 미니 앱

총 3개의 페이지로 구성되어 있습니다:

- `index.vue`: 사용자에게 묻는 질문을 보여주는 입구 페이지입니다. 사용자는 이러한 질문에 답할 수 있습니다.
- `outbox.vue`: 사용자가 보낸 질문을 표시합니다.
- `users/[id].vue`: 다른 사용자의 프로필을 보여주는 페이지입니다. 사용자는 이 페이지에서도 질문을 할 수 있습니다.

이 미니 앱은 Nitro와 함께 내부 서버를 제공합니다. FastAPI를 사용하는 대신 이 서버를 통해 데이터베이스에 쿼리를 날릴 수 있지만 SSR이 필요합니다. 현재는 정적으로 빌드된 미니 앱 버전이 사용되고 있습니다.

### 인증 및 권한

사용자가 텔레그램에서 미니 앱을 시작하면, 사용자 정보는 약관을 수락하면 미니 앱과 공유됩니다. 텔레그램에서 제공한 데이터는 봇의 비밀 키 및 제공된 데이터의 무결성 해시와 확인되어, 텔레그램에서 제공된 것임을 확인합니다. 더 많은 정보는 [backend/api/utils/web_app_data_validator.py](backend/api/utils/web_app_data_validator.py) 파일을 확인하세요.

이 시점부터 FastAPI에서 JWT가 생성됩니다. 각 사용자와 질문은 "링크" 값이 있고, 이 무작위 생성된 데이터는 ID 대신 사용됩니다. JWT 페이로드에는 사용자의 링크 값이 포함됩니다.

### 주요 미니 앱 의존성
- vue-tg: 미니 앱에서 사용되는 요소에 대한 멋진 및 매우 간단한 래퍼 라이브러리입니다. [여기에서 확인하세요](https://www.npmjs.com/package/vue-tg) 그 사용 방법에 대해 더 알아보세요. 나는 내 래퍼 라이브러리를 작성하려고 했지만, 이것을 찾아내었고 내 필요에 완벽했기 때문에 바퀴를 다시 발명할 필요가 없었습니다. 대신 텔레그램 미니 앱을 시작하는 데 도움이되는 샘플 프로젝트에 집중할 수 있습니다.

#### 예제 사용법
메인 버튼과 뒤로 버튼을 보이려면 [frontend/components/QAForm.vue](frontend/components/QAForm.vue)의 다음 코드를 확인하십시오. Vue가 페이지를 렌더링하면 자동으로 버튼이 표시됩니다. `progress` 속성은 메인 버튼에 로딩 인디케이터를 표시하는 데 사용됩니다. `disabled` 속성은 메인 버튼을 비활성화하는 데 사용됩니다. `text` 속성은 메인 버튼의 텍스트를 설정하는 데 사용됩니다. `@click` 이벤트는 부모 구성 요소에 이벤트를 발생시키는 데 사용됩니다. 뒤로 버튼의 `@click` 이벤트는 `onCancel` 메서드를 호출하여 폼 팝업을 닫습니다.

```
<MainButton 
  :progress="progressing"
  :disabled="disabled"
  :text="mainButtonText"
  @click="$emit('submitQAForm', text)" />

<BackButton @click="onCancel" />
```

#### 테마 색상 및 뷰포트 변수

텔레그램이 제공하는 구성 요소를 사용하는 것과 마찬가지로, 텔레그램이 제공하는 테마 색상을 사용할 수도 있습니다. 테마 색상은 초기 데이터에서 사용할 수 있지만 CSS 변수로도 사용할 수 있으며 아래에서 확인할 수 있습니다:

```
html {
  --tg-theme-button-text-color: #ffffff;
  --tg-theme-link-color: #f83b4c;
  --tg-theme-button-color: #f83b4c;
  --tg-color-scheme: dark;
  --tg-theme-bg-color: #3e2222;
  --tg-theme-secondary-bg-color: #271616;
  --tg-theme-text-color: #ffffff;
  --tg-theme-hint-color: #b1c3d5;
  --tg-viewport-height: 100vh;
  --tg-viewport-stable-height: 100vh;
}
```


이를 CSS에서 다음과 같이 사용할 수 있습니다:

```
body {
  background-color: var(--tg-theme-bg-color);
}
```

이 프로젝트에서는 TailwindCSS를 사용하고 있기 때문에 다음과 같이 인라인 스타일로 테마 색상을 사용할 수 있습니다:

```
<div class="bg-[var(--tg-theme-secondary-bg-color)]"></div>
```

인라인 스타일에 제한되지 않았음을 참고하세요. 자세한 내용은 TailwindCSS 문서를 참조하세요.

# 시작하기

1. `.env.example` 및 `.db.env.example` 환경 파일을 복제하고 편집하여 각각 `.env` 및 `.db.env`로 이름을 변경합니다.

2. `nuxt.config.ts`를 편집하고 `runtimeConfig.public.botUsername`을 봇의 사용자 이름으로 변경합니다.

실행하려면:

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```