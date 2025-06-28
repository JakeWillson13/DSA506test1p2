import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="University Dashboard", layout="wide")
st.title("University Growth & Dept. Enrollment Dashboard")

# ──────────────────────────────────────────
# Figure 1 – Overall metrics
# ──────────────────────────────────────────
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
palette1 = ["#1f77b4", "#2ca02c", "#d62728"]

fig1 = go.Figure()
for i, metric in enumerate(df1["Metric"].unique()):
    sub = df1[df1["Metric"] == metric]
    fig1.add_bar(
        x=sub["Category"],
        y=sub["Percent"],
        marker_color=palette1,
        text=[f"{v:.1f}%" for v in sub["Percent"]],
        textposition="outside",
        name=metric,
        visible=i == 0,
    )

buttons1 = [
    {
        "label": m,
        "method": "update",
        "args": [
            {"visible": [m == x for x in df1["Metric"].unique()]},
            {"title": m, "yaxis": {"range": [0, df1[df1.Metric == m].Percent.max() * 1.1]}}
        ],
    }
    for m in df1["Metric"].unique()
]

fig1.update_layout(
    updatemenus=[dict(buttons=buttons1, x=0.02, y=1.15, showactive=True)],
    title=df1["Metric"].unique()[0],
    title_x=0.5,
    template="plotly_white",
    bargap=0.3,
    height=450,
    yaxis_title="Percent",
    margin=dict(l=50, r=50, t=100, b=50),
)

# ──────────────────────────────────────────
# Figure 2 – Department enrollment % changes
# ──────────────────────────────────────────
dept_data = {
    "Department": ["Arts Enrolled", "Business Enrolled", "Engineering Enrolled", "Science Enrolled"],
    "Average YoY":   [3.9, 4.7, 4.7, -2.3],
    "2024 Increase": [6.1, 7.1, 5.3, -13.0],
}
df2 = pd.DataFrame(dept_data).set_index("Department")
metrics2 = df2.columns.tolist()
depts    = df2.index.tolist()
palette2 = ["#1f77b4", "#ff7f0e"]

fig2 = go.Figure()
for i, d in enumerate(depts):
    fig2.add_bar(
        x=metrics2,
        y=df2.loc[d].values,
        name=d,
        marker_color=palette2,
        text=[f"{v:.1f}%" for v in df2.loc[d].values],
        textposition="outside",
        visible=i == 0,
    )

buttons2 = [
    {
        "label": d,
        "method": "update",
        "args": [
            {"visible": [d == x for x in depts]},
            {"title": f"{d}: Enrollment % Changes"}
        ],
    }
    for d in depts
]

ymin, ymax = df2.values.min() * 1.2, df2.values.max() * 1.2
fig2.update_layout(
    updatemenus=[dict(
        buttons=buttons2,
        direction="down",
        x=0.0, y=0.8,
        xanchor="left", yanchor="top",
        pad={"l": 10, "t": 10},
        showactive=True,
    )],
    title=f"{depts[0]}: Enrollment % Changes",
    title_x=0.5,
    template="plotly_white",
    yaxis=dict(range=[ymin, ymax], title="Percent"),
    margin=dict(l=150, r=20, t=50, b=50),
)

# ──────────────────────────────────────────
# Streamlit layout
# ──────────────────────────────────────────
tab1, tab2 = st.tabs(["Overall Metrics", "Dept. Enrollment % Changes"])
with tab1:
    st.plotly_chart(fig1, use_container_width=True)
with tab2:
    st.plotly_chart(fig2, use_container_width=True)
