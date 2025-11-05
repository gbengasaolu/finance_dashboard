# type: ignore
# flake8: noqa
#
#
#
#
#
#
#
#
#
#
#
#| context: setup
import pandas as pd
from shiny import reactive, render, ui
import plotly.express as px
#
#
#
# --- Load Data ---
df = pd.read_csv("data\Finance_data.csv")
#
#
#
# Clean basic fields
df.columns = df.columns.str.strip().str.replace(" ", "_")
df['Purpose'] = df['Purpose'].astype(str).str.title()
df['Investment_Avenues'] = df['Investment_Avenues'].astype(str)
df['Stock_Marktet'] = df['Stock_Marktet'].astype(str)
df['Expect'] = df['Expect'].astype(str)
#
#
#
{.sidebar}
{width="80%"}

🔍 Filters
ui.input_select(
"investment_filter",
"Investment Avenues (Yes/No):",
choices=sorted(df["Investment_Avenues"].dropna().unique().tolist()),
selected="Yes"
)
#
#
#
ui.input_slider(
"age_filter",
"Select Age Range:",
min=int(df["age"].min()),
max=int(df["age"].max()),
value=(20, 40),
step=1
)

ui.input_select(
"purpose_filter",
"Select Purpose:",
choices=sorted(df["Purpose"].dropna().unique().tolist()),
selected="Wealth Creation"
)
#
#
#
@reactive.calc
def filtered_data():
dff = df.copy()
dff = dff[dff["Investment_Avenues"] == input.investment_filter()]
dff = dff[(dff["age"] >= input.age_filter()[0]) & (dff["age"] <= input.age_filter()[1])]
dff = dff[dff["Purpose"] == input.purpose_filter()]
return dff
#
#
#
#
📊 Dashboard Overview
@render.ui
def value_cards():
dff = filtered_data()
total_resp = len(dff)
top_option = dff[['Mutual_Funds','Equity_Market','Debentures','Government_Bonds',
'Fixed_Deposits','PPF','Gold']].mean().idxmin().replace('_',' ')
actual_avenue = dff['Avenue'].mode()[0] if not dff['Avenue'].mode().empty else "N/A"
stock_perc = round((dff['Stock_Marktet'].str.lower().eq('yes').mean())*100,1)
top_expect = dff['Expect'].mode()[0] if not dff['Expect'].mode().empty else "N/A"

return ui.layout_columns(
    ui.value_box("👥 Respondents", f"{total_resp}"),
    ui.value_box("💰 Preferred Investment", top_option.title()),
    ui.value_box("🏦 Common Avenue", actual_avenue.title()),
    ui.value_box("📈 Stock Market Investors", f"{stock_perc}%"),
    ui.value_box("🎯 Expected Returns", top_expect)
)
#
#
#
#
📈 Interactive Visuals
@render.plotly
def gender_chart():
dff = filtered_data()
fig = px.histogram(
dff, x="gender", color="Stock_Marktet", barmode="group",
title="Gender vs Stock Market Participation",
color_discrete_sequence=["#0F766E", "#38BDF8"]
)
fig.update_layout(title_font=dict(size=16))
return fig
#
#
#
#

@render.plotly
def factor_chart():
dff = filtered_data()
fig = px.bar(
dff.groupby("Factor")["age"].count().reset_index(),
x="Factor", y="age",
title="Key Factors Influencing Investment",
color="Factor", color_discrete_sequence=px.colors.qualitative.Bold
)
fig.update_traces(marker_line_color="#0F172A", marker_line_width=1)
fig.update_layout(title_font=dict(size=16))
return fig
#
#
#
#
@render.plotly
def objective_chart():
dff = filtered_data()
fig = px.pie(
dff, names="Objective",
title="Distribution of Investment Objectives",
color_discrete_sequence=px.colors.sequential.Teal
)
fig.update_traces(textinfo="percent+label")
return fig
#
#
#
#
📄 Data Explorer
@render.data_frame
def datatable():
return render.DataGrid(filtered_data(), height="100%")
#
#
#
