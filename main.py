import streamlit as st
import tempfile
import os
from saving_annotate_video import saving_annotated_video
# import subprocess
# if not os.path.isfile('model.h5'):
#     subprocess.run(['curl --output model.h5 "https://media.githubusercontent.com/media/Vaibhavsun/shoplifting_tracker/blob/main/model.h5"'], shell=True)
st.title("ShopLifting Tracking and Detection")

uploaded_file = st.file_uploader("Upload a video", type=["mp4"])

def save_uploaded_file(uploaded_file):
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path
if "button_pressed" not in st.session_state:
    st.session_state.button_pressed=False
if uploaded_file or st.session_state.button_pressed:
    saved_video_path = save_uploaded_file(uploaded_file)



    if st.button("Process Video") or st.session_state.button_pressed:
        text=st.empty()
        text.write("Processing Video...")
        progress=st.progress(0)
        if st.session_state.button_pressed==False:
            saving_annotated_video(saved_video_path,progress_bar=progress)
        st.session_state.button_pressed=True
        text.write("Completed..")
        st.success("Video processed successfully!")

        x1=st.empty()
        with open('out.mp4', "rb") as f:
            x1.download_button("Download Anotated Video", f, file_name="processed_video.mp4", mime="video/mp4")
        x2=st.empty()
        with open('out.csv', "rb") as f:
            x2.download_button("Download CSV", f, file_name="data.csv", mime="text/csv")


