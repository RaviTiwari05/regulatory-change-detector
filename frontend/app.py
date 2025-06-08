import streamlit as st
import requests

st.title("🧠 Regulatory Change Detector")

file1 = st.file_uploader("Upload OLD document", type="txt")
file2 = st.file_uploader("Upload NEW document", type="txt")

if st.button("Analyze Changes"):
    if file1 and file2:
        file1.seek(0)
        file2.seek(0)

        files = {
            "file1": ("old.txt", file1, "text/plain"),
            "file2": ("new.txt", file2, "text/plain"),
        }

        try:
            response = requests.post("http://localhost:8000/analyze/", files=files)
            response.raise_for_status()
            data = response.json()

            st.write("🔎 Raw backend response:")
            st.json(data)  # DEBUG: See what's coming back

            if not data["results"]:
                st.info("✅ No significant changes detected.")
            else:
                for i, result in enumerate(data["results"]):
                    with st.expander(f"Change #{i+1}"):
                        st.markdown(f"**Change Type:** {result['change_type']}")
                        st.markdown(f"**Summary:** {result['change_summary']}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to backend: {e}")
    else:
        st.warning("Please upload both files.")
