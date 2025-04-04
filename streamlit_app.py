import streamlit as st
from openai import OpenAI  # import openai가 아닌, OpenAI 클래스만 가져옴

# 맞춤형 CSS로 스타일 추가 (배너, 푸터 스타일)
st.markdown(
    """
    <style>
    .banner {
        background: linear-gradient(90deg, #4facfe, #00f2fe);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .footer {
        text-align: center;
        font-size: 0.8rem;
        color: #555;
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 상단 배너 추가
st.markdown('<div class="banner">💬 Code Editor & Helper</div>', unsafe_allow_html=True)
st.write("이 앱은 Konuri의 코드 에디터로, 코드 수정 및 작성 관련 도움을 드립니다. 즐겁게 사용하세요! 😄")

# 사이드바에 API 키 입력 및 간단 안내
st.sidebar.title("🔧 설정")
st.sidebar.write("OpenAI API 키를 입력해주세요. 이후, 대화형 코드 헬퍼와 대화하며 코드를 개선해 보세요!")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.sidebar.info("API 키를 입력하면 앱을 사용할 수 있습니다. 🗝️")
else:
    # 여기서 openai.api_key가 아닌, OpenAI.api_key로 설정
    OpenAI.api_key = openai_api_key

    # 세션 상태에 대화 기록 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 시스템 메시지 추가 (코드 헬퍼 역할 부여) - 최초 1회만 삽입
    if not any(msg["role"] == "system" for msg in st.session_state.messages):
        st.session_state.messages.insert(0, {
            "role": "system",
            "content": (
                "너는 코드 수정 및 작성에 특화된 코드 헬퍼 챗봇이야. "
                "사용자가 제공하는 코드나 코드 관련 요청에 대해 명확하고 효율적인 답변을 제공해줘. "
                "가능하면 구체적인 코드 예제와 수정 방법을 함께 제시해줘."
            )
        })

    # 기존 대화 내역 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 처리 (대화 입력 필드)
    if prompt := st.chat_input("질문이나 요청을 입력하세요:"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 응답 생성 전에 스피너 표시
        with st.spinner("답변 생성 중..."):
            # openai.ChatCompletion.create -> OpenAI.ChatCompletion.create
            response_stream = OpenAI.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
                stream=True,
            )

            full_response = ""
            with st.chat_message("assistant"):
                for chunk in response_stream:
                    if "choices" in chunk:
                        delta = chunk["choices"][0]["delta"]
                        chunk_text = delta.get("content", "")
                        full_response += chunk_text
                        st.markdown(chunk_text)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

    # 푸터 추가
    st.markdown('<div class="footer">Developed with ❤️ by Konuri</div>', unsafe_allow_html=True)
