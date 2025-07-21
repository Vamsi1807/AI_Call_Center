import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Authentication
def check_login():
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":  # Replace with secure method in production!
            st.session_state.admin_logged_in = True
        else:
            st.error("Invalid credentials")

if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    check_login()
    st.stop()

st.set_page_config(page_title="Admin Dashboard - AI Call Center", layout="wide")
st.title("📊 Admin Dashboard - Multi-File & Multi-Sheet AI Summary")

DATA_FOLDER = "excel_data"
SUMMARY_FILE = "ai_summary.txt"
FULL_CONTEXT_FILE = "ai_full_context.txt"

os.makedirs(DATA_FOLDER, exist_ok=True)

# Load Gemini API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Upload Section
st.header("📤 Upload Excel Files")
uploaded_files = st.file_uploader("Choose Excel files", type=["xlsx"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        save_path = os.path.join(DATA_FOLDER, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())
    st.success(f"✅ Uploaded {len(uploaded_files)} files successfully!")

# View & Edit Section
st.header("📄 View & Edit Files & Sheets")
excel_files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".xlsx")]

if excel_files:
    selected_file = st.selectbox("Select a file:", excel_files)
    file_path = os.path.join(DATA_FOLDER, selected_file)

    try:
        sheet_dict = pd.read_excel(file_path, sheet_name=None)
        selected_sheet = st.selectbox("Select a sheet:", list(sheet_dict.keys()))
        df = sheet_dict[selected_sheet]
        st.dataframe(df, use_container_width=True)

        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

        if st.button("💾 Save Changes to Sheet"):
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                for sheet_name, sheet_df in sheet_dict.items():
                    # Use edited_df only for selected sheet
                    if sheet_name == selected_sheet:
                        sheet_df = edited_df
                    sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
            st.success("✅ Changes saved successfully!")

    except Exception as e:
        st.error(f"❌ Error reading sheets: {e}")

    # Generate AI Summary & Full Context
    if st.button("🤖 Generate Combined AI Summary (Gemini)"):
        with st.spinner("Combining data and generating AI summary..."):
            full_context_lines = []
            for excel_file in excel_files:
                full_context_lines.append(f"📁 File: {excel_file}")
                excel_data = pd.read_excel(os.path.join(DATA_FOLDER, excel_file), sheet_name=None)
                for sheet_name, df in excel_data.items():
                    full_context_lines.append(f"📄 Sheet: {sheet_name}")
                    for _, row in df.iterrows():
                        row_text = " | ".join(f"{col}: {val}" for col, val in row.items())
                        full_context_lines.append(row_text)
                    full_context_lines.append("")
                full_context_lines.append("")

            full_context_text = "\n".join(full_context_lines)

            # Save full context
            with open(FULL_CONTEXT_FILE, "w", encoding='utf-8') as f:
                f.write(full_context_text)

            # Generate summary using Gemini
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"Summarize this educational information clearly:\n{full_context_text}"
                response = model.generate_content(prompt)
                summary_text = response.text.strip()

                with open(SUMMARY_FILE, "w", encoding='utf-8') as f:
                    f.write(summary_text)

                st.success("✅ AI Summary and Full Context saved successfully!")
                st.text_area("Generated AI Summary:", summary_text, height=200)

            except Exception as e:
                st.error(f"❌ Gemini summarization failed: {e}")
else:
    st.info("No Excel files uploaded yet.")

st.markdown("---")
st.info("✅ Supports multiple Excel files, multiple sheets, and generates a combined AI summary for user queries.")
