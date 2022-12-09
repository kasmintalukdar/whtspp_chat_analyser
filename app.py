import streamlit as st
import regex as re
import pandas as pd
import matplotlib.pyplot as plt
import preprocess
import Analyser
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocess.preprocess(data)
    st.dataframe(df)
    user_list = df[df['users'] != 'group_notification']['users'].unique().tolist()
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user=st.sidebar.selectbox("Show Analysis",user_list)
    if st.sidebar.button("Show Analysis"):
        col1,col2,col3,col4=st.columns(4)
        total_massage,word_count,media_massage,link_count=Analyser.analyse(df,selected_user)
        #4 statistics total_massage,word_count,media_massage,link_count
        with col1:
            st.subheader("Total Messages")
            st.subheader(total_massage)
        with col2:
            st.subheader("Total Words")
            st.subheader(word_count)
        with col3:
            st.subheader("Link Shared")
            st.subheader(link_count)
        with col4:
            st.subheader("Media Shared")
            st.subheader(media_massage)
        #most busy user
        if selected_user=='Overall':
            st.subheader("Most Active User")
            col1, col2=st.columns(2)
            top_user_df=Analyser.busy(df)
            bar_plot=Analyser.bar_ploter(x=top_user_df.head(5).Users, y=top_user_df.head(5).message_in_percentage, rotation=45,
                       xlabel="Users", ylabel="percentage contribution of massages")
            with col1:
                st.pyplot(bar_plot)
            with col2:
                st.dataframe(top_user_df)

        #montly time line
        st.subheader("Monthly Timeline")
        timeline = Analyser.monthly_timeline(df, selected_user)

        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['massages'], color='green')
        plt.xticks(rotation=90)
        st.pyplot(fig)
        #daily timeline
        st.subheader("Daily Timeline")
        daily_timeline = Analyser.daily_timeline(df, selected_user)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['massages'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #wordcloud
        st.subheader("Word Cloud")
        wordcloud=Analyser.wordcloud(df,selected_user)
        st.pyplot(wordcloud)
        #most common word
        commonword_df=Analyser.most_common_words(df, selected_user)
        bar_plot_common_word = Analyser.bar_ploter(x=commonword_df['words'], y=commonword_df['count'], rotation=90,
                                                   xlabel="Words", ylabel="words count")
        st.subheader("Most Common Word")

        st.pyplot(bar_plot_common_word)
        #most used emoji
        commonemoji_df = Analyser.emoji_helper(df, selected_user)
        st.subheader("Most Common emoji")
        st.dataframe(commonemoji_df)
        # activity map
        st.subheader('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Most busy day")
            busy_day = Analyser.week_activity_map(df, selected_user)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.subheader("Most busy month")
            busy_month = Analyser.month_activity_map(df, selected_user)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        #activity heatmap
        st.subheader("Weekly Activity Map")
        user_heatmap = Analyser.activity_heatmap(df,selected_user)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

















