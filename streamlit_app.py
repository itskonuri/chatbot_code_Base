import streamlit as st
from openai import OpenAI

# 앱 제목과 설명
st.title("🐍 파이썬 챗봇 선생님")
st.write(
    "안녕! 나는 파이썬을 쉽게 설명해주는 챗봇 선생님이야! 👩‍🏫\n"
    "파이썬이 궁금한 게 있으면 뭐든지 물어봐!\n\n"
    "먼저, OpenAI API 키를 입력해야 해. [API 키 받는 곳](https://platform.openai.com/account/api-keys)"
)

# OpenAI API 키 입력
openai_api_key = st.text_input("🔑 OpenAI API 키를 입력해 주세요", type="password")

if not openai_api_key:
    st.info("API 키를 넣어야 챗봇이 작동해요! 🗝️", icon="💡")
else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 이전 대화 저장
    if "messages" not in st.session_state:
        # 챗봇의 첫 인사
        st.session_state.messages = [
            {"role": "assistant", "content": "안녕! 나는 파이썬을 쉽게 알려주는 챗봇 선생님이야. 파이썬이 궁금한 게 있으면 무엇이든 물어봐 😊"}
        ]

    # 이전 대화 보여주기
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 받기
    if prompt := st.chat_input("파이썬에 대해 궁금한 걸 적어보세요!"):
        # 사용자 메시지 저장 및 출력
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # GPT 응답 생성
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 초등학생에게 파이썬을 쉽게 알려주는 친절한 선생님이야. 어려운 단어는 쓰지 말고, 예시도 들어줘."},
                *st.session_state.messages
            ],
            stream=True,
        )

        # 응답 출력 및 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
