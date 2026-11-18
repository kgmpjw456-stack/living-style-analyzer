import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# --- 1. 페이지 기본 설정 ---
st.set_page_config(page_title="자취방 구하기 전, 나의 라이프 파악하기", page_icon="🛋️", layout="centered")

# --- 2. 모던 반응형 CSS & 웹폰트 주입 ---
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
@font-face {
    font-family: 'GmarketSans';
    src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_2001@1.1/GmarketSansMedium.woff') format('woff');
    font-weight: 500;
    font-style: normal;
}
@font-face {
    font-family: 'GmarketSans';
    src: url('https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_2001@1.1/GmarketSansBold.woff') format('woff');
    font-weight: 700;
    font-style: normal;
}

html, body, [class*="css"], .stApp {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #F8FAFC !important;
    color: #0F172A !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {background-color: transparent !important;}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 740px !important;
}

/* 첫 화면 & 결과 상단 공통 히어로 박스 */
.hero-box {
    background: linear-gradient(145deg, #FFFFFF 0%, #F5F7FF 100%);
    border: 1.5px solid #E2E8F0;
    border-radius: 28px;
    padding: 38px 26px;
    text-align: center;
    box-shadow: 0 12px 36px -10px rgba(79, 70, 229, 0.12);
    margin-bottom: 24px;
}
.hero-emoji {
    font-size: 4.2rem;
    margin-bottom: 12px;
    display: inline-block;
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}
.hero-title {
    font-family: 'GmarketSans', 'Pretendard', sans-serif !important;
    font-size: 1.95rem;
    font-weight: 700;
    line-height: 1.38;
    margin: 0 0 14px 0;
    color: #0F172A;
    word-break: keep-all;
}
.hero-highlight {
    background: linear-gradient(135deg, #4F46E5 0%, #EC4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-desc {
    color: #475569;
    font-size: 1rem;
    line-height: 1.65;
    margin: 0 0 26px 0;
    word-break: keep-all;
}
.pill-badge {
    display: inline-block;
    background: linear-gradient(135deg, #EEF2FF 0%, #FCE7F3 100%);
    color: #4338CA;
    padding: 6px 15px;
    border-radius: 999px;
    font-family: 'GmarketSans', sans-serif !important;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    margin-bottom: 14px;
    border: 1px solid #C7D2FE;
}
.feature-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
}
.feature-item {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 18px;
    text-align: left;
    border: 1.5px solid #E2E8F0;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
}
.feature-item:hover {
    transform: translateY(-3px);
    background: #EEF2FF;
    border-color: #A5B4FC;
    box-shadow: 0 8px 18px rgba(79, 70, 229, 0.1);
}
.feature-icon {
    font-size: 1.6rem;
    margin-bottom: 6px;
}

/* 질문 화면 전용 히어로 카드 */
.q-hero-card {
    background: linear-gradient(145deg, #FFFFFF 0%, #F5F7FF 100%);
    border: 1.5px solid #E0E7FF;
    border-radius: 24px;
    padding: 28px 24px;
    text-align: center;
    box-shadow: 0 10px 30px -8px rgba(79, 70, 229, 0.12);
    margin-bottom: 20px;
}
.q-emoji-badge {
    font-size: 3.1rem;
    line-height: 1;
    margin-bottom: 12px;
    display: inline-block;
    animation: float 3.2s ease-in-out infinite;
}
.q-main-title {
    font-family: 'GmarketSans', 'Pretendard', sans-serif !important;
    font-size: 1.38rem;
    font-weight: 700;
    line-height: 1.48;
    color: #0F172A;
    margin: 0;
    word-break: keep-all;
}

/* 선지(라디오 버튼) 스타일링 */
div[data-testid="stRadio"] > label {
    display: none !important;
}
div[data-testid="stRadio"] > div {
    gap: 14px !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"] {
    background-color: #FFFFFF !important;
    border: 2px solid #E2E8F0 !important;
    border-radius: 18px !important;
    padding: 20px 22px !important;
    cursor: pointer !important;
    width: 100% !important;
    height: auto !important;
    min-height: 68px !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 3px 10px rgba(15, 23, 42, 0.04) !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {
    border-color: #818CF8 !important;
    background: linear-gradient(135deg, #FFFFFF 0%, #F5F7FF 100%) !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(79, 70, 229, 0.1) !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
    border-color: #4F46E5 !important;
    background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%) !important;
    box-shadow: 0 8px 22px rgba(79, 70, 229, 0.18) !important;
    transform: translateY(-1px);
}
div[data-testid="stRadio"] label[data-baseweb="radio"] p {
    color: #1E293B !important;
    font-size: 1.08rem !important;
    font-weight: 600 !important;
    white-space: normal !important;
    word-break: keep-all !important;
    line-height: 1.5 !important;
}
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p {
    color: #1E1B4B !important;
    font-weight: 700 !important;
}

/* 진행률 바 */
.progress-wrapper {
    width: 100%;
    background-color: #E2E8F0;
    border-radius: 999px;
    height: 10px;
    margin-top: 8px;
    margin-bottom: 20px;
    overflow: hidden;
    box-shadow: inset 0 1px 2px rgba(0,0,0,0.06);
}
.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #4F46E5 0%, #EC4899 100%);
    border-radius: 999px;
    transition: width 0.35s ease;
}

/* 버튼 디자인 */
div.stButton > button {
    border-radius: 16px !important;
    padding: 0.75rem 1.2rem !important;
    font-family: 'GmarketSans', 'Pretendard', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: 1.5px solid #CBD5E1 !important;
    background-color: #FFFFFF !important;
    color: #334155 !important;
    transition: all 0.2s ease !important;
}
div.stButton > button:hover {
    border-color: #94A3B8 !important;
    background-color: #F1F5F9 !important;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4F46E5 0%, #6366F1 100%) !important;
    border: none !important;
    color: #FFFFFF !important;
    box-shadow: 0 6px 18px rgba(79, 70, 229, 0.28) !important;
    padding: 0.85rem 1.2rem !important;
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #4338CA 0%, #4F46E5 100%) !important;
    transform: translateY(-1px);
}
div.stButton > button[kind="primary"] p {
    color: #FFFFFF !important;
}

/* 입력창 및 결과 화면 카드 */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #FAFBFD 100%) !important;
    border: 1.5px solid #E0E7FF !important;
    border-radius: 24px !important;
    padding: 22px 24px !important;
    box-shadow: 0 10px 30px -8px rgba(79, 70, 229, 0.09) !important;
    margin-bottom: 22px !important;
}
div[data-testid="stTextInput"] input {
    background-color: #FFFFFF !important;
    border: 1.5px solid #CBD5E1 !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    font-size: 1rem !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #4F46E5 !important;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
}

/* 결과 화면 4대 지수 미니 카드 */
.metric-box {
    background-color: #F8FAFC;
    border: 1.5px solid #E2E8F0;
    border-radius: 16px;
    padding: 14px 8px;
    text-align: center;
    transition: all 0.2s ease;
}
.metric-box-top {
    background: linear-gradient(145deg, #EEF2FF 0%, #FCE7F3 100%);
    border: 1.5px solid #6366F1;
    border-radius: 16px;
    padding: 14px 8px;
    text-align: center;
    box-shadow: 0 6px 16px -4px rgba(79, 70, 229, 0.18);
}
.metric-icon {
    font-size: 1.25rem;
    margin-bottom: 4px;
}
.metric-label {
    font-size: 0.78rem;
    color: #64748B;
    font-weight: 700;
    margin-bottom: 4px;
}
.metric-value {
    font-family: 'GmarketSans', sans-serif !important;
    font-size: 1.22rem;
    color: #0F172A;
    font-weight: 700;
}

/* 결과 화면 하단 조건 카드 */
.guide-card-must {
    background: linear-gradient(145deg, #F0FDF4 0%, #DCFCE7 100%);
    border: 1.5px solid #86EFAC;
    border-radius: 22px;
    padding: 22px 20px;
    height: 100%;
    box-shadow: 0 10px 26px -8px rgba(22, 163, 74, 0.16);
}
.guide-card-drop {
    background: linear-gradient(145deg, #FFF1F2 0%, #FFE4E6 100%);
    border: 1.5px solid #FDA4AF;
    border-radius: 22px;
    padding: 22px 20px;
    height: 100%;
    box-shadow: 0 10px 26px -8px rgba(225, 29, 72, 0.16);
}
.guide-pill-must {
    display: inline-block;
    background-color: #FFFFFF;
    color: #15803D;
    font-family: 'GmarketSans', sans-serif !important;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 4px 11px;
    border-radius: 999px;
    border: 1px solid #86EFAC;
    margin-bottom: 10px;
}
.guide-pill-drop {
    display: inline-block;
    background-color: #FFFFFF;
    color: #BE123C;
    font-family: 'GmarketSans', sans-serif !important;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 4px 11px;
    border-radius: 999px;
    border: 1px solid #FDA4AF;
    margin-bottom: 10px;
}
.guide-item {
    background-color: #FFFFFF;
    border-radius: 13px;
    padding: 12px 14px;
    margin-top: 9px;
    font-size: 0.95rem;
    color: #1E293B;
    font-weight: 600;
    line-height: 1.45;
    word-break: keep-all;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
}

@media (max-width: 600px) {
    .hero-title { font-size: 1.55rem !important; }
    .hero-emoji { font-size: 3.3rem !important; }
    .q-main-title { font-size: 1.18rem !important; }
    .feature-grid { grid-template-columns: 1fr !important; }
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
<div class="hero-box" style="padding: 32px 20px;">
<div class="hero-emoji" style="font-size: 3.2rem;">🔐</div>
<h2 class="hero-title" style="font-size: 1.45rem; margin-bottom: 8px;">자취방 구하기 전, 나의 라이프 파악하기</h2>
<p style="color: #64748B; font-size: 0.94rem; margin: 0;">계속하려면 입장 비밀번호를 입력해 주세요.</p>
</div>
""", unsafe_allow_html=True)

    password = st.text_input("비밀번호", type="password", placeholder="비밀번호 입력", label_visibility="collapsed")
    st.write("")
    if st.button("입장하기 🚀", type="primary", use_container_width=True):
        if password == "pnumis":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("비밀번호가 일치하지 않습니다.")
    st.stop()

# --- 5. 10개의 4지선다 질문 데이터 (이모지 + 테마 + 균형 배점) ---
QUESTIONS = [
    {
        "emoji": "💸",
        "tag": "STEP 01 · 월세 & 예산 기준",
        "q_head": "한 달에 숨만 쉬고 나가는 월세,",
        "q_highlight": "나의 마지노선은?",
        "options": [
            {"text": "💰 부모님 등골 브레이커는 면하자! 무조건 저렴한 방이 최고", "scores": {"cost": 3}},
            {"text": "🛡️ 방음·치안 확실한 신축·고층이라면 월세를 더 낼 의향 있음", "scores": {"defense": 3}},
            {"text": "🪟 채광 좋고 넓은 방에서 제대로 힐링하려면 투자는 필수", "scores": {"home": 3}},
            {"text": "🚇 학교·역 코앞 초역세권 인프라를 누릴 수 있다면 돈 안 아낌", "scores": {"lazy": 3}},
        ]
    },
    {
        "emoji": "🍽️",
        "tag": "STEP 02 · 식생활 & 주방 활용",
        "q_head": "자취방에서 이루어지는",
        "q_highlight": "나의 주된 식생활은?",
        "options": [
            {"text": "🚫 벌레 꼬일까 봐 집에서 조리 금지! 깔끔하게 밖에서 해결", "scores": {"defense": 2, "lazy": 1}},
            {"text": "🍳 방구석 흑백요리사 (도마부터 향신료까지 풀세팅 요리)", "scores": {"home": 3}},
            {"text": "🛵 배달앱 VVIP (문 앞까지 바로 오는 역세권·상권이 최고)", "scores": {"lazy": 3}},
            {"text": "🥡 햇반·밀키트·학식 위주 (주방 옵션 줄이고 월세·식비 절약)", "scores": {"cost": 3}},
        ]
    },
    {
        "emoji": "🛋️",
        "tag": "STEP 03 · 주말 여가 패턴",
        "q_head": "주말 오후 2시,",
        "q_highlight": "나는 어디서 무엇을 하고 있을까?",
        "options": [
            {"text": "🛌 이불 밖은 위험해! 넓은 방에서 넷플릭스 보며 귤 까먹는 중", "scores": {"home": 3}},
            {"text": "🏃 무조건 밖으로! 집 바로 앞 핫플·맛집·편의시설 도장 깨기", "scores": {"lazy": 3}},
            {"text": "📚 도서관·카공족 빙의 (집은 잠만 자는 곳이라 방 스펙 무관)", "scores": {"cost": 2, "lazy": 1}},
            {"text": "☕ 햇살 가득한 창가에서 홈카페 열고 인테리어 소품 정리", "scores": {"home": 2, "defense": 1}},
        ]
    },
    {
        "emoji": "🪳",
        "tag": "STEP 04 · 해충 & 위생 민감도",
        "q_head": "방에 거대한 바퀴벌레가 나타났다!",
        "q_highlight": "나의 현실 반응은?",
        "options": [
            {"text": "🏃 당장 짐 싸서 집 앞 24시간 카페나 친구 자취방으로 피신함", "scores": {"lazy": 3}},
            {"text": "🧻 '어, 왔니?' 휴지로 쿨하게 잡아서 변기에 바로 내림", "scores": {"cost": 3}},
            {"text": "😱 소름 돋아서 기절 직전, 방역 업체 부르고 트라우마 생김", "scores": {"defense": 3}},
            {"text": "🏢 벌레 나올까 봐 애초에 신축 고층·배수구 트랩 완벽한 곳만 찾음", "scores": {"defense": 2, "home": 1}},
        ]
    },
    {
        "emoji": "🔊",
        "tag": "STEP 05 · 소음 & 수면 환경",
        "q_head": "밤 11시, 옆집 통화 소리가 들린다.",
        "q_highlight": "나의 멘탈 상태는?",
        "options": [
            {"text": "🧱 거슬려서 잠을 설침, 이중창·콘크리트 벽돌 가벽 필수", "scores": {"defense": 3}},
            {"text": "🎧 노이즈 캔슬링 이어폰 끼고 내 방에서 영화 틀면 그만", "scores": {"home": 2, "defense": 1}},
            {"text": "😴 '잘 자네~' 머리 대면 3초 만에 기절해서 전혀 안 들림", "scores": {"cost": 3}},
            {"text": "🔇 잠귀가 예민해 스트레스 폭발! 조용한 탑층·신축만 고집함", "scores": {"defense": 2, "lazy": 1}},
        ]
    },
    {
        "emoji": "⏰",
        "tag": "STEP 06 · 통학 & 이동 거리",
        "q_head": "아침 9시 1교시 수업(또는 출근),",
        "q_highlight": "역·학교까지 허용 가능한 이동 시간은?",
        "options": [
            {"text": "⚡ '1분이라도 더 자야 해!' 슬리퍼 신고 5분 컷 초역세권 필수", "scores": {"lazy": 3}},
            {"text": "🚌 '버스 한 번 타면 되지 뭐' 조금 멀어도 넓고 쾌적한 방 선호", "scores": {"home": 3}},
            {"text": "⛰️ '등산이 곧 운동이다' 가파른 언덕 위라도 월세만 싸면 환영", "scores": {"cost": 3}},
            {"text": "👟 '10분 내외 평지 도보 OK' 집 주변에 편의점·카페만 있으면 됨", "scores": {"lazy": 2, "defense": 1}},
        ]
    },
    {
        "emoji": "🌙",
        "tag": "STEP 07 · 귀갓길 치안 & 상권",
        "q_head": "밤늦게 혼자 귀가할 때,",
        "q_highlight": "내가 바라는 집 주변 골목길 분위기는?",
        "options": [
            {"text": "💵 '누가 나 같은 걸 건드려' 치안보단 저렴한 보증금·월세가 우선", "scores": {"cost": 3}},
            {"text": "🚨 어둡고 으슥한 골목길은 절대 불가! 대로변·CCTV·공동현관 필수", "scores": {"defense": 3}},
            {"text": "🏪 1층에 편의점이나 24시간 가게가 있어 밤에도 불 켜진 번화가 선호", "scores": {"lazy": 3}},
            {"text": "💡 가로등 켜진 주택가 골목도 무난, 안전과 월세의 균형 중시", "scores": {"defense": 2, "cost": 1}},
        ]
    },
    {
        "emoji": "🎉",
        "tag": "STEP 08 · 공간 크기 & 프라이버시",
        "q_head": "자취방에 친구들을 초대하는 것에 대한",
        "q_highlight": "나의 솔직한 생각은?",
        "options": [
            {"text": "🍕 가끔 친한 친구 1~2명 불러서 홈파티·영화 감상 즐기는 편", "scores": {"home": 3}},
            {"text": "🍻 방은 좁아도 상관없음, 집 앞 번화가 술집·카페에서 만나면 됨", "scores": {"lazy": 2, "cost": 1}},
            {"text": "🔒 '우리 집은 성역이다' 외부인 출입 금지, 조용한 프라이버시 중시", "scores": {"defense": 3}},
            {"text": "🎈 '오늘 우리 집에서 모여!' 넓고 쾌적한 아지트 로망이 있음", "scores": {"home": 2, "lazy": 1}},
        ]
    },
    {
        "emoji": "🧺",
        "tag": "STEP 09 · 빨래 & 환기 습관",
        "q_head": "빨래와 청소에 대한",
        "q_highlight": "나의 현실적인 생활 모습은?",
        "options": [
            {"text": "🌬️ 화장실 창문 없으면 곰팡이 필까 봐 숨 막힘, 환기·위생 집착러", "scores": {"defense": 3}},
            {"text": "🧹 대충 살자! 먼지 좀 있어도 월세 저렴하고 내 몸만 편하면 그만", "scores": {"cost": 3}},
            {"text": "🧺 방 안에 드럼세탁기와 건조기(또는 널찍한 베란다)가 꼭 있어야 함", "scores": {"home": 3}},
            {"text": "🪙 옷 쌓아뒀다가 주말에 코인세탁소 가서 한 번에 해결함", "scores": {"cost": 2, "lazy": 1}},
        ]
    },
    {
        "emoji": "🪟",
        "tag": "STEP 10 · 채광 & 창밖 뷰",
        "q_head": "자취방 창문을 열었을 때,",
        "q_highlight": "내가 가장 바라는 뷰(View)와 채광은?",
        "options": [
            {"text": "🚏 창밖 뷰보단 문 열고 나갔을 때 정류장·상권이 코앞인 입지가 중요", "scores": {"lazy": 3}},
            {"text": "🌆 창문 열었을 때 뻥 뚫린 시티뷰나 공원 뷰가 보이는 방콕 감성 중시", "scores": {"home": 3}},
            {"text": "🧱 낮에 집에 없으니 창문 열면 앞집 벽이 보여도 월세만 싸면 OK", "scores": {"cost": 3}},
            {"text": "☀️ 습기·결로·곰팡이 방지! 맞통풍 잘 되고 채광 좋은 남향 필수", "scores": {"home": 2, "defense": 1}},
        ]
    }
]

# --- 6. 화면 렌더링 로직 ---

# [Step 0: 메인 웰컴 화면]
if st.session_state.step == 0:
    st.markdown("""
<div class="hero-box">
<div class="hero-emoji">🛋️✨</div>
<div><span class="pill-badge">자취 초보를 위한 성향 테스트</span></div>
<h1 class="hero-title">자취방 구하기 전,<br><span class="hero-highlight">나의 라이프 파악하기 🔍</span></h1>
<p class="hero-desc">부동산에 가기 전, 내 생활 패턴부터 정확히 알아야 <b>소중한 보증금과 월세</b>를 지킬 수 있습니다.<br>10개의 문항으로 나에게 꼭 맞는 맞춤형 자취 조건을 찾아보세요!</p>
<div class="feature-grid">
<div class="feature-item">
<div class="feature-icon">💰</div>
<div style="font-family: 'GmarketSans', sans-serif; font-weight: 700; color: #1E293B; font-size: 0.96rem;">통장수호 지수</div>
<div style="font-size: 0.82rem; color: #64748B; margin-top: 4px;">월세·고정지출 민감도</div>
</div>
<div class="feature-item">
<div class="feature-icon">🛡️</div>
<div style="font-family: 'GmarketSans', sans-serif; font-weight: 700; color: #1E293B; font-size: 0.96rem;">예민보스 지수</div>
<div style="font-size: 0.82rem; color: #64748B; margin-top: 4px;">방음·위생·치안 요구 수준</div>
</div>
<div class="feature-item">
<div class="feature-icon">🪟</div>
<div style="font-family: 'GmarketSans', sans-serif; font-weight: 700; color: #1E293B; font-size: 0.96rem;">방구석라이프 지수</div>
<div style="font-size: 0.82rem; color: #64748B; margin-top: 4px;">채광·주방·실내 거주 비중</div>
</div>
<div class="feature-item">
<div class="feature-icon">🚶</div>
<div style="font-family: 'GmarketSans', sans-serif; font-weight: 700; color: #1E293B; font-size: 0.96rem;">귀차니즘 지수</div>
<div style="font-size: 0.82rem; color: #64748B; margin-top: 4px;">통학 거리 및 상권 인프라</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    if st.button("🚀 내 라이프 진단 시작하기", type="primary", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

# [Step 1 ~ 10: 질문 화면]
elif 1 <= st.session_state.step <= 10:
    current_idx = st.session_state.step - 1
    q_data = QUESTIONS[current_idx]
    progress_pct = int((st.session_state.step / 10) * 100)

    st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center;">
<span style="font-family: 'GmarketSans', sans-serif; font-size: 0.88rem; font-weight: 700; color: #4F46E5;">QUESTION {st.session_state.step:02d} / 10</span>
<span style="font-family: 'GmarketSans', sans-serif; font-size: 0.88rem; font-weight: 700; color: #EC4899;">{progress_pct}%</span>
</div>
<div class="progress-wrapper">
<div class="progress-fill" style="width: {progress_pct}%;"></div>
</div>
<div class="q-hero-card">
<div class="q-emoji-badge">{q_data["emoji"]}</div>
<div><span class="pill-badge">{q_data["tag"]}</span></div>
<h2 class="q-main-title">{q_data["q_head"]}<br><span class="hero-highlight">{q_data["q_highlight"]}</span></h2>
</div>
""", unsafe_allow_html=True)

    option_texts = [opt["text"] for opt in q_data["options"]]
    default_idx = st.session_state.answers.get(current_idx, 0)
    choice = st.radio("선택지", option_texts, index=default_idx, key=f"radio_{current_idx}")

    st.write("")

    col1, col2 = st.columns([1, 2])
    with col1:
        if st.session_state.step > 1:
            if st.button("← 이전", use_container_width=True):
                st.session_state.answers[current_idx] = option_texts.index(choice)
                st.session_state.step -= 1
                st.rerun()
    with col2:
        btn_label = "다음 문항 →" if st.session_state.step < 10 else "분석 결과 확인하기 ✨"
        if st.button(btn_label, type="primary", use_container_width=True):
            st.session_state.answers[current_idx] = option_texts.index(choice)
            st.session_state.step += 1
            st.rerun()

# [Step 11: 생동감 있게 리뉴얼된 결과 분석 화면]
elif st.session_state.step == 11:
    with st.spinner('내 라이프스타일에 맞는 방 조건을 정리 중입니다...'):
        time.sleep(0.8)

    totals = {"cost": 0, "defense": 0, "home": 0, "lazy": 0}
    for q_idx, opt_idx in st.session_state.answers.items():
        scores = QUESTIONS[q_idx]["options"][opt_idx]["scores"]
        for k, v in scores.items():
            totals[k] += v

    for k in totals:
        if totals[k] < 1:
            totals[k] = 1

    label_map = {
        "cost": "통장수호 지수",
        "defense": "예민보스 지수",
        "home": "방구석라이프 지수",
        "lazy": "귀차니즘 지수"
    }
    emoji_map = {
        "cost": "💰",
        "defense": "🛡️",
        "home": "🪟",
        "lazy": "🚶"
    }

    sorted_stats = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    best_stat_key = sorted_stats[0][0]
    worst_stat_key = sorted_stats[-1][0]

    best_stat_name = label_map[best_stat_key]
    worst_stat_name = label_map[worst_stat_key]
    best_emoji = emoji_map[best_stat_key]

    # 1. 상단 결과 히어로 카드 (첫 화면·질문 화면과 통일된 디자인)
    st.markdown(f"""
<div class="hero-box" style="padding: 34px 24px; margin-bottom: 22px;">
<div class="hero-emoji" style="font-size: 3.8rem;">{best_emoji}✨</div>
<div><span class="pill-badge">MY HOUSING PROFILE</span></div>
<h1 class="hero-title" style="font-size: 1.75rem; margin-bottom: 12px;">자취방 선택의 핵심 기준은<br><span class="hero-highlight">{best_stat_name}</span> 입니다!</h1>
<p class="hero-desc" style="margin-bottom: 0; font-size: 0.96rem;">반면 <b style="color: #E11D48;">{worst_stat_name}</b> 영역의 조건은 과감히 타협하여<br>보증금과 월세 예산을 효율적으로 아낄 수 있습니다.</p>
</div>
""", unsafe_allow_html=True)

    # 2. 영역별 주거 중요도 프로파일 카드
    with st.container(border=True):
        st.markdown('<div style="text-align: center; margin-bottom: 14px;"><h3 style="font-family: \'GmarketSans\', sans-serif; font-size: 1.18rem; font-weight: 700; margin: 2px 0 4px 0;">📊 영역별 주거 중요도 프로파일</h3><p style="font-size: 0.84rem; color: #64748B; margin: 0;">4대 핵심 지표별 나의 성향 분포</p></div>', unsafe_allow_html=True)

        m_cols = st.columns(4)
        short_names = ["통장수호", "예민보스", "방구석라이프", "귀차니즘"]
        stat_keys = ["cost", "defense", "home", "lazy"]
        for idx, col in enumerate(m_cols):
            key = stat_keys[idx]
            val = totals[key]
            is_top = (key == best_stat_key)
            box_class = "metric-box-top" if is_top else "metric-box"
            val_color = "#4F46E5" if is_top else "#0F172A"
            with col:
                st.markdown(f"""
<div class="{box_class}">
<div class="metric-icon">{emoji_map[key]}</div>
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
            fillcolor='rgba(99, 102, 241, 0.22)',
            line=dict(color='#4F46E5', width=3),
            marker=dict(size=9, color='#EC4899', line=dict(color='#FFFFFF', width=2)),
            hovertemplate='<b>%{theta}</b><br>%{r}점<extra></extra>'
        ))

        fig.update_layout(
            polar=dict(
                bgcolor='rgba(248, 250, 252, 0.7)',
                radialaxis=dict(
                    visible=True,
                    range=[0, max_range],
                    showticklabels=False,
                    gridcolor='#E2E8F0',
                    linecolor='rgba(0,0,0,0)'
                ),
                angularaxis=dict(
                    tickfont=dict(size=11.5, color='#1E293B', family='Pretendard'),
                    gridcolor='#E2E8F0',
                    linecolor='#CBD5E1',
                    rotation=90,
                    direction="clockwise"
                )
            ),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=290,
            margin=dict(l=95, r=95, t=42, b=42)
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # 3. 입체 체크리스트 카드 (순위 없이 병렬 제시)
    MUST_HAVE_MAP = {
        "cost": ["✔ 시세보다 저렴한 급매물", "✔ 수도·인터넷 포함 관리비", "✔ 옵션보다 기본 구조 우선"],
        "defense": ["✔ 3층 이상 고층 · 신축", "✔ 콘크리트 벽 · 탑층 구조", "✔ 대로변 · 공동현관 보안"],
        "home": ["✔ 채광 좋은 남향 배치", "✔ 분리형 원룸 · 1.5룸", "✔ 넉넉한 수납 · 풀옵션"],
        "lazy": ["✔ 도보 5분 이내 초역세권", "✔ 도보 1분 컷 편의점", "✔ 밤에도 밝은 메인 상권"]
    }

    DROP_MAP = {
        "cost": ["➖ 역세권 초근접 입지", "➖ 관리비 비싼 신축 오피스텔", "➖ 불필요하게 넓은 평수"],
        "defense": ["➖ 무조건 신축 연식 고집", "➖ 저층(1~2층) 기피", "➖ 비싼 대로변 위치"],
        "home": ["➖ 남향 채광 고집", "➖ 넓은 주방 · 분리형 구조", "➖ 탁 트인 창밖 뷰(View)"],
        "lazy": ["➖ 완전 평지 입지", "➖ 번화가 중심 상권", "➖ 도보 5분 초역세권"]
    }

    col1, col2 = st.columns(2)
    with col1:
        items_html = "".join([f'<div class="guide-item">{item}</div>' for item in MUST_HAVE_MAP[best_stat_key]])
        st.markdown(f"""
<div class="guide-card-must">
<div><span class="guide-pill-must">MUST-HAVE · 최우선</span></div>
<h4 style="font-family: 'GmarketSans', sans-serif; margin: 0 0 4px 0; font-size: 1.15rem; font-weight: 700; color: #14532D;">✅ 우선 고려할 조건</h4>
<p style="font-size: 0.84rem; color: #166534; margin: 0 0 10px 0;">핵심 기준 · <b>{best_stat_name}</b></p>
{items_html}
</div>
""", unsafe_allow_html=True)

    with col2:
        drop_html = "".join([f'<div class="guide-item">{item}</div>' for item in DROP_MAP[worst_stat_key]])
        st.markdown(f"""
<div class="guide-card-drop">
<div><span class="guide-pill-drop">FLEXIBLE · 예산 절약</span></div>
<h4 style="font-family: 'GmarketSans', sans-serif; margin: 0 0 4px 0; font-size: 1.15rem; font-weight: 700; color: #881337;">✂️ 타협 가능한 조건</h4>
<p style="font-size: 0.84rem; color: #9F1239; margin: 0 0 10px 0;">타협 기준 · <b>{worst_stat_name}</b></p>
{drop_html}
</div>
""", unsafe_allow_html=True)

    st.write("")
    st.write("")
    if st.button("🔄 처음부터 다시 진단하기", type="primary", use_container_width=True):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()
