import streamlit as st
import pandas as pd
import plotly.express as px
import time

# --- 1. 페이지 기본 설정 ---
st.set_page_config(page_title="자취방 우선순위 판독기", page_icon="🏠", layout="centered")

# --- 2. 세션 상태(Session State) 초기화 ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

# --- 3. 비밀번호 인증 (과제 필수 조건) ---
if not st.session_state.authenticated:
    st.title("🔒 PNU 자취방 판독기")
    st.write("접속을 위해 시스템 비밀번호를 입력해 주세요.")
    password = st.text_input("비밀번호:", type="password")
    
    if st.button("로그인", use_container_width=True):
        if password == "pnumis":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("비밀번호가 일치하지 않습니다.")
    st.stop()

# --- 4. 10개의 4지선다 질문 (4대 지수 배점) ---
# cost(통장수호), defense(예민보스), home(방구석라이프), lazy(귀차니즘)
QUESTIONS = [
    {
        "q": "Q1. 한 달에 숨만 쉬고 나가는 월세, 나의 마지노선은?",
        "options": [
            {"text": "① 부모님 등골 브레이커는 면하자! 무조건 저렴한 게 최고", "scores": {"cost": 3}},
            {"text": "② 적당히 타협하자! 평균 시세 정도면 쿨하게 인정", "scores": {"cost": 1, "defense": 1}},
            {"text": "③ 내 몸 편한 게 장땡! 돈을 좀 더 주더라도 컨디션 좋은 방", "scores": {"defense": 2, "home": 1}},
            {"text": "④ 인생은 한 번뿐! 풀옵션 신축 오피스텔 아니면 안 산다", "scores": {"home": 2, "lazy": 2}},
        ]
    },
    {
        "q": "Q2. 자취방에서 나의 주된 식생활은?",
        "options": [
            {"text": "① 배달앱 VVIP (한 달 식비가 월세 맘먹음)", "scores": {"lazy": 2, "cost": -1}},
            {"text": "② 햇반·밀키트 생존러 (전자레인지만 있으면 만사 OK)", "scores": {"cost": 2}},
            {"text": "③ 방구석 흑백요리사 (도마부터 향신료까지 풀세팅 요리)", "scores": {"home": 3}},
            {"text": "④ 프로 외식러 (집에서는 숨만 쉬고 물만 마심)", "scores": {"lazy": 2, "cost": 1}},
        ]
    },
    {
        "q": "Q3. 주말 오후 2시, 나는 어디서 무엇을 하고 있을까?",
        "options": [
            {"text": "① 이불 밖은 위험해! 넷플릭스 보며 귤 까먹는 중", "scores": {"home": 3}},
            {"text": "② 햇살 가득한 방에서 인테리어 소품 정리 및 홈카페 오픈", "scores": {"home": 3}},
            {"text": "③ 무조건 밖으로! 친구들 만나서 핫플·맛집 도장 깨기", "scores": {"lazy": 3}},
            {"text": "④ 카공족 빙의, 집 근처 카페나 도서관에 박혀 있음", "scores": {"lazy": 2, "cost": 1}},
        ]
    },
    {
        "q": "Q4. 방에 거대한 바퀴벌레가 나타났다! 나의 반응은?",
        "options": [
            {"text": "① '어, 왔니?' 휴지로 쿨하게 잡아서 변기에 내림", "scores": {"cost": 3}},
            {"text": "② 비명을 지르며 에프킬라 한 통을 다 뿌리고 도망감", "scores": {"defense": 2}},
            {"text": "③ 119 부를 뻔함. 그날 밤 모텔 가서 자고 다음 날 이사 알아봄", "scores": {"defense": 3}},
            {"text": "④ 벌레 나올까 봐 애초에 신축 고층 아니면 쳐다도 안 봄", "scores": {"defense": 3, "home": 1}},
        ]
    },
    {
        "q": "Q5. 밤 11시, 옆집에서 통화하는 말소리가 들린다. 나의 멘탈은?",
        "options": [
            {"text": "① '잘 자네~' 머리 대면 3초 만에 기절해서 전혀 안 들림", "scores": {"cost": 3}},
            {"text": "② 이어폰 끼고 유튜브 틀면 해결됨, 크게 신경 안 씀", "scores": {"cost": 1, "home": 1}},
            {"text": "③ 거슬려서 잠을 설침. 벽 두드리고 싶지만 소심해서 참음", "scores": {"defense": 2}},
            {"text": "④ 잠귀가 예민해서 스트레스 폭발! 벽돌 가벽, 탑층 필수", "scores": {"defense": 3}},
        ]
    },
    {
        "q": "Q6. 아침 9시 1교시 수업(또는 출근), 집에서 역/학교까지 이동 시간은?",
        "options": [
            {"text": "① '1분이라도 더 자야 해!' 슬리퍼 신고 5분 컷 초역세권 필수", "scores": {"lazy": 3}},
            {"text": "② '10~15분 정도는 산책이지' 적당한 도보 거리 OK", "scores": {"lazy": 1, "cost": 1}},
            {"text": "③ '버스 한 번 타면 되지 뭐' 교통편만 있으면 좀 멀어도 됨", "scores": {"cost": 2}},
            {"text": "④ '등산이 곧 운동이다' 가파른 언덕 위라도 월세만 싸면 환영", "scores": {"cost": 3}},
        ]
    },
    {
        "q": "Q7. 밤늦게 혼자 귀가할 때, 집 주변 골목길 분위기는?",
        "options": [
            {"text": "① 어둡고 으슥한 골목길? 무서워서 절대 못 다님. 대로변 필수!", "scores": {"defense": 3, "lazy": 1}},
            {"text": "② 가로등만 잘 켜져 있으면 주택가 골목도 괜찮음", "scores": {"defense": 1, "cost": 1}},
            {"text": "③ '누가 나 같은 걸 건드려' 치안은 크게 신경 안 씀", "scores": {"cost": 3}},
            {"text": "④ 1층에 편의점이나 24시간 가게가 있어서 밤에도 환한 곳 선호", "scores": {"lazy": 3}},
        ]
    },
    {
        "q": "Q8. 자취방에 친구들을 초대하는 것에 대한 나의 생각은?",
        "options": [
            {"text": "① '우리 집은 성역이다' 가족 외에는 아무도 들이지 않음", "scores": {"defense": 2, "home": 1}},
            {"text": "② 가끔 친한 친구 1~2명 정도만 불러서 조용히 노는 편", "scores": {"home": 2}},
            {"text": "③ '오늘 우리 집에서 파티다!' 친구들의 아지트 자처", "scores": {"home": 3, "lazy": 1}},
            {"text": "④ 집이 좁아서 부를 수가 없음, 무조건 밖에서 만남", "scores": {"cost": 2, "lazy": 2}},
        ]
    },
    {
        "q": "Q9. 빨래와 청소에 대한 나의 현실적인 모습은?",
        "options": [
            {"text": "① 옷 쌓아뒀다가 주말에 코인세탁소 가서 한 번에 해결함", "scores": {"cost": 3}},
            {"text": "② 방 안에 드럼세탁기와 건조기(또는 넓은 베란다)가 꼭 있어야 함", "scores": {"home": 3}},
            {"text": "③ 화장실 창문 없으면 곰팡이 필까 봐 숨 막힘, 환기 집착러", "scores": {"defense": 2, "home": 1}},
            {"text": "④ 대충 살자! 먼지 좀 있어도 내 몸만 편하면 그만", "scores": {"cost": 2}},
        ]
    },
    {
        "q": "Q10. 자취방 창문을 열었을 때, 내가 가장 바라는 뷰(View)와 채광은?",
        "options": [
            {"text": "① 낮에 집에 없으니 창문 열면 앞집 벽이 보여도 상관없음", "scores": {"cost": 3}},
            {"text": "② 빨래 잘 마르고 우울하지 않게 햇빛 쨍쨍한 '남향' 필수", "scores": {"home": 3}},
            {"text": "③ 통풍만 잘 되면 방향(동·서·남·북)은 크게 안 따짐", "scores": {"cost": 1, "defense": 1}},
            {"text": "④ 창문 열었을 때 뻥 뚫린 시티뷰나 공원 뷰가 보이는 감성 중시", "scores": {"home": 3}},
        ]
    }
]

# --- 5. 화면 렌더링 로직 ---

# [Step 0: 메인 시작 화면]
if st.session_state.step == 0:
    st.title("🏠 대학생 자취방 우선순위 판독기")
    st.subheader("한정된 예산, 어디에 돈을 쓰고 어디서 아낄까?")
    st.markdown("""
    10가지 현실적인 질문을 통해 당신의 자취 라이프스타일을 분석하고, 
    **월세를 더 내서라도 사수할 조건 TOP 3**와 **과감히 포기할 조건 TOP 3**를 도출합니다.
    """)
    st.divider()
    if st.button("테스트 시작하기 🚀", type="primary", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

# [Step 1 ~ 10: 질문 화면]
elif 1 <= st.session_state.step <= 10:
    current_idx = st.session_state.step - 1
    q_data = QUESTIONS[current_idx]
    
    st.progress(st.session_state.step / 10, text=f"진행률: {st.session_state.step} / 10 문항")
    st.divider()
    st.subheader(q_data["q"])
    
    option_texts = [opt["text"] for opt in q_data["options"]]
    default_idx = st.session_state.answers.get(current_idx, 0)
    choice = st.radio("당신의 선택은?", option_texts, index=default_idx, key=f"radio_{current_idx}")
    
    st.write("")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.step > 1:
            if st.button("⬅️ 이전", use_container_width=True):
                st.session_state.answers[current_idx] = option_texts.index(choice)
                st.session_state.step -= 1
                st.rerun()
    with col2:
        btn_label = "다음 ➡️" if st.session_state.step < 10 else "결과 보기 📊"
        if st.button(btn_label, type="primary", use_container_width=True):
            st.session_state.answers[current_idx] = option_texts.index(choice)
            st.session_state.step += 1
            st.rerun()

# [Step 11: 결과 분석 화면]
elif st.session_state.step == 11:
    with st.spinner('자취 성향을 분석 중입니다...'):
        time.sleep(1.0)
        
    # 1. 점수 합산 로직
    totals = {"cost": 0, "defense": 0, "home": 0, "lazy": 0}
    for q_idx, opt_idx in st.session_state.answers.items():
        scores = QUESTIONS[q_idx]["options"][opt_idx]["scores"]
        for k, v in scores.items():
            totals[k] += v
            
    # 최소 1점 보정 (레이더 차트 형태 유지용)
    for k in totals:
        if totals[k] < 1:
            totals[k] = 1

    # 지수 이름 매핑
    label_map = {
        "cost": "통장수호 지수 (가성비)", 
        "defense": "예민보스 지수 (방음/치안)", 
        "home": "방구석라이프 지수 (채광/크기)", 
        "lazy": "귀차니즘 지수 (교통/인프라)"
    }
    
    # 정렬하여 최고/최저 스탯 찾기
    sorted_stats = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    best_stat_key = sorted_stats[0][0]
    worst_stat_key = sorted_stats[-1][0]
    
    best_stat_name = label_map[best_stat_key]
    worst_stat_name = label_map[worst_stat_key]

    # --- UI 렌더링 ---
    st.title("📊 맞춤형 자취방 분석 리포트")
    st.divider()

    # 1. 레이더 차트 (Plotly)
    st.subheader("🕸️ 4대 자취 지수 밸런스")
    
    df = pd.DataFrame({
        "지수": list(label_map.values()),
        "점수": [totals["cost"], totals["defense"], totals["home"], totals["lazy"]]
    })
    
    fig = px.line_polar(df, r='점수', theta='지수', line_close=True)
    fig.update_traces(fill='toself', line_color='#FF4B4B', fillcolor='rgba(255, 75, 75, 0.35)')
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(df['점수']) + 2], gridcolor="rgba(128, 128, 128, 0.4)"),
            angularaxis=dict(tickfont=dict(size=13))
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=70, r=70, t=30, b=30)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # 2. 사수할 조건 TOP 3 vs 버려도 될 조건 TOP 3
    st.subheader("💡 자취방 선택 우선순위 가이드")
    
    MUST_HAVE_MAP = {
        "cost": ["① 보증금/월세 시세보다 저렴한 급매물", "② 관리비에 수도·인터넷이 포함된 방", "③ 옵션이 부족해도 기본 구조가 멀쩡한 방"],
        "defense": ["① 벌레 차단! 3층 이상 고층 & 신축/리모델링", "② 층간소음 방지! 콘크리트 가벽 및 탑층", "③ 밤길 안전! 대로변 위치 + 공동현관 CCTV"],
        "home": ["① 우울감 타파! 햇빛 쨍쨍한 남향", "② 냄새 차단! 분리형 원룸 또는 1.5룸", "③ 집콕러의 필수품! 넉넉한 수납과 풀옵션"],
        "lazy": ["① 1분이라도 더 자자! 도보 5분 이내 초역세권", "② 슬리퍼 상권! 도보 1분 컷 편의점 필수", "③ 밤늦게 놀기 좋은 메인 상권 근처"]
    }

    DROP_MAP = {
        "cost": ["① 굳이 역 코앞 고집하기 (조금만 걸어도 월세 10만 원 세이브!)", "② 최신식 신축 오피스텔 (비싼 관리비의 주범)", "③ 불필요하게 넓은 평수 (청소만 힘들고 난방비 폭탄)"],
        "defense": ["① 신축 고집하기 (구축이라도 도배/장판 깔끔하면 OK)", "② 층수 제한 (1~2층이나 반지하도 가성비 최고)", "③ 대로변 프리미엄 (조용한 주택가 골목 추천)"],
        "home": ["① 남향 집착 (낮에 집에 없으니 북향 골라서 월세 절약)", "② 큰 주방 및 분리형 (인덕션 1구 원룸으로 충분)", "③ 감성 뷰(View) (창문 앞이 막혀도 잠만 잘 자면 장땡)"],
        "lazy": ["① 평지 입지 (가파른 언덕 위라도 운동 삼아 걷기)", "② 번화가 인프라 (식당 거리에서 벗어난 외곽 선택)", "③ 초역세권 (마을버스 10분 거리면 방 크기가 2배!)"]
    }

    col1, col2 = st.columns(2)
    with col1:
        st.success(f"🟢 **절대 사수할 조건 TOP 3**\n\n*(가장 높은 **{best_stat_name}** 기반)*")
        for item in MUST_HAVE_MAP[best_stat_key]:
            st.write(item)
            
    with col2:
        st.error(f"🔴 **버려도 될 조건 TOP 3**\n\n*(가장 낮은 **{worst_stat_name}** 기반)*")
        for item in DROP_MAP[worst_stat_key]:
            st.write(item)
            
    st.divider()
    
    # 다시 하기
    if st.button("🔄 테스트 다시 하기", use_container_width=True):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()
