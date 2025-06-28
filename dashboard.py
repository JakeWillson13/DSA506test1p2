# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="University Dashboard", layout="wide")
st.title("University Growth & Department Enrollment Dashboard")

COMMON_MARGIN = dict(l=150, r=50, t=40, b=50)
MENU_POS      = dict(x=0.02, y=1.15)   # same menu coordinates for both charts

# ──────────────────────────────────────────
# Figure 1 – Overall metrics
# ──────────────────────────────────────────
overall_data = {
    "Metric": ["Total Increase", "Average YoY", "CAGR"],
    "Applications": [40.0, 1.8, 3.8],
    "Admissions":   [40.0, 1.8, 3.8],
    "Enrollments":  [33.3, 1.5, 3.2],
}
df1 = pd.DataFrame(overall_data).melt(
    id_vars="Metric", var_name="Category", value_name="Percent"
)

palette1 = ["#1f77b4", "#2ca02c", "#d62728"]
fig1     = go.Figure()

for i, m in enumerate(df1["Metric"].unique()):
    sub = df1[df1["Metric"] == m]
    fig1.add_bar(
        x=sub["Category"],
        y=sub["Percent"],
        marker_color=palette1,
        text=[f"{v:.1f}%" for v in sub["Percent"]],
        textposition="outside",
        name=m,
        visible=i == 0,
    )

# toggle metric buttons
buttons1 = []
for i, m in enumerate(df1["Metric"].unique()):
    ymax = df1.query("Metric == @m")["Percent"].max() * 1.1
    vis  = [i == j for j in range(len(df1["Metric"].unique()))]
    buttons1.append(
        dict(
            label=m,
            method="update",
            args=[{"visible": vis}, {"yaxis": {"range": [0, ymax]}}],
        )
    )

fig1.update_layout(
    updatemenus=[dict(buttons=buttons1, **MENU_POS, showactive=True)],
    template="plotly_white",
    bargap=0.3,
    height=450,
    yaxis_title="Percent",
    margin=COMMON_MARGIN,
)

# ──────────────────────────────────────────
# Figure 2 – Department enrollment % changes
# ──────────────────────────────────────────
dept_data = {
    "Department": ["Arts Enrolled", "Business Enrolled",
                   "Engineering Enrolled", "Science Enrolled"],
    "Average YoY":   [ 3.9,  4.7,  4.7,  -2.3],
    "2024 Increase": [ 6.1,  7.1,  5.3, -13.0],
}
df2      = pd.DataFrame(dept_data).set_index("Department")
metrics2 = df2.columns.tolist()
depts    = df2.index.tolist()
colors2  = ["#1f77b4", "#ff7f0e"]
fig2     = go.Figure()

for i, d in enumerate(depts):
    fig2.add_bar(
        x=metrics2,
        y=df2.loc[d].values,
        name=d,
        marker_color=colors2,
        text=[f"{v:.1f}%" for v in df2.loc[d].values],
        textposition="outside",
        visible=i == 0,
    )

def pad_range(lo, hi, pct=0.10):
    span = max(abs(lo), abs(hi))
    pad  = span * pct
    return [lo - pad, hi + pad] if lo < hi else [hi - pad, lo + pad]

buttons2 = []
for i, d in enumerate(depts):
    vis    = [j == i for j in range(len(depts))]
    lo, hi = df2.loc[d].min(), df2.loc[d].max()
    yrange = pad_range(lo, hi)
    buttons2.append(
        dict(
            label=d,
            method="update",
            args=[
                {"visible": vis},
                {"yaxis": {"range": yrange, "title": "Percent"}},
            ],
        )
    )

init_yrange = pad_range(df2.iloc[0].min(), df2.iloc[0].max())

fig2.update_layout(
    updatemenus=[dict(
        buttons=buttons2,
        direction="down",
        **MENU_POS,
        xanchor="left", yanchor="top",
        pad={"l": 10, "t": 10},
        showactive=True,
    )],
    template="plotly_white",
    height=450,
    yaxis=dict(range=init_yrange, title="Percent"),
    margin=COMMON_MARGIN,
)

# ──────────────────────────────────────────
# Streamlit layout (tabs)
# ──────────────────────────────────────────
tab1, tab2 = st.tabs(["Overall Metrics", "Department Metrics"])
with tab1:
    st.plotly_chart(fig1, use_container_width=True)
with tab2:
    st.plotly_chart(fig2, use_container_width=True)
