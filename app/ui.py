import streamlit as st

from app.database import get_stats, get_storage_label


def render_sidebar(active_page: str) -> None:
    total_jokes = "?"
    latest = "Unavailable"
    storage_label = get_storage_label()

    try:
        stats = get_stats()
        total_jokes, latest = stats
    except RuntimeError as error:
        st.sidebar.warning(str(error))

    st.sidebar.title("Joke Studio")
    st.sidebar.caption("Template-driven jokes with searchable history.")
    st.sidebar.markdown(f"**Current page:** {active_page}")
    st.sidebar.markdown(f"**Storage:** {storage_label}")

    st.sidebar.markdown("### Quick stats")
    st.sidebar.write(f"Saved jokes: {total_jokes}")
    st.sidebar.write(f"Latest save: {latest}")

    st.sidebar.markdown("### Workflow")
    st.sidebar.markdown(
        """
        1. Open `Generate Joke`
        2. Add your input and optional add-on
        3. Pick a humor template and generate
        4. Open `Joke Library` to search what was saved
        """
    )
