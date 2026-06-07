# ============================================================
#  Sovereign Financial Distress — Early Warning System
#  GFST · Team F · Mentor: Anand Sharma
#  Streamlit Dashboard v2.0 | IMF Fund Accounts FA 8.0.0
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import math
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Sovereign Distress EWS · GFST Team F",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.main,.block-container{background:#040a1a!important;padding:1.2rem 1.8rem;}
section[data-testid="stSidebar"]{background:#06101f!important;border-right:1px solid #1a2d52;}
section[data-testid="stSidebar"] .block-container{padding:.8rem;}

.dash-header{
  background:linear-gradient(135deg,#040a1a 0%,#071630 50%,#0b2045 100%);
  border:1px solid #1a2d52;border-radius:10px;padding:22px 28px;
  margin-bottom:22px;display:flex;align-items:center;justify-content:space-between;
}
.dash-title{font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:#fff;margin:0;}
.dash-sub{font-size:11px;color:#6b7fa3;letter-spacing:1px;margin-top:5px;}
.dash-badge{background:#00d4ff;color:#000;font-size:10px;font-weight:800;
  padding:5px 12px;border-radius:4px;letter-spacing:2px;white-space:nowrap;}

.kpi-box{background:#0d1730;border:1px solid #1a2d52;border-radius:8px;
  padding:18px 20px;text-align:center;position:relative;overflow:hidden;height:100px;}
.kpi-box::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;}
.kpi-stable::before{background:#00e676;}
.kpi-vulnerable::before{background:#ffca28;}
.kpi-distressed::before{background:#ff7043;}
.kpi-crisis::before{background:#f44336;}
.kpi-total::before{background:#00d4ff;}
.kpi-score::before{background:linear-gradient(90deg,#00d4ff,#7b61ff);}
.kpi-val{font-family:'Syne',sans-serif;font-size:30px;font-weight:800;color:#fff;line-height:1;}
.kpi-lbl{font-size:9px;color:#6b7fa3;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;}
.kpi-sub{font-size:9px;color:#6b7fa3;margin-top:5px;}

.section-title{font-family:'Syne',sans-serif;font-size:11px;font-weight:700;
  color:#e8edf8;letter-spacing:2px;text-transform:uppercase;
  padding-bottom:8px;border-bottom:1px solid #1a2d52;margin-bottom:14px;margin-top:6px;}

.pill-Stable{background:rgba(0,230,118,.15);color:#00e676;border:1px solid rgba(0,230,118,.3);
  padding:2px 9px;border-radius:3px;font-size:10px;font-weight:700;}
.pill-Vulnerable{background:rgba(255,202,40,.15);color:#ffca28;border:1px solid rgba(255,202,40,.3);
  padding:2px 9px;border-radius:3px;font-size:10px;font-weight:700;}
.pill-Distressed{background:rgba(255,112,67,.15);color:#ff7043;border:1px solid rgba(255,112,67,.3);
  padding:2px 9px;border-radius:3px;font-size:10px;font-weight:700;}
.pill-Crisis{background:rgba(244,67,54,.15);color:#f44336;border:1px solid rgba(244,67,54,.3);
  padding:2px 9px;border-radius:3px;font-size:10px;font-weight:700;}

.alert-card{background:#0d1730;border:1px solid #1a2d52;border-radius:6px;
  padding:12px 16px;margin-bottom:8px;}
.alert-rising{border-left:4px solid #f44336!important;}
.alert-improving{border-left:4px solid #00e676!important;}

.chatbot-msg-user{background:#0d2a4a;border:1px solid #1a4a7a;border-radius:8px 8px 2px 8px;
  padding:10px 14px;margin:6px 0;font-size:12px;color:#e8edf8;text-align:right;}
.chatbot-msg-bot{background:#0d1730;border:1px solid #1a2d52;border-radius:8px 8px 8px 2px;
  padding:10px 14px;margin:6px 0;font-size:12px;color:#e8edf8;}
.chatbot-wrap{background:#06101f;border:1px solid #1a2d52;border-radius:8px;
  padding:14px;height:380px;overflow-y:auto;margin-bottom:10px;}

.rec-box{border-radius:6px;padding:14px;margin-bottom:8px;}
.rec-stable{background:rgba(0,230,118,.07);border:1px solid rgba(0,230,118,.2);}
.rec-vulnerable{background:rgba(255,202,40,.07);border:1px solid rgba(255,202,40,.2);}
.rec-distressed{background:rgba(255,112,67,.07);border:1px solid rgba(255,112,67,.2);}
.rec-crisis{background:rgba(244,67,54,.07);border:1px solid rgba(244,67,54,.2);}

div[data-testid="metric-container"]{background:#0d1730;border:1px solid #1a2d52;border-radius:6px;padding:10px;}
[data-testid="stMetricValue"]{color:#fff!important;font-weight:800;}
[data-testid="stMetricLabel"]{color:#6b7fa3!important;font-size:11px;}
</style>
""", unsafe_allow_html=True)

# ── Colors ───────────────────────────────────────────────────
TIER_CLR = {"Stable":"#00e676","Vulnerable":"#ffca28","Distressed":"#ff7043","Crisis":"#f44336"}
REGION_CLR = {
    "Asia-Pacific":"#00b4d8","Europe":"#7b61ff",
    "Latin America & Caribbean":"#00e676",
    "Middle East & Central Asia":"#ff7043",
    "North America":"#4895ef","Sub-Saharan Africa":"#f44336"
}
PT = {
    "paper_bgcolor":"rgba(0,0,0,0)","plot_bgcolor":"rgba(0,0,0,0)",
    "font":{"color":"#6b7fa3","family":"Inter"},
    "xaxis":{"gridcolor":"#111c35","linecolor":"#1a2d52","tickfont":{"color":"#6b7fa3","size":10}},
    "yaxis":{"gridcolor":"#111c35","linecolor":"#1a2d52","tickfont":{"color":"#6b7fa3","size":10}},
    "legend":{"bgcolor":"rgba(0,0,0,0)","font":{"color":"#e8edf8","size":10}},
    "margin":{"l":40,"r":20,"t":36,"b":40}
}

def pt_base(*exclude):
    """Return PT dict excluding specified top-level keys (to avoid duplicate keyword args)."""
    return {k:v for k,v in PT.items() if k not in exclude}

def hex_alpha(hex_color, alpha=0.12):
    """Convert #rrggbb hex to rgba string with given alpha (0-1)."""
    h = hex_color.lstrip("#")
    if len(h) == 6:
        r,g,b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
        return f"rgba({r},{g},{b},{alpha})"
    return hex_color  # fallback

# ── Load Data ────────────────────────────────────────────────
@st.cache_data
def load_all():
    import os
    base = "/mnt/user-data/uploads" if os.path.exists("/mnt/user-data/uploads/Dashboard_Master.csv") else "."
    dm  = pd.read_csv(f"{base}/Dashboard_Master.csv")
    cr  = pd.read_csv(f"{base}/Country_Distress_Ranking.csv")
    fi  = pd.read_csv(f"{base}/Feature_Importance.csv")
    fsd = pd.read_csv(f"{base}/Final_Sovereign_Distress_Dataset.csv")
    gd  = pd.read_csv(f"{base}/Global_Dashboard_Data.csv")
    ind = pd.read_csv(f"{base}/India_Dashboard_Data.csv")
    cp  = pd.read_csv(f"{base}/country_pillars_final.csv")
    fr  = pd.read_csv(f"{base}/final_sovereign_risk_rankings.csv")
    for df in [dm,cr,fi,fsd,gd,ind,cp,fr]:
        for c in df.select_dtypes(include='object').columns:
            try: df[c] = pd.to_numeric(df[c])
            except: pass
    return dm,cr,fi,fsd,gd,ind,cp,fr

dm,cr,fi,fsd,gd,ind,cp,fr = load_all()

# Add region mapping
REGION_MAP = {
    "Afghanistan":"Asia-Pacific","Albania":"Europe","Algeria":"Middle East & Central Asia",
    "Angola":"Sub-Saharan Africa","Argentina":"Latin America & Caribbean","Armenia":"Europe",
    "Australia":"Asia-Pacific","Austria":"Europe","Azerbaijan":"Europe",
    "Bahrain":"Middle East & Central Asia","Bangladesh":"Asia-Pacific",
    "Belarus":"Europe","Belgium":"Europe","Benin":"Sub-Saharan Africa",
    "Bhutan":"Asia-Pacific","Bolivia":"Latin America & Caribbean","Bosnia and Herzegovina":"Europe",
    "Botswana":"Sub-Saharan Africa","Brazil":"Latin America & Caribbean",
    "Bulgaria":"Europe","Burkina Faso":"Sub-Saharan Africa","Burundi":"Sub-Saharan Africa",
    "Cabo Verde":"Sub-Saharan Africa","Cambodia":"Asia-Pacific","Cameroon":"Sub-Saharan Africa",
    "Canada":"North America","Central African Republic":"Sub-Saharan Africa","Chad":"Sub-Saharan Africa",
    "Chile":"Latin America & Caribbean","China":"Asia-Pacific","Colombia":"Latin America & Caribbean",
    "Congo, Dem. Rep. of the":"Sub-Saharan Africa","Congo, Rep. of":"Sub-Saharan Africa",
    "Costa Rica":"Latin America & Caribbean","Cote d'Ivoire":"Sub-Saharan Africa",
    "Croatia":"Europe","Czech Republic":"Europe","Denmark":"Europe",
    "Dominican Republic":"Latin America & Caribbean","Ecuador":"Latin America & Caribbean",
    "Egypt":"Middle East & Central Asia","El Salvador":"Latin America & Caribbean",
    "Ethiopia":"Sub-Saharan Africa","Finland":"Europe","France":"Europe",
    "Gabon":"Sub-Saharan Africa","Georgia":"Europe","Germany":"Europe","Ghana":"Sub-Saharan Africa",
    "Greece":"Europe","Guatemala":"Latin America & Caribbean","Guinea":"Sub-Saharan Africa",
    "Haiti":"Latin America & Caribbean","Honduras":"Latin America & Caribbean","Hungary":"Europe",
    "India":"Asia-Pacific","Indonesia":"Asia-Pacific","Iraq":"Middle East & Central Asia",
    "Ireland":"Europe","Israel":"Middle East & Central Asia","Italy":"Europe",
    "Jamaica":"Latin America & Caribbean","Japan":"Asia-Pacific","Jordan":"Middle East & Central Asia",
    "Kazakhstan":"Europe","Kenya":"Sub-Saharan Africa","Korea, Republic of":"Asia-Pacific",
    "Kyrgyz Republic":"Europe","Lao P.D.R.":"Asia-Pacific","Latvia":"Europe","Lebanon":"Middle East & Central Asia",
    "Liberia":"Sub-Saharan Africa","Libya":"Middle East & Central Asia","Lithuania":"Europe",
    "Madagascar":"Sub-Saharan Africa","Malawi":"Sub-Saharan Africa","Malaysia":"Asia-Pacific",
    "Mali":"Sub-Saharan Africa","Mexico":"Latin America & Caribbean","Moldova":"Europe",
    "Mongolia":"Asia-Pacific","Montenegro":"Europe","Morocco":"Middle East & Central Asia",
    "Mozambique":"Sub-Saharan Africa","Myanmar":"Asia-Pacific","Namibia":"Sub-Saharan Africa",
    "Nepal":"Asia-Pacific","Netherlands":"Europe","New Zealand":"Asia-Pacific",
    "Nicaragua":"Latin America & Caribbean","Niger":"Sub-Saharan Africa","Nigeria":"Sub-Saharan Africa",
    "Norway":"Europe","Pakistan":"Middle East & Central Asia","Panama":"Latin America & Caribbean",
    "Papua New Guinea":"Asia-Pacific","Paraguay":"Latin America & Caribbean","Peru":"Latin America & Caribbean",
    "Philippines":"Asia-Pacific","Poland":"Europe","Portugal":"Europe",
    "Romania":"Europe","Russian Federation":"Europe","Rwanda":"Sub-Saharan Africa",
    "Saudi Arabia":"Middle East & Central Asia","Senegal":"Sub-Saharan Africa","Serbia":"Europe",
    "Sierra Leone":"Sub-Saharan Africa","Singapore":"Asia-Pacific","Slovak Republic":"Europe",
    "Slovenia":"Europe","Somalia":"Sub-Saharan Africa","South Africa":"Sub-Saharan Africa",
    "South Sudan":"Sub-Saharan Africa","Spain":"Europe","Sri Lanka":"Asia-Pacific",
    "Sudan":"Sub-Saharan Africa","Sweden":"Europe","Switzerland":"Europe",
    "Tajikistan":"Europe","Tanzania":"Sub-Saharan Africa","Thailand":"Asia-Pacific",
    "Tunisia":"Middle East & Central Asia","Turkey":"Europe","Uganda":"Sub-Saharan Africa",
    "Ukraine":"Europe","United Arab Emirates":"Middle East & Central Asia",
    "United Kingdom":"Europe","United States":"North America","Uruguay":"Latin America & Caribbean",
    "Uzbekistan":"Europe","Venezuela":"Latin America & Caribbean","Vietnam":"Asia-Pacific",
    "Yemen":"Middle East & Central Asia","Zambia":"Sub-Saharan Africa","Zimbabwe":"Sub-Saharan Africa",
}
dm["REGION"] = dm["COUNTRY_WB"].map(REGION_MAP).fillna("Other")
gd["REGION"] = gd["COUNTRY_WB"].map(REGION_MAP).fillna("Other")

latest_yr = int(dm["YEAR"].max())
latest    = dm[dm["YEAR"]==latest_yr].copy()
all_countries = sorted(dm["COUNTRY_WB"].unique())
all_years     = sorted(dm["YEAR"].unique())

# ── Chatbot Logic ────────────────────────────────────────────
def chatbot_response(user_msg, dm, latest, fi, cp):
    msg = user_msg.lower().strip()

    # Country risk query
    for country in dm["COUNTRY_WB"].unique():
        if country.lower() in msg:
            row = latest[latest["COUNTRY_WB"]==country]
            if row.empty:
                row = dm[dm["COUNTRY_WB"]==country].sort_values("YEAR").iloc[[-1]]
            if not row.empty:
                r = row.iloc[0]
                clr_map = {"Stable":"🟢","Vulnerable":"🟡","Distressed":"🟠","Crisis":"🔴"}
                icon = clr_map.get(r["RISK_CATEGORY"],"⚪")
                rec_map = {
                    "Stable":"Routine surveillance — no intervention needed.",
                    "Vulnerable":"Policy review recommended — monitor closely.",
                    "Distressed":"Financial assistance planning required.",
                    "Crisis":"Immediate IMF intervention needed."
                }
                return (f"{icon} **{country}** ({int(r['YEAR'])})\n\n"
                        f"• **Risk Category:** {r['RISK_CATEGORY']}\n"
                        f"• **Distress Probability:** {r['PD']*100:.1f}%\n"
                        f"• **Risk Score:** {r['SOVEREIGN_RISK_SCORE']:.3f}\n"
                        f"• **GDP Growth:** {r['GDP_GROWTH']:.2f}\n"
                        f"• **Inflation:** {r['INFLATION']:.2f}\n"
                        f"• **Current Account:** {r['CURRENT_ACCOUNT']:.3f}\n\n"
                        f"📋 **Recommendation:** {rec_map.get(r['RISK_CATEGORY'],'Monitor.')}")

    # Crisis countries
    if any(w in msg for w in ["crisis","highest risk","most at risk","top risk","worst"]):
        crisis = latest[latest["RISK_CATEGORY"]=="Crisis"].nlargest(5,"PD")
        if crisis.empty:
            return "No countries in Crisis tier in the latest data."
        lines = "\n".join([f"• **{r['COUNTRY_WB']}** — PD: {r['PD']*100:.1f}%" for _,r in crisis.iterrows()])
        return f"🔴 **Top Crisis Countries ({latest_yr}):**\n\n{lines}"

    # Stable countries
    if any(w in msg for w in ["stable","safest","lowest risk","best","safe"]):
        stable = latest[latest["RISK_CATEGORY"]=="Stable"].nsmallest(5,"PD")
        lines = "\n".join([f"• **{r['COUNTRY_WB']}** — PD: {r['PD']*100:.1f}%" for _,r in stable.iterrows()])
        return f"🟢 **Most Stable Countries ({latest_yr}):**\n\n{lines}"

    # Feature importance
    if any(w in msg for w in ["feature","important","driver","factor","predictor","variable"]):
        top5 = fi.nlargest(5,"Importance")
        lines = "\n".join([f"• **{r['Feature']}** — {r['Importance']*100:.1f}%" for _,r in top5.iterrows()])
        return f"📊 **Top 5 Risk Drivers (Random Forest):**\n\n{lines}\n\nThe Sovereign Risk Score is the strongest predictor of distress."

    # India
    if "india" in msg:
        ind_row = latest[latest["COUNTRY_WB"]=="India"]
        if not ind_row.empty:
            r = ind_row.iloc[0]
            return (f"🇮🇳 **India ({latest_yr})**\n\n"
                    f"• **Risk Category:** {r['RISK_CATEGORY']} 🟢\n"
                    f"• **Distress Probability:** {r['PD']*100:.1f}%\n"
                    f"• **GDP Growth:** {r['GDP_GROWTH']:.2f}\n"
                    f"• **Inflation:** {r['INFLATION']:.2f}\n\n"
                    f"India maintains a stable sovereign risk profile with strong reserve coverage.")

    # Distribution
    if any(w in msg for w in ["how many","count","distribution","breakdown","total"]):
        vc = latest["RISK_CATEGORY"].value_counts()
        lines = "\n".join([f"• **{k}:** {v} countries" for k,v in vc.items()])
        return f"📈 **Risk Distribution ({latest_yr}) — {len(latest)} countries:**\n\n{lines}"

    # Trend
    if any(w in msg for w in ["trend","over time","history","change","evolv"]):
        yearly = dm.groupby("YEAR")["PD"].mean()
        peak_yr = int(yearly.idxmax())
        return (f"📈 **Global Distress Trend:**\n\n"
                f"• Data spans **2007–{latest_yr}**\n"
                f"• Peak average PD was in **{peak_yr}**\n"
                f"• Crisis periods: GFC (2008–09), Euro Debt (2010–12), COVID-19 (2020–21), Post-COVID (2022–23)\n"
                f"• Latest global avg PD: **{dm[dm['YEAR']==latest_yr]['PD'].mean()*100:.1f}%**")

    # Model
    if any(w in msg for w in ["model","machine learning","random forest","xgboost","logistic","ml","algorithm"]):
        return ("🤖 **ML Models Used:**\n\n"
                "• **Logistic Regression** — Baseline model\n"
                "• **Random Forest** — Main predictive model (best performance)\n"
                "• **XGBoost** — Advanced benchmark\n\n"
                "📊 **Evaluation Metrics:** ROC-AUC, Precision, Recall, F1 Score\n\n"
                "Random Forest achieved the strongest overall performance with the Sovereign Risk Score as the #1 feature.")

    # PD explanation
    if any(w in msg for w in ["pd","probability","distress probability","what is pd"]):
        return ("📊 **Probability of Distress (PD):**\n\n"
                "PD is the model's estimated probability (0–1) that a country will experience sovereign financial distress in the **next year**.\n\n"
                "• **PD < 0.2** → Stable 🟢\n"
                "• **PD 0.2–0.5** → Vulnerable 🟡\n"
                "• **PD 0.5–0.7** → Distressed 🟠\n"
                "• **PD > 0.7** → Crisis 🔴")

    # Greeting
    if any(w in msg for w in ["hello","hi","hey","good morning","good evening"]):
        return ("👋 **Hello! I'm the Sovereign Risk Assistant.**\n\n"
                "I can help you with:\n"
                "• Country risk queries (e.g. *'What is Pakistan's risk?'*)\n"
                "• Crisis/stable country lists\n"
                "• Feature importance\n"
                "• Model information\n"
                "• Global trends\n\n"
                "Just ask me anything about sovereign distress! 🌍")

    # Help
    if any(w in msg for w in ["help","what can","what do","commands","options"]):
        return ("🆘 **What I can answer:**\n\n"
                "• *'What is [country]'s risk?'*\n"
                "• *'Which countries are in crisis?'*\n"
                "• *'Show most stable countries'*\n"
                "• *'What are the top risk drivers?'*\n"
                "• *'Explain PD'*\n"
                "• *'What ML models were used?'*\n"
                "• *'What is the global trend?'*\n"
                "• *'How many countries are distressed?'*")

    return ("🤔 I didn't quite understand that. Try asking:\n\n"
            "• *'What is [country name]'s risk?'*\n"
            "• *'Which countries are in crisis?'*\n"
            "• *'What are the top risk drivers?'*\n"
            "• Type **help** to see all options.")

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:10px 0 16px;'>
      <div style='font-family:Syne,sans-serif;font-size:16px;font-weight:800;color:#fff;'>🌍 EWS Dashboard</div>
      <div style='font-size:9px;color:#6b7fa3;letter-spacing:2px;margin-top:3px;'>GFST · TEAM F</div>
    </div>""", unsafe_allow_html=True)

    page = st.radio("Navigate", [
        "🏠 Overview",
        "🔍 Country Explorer",
        "📈 Risk Trajectory",
        "⚡ Early Warnings",
        "🗺️ Regional Analysis",
        "📊 Feature Importance",
        "⚖️ Country Comparison",
        "🃏 Health Card",
        "🇮🇳 India Deep Dive",
        "🤖 AI Chatbot"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("### 🎛️ Filters")
    sel_yr    = st.selectbox("Year", ["All"]+[str(y) for y in sorted(all_years, reverse=True)])
    sel_tier  = st.multiselect("Risk Tier", ["Stable","Vulnerable","Distressed","Crisis"],
                                default=["Stable","Vulnerable","Distressed","Crisis"])
    sel_reg   = st.multiselect("Region", sorted(dm["REGION"].unique()),
                                default=list(sorted(dm["REGION"].unique())))

    st.markdown("---")
    st.markdown("""
    <div style='font-size:9px;color:#6b7fa3;line-height:1.8;'>
    <b style='color:#e8edf8'>Categories</b><br>
    🟢 Stable — Very Low Risk<br>
    🟡 Vulnerable — Early Warning<br>
    🟠 Distressed — Elevated Risk<br>
    🔴 Crisis — Severe Risk<br><br>
    <b style='color:#e8edf8'>Model</b><br>
    Random Forest · ROC-AUC<br>
    191 Countries · 2007–2024
    </div>""", unsafe_allow_html=True)

# ── Apply Filters ─────────────────────────────────────────────
filt_dm = dm.copy()
if sel_yr != "All":
    filt_dm = filt_dm[filt_dm["YEAR"]==int(sel_yr)]
filt_dm = filt_dm[filt_dm["RISK_CATEGORY"].isin(sel_tier)]
filt_dm = filt_dm[filt_dm["REGION"].isin(sel_reg)]
filt_latest = latest[latest["RISK_CATEGORY"].isin(sel_tier) & latest["REGION"].isin(sel_reg)]

# ═══════════════════════════════════════════════
#  PAGE 1 — OVERVIEW
# ═══════════════════════════════════════════════
if page == "🏠 Overview":
    st.markdown("""
    <div class="dash-header">
      <div>
        <p class="dash-title">🌍 Sovereign Financial Distress · Early Warning System</p>
        <p class="dash-sub">GFST · TEAM F · IMF FUND ACCOUNTS FA 8.0.0 · 191 COUNTRIES · 2007–2024 · MENTOR: ANAND SHARMA</p>
      </div>
      <div class="dash-badge">ML · RANDOM FOREST</div>
    </div>""", unsafe_allow_html=True)

    # KPIs
    tc = filt_latest["RISK_CATEGORY"].value_counts()
    avg_pd = filt_latest["PD"].mean() if len(filt_latest) > 0 else 0
    total_shown = len(filt_latest)
    k1,k2,k3,k4,k5,k6 = st.columns(6)
    kpis = [
        (k1,"kpi-total",str(total_shown),"COUNTRIES","Filtered"),
        (k2,"kpi-stable",str(tc.get("Stable",0)),"STABLE","🟢 Very Low Risk"),
        (k3,"kpi-vulnerable",str(tc.get("Vulnerable",0)),"VULNERABLE","🟡 Early Warning"),
        (k4,"kpi-distressed",str(tc.get("Distressed",0)),"DISTRESSED","🟠 Elevated Risk"),
        (k5,"kpi-crisis",str(tc.get("Crisis",0)),"CRISIS","🔴 Severe Risk"),
        (k6,"kpi-score",f"{avg_pd*100:.1f}%","AVG DISTRESS PD","Filtered"),
    ]
    for col,cls,val,lbl,sub in kpis:
        with col:
            st.markdown(f"""
            <div class="kpi-box {cls}">
              <div class="kpi-lbl">{lbl}</div>
              <div class="kpi-val">{val}</div>
              <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # World Map
    st.markdown('<div class="section-title">🌍 Global Sovereign Risk Heatmap — Probability of Distress</div>', unsafe_allow_html=True)
    map_fig = px.scatter_geo(
        filt_latest, locations="COUNTRY_WB", locationmode="country names",
        color="RISK_CATEGORY", size="PD", size_max=28,
        color_discrete_map=TIER_CLR, hover_name="COUNTRY_WB",
        hover_data={"PD":":.3f","RISK_CATEGORY":True,"SOVEREIGN_RISK_SCORE":":.3f",
                    "GDP_GROWTH":":.2f","INFLATION":":.2f"},
        category_orders={"RISK_CATEGORY":["Stable","Vulnerable","Distressed","Crisis"]},
        labels={"PD":"Distress Probability","RISK_CATEGORY":"Risk Category"}
    )
    map_fig.update_geos(bgcolor="rgba(0,0,0,0)",showcoastlines=True,coastlinecolor="#1a2d52",
                        showland=True,landcolor="#0d1730",showocean=True,oceancolor="#040a1a",
                        showframe=False,projection_type="natural earth")
    map_fig.update_layout(**pt_base("xaxis","yaxis","margin","legend"),
                          height=460,margin=dict(l=0,r=0,t=10,b=0),
                          legend=dict(orientation="h",yanchor="bottom",y=0.01,xanchor="right",x=0.99,
                                      font=dict(color="#e8edf8",size=11),bgcolor="rgba(8,15,36,0.85)"))
    st.plotly_chart(map_fig, use_container_width=True)

    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Risk Category Distribution</div>', unsafe_allow_html=True)
        tc2 = filt_latest["RISK_CATEGORY"].value_counts().reindex(["Stable","Vulnerable","Distressed","Crisis"]).fillna(0)
        donut = go.Figure(go.Pie(
            labels=tc2.index, values=tc2.values, hole=0.65,
            marker_colors=[TIER_CLR[t] for t in tc2.index],
            textfont_color="#e8edf8",
            hovertemplate="<b>%{label}</b><br>%{value} countries (%{percent})<extra></extra>"
        ))
        donut.add_annotation(text=f"{total_shown}<br><span style='font-size:10px'>Countries</span>",
                             x=0.5,y=0.5,showarrow=False,font=dict(size=18,color="#fff",family="Syne"))
        donut.update_layout(**pt_base("xaxis","yaxis","legend"),
                            height=320,legend=dict(orientation="v",x=1,y=0.5,font=dict(color="#e8edf8",size=11)))
        st.plotly_chart(donut, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Global Average PD Trend (2007–2024)</div>', unsafe_allow_html=True)
        gt = filt_dm.groupby("YEAR")["PD"].mean().reset_index()
        tf = go.Figure()
        for s,e,lbl,clr in [("2008","2009","GFC","rgba(244,67,54,0.09)"),
                              ("2010","2012","Euro Debt","rgba(255,112,67,0.07)"),
                              ("2020","2021","COVID-19","rgba(244,67,54,0.11)"),
                              ("2022","2023","Post-COVID","rgba(255,202,40,0.07)")]:
            tf.add_vrect(x0=s,x1=e,fillcolor=clr,layer="below",line_width=0,
                         annotation_text=lbl,annotation_position="top left",
                         annotation_font=dict(color="rgba(255,255,255,0.35)",size=9))
        tf.add_trace(go.Scatter(x=gt["YEAR"].astype(str),y=gt["PD"],mode="lines+markers",
                                line=dict(color="#00d4ff",width=2.5),marker=dict(size=5,color="#00d4ff"),
                                fill="tozeroy",fillcolor="rgba(0,212,255,0.07)",
                                hovertemplate="Year: %{x}<br>Avg PD: %{y:.3f}<extra></extra>"))
        tf.update_layout(**PT,height=320,showlegend=False)
        st.plotly_chart(tf, use_container_width=True)

    col3,col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-title">Top 10 Highest Risk Countries</div>', unsafe_allow_html=True)
        top10 = filt_latest.nlargest(10,"PD")
        bf = go.Figure(go.Bar(
            x=top10["PD"]*100, y=top10["COUNTRY_WB"], orientation="h",
            marker_color=[TIER_CLR[t] for t in top10["RISK_CATEGORY"]],
            text=(top10["PD"]*100).round(1).astype(str)+"%",
            textposition="outside",textfont=dict(color="#e8edf8",size=10),
            hovertemplate="<b>%{y}</b><br>PD: %{x:.1f}%<extra></extra>"
        ))
        bf.update_layout(**pt_base("xaxis","yaxis"),height=340,xaxis=dict(**PT["xaxis"],range=[0,110],title="Distress Probability %"),
                         yaxis=dict(**PT["yaxis"],autorange="reversed"),showlegend=False)
        st.plotly_chart(bf, use_container_width=True)

    with col4:
        st.markdown('<div class="section-title">Crisis % by Region</div>', unsafe_allow_html=True)
        rs = filt_latest.groupby("REGION").apply(
            lambda g: pd.Series({"Crisis%":(g["RISK_CATEGORY"]=="Crisis").mean()*100,"n":len(g)})
        ).reset_index().sort_values("Crisis%",ascending=False)
        rf = px.bar(rs,x="REGION",y="Crisis%",color="REGION",color_discrete_map=REGION_CLR,
                    text=rs["Crisis%"].round(1).astype(str)+"%")
        rf.update_traces(textposition="outside",textfont=dict(color="#e8edf8",size=10))
        rf.update_layout(**pt_base("xaxis"),height=340,showlegend=False,
                         xaxis={**PT["xaxis"],"tickangle":25,"tickfont":{"color":"#6b7fa3","size":9}})
        st.plotly_chart(rf, use_container_width=True)

# ═══════════════════════════════════════════════
#  PAGE 2 — COUNTRY EXPLORER
# ═══════════════════════════════════════════════
elif page == "🔍 Country Explorer":
    st.markdown('<div class="section-title">🔍 Country Explorer — All 191 IMF Members</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns([2,1,1])
    with c1: srch = st.text_input("🔎 Search", placeholder="e.g. Pakistan, Greece, Sudan...")
    with c2: srt  = st.selectbox("Sort by",["PD","SOVEREIGN_RISK_SCORE","GDP_GROWTH","INFLATION","COUNTRY_WB"])
    with c3: asc  = st.radio("Order",["Descending","Ascending"],horizontal=True)=="Ascending"

    disp = filt_latest.copy()
    if srch: disp = disp[disp["COUNTRY_WB"].str.contains(srch,case=False,na=False)]
    disp = disp.sort_values(srt,ascending=asc)
    st.caption(f"Showing **{len(disp)}** countries")

    show = {
        "COUNTRY_WB":"Country","REGION":"Region","RISK_CATEGORY":"Category",
        "PD":"Distress PD","SOVEREIGN_RISK_SCORE":"Risk Score",
        "GDP_GROWTH":"GDP Growth","INFLATION":"Inflation",
        "CURRENT_ACCOUNT":"Current Account","TOTAL_RESERVES":"Total Reserves","FX_VOLATILITY":"FX Volatility"
    }
    tbl = disp[[c for c in show if c in disp.columns]].rename(columns=show).round(4)

    def clr_cat(v):
        m={"Stable":"background-color:#0a2a18;color:#00e676",
           "Vulnerable":"background-color:#2a2400;color:#ffca28",
           "Distressed":"background-color:#2a1400;color:#ff7043",
           "Crisis":"background-color:#2a0a0a;color:#f44336"}
        return m.get(v,"")
    def clr_pd(v):
        if v>0.7: return "color:#f44336;font-weight:bold"
        if v>0.5: return "color:#ff7043;font-weight:bold"
        if v>0.2: return "color:#ffca28"
        return "color:#00e676"

    styled = tbl.style.map(clr_cat,subset=["Category"]).map(clr_pd,subset=["Distress PD"])
    st.dataframe(styled,use_container_width=True,height=520)

    st.markdown('<div class="section-title" style="margin-top:20px;">Risk Score vs Distress Probability</div>', unsafe_allow_html=True)
    sc = px.scatter(filt_latest,x="SOVEREIGN_RISK_SCORE",y="PD",color="RISK_CATEGORY",
                    hover_name="COUNTRY_WB",color_discrete_map=TIER_CLR,size_max=12,
                    labels={"SOVEREIGN_RISK_SCORE":"Sovereign Risk Score","PD":"Distress Probability"},
                    category_orders={"RISK_CATEGORY":["Stable","Vulnerable","Distressed","Crisis"]})
    sc.update_layout(**PT,height=380)
    st.plotly_chart(sc,use_container_width=True)

# ═══════════════════════════════════════════════
#  PAGE 3 — RISK TRAJECTORY
# ═══════════════════════════════════════════════
elif page == "📈 Risk Trajectory":
    st.markdown('<div class="section-title">📈 Country Risk Trajectory (2007–2024)</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    with c1: s1 = st.selectbox("Country 1",all_countries,index=all_countries.index("Pakistan"))
    with c2: s2 = st.selectbox("Country 2",["— None —"]+all_countries,index=["— None —"]+all_countries.index("Greece") if False else 0)
    with c3: s3 = st.selectbox("Country 3",["— None —"]+all_countries)

    c2_opts = ["— None —"]+all_countries
    s2 = st.session_state.get("_s2","— None —")
    sel = [s1]+[x for x in [
        st.session_state.get("s2c","— None —"),
        st.session_state.get("s3c","— None —")
    ] if x!="— None —"]
    sel = [s1]
    if s2!="— None —": sel.append(s2)
    if s3!="— None —": sel.append(s3)
    sel = [s1,s2,s3]
    sel = [s for s in sel if s and s!="— None —"]

    colors = ["#00d4ff","#ffca28","#00e676"]
    tf2 = go.Figure()
    for s,e,lbl,clr in [("2008","2009","GFC","rgba(244,67,54,0.09)"),
                          ("2010","2012","Euro Debt","rgba(255,112,67,0.07)"),
                          ("2020","2021","COVID","rgba(244,67,54,0.11)"),
                          ("2022","2023","Post-COVID","rgba(255,202,40,0.07)")]:
        tf2.add_vrect(x0=s,x1=e,fillcolor=clr,layer="below",line_width=0,
                      annotation_text=lbl,annotation_font=dict(color="rgba(255,255,255,0.3)",size=9))

    for i,country in enumerate(sel):
        cd = dm[dm["COUNTRY_WB"]==country].sort_values("YEAR")
        tf2.add_trace(go.Scatter(
            x=cd["YEAR"].astype(str),y=cd["PD"]*100,mode="lines+markers",name=country,
            line=dict(color=colors[i%3],width=2.5),marker=dict(size=6,color=colors[i%3]),
            hovertemplate=f"<b>{country}</b><br>Year: %{{x}}<br>PD: %{{y:.1f}}%<extra></extra>"
        ))
    tf2.update_layout(**pt_base("yaxis","legend"),height=400,
                      yaxis=dict(**PT["yaxis"],title="Distress Probability (%)"),
                      legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(color="#e8edf8",size=12)))
    st.plotly_chart(tf2,use_container_width=True)

    # Stat cards
    cols = st.columns(len(sel))
    for i,(country,col) in enumerate(zip(sel,cols)):
        with col:
            cd  = dm[dm["COUNTRY_WB"]==country].sort_values("YEAR")
            row = latest[latest["COUNTRY_WB"]==country]
            if row.empty: continue
            r   = row.iloc[0]
            clr = TIER_CLR.get(r["RISK_CATEGORY"],"#fff")
            peak_yr  = int(cd.loc[cd["PD"].idxmax(),"YEAR"])
            peak_pd  = cd["PD"].max()*100
            curr_pd  = r["PD"]*100
            first_pd = cd.iloc[0]["PD"]*100
            chg      = curr_pd-first_pd
            st.markdown(f"""
            <div style="background:#0d1730;border:1px solid {clr}55;border-top:3px solid {clr};
                        border-radius:7px;padding:16px;">
              <div style="font-size:15px;font-weight:800;color:#fff;margin-bottom:4px;">{country}</div>
              <span class="pill-{r['RISK_CATEGORY']}">{r['RISK_CATEGORY']}</span>
              <div style="margin-top:12px;font-size:11px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                  <span style="color:#6b7fa3">Current PD</span>
                  <span style="color:#fff;font-weight:700">{curr_pd:.1f}%</span>
                </div>
                <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                  <span style="color:#6b7fa3">2007→2024 Change</span>
                  <span style="color:{'#f44336' if chg>=0 else '#00e676'};font-weight:700">{'+' if chg>=0 else ''}{chg:.1f}%</span>
                </div>
                <div style="display:flex;justify-content:space-between;">
                  <span style="color:#6b7fa3">Peak PD ({peak_yr})</span>
                  <span style="color:#fff">{peak_pd:.1f}%</span>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  PAGE 4 — EARLY WARNINGS
# ═══════════════════════════════════════════════
elif page == "⚡ Early Warnings":
    st.markdown('<div class="section-title">⚡ Early Warning Alert System</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#0d1730;border:1px solid #f4433633;border-radius:6px;
                padding:13px;margin-bottom:18px;font-size:11px;color:#6b7fa3;line-height:1.8;">
    🚨 <b style="color:#e8edf8">Early Warning Logic:</b> Countries where PD changed ≥ 0.1 over 2 years.
    Rising = imminent distress risk. Improving = successful policy impact.
    Lead time: <b style="color:#00d4ff">2–4 quarters</b> before crisis peak.
    </div>""", unsafe_allow_html=True)

    # Compute alerts — use filt_dm to respect region/tier filters
    alerts_list = []
    _ew_dm = filt_dm if sel_yr == "All" else dm  # use full history for trajectory, but filter by region/tier
    # Always use full dm for trajectory, but filter countries by region/tier from filt_latest
    _allowed = set(filt_latest["COUNTRY_WB"].unique())
    for country, grp in dm.groupby("COUNTRY_WB"):
        if country not in _allowed: continue
        grp = grp.sort_values("YEAR")
        if len(grp)>=3:
            last = grp.iloc[-1]; prev = grp.iloc[-3]
            chg  = last["PD"]-prev["PD"]
            if abs(chg)>=0.08:
                alerts_list.append({
                    "Country":country,"Category":last["RISK_CATEGORY"],
                    "Change":round(chg,3),"Current PD":round(last["PD"],3),
                    "Type":"🚨 RISING" if chg>0 else "📈 IMPROVING"
                })
    alert_df = pd.DataFrame(alerts_list).sort_values("Change",key=abs,ascending=False) if alerts_list else pd.DataFrame(columns=["Country","Category","Change","Current PD","Type"])

    c1,c2 = st.columns(2)
    with c1: at = st.radio("Filter",["All","🚨 RISING Only","📈 IMPROVING Only"],horizontal=True)
    with c2: mn = st.slider("Min |ΔPD|",0.05,0.30,0.08,0.01)

    adf = alert_df[alert_df["Change"].abs()>=mn]
    if at=="🚨 RISING Only":    adf = adf[adf["Type"].str.contains("RISING")]
    if at=="📈 IMPROVING Only": adf = adf[adf["Type"].str.contains("IMPROVING")]

    m1,m2,m3 = st.columns(3)
    m1.metric("Total Alerts",len(adf))
    m2.metric("🚨 Rising",(adf["Type"].str.contains("RISING")).sum())
    m3.metric("📈 Improving",(adf["Type"].str.contains("IMPROVING")).sum())
    st.markdown("<br>",unsafe_allow_html=True)

    for _,a in adf.iterrows():
        is_r = "RISING" in a["Type"]
        bc   = "#f44336" if is_r else "#00e676"
        ic   = "🚨" if is_r else "📈"
        st.markdown(f"""
        <div class="alert-card {'alert-rising' if is_r else 'alert-improving'}">
          <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;">
            <div style="font-size:20px">{ic}</div>
            <div style="flex:1">
              <div style="font-size:13px;font-weight:800;color:#fff">{a['Country']}</div>
              <div style="font-size:10px;color:#6b7fa3;margin-top:3px;">
                <span class="pill-{a['Category']}">{a['Category']}</span>
                &nbsp;·&nbsp; Current PD: <b style="color:#e8edf8">{a['Current PD']*100:.1f}%</b>
              </div>
            </div>
            <div style="text-align:right">
              <div style="font-size:18px;font-weight:800;color:{bc}">
                {'+' if is_r else ''}{a['Change']*100:.1f}pp
              </div>
              <div style="font-size:9px;color:#6b7fa3">2-year ΔPD</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="margin-top:20px;">IMF Intervention Recommendations</div>', unsafe_allow_html=True)
    r1,r2 = st.columns(2)
    recs = [
        (r1,"rec-stable","🟢 STABLE — Monitor","#00e676",
         "Routine Article IV surveillance. No intervention needed. Monitor reserve position and external balance quarterly."),
        (r1,"rec-vulnerable","🟡 VULNERABLE — Policy Review","#ffca28",
         "Engage in policy dialogue. Review fiscal sustainability. Consider precautionary credit line if external shock risk is elevated."),
        (r2,"rec-distressed","🟠 DISTRESSED — Assistance Planning","#ff7043",
         "Initiate program discussions. Assess debt sustainability. Prepare SBA/ECF/EFF program terms. Coordinate with World Bank."),
        (r2,"rec-crisis","🔴 CRISIS — Immediate Intervention","#f44336",
         "Emergency financing required. Debt restructuring negotiations. Overdue obligations clearance. High-frequency monitoring with conditionality."),
    ]
    for col,cls,title,clr,text in recs:
        with col:
            st.markdown(f"""
            <div class="{cls}" style="margin-bottom:10px;">
              <div style="font-size:11px;font-weight:700;color:{clr};margin-bottom:6px;">{title}</div>
              <div style="font-size:10px;color:#6b7fa3;line-height:1.7">{text}</div>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  PAGE 5 — REGIONAL ANALYSIS
# ═══════════════════════════════════════════════
elif page == "🗺️ Regional Analysis":
    st.markdown('<div class="section-title">🗺️ Regional Analysis</div>', unsafe_allow_html=True)

    rt = filt_latest.groupby(["REGION","RISK_CATEGORY"]).size().reset_index(name="n")
    rtt= filt_latest.groupby("REGION").size().reset_index(name="total")
    rt = rt.merge(rtt,on="REGION"); rt["pct"]=rt["n"]/rt["total"]*100
    sf = px.bar(rt,x="REGION",y="pct",color="RISK_CATEGORY",
                color_discrete_map=TIER_CLR,text=rt["n"].astype(str),
                category_orders={"RISK_CATEGORY":["Stable","Vulnerable","Distressed","Crisis"]},
                labels={"pct":"Share (%)","RISK_CATEGORY":"Category"})
    sf.update_traces(textposition="inside",textfont=dict(color="#fff",size=10))
    sf.update_layout(**pt_base("xaxis"),height=340,barmode="stack",xaxis=dict(**PT["xaxis"],tickangle=20))
    st.plotly_chart(sf,use_container_width=True)

    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-title">Avg Distress PD by Region</div>', unsafe_allow_html=True)
        ra = filt_latest.groupby("REGION")["PD"].mean().reset_index()
        raf= px.bar(ra.sort_values("PD"),x="PD",y="REGION",orientation="h",
                    color="REGION",color_discrete_map=REGION_CLR,
                    text=(ra.sort_values("PD")["PD"]*100).round(1).astype(str)+"%")
        raf.update_traces(textposition="outside",textfont=dict(color="#e8edf8",size=10))
        raf.update_layout(**PT,height=300,showlegend=False)
        st.plotly_chart(raf,use_container_width=True)

    with c2:
        st.markdown('<div class="section-title">Regional PD Trend Over Time</div>', unsafe_allow_html=True)
        ryt = filt_dm.groupby(["REGION","YEAR"])["PD"].mean().reset_index()
        rtf = px.line(ryt,x="YEAR",y="PD",color="REGION",color_discrete_map=REGION_CLR,markers=True,
                      labels={"PD":"Avg PD","YEAR":"Year"})
        rtf.update_layout(**PT,height=300)
        st.plotly_chart(rtf,use_container_width=True)

    st.markdown('<div class="section-title">Region Drill-Down</div>', unsafe_allow_html=True)
    sr = st.selectbox("Select Region",sorted(filt_latest["REGION"].unique()) if len(filt_latest)>0 else sorted(dm["REGION"].unique()),index=0)
    rc = filt_latest[filt_latest["REGION"]==sr].sort_values("PD",ascending=False)
    df2= px.bar(rc,x="COUNTRY_WB",y="PD",color="RISK_CATEGORY",color_discrete_map=TIER_CLR,
                hover_data={"GDP_GROWTH":":.2f","INFLATION":":.2f"},
                labels={"COUNTRY_WB":"Country","PD":"Distress PD"})
    df2.update_layout(**pt_base("xaxis"),height=320,xaxis={**PT["xaxis"],"tickangle":40,"tickfont":{"color":"#6b7fa3","size":8}})
    st.plotly_chart(df2,use_container_width=True)

# ═══════════════════════════════════════════════
#  PAGE 6 — FEATURE IMPORTANCE
# ═══════════════════════════════════════════════
elif page == "📊 Feature Importance":
    st.markdown('<div class="section-title">📊 ML Feature Importance — Random Forest</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#0d1730;border:1px solid #00d4ff33;border-radius:6px;
                padding:13px;margin-bottom:18px;font-size:11px;color:#6b7fa3;line-height:1.8;">
    📊 Features ranked by their contribution to the Random Forest model's prediction of sovereign distress.
    Higher importance = stronger predictor of <b style="color:#e8edf8">DISTRESS_NEXT_YEAR</b>.
    </div>""", unsafe_allow_html=True)

    fi_sorted = fi.sort_values("Importance",ascending=True)
    colors_fi  = ["#f44336" if i>=len(fi_sorted)-5 else "#00d4ff" if i>=len(fi_sorted)-10 else "#4a5a7a"
                  for i in range(len(fi_sorted))]
    fif = go.Figure(go.Bar(
        x=fi_sorted["Importance"]*100, y=fi_sorted["Feature"],orientation="h",
        marker_color=colors_fi,
        text=(fi_sorted["Importance"]*100).round(1).astype(str)+"%",
        textposition="outside",textfont=dict(color="#e8edf8",size=10),
        hovertemplate="<b>%{y}</b><br>Importance: %{x:.1f}%<extra></extra>"
    ))
    fif.update_layout(**pt_base("xaxis"),height=560,
                      xaxis=dict(**PT["xaxis"],title="Feature Importance (%)",range=[0,22]),
                      showlegend=False)
    st.plotly_chart(fif,use_container_width=True)

    # Top features table
    st.markdown('<div class="section-title">Top 5 Risk Drivers</div>', unsafe_allow_html=True)
    top5 = fi.nlargest(5,"Importance").reset_index(drop=True)
    descs = {
        "SOVEREIGN_RISK_SCORE":"Composite score combining all risk pillars — strongest single predictor",
        "imf_borrowing_ratio":"IMF credit outstanding as % of quota — direct stress indicator",
        "RESERVE_ADEQUACY_RISK":"Composite reserve coverage risk — buffer against external shocks",
        "IMF_DEPENDENCE_RISK":"Degree of reliance on IMF financing — structural vulnerability",
        "prgt_ratio":"Concessional lending ratio — low-income country distress indicator"
    }
    c1,c2 = st.columns(2)
    for i,(_,row) in enumerate(top5.iterrows()):
        col = c1 if i%2==0 else c2
        with col:
            pct = row["Importance"]*100
            st.markdown(f"""
            <div style="background:#0d1730;border:1px solid #1a2d52;border-radius:6px;
                        padding:14px;margin-bottom:10px;border-left:3px solid #00d4ff;">
              <div style="font-family:Syne,sans-serif;font-size:12px;font-weight:700;
                          color:#fff;margin-bottom:4px;">#{i+1} {row['Feature']}</div>
              <div style="font-size:20px;font-weight:800;color:#00d4ff;margin-bottom:6px;">{pct:.1f}%</div>
              <div style="font-size:10px;color:#6b7fa3;line-height:1.6">{descs.get(row['Feature'],'Key predictor of sovereign distress.')}</div>
            </div>""", unsafe_allow_html=True)

    # Pillar radar
    st.markdown('<div class="section-title">Risk Pillar Breakdown by Country</div>', unsafe_allow_html=True)
    sel_cp = st.selectbox("Select Country",sorted(cp["COUNTRY_WB"].unique()),
                           index=list(sorted(cp["COUNTRY_WB"].unique())).index("Pakistan") if "Pakistan" in cp["COUNTRY_WB"].values else 0)
    cp_row = cp[cp["COUNTRY_WB"]==sel_cp].iloc[0]
    pillars = ["IMF_DEPENDENCE_RISK","RESERVE_ADEQUACY_RISK","MACROECONOMIC_RISK",
               "CLIMATE_VULNERABILITY_RISK","MARKET_VULNERABILITY_RISK"]
    plabels = ["IMF Dependence","Reserve Adequacy","Macroeconomic","Climate Vulnerability","Market Vulnerability"]
    vals    = [cp_row[p] for p in pillars]
    mn_v,mx_v = min(vals),max(vals)
    norm_v  = [(v-mn_v)/(mx_v-mn_v+1e-9)*100 for v in vals]
    norm_v.append(norm_v[0]); plabels2=plabels+[plabels[0]]
    rf2 = go.Figure(go.Scatterpolar(r=norm_v,theta=plabels2,fill="toself",name=sel_cp,
                                     line=dict(color="#00d4ff",width=2),fillcolor="rgba(0,212,255,0.12)"))
    rf2.update_layout(
        polar=dict(bgcolor="rgba(0,0,0,0)",
                   radialaxis=dict(visible=True,range=[0,110],tickfont=dict(color="#6b7fa3",size=8),gridcolor="#1a2d52"),
                   angularaxis=dict(tickfont=dict(color="#6b7fa3",size=10),gridcolor="#1a2d52")),
        **pt_base("xaxis","yaxis","margin"),
        height=380,margin=dict(l=80,r=80,t=40,b=40),showlegend=False
    )
    st.plotly_chart(rf2,use_container_width=True)

# ═══════════════════════════════════════════════
#  PAGE 7 — COUNTRY COMPARISON
# ═══════════════════════════════════════════════
elif page == "⚖️ Country Comparison":
    st.markdown('<div class="section-title">⚖️ Country Comparison</div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: cm1 = st.selectbox("Country A",all_countries,index=all_countries.index("Pakistan"))
    with c2: cm2 = st.selectbox("Country B",all_countries,index=all_countries.index("India"))

    r1 = latest[latest["COUNTRY_WB"]==cm1].iloc[0] if len(latest[latest["COUNTRY_WB"]==cm1])>0 else None
    r2 = latest[latest["COUNTRY_WB"]==cm2].iloc[0] if len(latest[latest["COUNTRY_WB"]==cm2])>0 else None
    if r1 is None or r2 is None:
        st.error("Country data not found for selected year.")
    else:
        c1,c2 = st.columns(2)
        for col,r,nm in [(c1,r1,cm1),(c2,r2,cm2)]:
            with col:
                clr = TIER_CLR.get(r["RISK_CATEGORY"],"#fff")
                mets=[("Distress PD",f"{r['PD']*100:.1f}%"),
                      ("Risk Category",r["RISK_CATEGORY"]),
                      ("Risk Score",f"{r['SOVEREIGN_RISK_SCORE']:.3f}"),
                      ("GDP Growth",f"{r['GDP_GROWTH']:.3f}"),
                      ("Inflation",f"{r['INFLATION']:.3f}"),
                      ("Current Account",f"{r['CURRENT_ACCOUNT']:.3f}"),
                      ("Total Reserves",f"{r['TOTAL_RESERVES']:.3f}"),
                      ("FX Volatility",f"{r['FX_VOLATILITY']:.3f}")]
                rows_html="".join([f"""
                <div style="display:flex;justify-content:space-between;padding:7px 0;
                            border-bottom:1px solid #111c35;font-size:11px;">
                  <span style="color:#6b7fa3">{l}</span>
                  <span style="color:#fff;font-weight:600">{v}</span>
                </div>""" for l,v in mets])
                st.markdown(f"""
                <div style="background:#0d1730;border:1px solid {clr}44;
                            border-top:3px solid {clr};border-radius:7px;padding:18px;margin-bottom:12px;">
                  <div style="font-size:18px;font-weight:800;color:#fff;margin-bottom:8px;">{nm}</div>
                  {rows_html}
                </div>""", unsafe_allow_html=True)

        # Radar + Trend
        c1,c2 = st.columns(2)
        with c1:
            st.markdown('<div class="section-title">Indicator Radar</div>', unsafe_allow_html=True)
            rm = ["PD","GDP_GROWTH","INFLATION","TOTAL_RESERVES","FX_VOLATILITY","SOVEREIGN_RISK_SCORE"]
            rl = ["Distress PD","GDP Growth","Inflation","Total Reserves","FX Volatility","Risk Score"]
            def norm2(r,cols): return [min(100,abs(r[c])/max(abs(latest[c]).max(),1e-6)*100) for c in cols]
            rcf = go.Figure()
            for r,nm,clr in [(r1,cm1,"#00d4ff"),(r2,cm2,"#ffca28")]:
                vs = norm2(r,rm); vs.append(vs[0]); ls2=rl+[rl[0]]
                rcf.add_trace(go.Scatterpolar(r=vs,theta=ls2,fill="toself",name=nm,
                                               line=dict(color=clr,width=2),fillcolor=hex_alpha(clr,0.12)))
            rcf.update_layout(
                polar=dict(bgcolor="rgba(0,0,0,0)",
                           radialaxis=dict(visible=True,range=[0,110],tickfont=dict(color="#6b7fa3",size=8),gridcolor="#1a2d52"),
                           angularaxis=dict(tickfont=dict(color="#6b7fa3",size=9),gridcolor="#1a2d52")),
                **pt_base("xaxis","yaxis","margin","legend"),
                height=340,legend=dict(font=dict(color="#e8edf8",size=11)),margin=dict(l=70,r=70,t=30,b=30)
            )
            st.plotly_chart(rcf,use_container_width=True)

        with c2:
            st.markdown('<div class="section-title">PD Trend Comparison</div>', unsafe_allow_html=True)
            ctd = dm[dm["COUNTRY_WB"].isin([cm1,cm2])].sort_values("YEAR")
            ctf = px.line(ctd,x="YEAR",y="PD",color="COUNTRY_WB",markers=True,
                          color_discrete_map={cm1:"#00d4ff",cm2:"#ffca28"},
                          labels={"PD":"Distress Probability","YEAR":"Year","COUNTRY_WB":"Country"})
            ctf.update_layout(**PT,height=340)
            st.plotly_chart(ctf,use_container_width=True)

# ═══════════════════════════════════════════════
#  PAGE 8 — HEALTH CARD
# ═══════════════════════════════════════════════
elif page == "🃏 Health Card":
    st.markdown('<div class="section-title">🃏 Sovereign Health Card + Similarity Engine</div>', unsafe_allow_html=True)
    sel = st.selectbox("Select Country",all_countries,index=all_countries.index("Pakistan"))
    row = latest[latest["COUNTRY_WB"]==sel]
    if row.empty:
        st.warning("No data for latest year.")
    else:
        r   = row.iloc[0]
        clr = TIER_CLR.get(r["RISK_CATEGORY"],"#fff")
        c1,c2 = st.columns([1,2])
        with c1:
            def hl(val,th,lb): return next((l for t,l in zip(th,lb) if val>=t),lb[-1])
            bh = hl(abs(r["PD"]),[0.7,0.5,0.2],[("🔴 Poor","#f44336"),("🟠 Moderate","#ff7043"),("🟢 Good","#00e676")])
            rh = hl(r["TOTAL_RESERVES"],[0.5,0],[("🟢 Strong","#00e676"),("🟡 Moderate","#ffca28"),("🔴 Weak","#f44336")])
            ir = hl(r["INFLATION"],[1,0.5,0],[("🔴 High","#f44336"),("🟠 Elevated","#ff7043"),("🟢 Normal","#00e676")])
            rc_map={"Stable":"✅ Monitor","Vulnerable":"⚠️ Policy Review",
                    "Distressed":"🟠 Assistance","Crisis":"🔴 Emergency"}
            rc_txt={"Stable":"Routine surveillance. No intervention needed.",
                    "Vulnerable":"Engage policy dialogue. Consider precautionary credit line.",
                    "Distressed":"Initiate IMF program. Assess debt sustainability.",
                    "Crisis":"Emergency financing. Debt restructuring. Immediate action."}
            health_grid = "".join([f"""
            <div style="background:#101c38;border-radius:4px;padding:10px;text-align:center;">
              <div style="font-size:12px;font-weight:700;color:{v[1]}">{v[0]}</div>
              <div style="font-size:8px;color:#6b7fa3;margin-top:3px;letter-spacing:1px">{l}</div>
            </div>""" for v,l in [(bh,"DISTRESS RISK"),(rh,"RESERVES"),(ir,"INFLATION"),
                                   (("🔴 Overdue","#f44336") if r.get("FX_VOLATILITY",0)>1 else ("🟢 Normal","#00e676"),"FX STABILITY")]])
            st.markdown(f"""
            <div style="background:#0d1730;border:1px solid {clr}55;border-top:3px solid {clr};
                        border-radius:8px;padding:20px;">
              <div style="font-size:20px;font-weight:800;color:#fff;margin-bottom:4px">{sel}</div>
              <span class="pill-{r['RISK_CATEGORY']}">{r['RISK_CATEGORY']}</span>
              <div style="font-size:38px;font-weight:800;color:{clr};text-align:center;
                          padding:16px 0;margin:14px 0;border-top:1px solid #1a2d52;border-bottom:1px solid #1a2d52;">
                {r['PD']*100:.1f}% PD
              </div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px;">
                {health_grid}
              </div>
              <div style="background:{clr}12;border:1px solid {clr}33;border-radius:5px;padding:12px;">
                <div style="font-size:10px;font-weight:700;color:{clr};letter-spacing:1px;margin-bottom:5px">
                  🏛 {rc_map.get(r['RISK_CATEGORY'],'Monitor')}
                </div>
                <div style="font-size:10px;color:#6b7fa3;line-height:1.7">{rc_txt.get(r['RISK_CATEGORY'],'')}</div>
              </div>
            </div>""", unsafe_allow_html=True)

        with c2:
            # PD trend
            st.markdown('<div class="section-title">Risk Trajectory</div>', unsafe_allow_html=True)
            cd = dm[dm["COUNTRY_WB"]==sel].sort_values("YEAR")
            tf3= px.line(cd,x="YEAR",y="PD",color_discrete_sequence=[clr],markers=True,
                         labels={"PD":"Distress PD","YEAR":"Year"})
            tf3.update_traces(fill="tozeroy",fillcolor=hex_alpha(clr,0.08),line_width=2.5,marker_size=6)
            tf3.update_layout(**pt_base("yaxis"),height=220,showlegend=False,
                              yaxis=dict(**PT["yaxis"],title="Distress PD"))
            st.plotly_chart(tf3,use_container_width=True)

            # Pillar radar
            st.markdown('<div class="section-title">Risk Pillar Breakdown</div>', unsafe_allow_html=True)
            if sel in cp["COUNTRY_WB"].values:
                cp_r = cp[cp["COUNTRY_WB"]==sel].iloc[0]
                pvs  = [cp_r[p] for p in ["IMF_DEPENDENCE_RISK","RESERVE_ADEQUACY_RISK",
                                            "MACROECONOMIC_RISK","CLIMATE_VULNERABILITY_RISK","MARKET_VULNERABILITY_RISK"]]
                pls  = ["IMF Depend.","Reserve\nAdequacy","Macro","Climate","Market"]
                pvn  = [(v-min(pvs))/(max(pvs)-min(pvs)+1e-9)*100 for v in pvs]
                pvn.append(pvn[0]); pls2=pls+[pls[0]]
                rf3  = go.Figure(go.Scatterpolar(r=pvn,theta=pls2,fill="toself",
                                                  line=dict(color=clr,width=2),fillcolor=hex_alpha(clr,0.12)))
                rf3.update_layout(
                    polar=dict(bgcolor="rgba(0,0,0,0)",
                               radialaxis=dict(visible=True,range=[0,110],tickfont=dict(color="#6b7fa3",size=8),gridcolor="#1a2d52"),
                               angularaxis=dict(tickfont=dict(color="#6b7fa3",size=9),gridcolor="#1a2d52")),
                    **pt_base("xaxis","yaxis","margin"),
                    height=250,margin=dict(l=60,r=60,t=20,b=20),showlegend=False
                )
                st.plotly_chart(rf3,use_container_width=True)

        # Similarity Engine
        st.markdown('<div class="section-title">🤖 Crisis Similarity Engine</div>', unsafe_allow_html=True)
        feats=["PD","SOVEREIGN_RISK_SCORE","GDP_GROWTH","INFLATION","FX_VOLATILITY"]
        dists=[]
        for _,ot in latest.iterrows():
            if ot["COUNTRY_WB"]==sel: continue
            d=math.sqrt(sum((r[f]-ot[f])**2 for f in feats if f in latest.columns))
            dists.append({"Country":ot["COUNTRY_WB"],"Category":ot["RISK_CATEGORY"],
                          "PD":ot["PD"],"Match%":round(max(0,100-d*30),1)})
        sim=pd.DataFrame(dists).sort_values("Match%",ascending=False).head(5)
        sc2=st.columns(5)
        for i,(_,s) in enumerate(sim.iterrows()):
            if i>=5: break
            with sc2[i]:
                sc=TIER_CLR.get(s["Category"],"#fff")
                st.markdown(f"""
                <div style="background:#0d1730;border:1px solid {sc}44;border-top:2px solid {sc};
                            border-radius:5px;padding:12px;text-align:center;">
                  <div style="font-size:12px;font-weight:700;color:#fff;margin-bottom:4px">{s['Country']}</div>
                  <span class="pill-{s['Category']}">{s['Category']}</span>
                  <div style="font-size:20px;font-weight:800;color:{sc};margin-top:8px">{s['Match%']:.0f}%</div>
                  <div style="font-size:9px;color:#6b7fa3">match</div>
                  <div style="font-size:10px;color:#e8edf8;margin-top:4px">PD: {s['PD']*100:.1f}%</div>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  PAGE 9 — INDIA DEEP DIVE
# ═══════════════════════════════════════════════
elif page == "🇮🇳 India Deep Dive":
    st.markdown('<div class="section-title">🇮🇳 India Sovereign Risk — Deep Dive</div>', unsafe_allow_html=True)
    import os
    _base = "/mnt/user-data/uploads" if os.path.exists("/mnt/user-data/uploads/India_Dashboard_Data.csv") else "."
    ind2 = pd.read_csv(f"{_base}/India_Dashboard_Data.csv")
    ir   = ind2.iloc[-1]
    clr  = TIER_CLR.get(ir["RISK_CATEGORY"],"#00e676")

    k1,k2,k3,k4 = st.columns(4)
    for col,val,lbl in [
        (k1,f"{ir['PD']*100:.1f}%","Distress PD"),
        (k2,ir["RISK_CATEGORY"],"Risk Category"),
        (k3,f"{ir['GDP_GROWTH']:.3f}","GDP Growth"),
        (k4,f"{ir['INFLATION']:.3f}","Inflation")
    ]:
        with col: st.metric(lbl,val)

    st.markdown('<div class="section-title" style="margin-top:16px;">India PD Trend (2007–2024)</div>', unsafe_allow_html=True)
    itf = go.Figure()
    itf.add_trace(go.Scatter(x=ind2["YEAR"].astype(str),y=ind2["PD"]*100,mode="lines+markers",
                              name="Distress PD",line=dict(color="#00d4ff",width=2.5),
                              marker=dict(size=7,color="#00d4ff"),fill="tozeroy",fillcolor="rgba(0,212,255,0.08)",
                              hovertemplate="Year: %{x}<br>PD: %{y:.1f}%<extra></extra>"))
    itf.add_trace(go.Scatter(x=ind2["YEAR"].astype(str),y=ind2["SOVEREIGN_RISK_SCORE"],mode="lines",
                              name="Risk Score",line=dict(color="#ffca28",width=1.5,dash="dot"),
                              hovertemplate="Year: %{x}<br>Score: %{y:.3f}<extra></extra>"))
    itf.update_layout(**pt_base("legend"),height=320,legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(color="#e8edf8",size=11)))
    st.plotly_chart(itf,use_container_width=True)

    c1,c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-title">GDP Growth vs Inflation</div>', unsafe_allow_html=True)
        gf = go.Figure()
        gf.add_trace(go.Bar(x=ind2["YEAR"].astype(str),y=ind2["GDP_GROWTH"],name="GDP Growth",marker_color="rgba(0,230,118,0.67)"))
        gf.add_trace(go.Bar(x=ind2["YEAR"].astype(str),y=ind2["INFLATION"],name="Inflation",marker_color="rgba(255,202,40,0.67)"))
        gf.update_layout(**pt_base("xaxis"),height=280,barmode="group",xaxis=dict(**PT["xaxis"],tickangle=45))
        st.plotly_chart(gf,use_container_width=True)

    with c2:
        st.markdown('<div class="section-title">India Risk Category Timeline</div>', unsafe_allow_html=True)
        cat_map = {"Stable":1,"Vulnerable":2,"Distressed":3,"Crisis":4}
        ind2["cat_num"] = ind2["RISK_CATEGORY"].map(cat_map)
        cf = px.line(ind2,x="YEAR",y="cat_num",color_discrete_sequence=["#00d4ff"],markers=True)
        cf.update_yaxes(tickvals=[1,2,3,4],ticktext=["Stable","Vulnerable","Distressed","Crisis"])
        cf.update_layout(**PT,height=280,showlegend=False)
        st.plotly_chart(cf,use_container_width=True)

    st.markdown('<div class="section-title">India vs Global Average</div>', unsafe_allow_html=True)
    global_avg = dm.groupby("YEAR")["PD"].mean().reset_index()
    cmp_fig = go.Figure()
    cmp_fig.add_trace(go.Scatter(x=ind2["YEAR"].astype(str),y=ind2["PD"]*100,mode="lines+markers",
                                  name="India",line=dict(color="#00d4ff",width=2.5),marker_size=6))
    cmp_fig.add_trace(go.Scatter(x=global_avg["YEAR"].astype(str),y=global_avg["PD"]*100,mode="lines",
                                  name="Global Avg",line=dict(color="#f44336",width=1.5,dash="dot")))
    cmp_fig.update_layout(**pt_base("legend"),height=300,legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(color="#e8edf8",size=11)))
    st.plotly_chart(cmp_fig,use_container_width=True)

# ═══════════════════════════════════════════════
#  PAGE 10 — AI CHATBOT
# ═══════════════════════════════════════════════
elif page == "🤖 AI Chatbot":
    st.markdown('<div class="section-title">🤖 Sovereign Risk AI Assistant</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#0d1730;border:1px solid #00d4ff33;border-radius:7px;
                padding:14px;margin-bottom:16px;font-size:11px;color:#6b7fa3;line-height:1.8;">
    💡 <b style="color:#e8edf8">Ask me anything about sovereign risk!</b><br>
    Try: <i>"What is Pakistan's risk?"</i> · <i>"Which countries are in crisis?"</i> · 
    <i>"What are the top risk drivers?"</i> · <i>"Explain PD"</i> · <i>"Show stable countries"</i>
    </div>""", unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            ("bot","👋 Hello! I'm your Sovereign Risk AI Assistant.\n\nI can answer questions about:\n• Any country's risk profile\n• Crisis / stable country lists\n• Feature importance & ML models\n• Global distress trends\n• IMF intervention recommendations\n\nJust type your question below! 🌍")
        ]

    # Display chat
    chat_html = ""
    for role, msg in st.session_state.chat_history:
        if role=="user":
            chat_html += f'<div class="chatbot-msg-user">👤 {msg}</div>'
        else:
            formatted = msg.replace("\n","<br>").replace("**","<b>").replace("**","</b>")
            # Simple bold formatting
            import re
            formatted = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', msg.replace("\n","<br>"))
            chat_html += f'<div class="chatbot-msg-bot">🤖 {formatted}</div>'

    st.markdown(f'<div class="chatbot-wrap">{chat_html}</div>', unsafe_allow_html=True)

    # Input
    with st.form("chat_form", clear_on_submit=True):
        c1,c2 = st.columns([5,1])
        with c1: user_input = st.text_input("",placeholder="Ask about any country, risk drivers, trends...",label_visibility="collapsed")
        with c2: submitted  = st.form_submit_button("Send 🚀")

    if submitted and user_input.strip():
        response = chatbot_response(user_input, dm, latest, fi, cp)
        st.session_state.chat_history.append(("user", user_input))
        st.session_state.chat_history.append(("bot", response))
        st.rerun()

    # Quick questions
    st.markdown("**💡 Quick Questions:**")
    qcols = st.columns(4)
    quick_qs = [
        "Which countries are in crisis?",
        "What are the top risk drivers?",
        "Show most stable countries",
        "What is the global trend?"
    ]
    for col, q in zip(qcols, quick_qs):
        with col:
            if st.button(q, use_container_width=True):
                response = chatbot_response(q, dm, latest, fi, cp)
                st.session_state.chat_history.append(("user", q))
                st.session_state.chat_history.append(("bot", response))
                st.rerun()

    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = [("bot","Chat cleared! Ask me anything about sovereign risk. 🌍")]
        st.rerun()

# ── Footer ────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:20px;color:#6b7fa3;font-size:9px;
            letter-spacing:2px;border-top:1px solid #1a2d52;margin-top:24px;">
GFST · TEAM F · SOVEREIGN FINANCIAL DISTRESS EARLY WARNING SYSTEM · IMF FA 8.0.0 · 2007–2024 · MENTOR: ANAND SHARMA
</div>""", unsafe_allow_html=True)
