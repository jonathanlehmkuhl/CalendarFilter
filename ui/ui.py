from urllib import parse

import requests
import streamlit as st
from streamlit import session_state as state

if "number_of_patterns" not in state:
    state.number_of_patterns = 4

if "missing_url" not in state:
    state.missing_url = False

if "invalid_url" not in state:
    state.invalid_url = False


if "missing_patterns" not in state:
    state.missing_patterns = False


def add_pattern():
    state.number_of_patterns += 1


def generate_url():
    if not "input_url" in state or not state.input_url:
        state.missing_url = True
        return
    state.missing_url = False

    response = requests.get(state.input_url)
    if not response.status_code == 200:
        state.invalid_url = True
        return
    state.invalid_url = False
    calendar_url = parse.quote(state.input_url)

    if not any(state[f"input_pattern_{i}"] for i in range(state.number_of_patterns)):
        state.missing_patterns = True
        return
    state.missing_patterns = False
    patterns = ",".join(
        [
            state[f"input_pattern_{i}"]
            for i in range(state.number_of_patterns)
            if state[f"input_pattern_{i}"]
        ]
    )
    patterns = parse.quote(patterns)

    url = f"https://calendarfilter.jlehmkuhl.com/filter-calendar?url={calendar_url}&patterns={patterns}"
    state.result_url = url


st.set_page_config(page_title="Filter your Calendar", page_icon="📅")

st.title("Filter your Calendar")

st.markdown("")

st.button("Filter Calendar", type="primary", on_click=generate_url)

if state.missing_url:
    st.error("Please provide a URL for your calendar.")
elif state.invalid_url:
    st.error("The provided URL is invalid. Please provide a valid URL.")
elif state.missing_patterns:
    st.error("Please provide at least one pattern to filter.")
elif "result_url" in state:
    st.write("URL of the filtered iCal calendar:")
    st.code(state.result_url, language=None)
    st.markdown(
        ":material/info: This URL provides a dynamically generated iCal calendar that automatically applies your filters to the latest version of your calendar. "
        "Your are welcome to subscribe to it in your preferred calendar app.",
    )

st.markdown("")

with st.container(border=True):

    st.text(
        "URL of the iCal calendar",
        help="Enter the URL of your iCal calendar. This should be a valid URL pointing to an .ics file.\n"
        "Example: https://example.com/calendar.ics",
    )
    calendar_url = st.text_input(
        "Calendar URL",
        key="input_url",
        placeholder="Calendar URL",
        label_visibility="collapsed",
    )

    st.markdown("")

    st.text(
        "Events/regexps you want to filter",
        help="Enter regular expressions to filter events. Examples:\n"
        "- 'Meeting' to match any event with 'Meeting' in its name.\n"
        "- '^Project' to match events that start with 'Project'.\n"
        "- 'Deadline$' to match events that end with 'Deadline'.\n"
        "- '^(?!Lunch)' to exclude any event that starts with 'Lunch'.\n\n"
        "Multiple regular expressions will be evaluated as a logical OR. ",
    )
    for i in range(state.number_of_patterns):
        st.text_input(
            "Patterns",
            key=f"input_pattern_{i}",
            placeholder=f"Event/regexp {i+1}",
            label_visibility="collapsed",
        )

    st.button("Add Event", on_click=add_pattern, icon=":material/add:", key="add_event")

st.markdown(
    """
    <style>
    button[kind="secondary"] {
        padding: 0px !important;
        margin-top: -12px !important;
        border: none;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        padding-bottom: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
