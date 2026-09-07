import streamlit as st
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# モデル選択のためのオプションボタンを追加
def select_model():
    model = st.sidebar.radio("Choose a model:", ("claude-haiku-4-5", "claude-sonnet-4-6"))
    if model == "claude-haiku-4-5":
        model_name = "claude-haiku-4-5"
    else:
        model_name = "claude-sonnet-4-6"

    # サイドバーにスライダーを追加し、temperatureを0から1までの範囲で選択可能にする
    # 初期値は0.0、刻み幅は0.1とする
    temperature = st.sidebar.slider("Temperature:", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
    return ChatAnthropic(model=model_name, temperature=temperature, streaming=True)

def main():
    st.set_page_config(
        page_title="My Great ChatGPT",
        page_icon="🤗"
    )
    st.header("My Great ChatGPT 🤗")
    st.sidebar.title("Options")

    # モデルオプションから、モデル情報を取得
    model = select_model()

    # 履歴クリアボタンの追加
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    if clear_button or "messages" not in st.session_state:
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]
        st.session_state.costs = []

    # 過去のトーク履歴を保持
    messages = st.session_state.get('messages', [])
    for message in messages:
        if isinstance(message, AIMessage):
            with st.chat_message('assistant'):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message('user'):
                st.markdown(message.content)
        else:  # isinstance(message, SystemMessage):
            st.write(f"System message: {message.content}")

    # チャット入力エリア
    # 改善点：入力エリアが、前々回のAIアシスタントの最終行と前回入力フォームの先頭行の間に位置してしまっている
    container = st.container()
    with container:
        # 入力フォーム情報
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_area(label='Message: ', key='input', height=100)
            submit_button = st.form_submit_button(label='send')

        # ユーザーが入力した場合
        if user_input and submit_button:
            st.session_state.messages.append(HumanMessage(content=user_input))
            st.chat_message("user").markdown(user_input)
            # AIアシスタントの応答を表示
            with st.chat_message("assistant"):
                # st_callback = StreamlitCallbackHandler(st.container())
                # response = model.invoke(st.session_state.messages, callbacks=[st_callback])
                stream = model.stream(st.session_state.messages)
                res = st.write_stream(stream)
            # AIアシスタントの応答結果を記録
            st.session_state.messages.append(AIMessage(content=res))     

if __name__ == "__main__":
    main()