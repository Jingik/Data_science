import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import plotly.express as px 
        
@st.cache_data
def load_data(k):
    # 데이터프레임을 여기에서 로드합니다
    if k == 1:
        df = pd.read_excel('./data/29cm_outer.xlsx', engine='openpyxl')
        df['기존가격'] = df['기존가격'].str.replace('원', '')
        df['기존가격'] = df['기존가격'] + '원'
        df['이미지링크'] = 'https:' + df['이미지링크']

    elif k == 2:
        df = pd.read_excel('./data/Musinsa_outer.xlsx', engine='openpyxl')
   
    elif k == 3:
        df = pd.read_excel('./data/KREAM_outer.xlsx', engine='openpyxl')
    
    elif k == 4:
        df = pd.read_excel('./data/KREAM_outer.xlsx', engine='openpyxl')
        df = df.drop(columns=['이미지링크'], axis=1)
    else : 
        print('Load 데이터가 없습니다.')
    return df

## Option 1
# Ranking 별 데이터 시각화
def process_data_for_option_1(df, selected_brand, site):
    brand_data = df[df['브랜드'] == selected_brand]
    return brand_data


def display_images_with_toggle(df):
    if 'toggle_info' not in st.session_state:
        st.session_state['toggle_info'] = {}

    for index, row in df.iterrows():
        image_url = row['이미지링크']
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        
        col1, col2 = st.columns([0.1, 1]) 
        with col1:
            st.markdown(f"<p style='color: black;'>{index}.</p>", unsafe_allow_html=True)  # 인덱스 번호 표시
        with col2:
            product_name_html = f"<a href='{row['사이트']}' target='_blank'>{row['상품명']}</a>"
            st.markdown(product_name_html, unsafe_allow_html=True)
            st.image(image, caption=row['상품명'], width=300)  # 이미지 표시
            
        button_key = f"toggle_{index}"
        if st.button("상세 정보 보기/숨기기", key=button_key):
            st.session_state['toggle_info'][button_key] = not st.session_state['toggle_info'].get(button_key, False)

        if st.session_state['toggle_info'].get(button_key, False):
            col =['사이트','이미지링크']
            row = row.drop(col)
            # info_to_display = row  # '이미지링크' 정보 제외
            st.write(row)  # 상세 정보 표시
        else:
            st.write("")  # 상세 정보 숨기기 (빈 문자열 출력)
            
## Option 2          
# 그래프를 이용한 데이터 시각화
def process_data_for_option_2(df):
    brand_counts = df['브랜드'].value_counts()
    top_10_brands = brand_counts.head(10)
    
    others_count = brand_counts[10:].sum()
    top_10_brands['기타'] = others_count

    return top_10_brands

def create_pie_bar_chart(top_10_brands):
    # 데이터 준비
    brands = top_10_brands[:-1].index
    counts = top_10_brands[:-1].values
    # Plotly로 원형 그래프 생성
    
    pie_fig = px.pie(values=counts, names=brands, title='Top 10 Brands by Product Count')
    bar_fig = px.bar(top_10_brands, x = brands, y = counts, title='Top 10 Brands by Product Count',labels={'x': 'Brand', 'y': 'Count'})
    
    return pie_fig, bar_fig

def display_summary_table(top_10_brands):
    summary_table = pd.DataFrame(top_10_brands)
    summary_table.columns = ['Number of Products']
    st.table(summary_table)

    
## Option 3    
# 이미지를 포함하는 HTML 테이블을 생성하는 함수

def create_table_with_index_and_images(df):
    # 인덱스 번호를 포함하는 새로운 열 추가
    df_display = df.copy()
    df_display = df_display[:300]
    # HTML 테이블의 시작
    html = "<table>"
    html += "<tr>"
    for col in df_display.columns:
        html += f"<th>{col}</th>"
    html += "</tr>"

    # 데이터 행 추가
    try :
        for _, row in df_display.iterrows():
            html += "<tr>"
            for col in df_display.columns:
                if col == '이미지링크':  # 이미지 링크인 경우
                    html += f"<td><img src='{row[col]}' width='100'></td>"
                elif col == '사이트':  # 사이트 링크인 경우
                    html += f"<td><a href='{row[col]}' target='_blank'>{row[col]}</a></td>"
                else:
                    html += f"<td>{row[col]}</td>"
            html += "</tr>"
            
    except Exception as e:
        for _, row in df_display.iterrows():
            html += "<tr>"
            for col in df_display.columns:
                if col == '사이트':  # 사이트 링크인 경우
                    html += f"<td><a href='{row[col]}' target='_blank'>{row[col]}</a></td>"
                else:
                    html += f"<td>{row[col]}</td>"
            html += "</tr>"
            
    # HTML 테이블의 끝
    html += "</table>"

    return html


def streamlit_app():
    # Sidebar
    site = st.sidebar.selectbox("Select a Site", options=["Explain", "29cm", "Musinsa", "Kream"])

    # Load the appropriate dataset
    if site == "Explain":
        st.title("Gmarket / 의류팀 ")
        st.markdown("")

        # 활용도/의미 섹션
        st.header("활용도/의미")
        st.markdown("")
        st.markdown("[온라인 쇼핑몰 이용 순위](https://cosinkorea.com/mobile/article.html?no=48855)")
        st.markdown(" - 위의 뉴스를 통해 Gmarket이 온라인 쇼핑몰 3위를 하고 있다.")
        st.markdown(" - Gmarket의 주요 구매 품목은 가전/디지털 제품에 한정되고 있다.")
        st.markdown(" - Gmarket의 경쟁력 향상을 위해서는 주요 구매 품목 이외의 경쟁력이 필요함을 알 수 있다.")
        st.markdown("")
        st.markdown("[MZ 세대 사용률](https://www.yna.co.kr/view/AKR20230425039000017)")
        st.markdown(" - 최근 MZ 세대의 의류 구매 방법은 90% 이상이 온라인을 이용한다는 통계")
        st.markdown(" - 남성 의류 시장의 성장 지속 중.")
        st.markdown("")
        st.markdown("[타겟 대상 선택 TOP3](https://www.yna.co.kr/view/AKR20230425039000017)")
        st.markdown(" - 위의 패션앱 순위를 분석한 보고서를 바탕으로 여성의류 판매 전문 앱을 뺀 앱 TO3 크롤링")
        st.markdown(" - 카테고리 : 남성, 아우터")
        st.markdown(" - Gmarket 의류팀은 남성 의류 아우터 분야에서 경쟁력을 확보하고자 함.")
        st.markdown("")
        st.markdown("")

        # 데이터 수집 페이지 섹션
        st.header("데이터 수집 페이지")
        st.markdown("")
        st.subheader("무신사 (Musinsa)")
        st.markdown(" - 크롤링 사이트 : [무신사 아우터 랭킹](https://www.musinsa.com/ranking/best?period=now&age=ALL&mainCategory=002&subCategory=002021&leafCategory=&price=&golf=false&kids=false&newProduct=false&exclusive=false&discount=false&soldOut=false&page=1&viewType=small&priceMin=&priceMax=)")
        st.markdown(" - 대분류 : 아우터")
        st.markdown(" - 전체 수집 : 약 10,000개")
        st.markdown("")

        st.subheader("29cm")
        st.markdown(" - 크롤링 사이트 : [29cm 아우터](https://www.29cm.co.kr/shop/category/list?category_large_code=272100100&category_medium_code=272102100&sort=latest&category_small_code=&page=1&brand=&min_price=&max_price=&is_free_shipping=&is_discount=&is_soldout=&colors=&count=50)")
        st.markdown(" - 대분류 : 아우터")
        st.markdown(" - 전체 수집 : 약 30,000개")
        st.markdown("")

        st.subheader("크림 (Kream)")
        st.markdown(" - 크롤링 사이트 : [크림 아우터](https://kream.co.kr/search?shop_category_id=63&gender=men&sort=popularity_without_trading)")
        st.markdown(" - 대분류 : 아우터")
        st.markdown(" - 전체 : 약 5,000개 (pagedown 기능 활용)")
        st.markdown("")
        st.markdown("")

        # 데이터 분석 과정 섹션
        st.header("데이터 분석 과정")
        st.markdown("각 사이트에서 남성 아우터 카테고리에서 제공하는 데이터 수집:")
        st.markdown("- 랭킹, 브랜드, 상품명, 기존 가격, 판매 가격, 해당 웹페이지, 이미지 등의 정보 수집.")
        st.markdown("")
        st.markdown("")
        st.markdown("수집된 데이터를 바탕으로 사용자에게 다음을 제공")
        st.markdown("- 해당 사이트에서 판매하는 제품의 랭킹을 보여줌.")
        st.markdown("- TOP10 브랜드를 볼 수 있는 페이지 제공.")
        st.markdown("- 각 브랜드별로 해당 사이트에서 판매되는 제품을 보여줌.")
        st.markdown("- 어떤 브랜드의 어떤 상품이 주로 판매되고 있는지 확인 가능.")        


    else:
        st.title("Fashion Brand Analysis")
        
        if site == "29cm":
            df = load_data(1)
        elif site == "Musinsa":
            df = load_data(2)
        elif site == "Kream":
            df = load_data(3)

        # Option
        option = st.sidebar.radio("Select an Option", options=["Ranking", "Brand Selection", "Top 10 Brands"])
        
        if option == "Brand Selection":
            # Dropdown for brand selection
            selected_brand = st.sidebar.selectbox("Select a Brand", options=df['브랜드'].unique())
            
            # Displaying data and images for the selected brand
            brand_data = process_data_for_option_1(df, selected_brand, site)
            display_images_with_toggle(brand_data)
            
        elif option == "Top 10 Brands":
            
            top_10_brands = process_data_for_option_2(df)
            pie_fig, bar_fig = create_pie_bar_chart(top_10_brands)
    #         bar_fig.update_yaxes(tickangle=0)
            st.plotly_chart(pie_fig)
            st.plotly_chart(bar_fig)
            
            # Display summary table
            display_summary_table(top_10_brands)
            
            
        elif option == "Ranking":

            if site == "Kream":
                  df = load_data(4)
                
            # HTML table
            html_table = create_table_with_index_and_images(df)
            st.markdown(html_table, unsafe_allow_html=True)


if __name__ == "__main__":
    streamlit_app()