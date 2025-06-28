st.set_page_config(page_title="University Dashboard", layout="wide")
st.title("University Growth & Dept. Enrollment Dashboard")

# -- Load data --
df = pd.read_csv("university_student_dashboard_data.csv")

# === FIGURE 1: Overall Metrics ===

# 1a) Aggregate by Year
df_summary = df.groupby("Year")[["Applications", "Admitted", "Enrolled"]].sum()

# 1b) Year-over-year %
yoy = df_summary.pct_change() * 100

# 1c) Compute the three stats
total_inc = ((df_summary.iloc[-1] - df_summary.iloc[0]) / df_summary.iloc[0] * 100).rename("Total Increase")
avg_annual = yoy.mean().rename("Average YoY")
n_years = df_summary.index.max() - df_summary.index.min()
cagr = (((df_summary.iloc[-1] / df_summary.iloc[0]) ** (1 / n_years)) - 1) * 100
cagr = cagr.rename("CAGR")

# 1d) Build a tidy table
summary1 = pd.concat([total_inc, avg_annual, cagr], axis=1).round(1).T
df1 = (
    summary1
    .reset_index()
    .melt(id_vars="index", var_name="Category", value_name="Percent")
    .rename(columns={"index": "Metric"})
)

# 1e) Plotly figure
palette1 = ["#1f77b4", "#2ca02c", "#d62728"]
fig1 = go.Figure()
for i, metric in enumerate(df1["Metric"].unique()):
    sub = df1[df1["Metric"] == metric]
    ymax = df1.query("Metric == @metric")["Percent"].max() * 1.1
    fig1.add_bar(
        x=sub["Category"],
        y=sub["Percent"],
        marker_color=palette1,
        text=sub["Percent"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside",
        name=metric,
        visible=(i == 0),
    )

buttons1 = []
for i, metric in enumerate(df1["Metric"].unique()):
    ymax = df1.query("Metric == @metric")["Percent"].max() * 1.1
    vis = [i == j for j in range(len(df1["Metric"].unique()))]
    buttons1.append(dict(
        label=metric,
        method="update",
        args=[
            {"visible": vis},
            {"title": metric, "yaxis": {"range": [0, ymax]}}
        ],
    ))

fig1.update_layout(
    updatemenus=[dict(buttons=buttons1, x=0.02, y=1.15, showactive=True)],
    title="Total Increase",       # initial title
    title_x=0.5,                   # center title
    template="plotly_white",
    bargap=0.3,
    height=450,
    yaxis=dict(title="Percent"),
    margin=dict(l=50, r=50, t=100, b=50),
)

# === FIGURE 2: Dept. Enrollment % Changes ===

# 2a) Melt only the Enrolled columns by department
dept_cols = [
    "Engineering Enrolled",
    "Business Enrolled",
    "Arts Enrolled",
    "Science Enrolled",
]
df_dept = df.melt(
    id_vars="Year",
    value_vars=dept_cols,
    var_name="Department",
    value_name="Enrollment_Count"
)

# 2b) Aggregate & YOY %
df_dept_agg = (
    df_dept
    .groupby(["Department", "Year"])["Enrollment_Count"]
    .sum()
    .reset_index()
)
yoy2 = df_dept_agg.set_index(["Department", "Year"])["Enrollment_Count"] \
    .groupby(level=0).pct_change() * 100

# 2c) Build summary
avg2    = yoy2.groupby(level=0).mean().rename("Average YoY")
inc2024 = yoy2.xs(2024, level="Year").rename("2024 Increase")
summary2 = pd.concat([avg2, inc2024], axis=1).round(1)
metrics2    = summary2.columns.tolist()      # ["Average YoY","2024 Increase"]
departments = summary2.index.tolist()
palette2    = ["#1f77b4", "#ff7f0e"]

# 2d) Plotly figure
fig2 = go.Figure()
for i, dept in enumerate(departments):
    vals = summary2.loc[dept, metrics2].values
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
    yaxis=dict(range=[0, summary2.values.max() * 1.2], title="Percent"),
    margin=dict(l=150, r=20, t=50, b=50),
)

# === LAYOUT IN STREAMLIT ===

tab1, tab2 = st.tabs(["Overall Metrics", "Dept. Enroll % Changes"])

with tab1:
    st.subheader("Overall % Metrics")
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    st.subheader("Department Enrollment % Changes")
    st.plotly_chart(fig2, use_container_width=True)
