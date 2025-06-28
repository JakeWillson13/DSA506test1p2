# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="University Dashboard", layout="wide")
st.title("University Growth & Dept. Enrollment Dashboard")

# === FIGURE 1: Overall Metrics ===
# Build df in-memory
data1 = {
    "Metric"      : ["Total Increase", "Average YoY", "CAGR"],
    "Applications": [40.0, 1.8, 3.8],
    "Admissions"  : [40.0, 1.8, 3.8],
    "Enrollments" : [33.3, 1.5, 3.2],
}
df1 = pd.DataFrame(data1).melt(
    id_vars="Metric", var_name="Category", value_name="Percent"
)

# Plotly bar chart with buttons
palette1 = ["#1f77b4", "#2ca02c", "#d62728"]
fig1 = go.Figure()
plot_metrics = df1["Metric"].unique()

for i, m in enumerate(plot_metrics):
    sub = df1[df1["Metric"] == m]
    fig1.add_bar(
        x=sub["Category"],
        y=sub["Percent"],
        marker_color=palette1,
        text=sub["Percent"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside",
        name=m,
        visible=(i == 0),
    )

buttons1 = []
for i, m in enumerate(plot_metrics):
    ymax = df1.query("Metric == @m")["Percent"].max() * 1.1
    vis = [i == j for j in range(len(plot_metrics))]
    buttons1.append(dict(
        label=m,
        method="update",
        args=[
            {"visible": vis},
            {"title": m, "yaxis": {"range": [0, ymax]}}
        ],
    ))

fig1.update_layout(
    updatemenus=[dict(buttons=buttons1, x=0.02, y=1.15, showactive=True)],
    title=plot_metrics[0],
    title_x=0.5,
    template="plotly_white",
    bargap=0.3,
    height=450,
    yaxis=dict(title="Percent"),
    margin=dict(l=50, r=50, t=100, b=50),
)

# === FIGURE 2: Dept. Enrollment % Changes ===
data2 = {
    "Department"    : [
        "Arts Enrolled",
        "Business Enrolled",
        "Engineering Enrolled",
        "Science Enrolled"
    ],
    "Average YoY"   : [3.9, 4.7, 4.7, -2.3],
    "2024 Increase" : [6.1, 7.1, 5.3, -13.0],
}
df2 = pd.DataFrame(data2).set_index("Department")
metrics2    = df2.columns.tolist()      # ["Average YoY","2024 Increase"]
departments = df2.index.tolist()
palette2    = ["#1f77b4", "#ff7f0e"]

fig2 = go.Figure()
for i, dept in enumerate(departments):
    vals = df2.loc[dept, metrics2].values
    fig2.add_bar(
        x=metrics2,
        y=vals,
        name=dept,
        marker_color=palette2,
        text=[f"{v:.1f}%" for v in vals],
        textposition="outside",
        visible=(i == 0),
    )

buttons2 = []
for i, dept in enumerate(departments):
    vis = [j == i for j in range(len(departments))]
    buttons2.append(dict(
        label=dept,
        method="update",
        args=[
            {"visible": vis},
            {"title": f"{dept}: Enrollment % Changes"}
        ],
    ))

# choose y-range to include negatives if any
ymin = df2.min().min() * 1.2
ymax = df2.max().max() * 1.2

fig2.update_layout(
    updatemenus=[dict(
        buttons=buttons2,
        direction="v",
        x=0.0,
        y=0.8,
        xanchor="left",
        yanchor="top",
        pad={"l": 10, "t": 10},
        showactive=True,
    )],
    title=f"{departments[0]}: Enrollment % Changes",
    title_x=0.5,
    template="plotly_white",
    yaxis=dict(range=[ymin, ymax], title="Percent"),
    margin=dict(l=150, r=20, t=50, b=50),
)

# === STREAMLIT LAYOUT ===
tab1, tab2 = st.tabs(["Overall Metrics", "Dept. Enrollment % Changes"])

with tab1:
    st.subheader("Overall % Metrics")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("Department Enrollment % Changes")
    st.plotly_chart(fig2, use_container_width=True)


with tab2:
    st.subheader("Department Enrollment % Changes")
    st.plotly_chart(fig2, use_container_width=True)
