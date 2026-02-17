import csv
import io
from datetime import datetime, timezone

import streamlit as st

from app.database import JokeRecord, init_db, list_jokes
from app.joke_engine import get_template, template_keys
from app.ui import render_sidebar


def shorten(value: str, max_length: int = 90) -> str:
    if len(value) <= max_length:
        return value
    return value[: max_length - 3] + "..."


def records_to_csv(records: list[JokeRecord]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        [
            "id",
            "created_at",
            "template_key",
            "template_name",
            "user_input",
            "add_on",
            "generated_joke",
        ]
    )
    for record in records:
        writer.writerow(
            [
                record.id,
                record.created_at,
                record.template_key,
                record.template_name,
                record.user_input,
                record.add_on,
                record.generated_joke,
            ]
        )
    return buffer.getvalue()


st.set_page_config(page_title="Joke Library", layout="wide")
try:
    init_db()
except RuntimeError as error:
    st.error(str(error))
    st.stop()

render_sidebar("Joke Library")

st.title("Joke Library")
st.write("Search saved jokes by text and filter by template type.")

all_template_keys = template_keys()

search_col, limit_col = st.columns([3, 1])
with search_col:
    search_text = st.text_input(
        "Search text",
        placeholder="Search input, add-on, joke text, or template name",
    )
with limit_col:
    limit = st.slider("Max rows", min_value=10, max_value=200, value=50, step=10)

selected_template_keys = st.multiselect(
    "Filter by template",
    options=all_template_keys,
    format_func=lambda key: get_template(key).name,
)

try:
    records = list_jokes(
        search_text=search_text,
        template_keys=selected_template_keys or None,
        limit=limit,
    )
except RuntimeError as error:
    st.error(str(error))
    st.stop()

st.write(f"Found {len(records)} joke(s).")

if records:
    csv_data = records_to_csv(records)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    st.download_button(
        "Export filtered results to CSV",
        data=csv_data,
        file_name=f"jokes-{timestamp}.csv",
        mime="text/csv",
    )

    preview_rows = [
        {
            "ID": record.id,
            "Saved at (UTC)": record.created_at,
            "Template": record.template_name,
            "Input": shorten(record.user_input),
            "Joke preview": shorten(record.generated_joke),
        }
        for record in records
    ]
    st.dataframe(preview_rows, use_container_width=True, hide_index=True)

    st.subheader("Full records")
    for record in records:
        with st.expander(f"#{record.id} | {record.template_name} | {record.created_at}"):
            st.markdown("**Input**")
            st.write(record.user_input)
            if record.add_on:
                st.markdown("**Add-on**")
                st.write(record.add_on)
            st.markdown("**Generated joke**")
            st.write(record.generated_joke)
else:
    st.info("No jokes found yet. Generate one on the `Generate Joke` page.")
