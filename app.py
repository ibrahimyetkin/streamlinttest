import streamlit as st

def home_page():
    st.title('Ana Sayfa')
    st.write('Bu çok sayfalı bir Streamlit uygulamasının ana sayfasıdır.')

def page_one():
    st.title('1. Sayfa')
    st.write('Bu çok sayfalı bir Streamlit uygulamasının birinci sayfasıdır.')

def page_two():
    st.title('2. Sayfa')
    st.write('Bu çok sayfalı bir Streamlit uygulamasının ikinci sayfasıdır.')

PAGES = {
    'Ana Sayfa': home_page,
    '1. Sayfa': page_one,
    '2. Sayfa': page_two
}

st.sidebar.title('Navigasyon')
selection = st.sidebar.radio('Sayfalar', list(PAGES.keys()))

page = PAGES[selection]
page()