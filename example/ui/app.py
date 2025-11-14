import streamlit as st
import os
import sys
import base64

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '')))
sys.path.append(os.path.dirname(__file__))


def question_page():
    from dotenv import load_dotenv
    import requests
    from cf_api import get_data

    base_dir = os.path.dirname(os.path.abspath(__file__))
    submissions_path = os.path.join(base_dir, '..', 'data', 'submission_data.jsonl')
    problems_path = os.path.join(base_dir, '..', 'data', 'problems_data.jsonl')

    # ---------- Load logo once (we'll use the same image for sidebar + main) ----------
    logo_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'Logo.png')
    )
    try:
        with open(logo_path, 'rb') as f:
            contents = f.read()
            logo_b64 = base64.b64encode(contents).decode('utf-8')
    except FileNotFoundError:
        logo_b64 = ''

    # -------------------------- SIDEBAR CONTENT ---------------------------------------
    with st.sidebar:
        if logo_b64:
            sidebar_logo_html = f"""
            <div style="text-align: center;">
                <br>
                <img src="data:image/png;base64,{logo_b64}"
                     alt="Logo"
                     style="width: 120px; max-width: 100%; height: auto; object-fit: contain;">
                <br>
                <h2 style="margin-top: 10px;">UCS748</h2>
                <br>
            </div>
            """
            st.markdown(sidebar_logo_html, unsafe_allow_html=True)
        else:
            st.markdown("## UCS748")

        programming_language = st.text_input(
            "Enter preferred programming language (Optional):",
            placeholder="Python/C++/Java etc.",
            help="Any code output will be in this language."
        )

        st.markdown(
            "## How to use\n"
            "1. Enter your Codeforces handle (Case Sensitive).\n"
            "2. Ask any question and you will get personalized answers.\n"
        )

        st.markdown("---")

    # -------------------------- MAIN PAGE CONTENT -------------------------------------
    load_dotenv()
    api_host = os.environ.get("HOST", "0.0.0.0")
    api_port = int(os.environ.get("PORT", 8080))

    # Main logo in center (NOT circular)
    if logo_b64:
        main_logo_html = f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{logo_b64}"
                 alt="Logo"
                 style="width: 220px; max-width: 100%; height: auto; object-fit: contain;">
            <br>
        </div>
        """
        st.markdown(main_logo_html, unsafe_allow_html=True)

    st.title("UCS748 : Codeforces Helper")

    cf_handle = st.text_input(
        "Enter handle",
        placeholder="codeforces_handle",
    )

    question = st.text_input(
        "Ask any question",
        placeholder="What insights do you want?",
    )

    if cf_handle:
        get_data.send_request(cf_handle)

    if cf_handle and question:
        if not os.path.exists(submissions_path) and not os.path.exists(problems_path):
            st.error("Failed to process file. Please check the Codeforces handle")
        else:
            url = f'http://{api_host}:{api_port}/'
            data = {"query": question, "language": programming_language}

            response = requests.post(url, json=data)

            if response.status_code == 200:
                st.write("### Answer")
                st.write(response.json())
            else:
                st.error(
                    f"Failed to send data to Codeforces API. "
                    f"Status code: {response.status_code}"
                )


# No extra sidebar / mode selector anymore – just show Q&A page
question_page()
