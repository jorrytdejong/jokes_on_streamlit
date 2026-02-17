import streamlit as st

from app.database import init_db, save_joke
from app.joke_engine import (
    echo_input,
    extend_input,
    generate_joke,
    get_template,
    template_keys,
)
from app.ui import render_sidebar

st.set_page_config(page_title="Generate Joke", layout="wide")
try:
    init_db()
except RuntimeError as error:
    st.error(str(error))
    st.stop()

render_sidebar("Generate Joke")

st.title("Generate Joke")
st.write("Enter text, choose a humor template, and save the generated joke.")

all_template_keys = template_keys()

with st.form("generate_joke_form"):
    user_input = st.text_area(
        "Your input",
        placeholder="Example: My manager asked for a quick update",
        height=120,
    )
    add_on = st.text_input(
        "Optional add-on",
        placeholder="Example: right before lunch on Friday",
    )
    selected_template_key = st.selectbox(
        "Humor template",
        options=all_template_keys,
        format_func=lambda key: get_template(key).name,
    )
    st.caption(get_template(selected_template_key).description)
    submitted = st.form_submit_button("Generate and save")

if submitted:
    if not user_input.strip():
        st.error("Add some input text first.")
    else:
        try:
            generated = generate_joke(selected_template_key, user_input, add_on)
        except RuntimeError as error:
            st.error(str(error))
            st.stop()

        template_name = get_template(selected_template_key).name
        try:
            joke_id = save_joke(
                template_key=selected_template_key,
                template_name=template_name,
                user_input=user_input,
                add_on=add_on,
                generated_joke=generated,
            )
        except RuntimeError as error:
            st.error(str(error))
            st.stop()

        st.success(f"Saved joke #{joke_id}")
        st.markdown("**Echoed input**")
        st.write(echo_input(user_input))
        st.markdown("**Input plus add-on**")
        st.write(extend_input(user_input, add_on))
        st.markdown("**Generated joke**")
        st.text_area("Generated output", value=generated, height=180)
