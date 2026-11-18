import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# --- 1. 페이지 기본 설정 ---
st.set_page_config(page_title="자취방 우선순위 판독기", page_icon="🏠", layout="centered")

# --- 2. 모던 UI 커스텀 CSS 주입 ---
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

html, body, [class*="css"], .stApp {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #F8FAFC !important;
    color: #0F172A !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {background-color: transparent !important;}

.block-container {
    padding-top: 2.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 720px !important;
}

h1, h2, h3, h4, p, span, label {
    color: #0F172A;
}

div[data-testid="stTextInput"] input {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 10px !important;
    padding: 12px 14px !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #4F46E5 !important;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
}

div[data-testid="stRadio"] > label {
    display: none !important;
}
div[data-testid="stRadio"] > div {
    gap: 12px !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"] {
    background-color: #FFFFFF !important;
    border: 1.5px solid #E2E8F0 !important;
    border-radius: 14px !important;
    padding: 16px 20px !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04) !important;
    width: 100% !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {
    border-color: #818CF8 !important;
    background-color: #F5F7FF !important;
    transform: translateY(-1px);
}
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
    border-color: #4F46E5 !important;
    background-color: #EEF2FF !important;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.12) !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"] p {
    color: #1E293B !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    line-height: 1.5 !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p {
    color: #312E81 !important;
    font-weight: 600 !important;
}

div.stButton > button {
    border-radius: 12px !important;
    padding: 0.65rem 1.2rem !important;
    font-weight: 600 !important;
    font-size: 0.98rem !important;
    transition: all 0.2s ease !important;
    border: 1.5px solid #CBD5E1 !important;
    background-color: #FFFFFF !important;
    color: #334155 !important;
}
div.stButton > button:hover {
    border-color: #94A3B8 !important;
    background-color: #F1F5F9 !important;
}
div.stButton > button[kind="primary"] {
    background-color: #4F46E5 !important;
    border-color: #4F46E5 !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25) !important;
}
div.stButton > button[kind="primary"]:hover {
    background-color: #4338CA !important;
    border-color: #4338CA !important;
}
div.stButton > button[kind="primary"] p {
    color: #FFFFFF !important;
}

.ui-card {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 18px;
    padding: 28px;
    box-shadow: 0 4px 20px rgba(15, 23, 42, 0.04);
    margin-bottom: 20px;
}
.badge {
    display: inline-block;
    background-color: #EEF2FF;
    color: #4F46E5;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 5px 12px;
    border-radius: 999px;
    letter-spacing: 0.04em;
    margin-bottom: 12px;
}
.progress-wrapper {
    width: 100%;
    background-color: #E2E8F0;
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
    margin-top: 8px;
    margin-bottom: 24px;
}
.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #6366F1 0%, #4F46E5 100%);
    border-radius: 999px;
    transition: width 0.35s ease;
}
.metric-box {
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 14px 12px;
    text-align: center;
}
.metric-label {
    font-size: 0.8rem;
    color: #64748B;
    font-weight: 600;
    margin-bottom: 4px;
}
.metric-value {
    font-size: 1.25rem;
    color: #0F172A;
    font-weight: 800;
}
.guide-card-must {
    background-color: #F0FDF4;
    border: 1px solid #BBF7D0;
    border-radius: 16px;
    padding: 22px;
    height: 100%;
}
.guide-card-drop {
    background-color: #FFF1F2;
    border: 1px solid #FECDD3;
    border-radius: 16px;
    padding: 22px;
    height: 100%;
}
.guide-item {
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 10px;
    padding: 12px 14px;
    margin-top: 10px;
    font-size: 0.92rem;
    color: #1E293B;
    font-weight: 500;
    line-height: 1.45;
}
</style>
""", unsafe_allow_html=True)

# --- 3. 세션 상태(Session State) 초기화 ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

# --- 4. 비밀번호 인증 ---
if not st.session_state.authenticated:
    st.markdown("""
    <div class="ui-card" style="margin-top: 40px;">
        <span class="badge">PNU MIS PROJECT</span>
        <h2 style="margin: 0 0 8px 0; font-size: 1.6rem; font-weight: 800;">자취방 우선순위 판독기</h2>
        <p style="color: #64748B; font-size: 0.95rem; margin-bottom: 0;">시스템 접근을 위해 인증 비밀번호를 입력해 주세요.</p>
    </div>
    """, unsafe_allow_html=True)
    
    password = st.text_input("비밀번호", type="password", placeholder="비밀번호 입력", label_visibility="collapsed")
    st.write("")
    if st.button("시스템 접속", type="primary", use_container_width=True):
        if password == "pnumis":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("비밀번호가 일치하지 않습니다.")
    st.stop()

# --- 5. 10개의 4지선다 질문 데이터 (4대 지수 누적 풀 각 30점 균형 설계) ---
QUESTIONS = [
    {
        "q": "Q1. 한 달에 숨만 쉬고 나가는 월세, 나의 마지노선은?",
        "options": [
            {"text": "① 부모님 등골 브레이커는 면하자! 무조건 저렴한 방이 최고", "scores": {"cost": 3}},
            {"text": "② 방음·치안 확실한 신축·고층이라면 월세를 더 낼 의향 있음", "scores": {"defense": 3}},
            {"text": "③ 채광 좋고 넓은 방에서 제대로 힐링하려면 투자는 필수", "scores": {"home": 3}},
            {"text": "④ 학교·역 코앞 초역세권 인프라를 누릴 수 있다면 돈 안 아낌", "scores": {"lazy": 3}},
        ]
    },
    {
        "q": "Q2. 자취방에서 나의 주된 식생활은?",
        "options": [
            {"text": "① 벌레 꼬일까 봐 집에서 조리 금지! 깔끔하게 밖에서 해결", "scores": {"defense": 2, "lazy": 1}},
            {"text": "② 방구석 흑백요리사 (도마부터 향신료까지 풀세팅 요리)", "scores": {"home": 3}},
            {"text": "③ 배달앱 VVIP (문 앞까지 바로 오는 역세권·상권이 최고)", "scores": {"lazy": 3}},
            {"text": "④ 햇반·밀키트·학식 위주 (주방 옵션 줄이고 월세·식비 절약)", "scores": {"cost": 3}},
        ]
    },
    {
        "q": "Q3. 주말 오후 2시, 나는 어디서 무엇을 하고 있을까?",
        "options": [
            {"text": "① 이불 밖은 위험해! 넓은 방에서 넷플릭스 보며 귤 까먹는 중", "scores": {"home": 3}},
            {"text": "② 무조건 밖으로! 집 바로 앞 핫플·맛집·편의시설 도장 깨기", "scores": {"lazy": 3}},
            {"text": "③ 도서관·카공족 빙의 (집은 잠만 자는 곳이라 방 스펙 상관없음)", "scores": {"cost": 2, "lazy": 1}},
            {"text": "④ 햇살 가득한 창가에서 홈카페 열고 인테리어 소품 정리", "scores": {"home": 2, "defense": 1}},
        ]
    },
    {
        "q": "Q4. 방에 거대한 바퀴벌레가 나타났다! 나의 반응은?",
        "options": [
            {"text": "① 당장 짐 싸서 집 앞 24시간 카페나 친구 자취방으로 피신함", "scores": {"lazy": 3}},
            {"text": "② '어, 왔니?' 휴지로 쿨하게 잡아서 변기에 내림", "scores": {"cost": 3}},
            {"text": "③ 소름 돋아서 기절 직전, 방역 업체 부르고 트라우마 생김", "scores": {"defense": 3}},
            {"text": "④ 벌레 나올까 봐 애초에 신축 고층·배수구 트랩 완벽한 곳만 찾음", "scores": {"defense": 2, "home": 1}},
        ]
    },
    {
        "q": "Q5. 밤 11시, 옆집에서 통화하는 말소리가 들린다. 나의 멘탈은?",
        "options": [
            {"text": "① 거슬려서 잠을 설침, 이중창·콘크리트 벽돌 가벽 필수", "scores": {"defense": 3}},
            {"text": "② 노이즈 캔슬링 이어폰 끼고 내 방에서 영화 틀면 그만", "scores": {"home": 2, "defense": 1}},
            {"text": "③ '잘 자네~' 머리 대면 3초 만에 기절해서 전혀 안 들림", "scores": {"cost": 3}},
            {"text": "④ 잠귀가 예민해 스트레스 폭발! 조용한 탑층·신축만 고집함", "scores": {"defense": 2, "lazy": 1}},
        ]
    },
    {
        "q": "Q6. 아침 9시 1교시 수업(또는 출근), 집에서 역/학교까지 이동 시간은?",
        "options": [
            {"text": "① '1분이라도 더 자야 해!' 슬리퍼 신고 5분 컷 초역세권 필수", "scores": {"lazy": 3}},
            {"text": "② '버스 한 번 타면 되지 뭐' 조금 멀어도 넓고 쾌적한 방 선호", "scores": {"home": 3}},
            {"text": "③ '등산이 곧 운동이다' 가파른 언덕 위라도 월세만 싸면 환영", "scores": {"cost": 3}},
            {"text": "④ '10분 내외 평지 도보 OK' 집 주변에 편의점·카페만 있으면 됨", "scores": {"lazy": 2, "defense": 1}},
        ]
    },
    {
        "q": "Q7. 밤늦게 혼자 귀가할 때, 집 주변 골목길 분위기는?",
        "options": [
            {"text": "① '누가 나 같은 걸 건드려' 치안보단 저렴한 보증금·월세가 우선", "scores": {"cost": 3}},
            {"text": "② 어둡고 으슥한 골목길은 절대 불가! 대로변·CCTV·공동현관 필수", "scores": {"defense": 3}},
            {"text": "③ 1층에 편의점이나 24시간 가게가 있어 밤에도 불 켜진 번화가 선호", "scores": {"lazy": 3}},
            {"text": "④ 가로등 켜진 주택가 골목도 무난, 안전과 월세의 균형 중시", "scores": {"defense": 2, "cost": 1}},
        ]
    },
    {
        "q": "Q8. 자취방에 친구들을 초대하는 것에 대한 나의 생각은?",
        "options": [
            {"text": "① 가끔 친한 친구 1~2명 불러서 홈파티·영화 감상 즐기는 편", "scores": {"home": 3}},
            {"text": "② 방은 좁아도 상관없음, 집 앞 번화가 술집·카페에서 만나면 됨", "scores": {"lazy": 2, "cost": 1}},
            {"text": "③ '우리 집은 성역이다' 외부인 출입 금지, 조용한 프라이버시 중시", "scores": {"defense": 3}},
            {"text": "④ '오늘 우리 집에서 모여!' 넓고 쾌적한 아지트 로망이 있음", "scores": {"home": 2, "lazy": 1}},
        ]
    },
    {
        "q": "Q9. 빨래와 청소에 대한 나의 현실적인 모습은?",
        "options": [
            {"text": "① 화장실 창문 없으면 곰팡이 필까 봐 숨 막힘, 환기·위생 집착러", "scores": {"defense": 3}},
            {"text": "② 대충 살자! 먼지 좀 있어도 월세 저렴하고 내 몸만 편하면 그만", "scores": {"cost": 3}},
            {"text": "③ 방 안에 드럼세탁기와 건조기(또는 널찍한 베란다)가 꼭 있어야 함", "scores": {"home": 3}},
            {"text": "④ 옷 쌓아뒀다가 주말에 코인세탁소 가서 한 번에 해결함", "scores": {"cost": 2, "lazy": 1}},
        ]
    },
    {
        "q": "Q10. 자취방 창문을 열었을 때, 내가 가장 바라는 뷰(View)와 채광은?",
        "options": [
            {"text": "① 창밖 뷰보단 문 열고 나갔을 때 정류장·상권이 코앞인 입지가 중요", "scores": {"lazy": 3}},
            {"text": "② 창문 열었을 때 뻥 뚫린 시티뷰나 공원 뷰가 보이는 방콕 감성 중시", "scores": {"home": 3}},
            {"text": "③ 낮에 집에 없으니 창문 열면 앞집 벽이 보여도 월세만 싸면 OK", "scores": {"cost": 3}},
            {"text": "④ 습기·결로·곰팡이 방지! 맞통풍 잘 되고 채광 좋은 남향 필수", "scores": {"home": 2, "defense": 1}},
        ]
    }
]

# --- 6. 화면 렌더링 로직 ---

# [Step 0: 메인 시작 화면]
if st.session_state.step == 0:
    st.markdown("""
    <div class="ui-card" style="margin-top: 20px;">
        <span class="badge">HOUSING PRIORITY ANALYZER</span>
        <h1 style="font-size: 2rem; font-weight: 800; line-height: 1.3; margin: 0 0 14px 0;">
            대학생 자취방<br>우선순위 판독기
        </h1>
        <p style="color: #475569; font-size: 1.02rem; line-height: 1.65; margin-bottom: 24px;">
            한정된 예산 안에서 모든 조건을 갖춘 방을 찾기란 불가능합니다.<br>
            10가지 라이프스타일 문항을 통해 <b>반드시 사수해야 할 조건 TOP 3</b>와 
            <b>과감히 타협해 월세를 아낄 조건 TOP 3</b>를 정밀하게 도출합니다.
        </p>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 8px;">
            <div class="metric-box" style="text-align: left; padding: 14px 16px;">
                <div style="font-weight: 700; color: #4F46E5; font-size: 0.85rem;">01 · 통장수호 지수</div>
                <div style="font-size: 0.85rem; color: #64748B; margin-top: 2px;">월세 및 고정지출 민감도</div>
            </div>
            <div class="metric-box" style="text-align: left; padding: 14px 16px;">
                <div style="font-weight: 700; color: #4F46E5; font-size: 0.85rem;">02 · 예민보스 지수</div>
                <div style="font-size: 0.85rem; color: #64748B; margin-top: 2px;">방음·위생·치안 요구 수준</div>
            </div>
            <div class="metric-box" style="text-align: left; padding: 14px 16px;">
                <div style="font-weight: 700; color: #4F46E5; font-size: 0.85rem;">03 · 방구석라이프 지수</div>
                <div style="font-size: 0.85rem; color: #64748B; margin-top: 2px;">채광·주방·실내 거주 비중</div>
            </div>
            <div class="metric-box" style="text-align: left; padding: 14px 16px;">
                <div style="font-weight: 700; color: #4F46E5; font-size: 0.85rem;">04 · 귀차니즘 지수</div>
                <div style="font-size: 0.85rem; color: #64748B; margin-top: 2px;">통학 거리 및 주변 인프라</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("진단 시작하기 →", type="primary", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

# [Step 1 ~ 10: 질문 화면]
elif 1 <= st.session_state.step <= 10:
    current_idx = st.session_state.step - 1
    q_data = QUESTIONS[current_idx]
    progress_pct = int((st.session_state.step / 10) * 100)

    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 0.85rem; font-weight: 700; color: #4F46E5;">QUESTION {st.session_state.step:02d} / 10</span>
        <span style="font-size: 0.85rem; font-weight: 700; color: #64748B;">{progress_pct}% 완료</span>
    </div>
    <div class="progress-wrapper">
        <div class="progress-fill" style="width: {progress_pct}%;"></div>
    </div>
    <div class="ui-card" style="padding: 24px 28px; margin-bottom: 18px;">
        <h3 style="margin: 0; font-size: 1.28rem; font-weight: 700; line-height: 1.45; color: #0F172A;">
            {q_data["q"]}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    option_texts = [opt["text"] for opt in q_data["options"]]
    default_idx = st.session_state.answers.get(current_idx, 0)
    choice = st.radio("선택지", option_texts, index=default_idx, key=f"radio_{current_idx}")
    
    st.write("")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.session_state.step > 1:
            if st.button("← 이전 문항", use_container_width=True):
                st.session_state.answers[current_idx] = option_texts.index(choice)
                st.session_state.step -= 1
                st.rerun()
    with col2:
        btn_label = "다음 문항 →" if st.session_state.step < 10 else "분석 리포트 확인하기"
        if st.button(btn_label, type="primary", use_container_width=True):
            st.session_state.answers[current_idx] = option_texts.index(choice)
            st.session_state.step += 1
            st.rerun()

# [Step 11: 결과 분석 화면]
elif st.session_state.step == 11:
    with st.spinner('응답 데이터를 기반으로 우선순위를 산출하고 있습니다...'):
        time.sleep(0.8)
        
    # 1. 점수 합산 로직
    totals = {"cost": 0, "defense": 0, "home": 0, "lazy": 0}
    for q_idx, opt_idx in st.session_state.answers.items():
        scores = QUESTIONS[q_idx]["options"][opt_idx]["scores"]
        for k, v in scores.items():
            totals[k] += v
            
    # 최소 1점 보정 (레이더 차트 형태 유지)
    for k in totals:
        if totals[k] < 1:
            totals[k] = 1

    label_map = {
        "cost": "통장수호 지수 (가성비)", 
        "defense": "예민보스 지수 (방음/치안)", 
        "home": "방구석라이프 지수 (채광/크기)", 
        "lazy": "귀차니즘 지수 (교통/인프라)"
    }
    
    sorted_stats = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    best_stat_key = sorted_stats[0][0]
    worst_stat_key = sorted_stats[-1][0]
    
    best_stat_name = label_map[best_stat_key]
    worst_stat_name = label_map[worst_stat_key]

    # 상단 리포트 헤더 카드
    st.markdown(f"""
    <div class="ui-card" style="margin-bottom: 20px;">
        <span class="badge">ANALYSIS REPORT</span>
        <h1 style="font-size: 1.75rem; font-weight: 800; margin: 0 0 8px 0;">맞춤형 자취방 우선순위 리포트</h1>
        <p style="color: #475569; font-size: 0.96rem; margin: 0;">
            가장 높은 우선순위는 <b style="color: #4F46E5;">{best_stat_name}</b>이며, 
            상대적으로 타협 가능한 영역은 <b style="color: #E11D48;">{worst_stat_name}</b>입니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 1. 영역별 주거 중요도 프로파일 (레이더 차트 + 지표 요약 카드)
    st.markdown("""
    <div class="ui-card" style="padding-bottom: 16px;">
        <h3 style="font-size: 1.15rem; font-weight: 700; margin: 0 0 4px 0;">영역별 주거 중요도 프로파일</h3>
        <p style="font-size: 0.85rem; color: #64748B; margin: 0 0 12px 0;">4대 핵심 지표별 누적 가중치 분포</p>
    """, unsafe_allow_html=True)

    m_cols = st.columns(4)
    short_names = ["통장수호", "예민보스", "방구석라이프", "귀차니즘"]
    stat_keys = ["cost", "defense", "home", "lazy"]
    for idx, col in enumerate(m_cols):
        val = totals[stat_keys[idx]]
        is_top = (stat_keys[idx] == best_stat_key)
        border_style = "border: 1.5px solid #4F46E5; background-color: #EEF2FF;" if is_top else ""
        val_color = "#4F46E5" if is_top else "#0F172A"
        with col:
            st.markdown(f"""
            <div class="metric-box" style="{border_style}">
                <div class="metric-label">{short_names[idx]}</div>
                <div class="metric-value" style="color: {val_color};">{val}점</div>
            </div>
            """, unsafe_allow_html=True)

    categories = [
        "통장수호 지수<br>(가성비)",
        "예민보스 지수<br>(방음·치안)",
        "방구석라이프 지수<br>(채광·공간)",
        "귀차니즘 지수<br>(교통·인프라)"
    ]
    values = [totals["cost"], totals["defense"], totals["home"], totals["lazy"]]
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]
    max_range = max(values) + 3

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(99, 102, 241, 0.20)',
        line=dict(color='#4F46E5', width=3),
        marker=dict(size=9, color='#FFFFFF', line=dict(color='#4F46E5', width=2.5)),
        hovertemplate='<b>%{theta}</b><br>획득 점수: %{r}점<extra></extra>'
    ))

    fig.update_layout(
        polar=dict(
            bgcolor='rgba(248, 250, 252, 0.6)',
            radialaxis=dict(
                visible=True,
                range=[0, max_range],
                showticklabels=False,
                gridcolor='#E2E8F0',
                linecolor='rgba(0,0,0,0)'
            ),
            angularaxis=dict(
                tickfont=dict(size=12.5, color='#1E293B', family='Pretendard'),
                gridcolor='#E2E8F0',
                linecolor='#CBD5E1',
                rotation=90,
                direction="clockwise"
            )
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=360,
        margin=dict(l=65, r=65, t=35, b=35)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. 사수할 조건 TOP 3 vs 버려도 될 조건 TOP 3
    MUST_HAVE_MAP = {
        "cost": ["① 보증금·월세 시세보다 저렴한 급매물", "② 관리비에 수도·인터넷이 포함된 방", "③ 옵션이 다소 부족해도 기본 구조가 멀쩡한 방"],
        "defense": ["① 벌레 차단! 3층 이상 고층 & 신축·리모델링", "② 층간소음 방지! 콘크리트 가벽 및 탑층", "③ 밤길 안전! 대로변 위치 + 공동현관 CCTV"],
        "home": ["① 우울감 타파! 햇빛 쨍쨍한 남향 채광", "② 냄새 차단! 분리형 원룸 또는 1.5룸 구조", "③ 넉넉한 수납공간 및 내부 풀옵션 구비"],
        "lazy": ["① 1분이라도 더 자자! 도보 5분 이내 초역세권", "② 슬리퍼 상권! 도보 1분 컷 편의점 필수", "③ 밤늦게 귀가해도 환한 메인 상권 인접지"]
    }

    DROP_MAP = {
        "cost": ["① 굳이 역 코앞 고집하기 (조금만 걸어도 월세 10만 원 세이브)", "② 최신식 풀옵션 신축 오피스텔 (높은 관리비의 주범)", "③ 불필요하게 넓은 평수 (청소 부담 및 냉난방비 증가)"],
        "defense": ["① 신축 연식 집착 (구축이라도 도배·장판만 깔끔하면 OK)", "② 층수 제한 (1~2층도 방범창·방충망만 확인하면 가성비 우수)", "③ 대로변 프리미엄 (조용한 주택가 골목으로 보증금 절약)"],
        "home": ["① 남향 채광 집착 (낮에 외출 비중이 높다면 북향·동향으로 월세 절약)", "② 큰 주방 및 분리형 구조 (인덕션 1구 오픈형 원룸으로 충분)", "③ 탁 트인 전망(View) (창문 앞이 막혀도 수면·휴식엔 무관)"],
        "lazy": ["① 완전 평지 입지 (약간의 오르막을 감수하고 쾌적한 컨디션 확보)", "② 번화가 중심 상권 (식당가에서 벗어난 조용한 외곽 선택)", "③ 초역세권 도보 거리 (마을버스 10분 거리로 방 크기 업그레이드)"]
    }

    col1, col2 = st.columns(2)
    with col1:
        items_html = "".join([f'<div class="guide-item">{item}</div>' for item in MUST_HAVE_MAP[best_stat_key]])
        st.markdown(f"""
        <div class="guide-card-must">
            <div style="font-size: 0.78rem; font-weight: 700; color: #15803D; letter-spacing: 0.03em;">MUST-HAVE PRIORITY</div>
            <h4 style="margin: 4px 0 6px 0; font-size: 1.1rem; font-weight: 800; color: #14532D;">절대 사수할 조건 TOP 3</h4>
            <p style="font-size: 0.82rem; color: #166534; margin: 0 0 12px 0;">최우선 지표: <b>{best_stat_name}</b></p>
            {items_html}
        </div>
        """, unsafe_allow_html=True)
            
    with col2:
        drop_html = "".join([f'<div class="guide-item">{item}</div>' for item in DROP_MAP[worst_stat_key]])
        st.markdown(f"""
        <div class="guide-card-drop">
            <div style="font-size: 0.78rem; font-weight: 700; color: #BE123C; letter-spacing: 0.03em;">BUDGET SAVING</div>
            <h4 style="margin: 4px 0 6px 0; font-size: 1.1rem; font-weight: 800; color: #881337;">과감히 포기할 조건 TOP 3</h4>
            <p style="font-size: 0.82rem; color: #9F1239; margin: 0 0 12px 0;">후순위 지표: <b>{worst_stat_name}</b></p>
            {drop_html}
        </div>
        """, unsafe_allow_html=True)
            
    st.write("")
    st.write("")
    if st.button("처음부터 다시 진단하기", use_container_width=True):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()
