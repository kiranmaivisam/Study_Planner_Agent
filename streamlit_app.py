import os
import requests
import streamlit as st


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📚",
    layout="centered"
)


# --------------------------------------------------
# Backend URL
# --------------------------------------------------

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)


# --------------------------------------------------
# UI
# --------------------------------------------------

st.title("📚 AI Study Planner")
st.write(
    "Tell me what you want to study, how much time you have, "
    "and I'll create a realistic study plan."
)


st.divider()


study_request = st.text_area(
    "What do you want to study?",
    placeholder=(
        "Example:\n"
        "I have 2 hours tonight. "
        "I want to study DBMS and Java."
    ),
    height=150
)


# --------------------------------------------------
# Generate plan
# --------------------------------------------------

if st.button("✨ Create Study Plan", use_container_width=True):

    if not study_request.strip():
        st.warning("Please enter your study requirements.")
    else:

        with st.spinner("Creating your study plan..."):

            try:

                response = requests.post(
                    f"{API_URL}/plan",
                    json={
                        "request": study_request
                    },
                    timeout=120
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success("Study plan created!")

                    st.markdown(result["plan"])

                else:

                    st.error(
                        f"Backend error: {response.status_code}"
                    )

                    st.write(response.text)

            except requests.exceptions.RequestException as e:

                st.error(
                    "Could not connect to the Study Planner backend."
                )

                st.code(str(e))