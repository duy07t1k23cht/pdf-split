import os
import streamlit as st
from PyPDF2 import PdfFileReader, PdfFileWriter
from io import BytesIO
import boto3
from dotenv import load_dotenv
import traceback
from botocore.exceptions import NoCredentialsError

load_dotenv()

from split import split_pdf

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_REGION = "ap-southeast-1"
S3_BUCKET_NAME = "duynm98-pdf-split"

# Initialize S3 client
s3_client = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)


def upload_to_s3(file, bucket_name, object_name):
    try:
        s3_client.upload_fileobj(file, bucket_name, object_name)
        st.success(f"File successfully uploaded to {bucket_name}/{object_name}")
    except NoCredentialsError:
        st.error("Credentials not available")


def main():
    st.set_page_config(
        page_title="PDF Split for X",  # The title that will appear in the tab
        # page_icon=":shark:",  # You can also set a custom favicon
        # layout="centered",  # Other options: "wide"
        # initial_sidebar_state="auto",  # Other options: "expanded", "collapsed"
    )

    st.title("Công nghệ tách pdf đỉnh của chóp cho Xuân")

    uploaded_file = st.file_uploader("Upload file cần tách lên đây", type="pdf")

    if uploaded_file is not None:
        # pdf_preview(pdf_bytes)

        # Show original PDF bytes (optional)
        # st.write(pdf_bytes)

        # Split PDF
        if st.button("Submit"):
            with st.spinner("Đang xử lý, đợi xíu..."):
                pdf_bytes = uploaded_file.read()
                output_pdf = BytesIO()
                try:
                    s3_client.upload_fileobj(BytesIO(pdf_bytes), S3_BUCKET_NAME, uploaded_file.name)
                    print(">" * 100)
                    print("Splitting:", uploaded_file.name)
                    output = split_pdf(BytesIO(pdf_bytes))
                except Exception as e:
                    print(e)
                    st.error("Thôi xong! Có lỗi gì rồi. Thử lại lần nữa hoặc liên hệ anh Duy để được xử lý :)")
                    st.code(traceback.format_exc(), language="bash")
                    return

                output.write(output_pdf)
                st.success("Đã tách xong thành .Bấm vào nút phía dưới để tải!")

                # Download link for split PDF
                st.download_button(label="Tải xuống", data=output_pdf.getvalue(), file_name=f"{uploaded_file.name}_split.pdf", mime="application/pdf", type="primary")

                st.info("Nếu tải file về mà thấy file có vấn đề gì, liên hệ anh Duy để xử lý.")


if __name__ == "__main__":
    main()
