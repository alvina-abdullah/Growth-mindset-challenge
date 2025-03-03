
# Function to apply separate styles for different components
import streamlit as st
import time
import openpyxl
import pandas as pd
import os
from io import BytesIO


# Move this to the first line after imports
st.set_page_config(page_title="File Converter", layout="wide")



# Function to apply separate styles for different components
def apply_theme():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: white;
            color: black;
        }
        .main-title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: black;
        }
        .sub-title {
            font-size: 24px;
            font-weight: bold;
            color: black;
        }
        .st-emotion-cache-1qg05tj {
            color: black !important;
        }
        .st-emotion-cache-atejua {
        color: black !important;
        }
        .file-uploader {
            border: 2px dashed #4A90E2;
            padding: 10px;
            border-radius: 10px;
        }
        .button-style > button {
            background-color: rgb(0, 0, 0);
            color: rgb(255, 255, 255);
            padding: 8px 16px;
            border: none;
            font-weight: bold;
        }
        .data-frame {
            background-color:rgb(50, 143, 235);
            padding: 10px;
            border-radius: 5px;
        }
        .success-message {
            background-color: #D4EDDA;
            color: rgb(0, 0, 0);
            padding: 10px;
            border-radius: 5px;
        }
        .warning-message {
            background-color: #FFF3CD;
            color: #856404;
            padding: 10px;
            border-radius: 5px;
        }
        .error-message {
            background-color: #F8D7DA;
            color: #721C24;
            padding: 10px;
          
        }
        .st-emotion-cache-atejua {
        color: black
        }

 st-emotion-cache-b0y9n5 e1d5ycv52{
 background-color: #721C24;}
.st-emotion-cache-atejua.egexzqm0 {
background-color:white;}
        </style>
        """,
        unsafe_allow_html=True,
    )

apply_theme()


st.markdown("<h1 class='main-title'>🤓 Growth Mindset Challenge</h1>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>🤓 Growth Mindset Challenge</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='sub-title'>📂 File Converter & Cleaner</h2>", unsafe_allow_html=True)
st.write("Upload CSV or Excel files, clean data, and convert formats.")

# File uploader
files = st.file_uploader("Upload CSV or Excel Files.", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]

        try:
            # Check file extension and read accordingly
            if ext == "csv":
                df = pd.read_csv(file)
            elif ext == "xlsx":
                try:
                    import openpyxl  # Ensure openpyxl is available
                    df = pd.read_excel(file, engine="openpyxl")
                except ImportError:
                    st.error("❌ Error: `openpyxl` is required to read Excel files. Install it using `pip install openpyxl`.")
                    continue
            else:
                st.error(f"❌ Unsupported file format: {ext}")
                continue

            # Display preview
            st.markdown(f"<h3 class='sub-title'>📄 {file.name} - Preview</h3>", unsafe_allow_html=True)
            st.dataframe(df.head())

            # Remove duplicates
            if st.checkbox(f"Remove Duplicates - {file.name}"):
                df = df.drop_duplicates()
                st.markdown("<div class='success-message'>✅ Duplicates Removed</div>", unsafe_allow_html=True)
                st.dataframe(df.head())

            # Fill missing values
            if st.checkbox(f"Fill Missing Values - {file.name}"):
                df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
                st.markdown("<div class='success-message'>✅ Missing Values filled with mean</div>", unsafe_allow_html=True)
                st.dataframe(df.head())

            # Column selection
            selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns.tolist(), default=df.columns.tolist())
            df = df[selected_columns]
            st.dataframe(df.head())

            # Show chart
            if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
                st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

            # File conversion
            format_choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

            if st.button(f"Download {file.name} as {format_choice}"):
                output = BytesIO()
                if format_choice.lower() == "csv":
                    df.to_csv(output, index=False)
                    mime = "text/csv"
                    new_name = file.name.replace(ext, "csv")
                else:
                    df.to_excel(output, index=False, engine='openpyxl')
                    mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    new_name = file.name.replace(ext, "xlsx")

                output.seek(0)
                st.download_button("⬇️ Download file", file_name=new_name, data=output.getvalue(), mime=mime)

            st.markdown("<div class='success-message'>✅ Processing Complete!</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error processing {file.name}: {e}")



