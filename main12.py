import os

import pandas as pd
import streamlit as st
import plotly.express as px

# データの読み込み
@st.cache_data
def load_data():
    # CSVファイルのパスを取得
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, 'data', 'cafe_sales.csv')
    
    # CSVファイルを読み込む
    return pd.read_csv(csv_path)

# アプリケーションのタイトル
st.title("カフェメニュー分析ダッシュボード")

# データの読み込み
df = load_data()

# サイドバーでのフィルタリング
selected_menu = st.sidebar.multiselect(
    "メニューを選択",
    options=df["メニュー名"].unique(),
    default=df["メニュー名"].unique()
)

# データのフィルタリング
filtered_df = df[df["メニュー名"].isin(selected_menu)]

# 売上数の推移グラフ
fig = px.line(
    filtered_df,
    x="月",
    y="売上数",
    color="メニュー名",
    title="月別売上数の推移"
)

# グラフの表示
st.plotly_chart(fig)

# 売上金額の計算
filtered_df['売上金額'] = filtered_df['価格'] * filtered_df['売上数']

# 基本統計量の表示
st.subheader("基本統計量")
stats_df = filtered_df.groupby('メニュー名').agg({
    '売上数': ['mean', 'sum'],
    '売上金額': 'sum'
}).round(0)

# カラム名を日本語に変更
stats_df.columns = ['月平均売上数', '総売上数', '総売上金額']
st.write(stats_df)

# 月別売上金額の集計
st.subheader("月別売上金額")
monthly_sales = filtered_df.groupby(['月', 'メニュー名'])['売上金額'].sum().reset_index()
st.write(monthly_sales.pivot(index='月', columns='メニュー名', values='売上金額').fillna(0).round(0))
