import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

# Load custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load the CSS
load_css("styles.css")

# Sidebar Title
st.sidebar.title("WhatsApp Chat Analyzer")

# File Upload
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # Show Analysis Button
    if st.sidebar.button("Show Analysis"):
        # Header Section
        st.markdown("""
        <div class="container">
            <div class="header">
                <h1>WhatsApp Chat Analyzer</h1>
                <p>Get insights into your chat conversations!</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Top Statistics
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.markdown(f"""
        <div class="flex-container">
            <div class="metric-card">
                <h2>Total Messages</h2>
                <p>{num_messages}</p>
            </div>
            <div class="metric-card">
                <h2>Total Words</h2>
                <p>{words}</p>
            </div>
            <div class="metric-card">
                <h2>Media Shared</h2>
                <p>{num_media_messages}</p>
            </div>
            <div class="metric-card">
                <h2>Links Shared</h2>
                <p>{num_links}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Monthly Timeline
        st.markdown("<div class='chart-container'><h2>Monthly Timeline</h2></div>", unsafe_allow_html=True)
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.markdown("<div class='chart-container'><h2>Daily Timeline</h2></div>", unsafe_allow_html=True)
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity Map
        st.markdown("<div class='chart-container'><h2>Activity Map</h2></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h3>Most Busy Day</h3>", unsafe_allow_html=True)
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.markdown("<h3>Most Busy Month</h3>", unsafe_allow_html=True)
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # WordCloud
        st.markdown("<div class='chart-container'><h2>WordCloud</h2></div>", unsafe_allow_html=True)
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)

        # Emoji Analysis
        st.markdown("<div class='chart-container'><h2>Emoji Analysis</h2></div>", unsafe_allow_html=True)
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
