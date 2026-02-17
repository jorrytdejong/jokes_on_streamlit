import streamlit as st

from app.database import get_storage_label, init_db
from app.joke_engine import template_list
from app.ui import render_sidebar

st.set_page_config(page_title="Joke Studio", layout="wide")
try:
    init_db()
except RuntimeError as error:
    st.error(str(error))
    st.stop()

render_sidebar("Home")

st.title("Joke Studio")
st.write(
    "Create jokes from your own input, save each generated joke, and search them later."
)
st.success(f"Database connected: {get_storage_label()}")

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Page split")
    st.markdown(
        """
        - `Generate Joke` is for entering input, choosing a humor template, and generating a joke.
        - `Joke Library` is for searching saved jokes and reviewing both input and generated output.
        """
    )

with right_col:
    st.subheader("Sidebar role")
    st.markdown(
        """
        - Shows where you are in the app.
        - Shows quick database stats.
        - Gives a short workflow so page responsibilities stay clear.
        """
    )

st.subheader("Humor templates")
with st.expander("Show all available templates", expanded=False):
    for template in template_list():
        st.markdown(f"**{template.name}**")
        st.caption(template.description)

st.info("Use the page selector in the sidebar to open `Generate Joke` or `Joke Library`.")
