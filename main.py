import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # '날짜' 열을 문자열로 변환 후 datetime 객체로 변환 (YYYYMMDD 형식)
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    
    # 숫자로 다뤄야 할 열 타입 정리 (필요시)
    numeric_cols = ['순위', '일관객', '누적관객', '스크린수', '상영횟수']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    return df

try:
    df = load_data()
    st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
    st.markdown("일별 박스오피스 데이터를 바탕으로 시간에 따른 영화 흥행 추이를 시각화합니다.")
    st.divider()

    st.header("1. 영화별 일별 관객수 변화 추이")
    
    # 영화 선택 드롭다운 목록 (관객수 총합 순 또는 가나다 순 정리)
    movie_list = sorted(df['영화명'].dropna().unique())
    selected_movie = st.selectbox("영화를 선택하세요:", movie_list)

    if selected_movie:
        # 선택된 영화 데이터 필터링 및 날짜순 정렬
        movie_df = df[df['영화명'] == selected_movie].sort_values('날짜')

        # Plotly 선 그래프 생성
        fig1 = px.line(
            movie_df,
            x='날짜',
            y='일관객',
            title=f"[{selected_movie}] 일별 관객수 추이",
            labels={'날짜': '날짜', '일관객': '일별 관객수(명)'},
            hover_data={'날짜': '|%Y-%m-%d', '일관객': ':,d'},
            markers=True
        )

        fig1.update_traces(
            hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객수:</b> %{y:,}명<extra></extra>"
        )

        fig1.update_layout(
            xaxis_title="날짜",
            yaxis_title="일관객수 (명)",
            hovermode="x unified",
            template="plotly_white"
        )

        # 그래프 출력
        st.plotly_chart(fig1, use_container_width=True)

        # 그래프 분석 가이드 문구 위치
        st.info(f"💡 **이 그래프로 알 수 있는 것:** {selected_movie}의 상영 기간 동안 일별 관객수가 가장 높았던 시점과 주말/평일 관객 변화 폭을 한눈에 파악할 수 있습니다.")

    st.divider()

    st.header("2. 기간별 상위 흥행작 누적 관객 추이 (추가 예정)")
    st.write("*(여기에 새로운 그래프 구역을 추가할 수 있습니다.)*")
    
    # 분석 가이드 틀 예시
    st.info("💡 **이 그래프로 알 수 있는 것:** (구현 시 추가될 분석 설명 문구 자리입니다.)")

    st.divider()

    st.header("3. 요일별/월별 관객 분포 비교 (추가 예정)")
    st.write("*(여기에 새로운 그래프 구역을 추가할 수 있습니다.)*")
    
    # 분석 가이드 틀 예시
    st.info("💡 **이 그래프로 알 수 있는 것:** (구현 시 추가될 분석 설명 문구 자리입니다.)")

except Exception as e:
    st.error(f"데이터를 불러오거나 처리하는 중 오류가 발생했습니다: {e}")
