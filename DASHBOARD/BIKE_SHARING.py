import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
sns.set(style='dark')

# Set page config for wide layout
st.set_page_config(
    page_title="Dashboard Bike Sharing",
    layout="wide",  # Layout menjadi wide
    initial_sidebar_state="expanded"  # Sidebar dalam keadaan terbuka
)

uploaded_file = st.file_uploader("Upload Dataset CSV", type=["csv"])

if uploaded_file is not None:
    # Membaca file CSV dengan pandas
    df_hour = pd.read_csv(uploaded_file)
    
    total_book = df_hour.groupby(['yr','mnth','mnth_name']).agg(
        total_count = ('cnt','sum')
    ).sort_values(by=['yr','mnth'], ascending=[True, True]).reset_index()
    
    st.title("Dashboard Bike Sharing")

    st.header("Analisis Total Peminjaman Sepeda Setiap Tahun")


    st.sidebar.header("Total Penyewaan Sepeda Setiap Tahun")
    avail_years = sorted(df_hour['yr'].unique())
    selected_year = st.sidebar.multiselect("Pilih Tahun :", options=avail_years)
    
    if selected_year :
        filtered_year = df_hour[df_hour["yr"].isin(selected_year)]

        total_book = filtered_year.groupby(['yr','mnth','mnth_name']).agg(
            total_count = ('cnt','sum')
            ).sort_values(by=['yr','mnth'], ascending=[True, True]).reset_index()
        
        total_total = df_hour['cnt'].sum()
        # total_total_df = pd.DataFrame({'Total Penyewaan Keseluruhan': [total_total]})
        st.metric("Total Penyewaan Sepeda Keseluruhan :", value=total_total)

        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"Penjualan Tahun : {', '.join(map(str, selected_year))}")
            st.dataframe(total_book)

        with col2:    
            st.subheader(f"Grafik Pola Penjualan Pada Tahun : {', '.join(map(str, selected_year)) }")

            fig, ax = plt.subplots(figsize=(20,10))
            ax.plot(
                total_book[total_book['yr'] == 2011]['mnth_name'], 
                total_book[total_book['yr']==2011]['total_count'], 
                marker='o',  
                color='orange',
                linewidth = 2
            )

            ax.plot(
                total_book[total_book['yr'] == 2012]['mnth_name'], 
                total_book[total_book['yr']==2012]['total_count'], 
                marker='o',  
                color='skyblue',
                linewidth = 2
            )

            ax.set_title(f"Pola Penjualan Berdasarkan Tahun: {', '.join(map(str, selected_year))}", fontsize=16)
            ax.tick_params(axis="x", labelsize=20)
            ax.tick_params(axis="y", labelsize=15)
            st.pyplot(fig)
     
    else:
        st.warning("Silakan pilih setidaknya satu tahun untuk melihat data.")
    
    st.header("Analisis Total Peminjaman Berdasarkan Setiap Musim")

    st.sidebar.header("Total Penyewaan Sepeda Setiap Musim")
    avail_season = sorted(df_hour['season'].unique())
    selected_season = st.sidebar.multiselect("Pilih Musim :", options=avail_season)
    
    if selected_season:
        filtered_season = df_hour[df_hour["season"].isin(selected_season)]

        total_season = filtered_season.groupby(['yr','season']).agg(
                total_count_season = ('cnt','sum')
            ).sort_values(by=['yr','total_count_season'], ascending=[True, True]).reset_index()
        
        # Membagi layout menjadi dua kolom
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"Penjualan Musim : {', '.join(map(str, selected_season))}")
            st.dataframe(total_season)

        with col2:
            st.subheader(f"Grafik Pola Penjualan Pada Musim : {', '.join(map(str, selected_season)) }")

            fig, ax = plt.subplots(figsize=(20,10))

            ax.bar(
                total_season[total_season['yr'] == 2012]['season'], 
                total_season[total_season['yr']==2012]['total_count_season'], 
                color='skyblue'
            )

            ax.bar(
                total_season[total_season['yr'] == 2011]['season'], 
                total_season[total_season['yr']==2011]['total_count_season'], 
                color='orange'
            )

            ax.set_title(f"Pola Penjualan Berdasarkan Musim: {', '.join(map(str, selected_season))}", fontsize=16)
            ax.tick_params(axis="x", labelsize=20)
            ax.tick_params(axis="y", labelsize=15)
            st.pyplot(fig)
    else:
        st.warning("Silakan pilih setidaknya satu musim untuk melihat data.")

    st.header("Analisis Total Penyewaan Berdasarkan Kategori Pengguna")

    st.sidebar.header("Total Penyewaan Berdasarkan Kategori Pengguna")
    avail_user = sorted(['Casual','Registered'])
    selected_user = st.sidebar.multiselect("Pilih Kategori Pengguna :", options=avail_user)


    if selected_user :
        for user_type in selected_user :
            if user_type == "Casual":
                def autopct_with_count(pct, all_values):
                    absolute = int(round(pct/100. * sum(all_values)))  # Hitung nilai absolut
                    return f'{absolute}\n({pct:.1f}%)'  # Gabungkan nilai absolut dan persentase
                
                total_user = df_hour.groupby(['yr']).agg(
                    total_casual_user=('casual', 'sum')
                ).sort_values(by=['yr'], ascending=True).reset_index()
                col1 , col2 = st.columns(2)
                with col1 :
                    st.subheader(f"Penjualan Kategori: Casual")
                    st.dataframe(total_user)
                with col2 :
                    fig = px.pie(
                        total_user,
                        names=total_user['yr'],
                        values=total_user['total_casual_user'],    
                    )

                    fig.update_layout(
                        width=300,  
                        height=300  
                    )
                    st.plotly_chart(fig)
            elif user_type == "Registered":
                total_user = df_hour.groupby(['yr']).agg(
                    total_registered_user =('registered', 'sum')
                ).sort_values(by=['yr'], ascending=True).reset_index()


                col1 , col2 = st.columns(2)
                with col1 :
                    st.subheader(f"Penjualan Kategori: Registered")
                    st.dataframe(total_user)
                with col2 :    
                    fig = px.pie(
                        total_user,
                        names=total_user['yr'],
                        values=total_user['total_registered_user'],    
                    )

                    fig.update_layout(
                        width=300,  
                        height=300  
                    )
                    st.plotly_chart(fig)
    else:
        st.warning("Silakan pilih setidaknya satu kategori pengguna.")
else:
    st.header("Silakan unggah file untuk melihat datanya.")
