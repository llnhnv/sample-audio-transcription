import streamlit as st
import tempfile
import whisper
import os
import json

st.set_page_config(page_title="Audio Transcription", page_icon="🎙️", layout="centered")

st.title("🎙️ Audio → Text (Whisper)")
st.caption("Upload audio, bấm Transcribe để lấy văn bản.")

@st.cache_resource
def load_model(model_size: str):
    # Các model: tiny, base, small, medium, large
    return whisper.load_model(model_size)

with st.sidebar:
    st.header("Settings")
    model_size = st.selectbox("Whisper model", ["tiny", "base", "small", "medium", "large"], index=1)
    language = st.text_input("Language (optional, ví dụ: vi / en). Để trống = auto", value="")
    task = st.selectbox("Task", ["transcribe", "translate"], index=0)
    st.markdown("---")
    st.write("Tip: model càng lớn càng chính xác nhưng chạy chậm hơn.")

audio_file = st.file_uploader("Upload audio file", type=["mp3", "wav", "m4a", "ogg", "flac", "aac", "webm"])

if audio_file is not None:
    st.audio(audio_file)

    if st.button("🚀 Transcribe", type="primary"):
        model = load_model(model_size)

        # Lưu file upload ra temp để whisper đọc
        suffix = os.path.splitext(audio_file.name)[-1] or ".audio"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(audio_file.getbuffer())
            tmp_path = tmp.name

        try:
            with st.spinner("Đang nhận dạng..."):
                kwargs = {}
                if language.strip():
                    kwargs["language"] = language.strip()
                result = model.transcribe(tmp_path, task=task, **kwargs)

            text = (result.get("text") or "").strip()
            st.subheader("✅ Output Text")
            st.text_area("Transcript", value=text, height=280)

            # Copy to clipboard
            st.components.v1.html(
                f"""
                <script>
                const _text = {json.dumps(text)};
                </script>
                <button onclick="navigator.clipboard.writeText(_text).then(() => {{
                    this.textContent = '✅ Copied!';
                    setTimeout(() => this.textContent = '📋 Copy to Clipboard', 2000);
                }})" style="
                    background:#4CAF50; color:white; border:none; padding:8px 16px;
                    border-radius:6px; cursor:pointer; font-size:14px;
                ">📋 Copy to Clipboard</button>
                """,
                height=45,
            )

            # Download transcript
            st.download_button(
                "⬇️ Download .txt",
                data=text.encode("utf-8"),
                file_name="transcript.txt",
                mime="text/plain",
            )

            # (Optional) Hiển thị segments
            with st.expander("Show segments (timestamps)"):
                segments = result.get("segments", [])
                for seg in segments:
                    st.write(f"[{seg['start']:.2f} → {seg['end']:.2f}] {seg['text']}")

        finally:
            # dọn temp file
            try:
                os.remove(tmp_path)
            except Exception:
                pass
else:
    st.info("Hãy upload một file audio để bắt đầu.")