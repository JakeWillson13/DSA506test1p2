# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="University Dashboard", layout="wide")
st.title("University Growth & Dept. Enrollment Dashboard")

# ────────────────────────────────────────────
# Figure 1 – Overall metrics (3-bar view)
# ────────────────────────────────────────────
overall_data = {
    "Metric": ["Total Increase", "Average YoY", "CAGR"],
    "Applications": [40.0, 1.8, 3.8],
    "Admissions":   [40.0, 1.8, 3.8],
    "Enrollments":  [33.3, 1.5, 3.2],
}
df1 = (
    pd.DataFrame(overall_data)
      .melt(id_vars="Metric", var_name="Category", value_name="Percent")
)

palette1   = ["#1f77b4", "#2ca02c", "#d62728"]
metrics1   = df1["Metric"].unique()
fig1       = go.Figure()

for i, m in enumerate(metrics1):
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

# buttons to toggle metric
buttons1 = []
for i, m in enumerate(metrics1):
    ymax = df1.query("Metric == @m")["Percent"].max() * 1.1
    vis  = [i == j for j in range(len(metrics1))]
    buttons1.append(
        dict(
            label=m,
            method="update",
            args=[
                {"visible": vis},
                {"title": m, "yaxis": {"range": [0, ymax]}}
            ],
        )
    )

fig1.update_layout(
    updatemenus=[dict(buttons=buttons1, x=0.02, y=1.15, showactive=True)],
    title=metrics1[0],
    title_x=0.5,
    template="plotly_white",
    bargap=0.3,
    height=450,
    yaxis_title="Percent",
    margin=dict(l=50, r=50, t=100, b=50),
)

# ────────────────────────────────────────────
# Figure 2 – Dept. enrollment % changes
# ────────────────────────────────────────────
dept_data = {
    "Department": ["Arts Enrolled", "Business Enrolled",
                   "Engineering Enrolled", "Science Enrolled"],
    "Average YoY":   [ 3.9,  4.7,  4.7,  -2.3],
    "2024 Increase": [ 6.1,  7.1,  5.3, -13.0],
}
df2      = pd.DataFrame(dept_data).set_index("Department")
metrics2 = df2.columns.tolist()        # ["Average YoY", "2024 Increase"]
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

# helper to build symmetric y-ranges with padding
def pad_range(lo: float, hi: float, pct: float = 0.10):
    span = max(abs(lo), abs(hi))
    pad  = span * pct
    return [lo - pad, hi + pad] if lo < hi else [hi - pad, lo + pad]

# buttons to toggle department with per-dept scaling
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
                {"title": f"{d}: Enrollment % Changes",
                 "yaxis": {"range": yrange, "title": "Percent"}}
            ],
        )
    )

# initial y-axis for first department
init_yrange = pad_range(df2.iloc[0].min(), df2.iloc[0].max())

fig2.update_layout(
    updatemenus=[dict(
        buttons=buttons2,
        direction="down",          # still a vertical list
        x=0.02, y=1.15,           
        xanchor="left", yanchor="top",
        pad={"l": 10, "t": 10},
        showactive=True,
    )],
    title=f"{depts[0]}: Enrollment % Changes",
    title_x=0.5,
    template="plotly_white",
    yaxis=dict(range=init_yrange, title="Percent"),
    margin=dict(l=150, r=20, t=50, b=50),

# ────────────────────────────────────────────
# Streamlit layout (two tabs)
# ────────────────────────────────────────────
tab1, tab2 = st.tabs(["Overall Metrics", "Dept. Enrollment % Changes"])
with tab1:
    st.plotly_chart(fig1, use_container_width=True)
with tab2:
    st.plotly_chart(fig2, use_container_width=True)

