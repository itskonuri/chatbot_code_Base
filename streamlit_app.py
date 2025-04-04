import streamlit as st
from openai import OpenAI

# 🧁 귀여운 CSS 스타일 적용
st.markdown("""
    <style>
    /* 전체 배경 */
    body {
        background-color: #FFF5F7;
    }

    /* 앱 전체 배경과 폰트 */
    .stApp {
        background-color: #FFF0F5;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        color: #4B4B4B;
    }

    /* 제목 색상과 정렬 */
    h1 {
        color: #FF69B4;
        text-align: center;
    }

    /* 채팅 메시지 스타일 */
    .stChatMessage {
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 10px;
        margin-bottom: 10px;
        box-shadow: 0px 4px 6px rgba(255, 182, 193, 0.3);
    }

    /* 입력창 스타일 */
    textarea, input {
        border-radius: 10px !important;
    }

    /* 채팅 인풋 박스 배경 */
    .stChatInputContainer {
        background-color: #FFF0F5;
        padding: 8px;
        border-radius: 10px;
    }

    /* 버튼 꾸미기 */
    button {
        background-color: #FFB6C1 !important;
        color: white !important;
        border-radius: 10px !important;
    }

    /* 링크 색상 */
    a {
        color: #FF69B4;
    }
    </style>
""", unsafe_allow_html=True)

# 앱 제목과 설명
st.title("🐍 파이썬 친구 챗봇 🧸")
st.write(
    "안녕! 나는 파이썬을 쉽게 알려주는 작은 친구야! 🐥\n"
    "파이썬이 뭐야? 변수는 뭐 하는 거야? 궁금한 건 뭐든지 물어봐줘! ✨\n\n"
    "먼저 마법의 열쇠🔑(API 키)을 넣어줘야 해! [여기서 받을 수 있어요](https://platform.openai.com/account/api-keys)"
)

# OpenAI API 키 입력
openai_api_key = st.text_input("🔐 API 키를 넣어주세요!", type="password")

if not openai_api_key:
    st.info("열쇠를 넣으면 문이 열려요! ✨ 챗봇이 움직이려면 API 키가 필요해요 🗝️", icon="💫")
else:
    # OpenAI 클라이언트 만들기
    client = OpenAI(api_key=openai_api_key)

    # 대화 저장 공간 만들기
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "안녕하세요! 🐣 나는 파이썬을 아주 쉽게 알려주는 똑똑한 친구예요! 궁금한 게 있다면 언제든지 물어봐요 💬"}
        ]

    # 예전 대화 보여주기
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 받기
    if prompt := st.chat_input("파이썬에 대해 궁금한 걸 적어볼까요? 😊"):
        # 사용자 메시지 저장하고 보여주기
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 챗봇 대답 만들기
        stream = client.chat.completions.create(
            model="gpt-4o-mini",  # gpt-4o나 gpt-3.5-turbo도 가능
            messages=[
                {"role": "system", "content": (
                    "넌 아주 귀엽고 친절한 파이썬 선생님이야. 초등학생이 쉽게 이해할 수 있게 말해줘. "
                    "어려운 단어는 쓰지 말고, 꼭 쉬운 예시를 들어서 설명해줘. 동화처럼 부드럽게 말해줘. "
                    "친근한 말투로, 이모지도 많이 써줘!"
                )},
                *st.session_state.messages
            ],
            stream=True,
        )

        # 대답 보여주고 저장하기
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
