import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from io import BytesIO
from main import predict
from his_horizontal import Extract

ex = Extract()

st.set_page_config(layout="wide", page_title="Text Extracter")

<< << << < HEAD
names, group = st.columns(2)
with st.container():
    names.write("## Nguyễn Thị Tuyết Mai - 20110381")
    names.write("## Vũ Hoàng Trúc Vy - 20110415")
    names.write("## Nguyễn Văn Hơn - 20110371")
    new_title = '<p style="font-family:sans-serif; color:Green; font-size: 23px;">Group 3</p>'
    group.markdown(new_title, unsafe_allow_html=True)
    new_title2 = '<p style="font-family:sans-serif; color:Red; font-size: 25px;">HANDWRITTEN TEXT RECOGNITION USING IMAGE PROCESSING AND PATTERN RECOGNITION TECHNIQUES</p>'
    group.markdown(new_title2, unsafe_allow_html=True)
== == == =


def hide_footer():
    hide_footer_style = """
  <style>
  footer {visibility: hidden;}
  div
  {
      font-size: 14px
  }
  div.sticky {
  position:fixed !important;
  top: 0 !important;
  background-color: black !important;
  margin-top: 2.875rem !important;
  font-size: 20px;
  z-index: 100;
  align-items: center;
  }

  div.sticky-right {
  position:fixed !important;
  top: 0 !important;
  left: 50vh;
  background-color: black !important;
  margin-top: 2.875rem !important;
  margin-left: 50vh !important;
  font-size: 20px;
  z-index: 100;
  align-items: center;
  }

  div.sticky .column {
  flex: 1;
  padding: 10px;
  }

  </style>
  """
    st.markdown(hide_footer_style, unsafe_allow_html=True)


st.write("""<div class="sticky-right"> <div><details> <summary>Group 3</summary>
<ul class="team-content">
<li>HANDWRITTEN TEXT RECOGNITION USING IMAGE PROCESSING AND PATTERN RECOGNITION TECHNIQUES</li> 
</ul> </details> </div>
</div>""", unsafe_allow_html=True)


hide_footer()

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


<< << << < HEAD
# extracted_content = "\n".join(extracted_content)

col2.write("Extracted Image :wrench:")
col2.image(cropped, caption=extracted_content)

# col2.write(extracted_content)
== == == =
col2.write("Extracted Image :wrench:")
col2.image(cropped, caption=extracted_content)

>>>>>> > e34651dee3887ac56d8e876ff8d1e8ccacfb256b
st.sidebar.markdown("\n")


col1, col2 = st.columns(2)

my_upload = st.sidebar.file_uploader(
    "Upload an image", type=["png", "jpg", "jpeg"])


if my_upload is not None:
    try:
        fix_image(upload=my_upload)
    except:
        st.warning('Please upload a valid image', icon="⚠️")
else:
    fix_image("./images/cropImage-0.png")
