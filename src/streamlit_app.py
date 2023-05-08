import numpy as np
import streamlit as st
from PIL import Image
from io import BytesIO
from main import predict
from his_horizontal import Extract
import base64

ex = Extract()

st.set_page_config(layout="wide", page_title="Text Extracter")

names, group = st.columns(2)
with st.container():
    with names.expander("Members"):
        st.write("## Nguyễn Thị Tuyết Mai - 20110381")
        st.write("## Vũ Hoàng Trúc Vy - 20110415")
        st.write("## Nguyễn Văn Hơn - 20110371")

    group.write("Group 3")



st.write("## Extract text from your image")
st.write(
    ":dog: Try uploading an image to watch the text magically extracted :grin:"
)
st.sidebar.write("## Upload and download :gear:")


# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

def fix_image(upload):

    print(upload)

    image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image)

    imageArr = np.array(image)
    ex.loadImage(image=imageArr)
    ex.preProcessing()
    groups = ex.group_peaks(ex.peaks, 2)

    cropped = ex.crop_peaks(ex.img, groups)

    extracted_content = predict(cropped)

    extracted_content = "\n".join(extracted_content)

    col2.write("Extracted Image :wrench:")
    col2.image(cropped)
    col2.write(extracted_content)
    st.sidebar.markdown("\n")


# hide footer
hide_footer_style = """
<style>
footer {visibility: hidden;}
div
{
    font-size: 14px
}
</style>
"""

st.markdown(hide_footer_style, unsafe_allow_html=True)

col1, col2 = st.columns(2)

my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])


if my_upload is not None:
    fix_image(upload=my_upload)
else:
    fix_image("./images/cropImage-0.png")
