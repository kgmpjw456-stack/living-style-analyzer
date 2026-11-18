import streamlit as st
import pandas as pd

# --- 1. 페이지 기본 설정 ---
st.set_page_config(page_title="자취방 우선순위 판독기", page_icon="🏠", layout="centered")

# --- 2. 세션 상태(Session State) 초기화 (화면 전환 및 점수 저장용) ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "step" not in st.session_state:
    st.session_state.step = 0  # 0: 시작 화면, 1~10: 질문, 11: 결과 화면
if "answers" not in st.session_state:
    st.session_state.answers = {}

# --- 3. 비밀번호 인증 (과제 필수 조건) ---
if not st.session_state.authenticated:
    st.title("🔒 접근 제한 구역")
    st.write("시스템을 이용하려면 과제 비밀번호를 입력하세요.")
    password = st.text_input("비밀번호 입력:", type="password")
    
    if st.button("접속하기"):
        if password == "pnumis":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("비밀번호가 일치하지 않습니다.")
    st.stop()

# --- 4. 10개의 4지선다 질문 데이터 및 스탯 배점 설계 ---
# 스탯 종류: 가성비(cost), 방어력(defense), 집콕력(homebody), 역세권(location)
QUESTIONS = [
    {
        "q": "Q1. 한 달에 숨만 쉬고 나가는 월세, 나의 마지노선은?",
        "options": [
            {"text": "① 부모님 등골 브레이커는 면하자! 무조건 저렴한 게 최고", "scores": {"cost": 3}},
            {"text": "② 적당히 타협하자! 평균 시세 정도면 쿨하게 인정", "scores": {"cost": 1, "defense": 1}},
            {"text": "③ 내 몸 편한 게 장땡! 돈을 좀 더 주더라도 컨디션 좋은 방", "scores": {"defense": 2, "homebody": 1}},
            {"text": "④ 인생은 한 번뿐! 풀옵션 신축 오피스텔 아니면 안 산다", "scores": {"homebody": 2, "location": 2}},
        ]
    },
    {
        "q": "Q2. 자취방에서 나의 주된 식생활은?",
        "options": [
            {"text": "① 배달앱 VVIP (한 달 식비가 월세 맘먹음)", "scores": {"location": 2, "cost": -1}},
            {"text": "② 햇반·밀키트 생존러 (전자레인지만 있으면 만사 OK)", "scores": {"cost": 2}},
            {"text": "③ 방구석 흑백요리사 (도마부터 향신료까지 풀세팅 요리)", "scores": {"homebody": 3}},
            {"text": "④ 프로 외식러 (집에서는 숨만 쉬고 물만 마심)", "scores": {"location": 2, "cost": 1}},
        ]
    },
    {
        "q": "Q3. 주말 오후 2시, 나는 어디서 무엇을 하고 있을까?",
        "options": [
            {"text": "① 이불 밖은 위험해! 넷플릭스 보며 귤 까먹는 중", "scores": {"homebody": 3}},
            {"text": "② 햇살 가득한 방에서 인테리어 소품 정리 및 홈카페 오픈", "scores": {"homebody": 3}},
            {"text": "③ 무조건 밖으로! 친구들 만나서 핫플·맛집 도장 깨기", "scores": {"location": 3}},
            {"text": "④ 카공족 빙의, 집 근처 카페나 도서관에 박혀 있음", "scores": {"location": 2, "cost": 1}},
        ]
    },
    {
        "q": "Q4. 방에 거대한 바퀴벌레가 나타났다! 나의 반응은?",
        "options": [
            {"text": "① '어, 왔니?' 휴지로 쿨하게 잡아서 변기에 내림", "scores": {"cost": 3}},
            {"text": "② 비명을 지르며 에프킬라 한 통을 다 뿌리고 도망감", "scores": {"defense": 2}},
            {"text": "③ 119 부를 뻔함. 그날 밤 모텔 가서 자고 다음 날 이사 알아봄", "scores": {"defense": 3}},
            {"text": "④ 벌레 나올까 봐 애초에 신축 고층 아니면 쳐다도 안 봄", "scores": {"defense": 3, "homebody": 1}},
        ]
    },
    {
        "q": "Q5. 밤 11시, 옆집에서 통화하는 말소리가 들린다. 나의 멘탈은?",
        "options": [
            {"text": "① '잘 자네~' 머리 대면 3초 만에 기절해서 전혀 안 들림", "scores": {"cost": 3}},
            {"text": "② 이어폰 끼고 유튜브 틀면 해결됨, 크게 신경 안 씀", "scores": {"cost": 1, "homebody": 1}},
            {"text": "③ 거슬려서 잠을 설침. 벽 두드리고 싶지만 소심해서 참음", "scores": {"defense": 2}},
            {"text": "④ 잠귀가 예민해서 스트레스 폭발! 벽돌 가벽, 탑층 필수", "scores": {"defense": 3}},
        ]
    },
    {
        "q": "Q6. 아침 9시 1교시 수업(또는 출근), 집에서 역/학교까지 이동 시간은?",
        "options": [
            {"text": "① '1분이라도 더 자야 해!' 슬리퍼 신고 5분 컷 초역세권 필수", "scores": {"location": 3}},
            {"text": "② '10~15분 정도는 산책이지' 적당한 도보 거리 OK", "scores": {"location": 1, "cost": 1}},
            {"text": "③ '버스 한 번 타면 되지 뭐' 교통편만 있으면 좀 멀어도 됨", "scores": {"cost": 2}},
            {"text": "④ '등산이 곧 운동이다' 가파른 언덕 위라도 월세만 싸면 환영", "scores": {"cost": 3}},
        ]
    },
    {
        "q": "Q7. 밤늦게 혼자 귀가할 때, 집 주변 골목길 분위기는?",
        "options": [
            {"text": "① 어둡고 으슥한 골목길? 무서워서 절대 못 다님. 대로변 필수!", "scores": {"defense": 3, "location": 1}},
            {"text": "② 가로등만 잘 켜져 있으면 주택가 골목도 괜찮음", "scores": {"defense": 1, "cost": 1}},
            {"text": "③ '누가 나 같은 걸 건드려' 치안은 크게 신경 안 씀", "scores": {"cost": 3}},
            {"text": "④ 1층에 편의점이나 24시간 가게가 있어서 밤에도 환한 곳 선호", "scores": {"location": 3}},
        ]
    },
    {
        "q": "Q8. 자취방에 친구들을 초대하는 것에 대한 나의 생각은?",
        "options": [
            {"text": "① '우리 집은 성역이다' 가족 외에는 아무도 들이지 않음", "scores": {"defense": 2, "homebody": 1}},
            {"text": "② 가끔 친한 친구 1~2명 정도만 불러서 조용히 노는 편", "scores": {"homebody": 2}},
            {"text": "③ '오늘 우리 집에서 파티다!' 친구들의 아지트 자처", "scores": {"homebody": 3, "location": 1}},
            {"text": "④ 집이 좁아서 부를 수가 없음, 무조건 밖에서 만남", "scores": {"cost": 2, "location": 2}},
        ]
    },
    {
        "q": "Q9. 빨래와 청소에 대한 나의 현실적인 모습은?",
        "options": [
            {"text": "① 옷 쌓아뒀다가 주말에 코인세탁소 가서 한 번에 해결함", "scores": {"cost": 3}},
            {"text": "② 방 안에 드럼세탁기와 건조기(또는 넓은 베란다)가 꼭 있어야 함", "scores": {"homebody": 3}},
            {"text": "③ 화장실 창문 없으면 곰팡이 필까 봐 숨 막힘, 환기 집착러", "scores": {"defense": 2, "homebody": 1}},
            {"text": "④ 대충 살자! 먼지 좀 있어도 내 몸만 편하면 그만", "scores": {"cost": 2}},
        ]
    },
    {
        "q": "Q10. 자취방 창문을 열었을 때, 내가 가장 바라는 뷰(View)와 채광은?",
        "options": [
            {"text": "① 낮에 집에 없으니 창문 열면 앞집 벽이 보여도 상관없음", "scores": {"cost": 3}},
            {"text": "② 빨래 잘 마르고 우울하지 않게 햇빛 쨍쨍한 '남향' 필수", "scores": {"homebody": 3}},
            {"text": "③ 통풍만 잘 되면 방향(동·서·남·북)은 크게 안 따짐", "scores": {"cost": 1, "defense": 1}},
            {"text": "④ 창문 열었을 때 뻥 뚫린 시티뷰나 공원 뷰가 보이는 감성 중시", "scores": {"homebody": 3}},
        ]
    }
]

# --- 5. 화면 렌더링 로직 ---

# [Step 0: 시작 화면]
if st.session_state.step == 0:
    st.title("🏠 자취방 우선순위 판독기")
    st.subheader("한정된 예산, 어디에 돈을 쓰고 어디서 아낄까?")
    st.markdown("""
    자취방을 구할 때 모든 조건을 다 갖춘 집은 너무 비쌉니다. 
    10가지 현실적인 질문을 통해 당신의 라이프스타일을 분석하고,
    * **🟢 월세를 더 내서라도 사수해야 할 조건 TOP 3**
    * **🔴 과감히 포기하고 월세를 아낄 조건 TOP 3**
    를 정확하게 도출해 드립니다!
    """)
    st.divider()
    if st.button("테스트 시작하기 🚀", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

# [Step 1 ~ 10: 질문 진행 화면 (한 화면에 한 문항씩)]
elif 1 <= st.session_state.step <= 10:
    current_idx = st.session_state.step - 1
    q_data = QUESTIONS[current_idx]
    
    # 상단 실시간 진행률 표시
    st.progress(st.session_state.step / 10, text=f"진행률: {st.session_state.step} / 10 문항")
    st.divider()
    
    # 질문 출력
    st.subheader(q_data["q"])
    
    # 보기 텍스트 리스트 추출
    option_texts = [opt["text"] for opt in q_data["options"]]
    
    # 이전에 선택한 값이 있다면 유지
    default_idx = st.session_state.answers.get(current_idx, 0)
    choice = st.radio("가장 가까운 상황을 선택하세요:", option_texts, index=default_idx, key=f"radio_{current_idx}")
    
    st.write("") # 여백
    
    # 이전 / 다음 버튼 배치
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state.step > 1:
            if st.button("⬅️ 이전 질문", use_container_width=True):
                st.session_state.answers[current_idx] = option_texts.index(choice)
                st.session_state.step -= 1
                st.rerun()
    with col2:
        btn_label = "다음 질문 ➡️" if st.session_state.step < 10 else "결과 분석하기 📊"
        if st.button(btn_label, type="primary", use_container_width=True):
            st.session_state.answers[current_idx] = option_texts.index(choice)
            st.session_state.step += 1
            st.rerun()

# [Step 11: 최종 결과 화면 (하이브리드형)]
elif st.session_state.step == 11:
    st.balloons() # 축하 효과
    
    # 1. 스탯 점수 합산
    totals = {"가성비": 0, "방어력": 0, "집콕력": 0, "역세권": 0}
    key_map = {"cost": "가성비", "defense": "방어력", "homebody": "집콕력", "location": "역세권"}
    
    for q_idx, opt_idx in st.session_state.answers.items():
        scores = QUESTIONS[q_idx]["options"][opt_idx]["scores"]
        for k, v in scores.items():
            totals[key_map[k]] += v
            
    # 점수가 음수가 되지 않도록 최소 1점 보정 (그래프 시각화용)
    for k in totals:
        if totals[k] < 1:
            totals[k] = 1

    # 최고 스탯 & 최저 스탯 추출
    sorted_stats = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    best_stat = sorted_stats[0][0]   # 1등 스탯
    worst_stat = sorted_stats[-1][0] # 꼴찌 스탯
    
    # 2. 캐릭터 타이틀 매핑 데이터
    CHARACTER_MAP = {
        ("가성비", "방어력"): ("강철 멘탈 자연인", "벌레도 잡고 소음도 이겨내는 자취계 베어그릴스! 월세 아끼는 데 도가 텄습니다."),
        ("가성비", "집콕력"): ("프로 밖순이·밖돌이", "방은 오직 잠만 자는 곳! 좁고 어두워도 월세만 싸면 장땡인 실속파입니다."),
        ("가성비", "역세권"): ("갓성비 산악인", "가파른 언덕과 먼 거리도 두 다리로 극복! 아낀 월세로 맛있는 거 사 먹는 알뜰족입니다."),
        ("방어력", "가성비"): ("온실 속 유리멘탈 귀족", "통장 잔고는 줄어들어도 벌레, 층간소음, 어두운 밤길은 절대 용납 못 하는 예민보스!"),
        ("방어력", "집콕력"): ("철통보안 요새 수호자", "집에 오래 있진 않지만, 내 안전과 수면의 질만큼은 완벽히 보호받아야 직성이 풀립니다."),
        ("방어력", "역세권"): ("조용한 숲속의 은둔자", "번화가는 시끄럽고 위험해! 조금 멀더라도 조용하고 치안 좋은 신축 빌라를 선호합니다."),
        ("집콕력", "가성비"): ("방구석 플렉스 장인", "집이 곧 나의 우주! 월세를 팍팍 쓰더라도 채광 좋고 넓은 방에서 홈카페와 요리를 즐깁니다."),
        ("집콕력", "역세권"): ("이불 밖은 위험해 집순이", "학교나 역이 멀면 어때? 한 번 집에 들어가면 주말 내내 안 나오는데! 내부 컨디션이 최고입니다."),
        ("집콕력", "방어력"): ("감성 충만 인테리어러", "벌레나 소음은 좀 참더라도 햇빛 쨍쨍한 남향과 예쁜 뷰만큼은 절대 포기 못 하는 낭만파!"),
        ("역세권", "가성비"): ("시간이 금인 욜로족", "1분이라도 더 자고 1초라도 빨리 놀아야 해! 초역세권 인프라를 위해 월세를 태우는 도시인입니다."),
        ("역세권", "집콕력"): ("슬리퍼 세권 하이애나", "집은 좁아도 상관없어! 문 열자마자 편의점, 카페, 지하철역이 있어야 숨통이 트이는 타입입니다."),
        ("역세권", "방어력"): ("도심 속 야생마", "번화가의 소음과 구축의 한계쯤은 쿨하게 넘깁니다. 오직 압도적인 교통과 위치만이 살길!")
    }
    
    # 예외 조합 처리 (기본값)
    char_title, char_desc = CHARACTER_MAP.get(
        (best_stat, worst_stat), 
        (f"{best_stat} 몰빵형 자취생", f"다른 건 몰라도 '{best_stat}' 하나만큼은 절대 타협하지 않는 확고한 취향의 소유자입니다!")
    )

    # 3. 조건 매핑 데이터 (사수 TOP 3 / 포기 TOP 3)
    MUST_HAVE_MAP = {
        "가성비": ["① 보증금/월세 시세보다 저렴한 급매물", "② 관리비에 수도·인터넷이 포함된 방", "③ 옵션이 다소 부족해도 기본 구조가 멀쩡한 방"],
        "방어력": ["① 벌레 유입을 막는 3층 이상 고층 & 신축/리모델링", "② 층간·벽간 소음을 막는 콘크리트 가벽 및 탑층", "③ 밤길 안전한 대로변 위치 + 공동현관 CCTV/도어락"],
        "집콕력": ["① 빨래 잘 마르고 우울감 없는 남향(풍부한 채광)", "② 요리 냄새 차단되는 분리형 원룸 또는 1.5룸", "③ 넉넉한 수납공간과 내부 풀옵션(드럼세탁기 등)"],
        "역세권": ["① 학교 정문 또는 지하철역 도보 5분 이내 초역세권", "② 도보 1분 컷 편의점, 세탁소 등 핵심 생활 인프라", "③ 밤늦게 다녀도 환하고 유동 인구가 많은 메인 상권"]
    }

    DROP_MAP = {
        "가성비": ["① 역/학교 코앞 프리미엄 (조금만 걸어가도 월세 10만 원 세이브!)", "② 최신식 풀옵션 신축 오피스텔 (비싼 관리비의 주범)", "③ 불필요하게 넓은 평수 (청소만 힘들고 냉난방비만 많이 나옴)"],
        "방어력": ["① 굳이 신축 고집하기 (구축이라도 도배/장판만 깔끔하면 OK)", "② 층수 제한 (1~2층이나 반지하도 치안/방충망만 확인하면 가성비 최고)", "③ 대로변 프리미엄 (조용한 주택가 골목으로 들어가 보증금 아끼기)"],
        "집콕력": ["① 남향 채광 집착 (낮에 집에 없으니 북향/동향 골라 월세 대폭 절약)", "② 큰 주방 및 분리형 구조 (인덕션 1구짜리 오픈형 원룸으로 충분)", "③ 감성 뷰(View) (창문 열면 앞집 벽이 보여도 잠만 잘 자면 장땡)"],
        "역세권": ["① 평지 입지 (가파른 언덕 위라도 운동 삼아 걸으며 쾌적한 방 구하기)", "② 번화가 인프라 (술집/식당 거리에서 벗어나 조용하고 싼 외곽 선택)", "③ 초역세권 거리 (마을버스 10분 거리로 눈을 돌리면 방 크기가 2배!)"]
    }

    # --- 결과 화면 UI 출력 ---
    st.title("📊 당신의 자취방 분석 리포트")
    st.divider()
    
    # 1단: 캐릭터 타이틀
    st.subheader(f"🏷️ 당신의 자취 유형: **[{char_title}]**")
    st.info(char_desc)
    
    # 2단: 4대 스탯 시각화 (막대 그래프)
    st.subheader("📈 4대 자취 성향 스탯 분석")
    df_stats = pd.DataFrame({
        "항목": list(totals.keys()),
        "점수": list(totals.values())
    }).set_index("항목")
    st.bar_chart(df_stats, color="#4A90E2")
    
    # 3단: 사수할 조건 vs 버려도 될 조건 TOP 3
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"🟢 **사수할 조건 TOP 3**\n*(가장 높은 '{best_stat}' 기반)*")
        for item in MUST_HAVE_MAP[best_stat]:
            st.write(item)
            
    with col2:
        st.error(f"🔴 **버려도 될 조건 TOP 3**\n*(가장 낮은 '{worst_stat}' 기반)*")
        for item in DROP_MAP[worst_stat]:
            st.write(item)
            
    st.divider()
    
    # 다시 하기 버튼
    if st.button("🔄 처음부터 다시 테스트하기", use_container_width=True):
        st.session_state.step = 0
        st.session_state.answers = {}
        st.rerun()
