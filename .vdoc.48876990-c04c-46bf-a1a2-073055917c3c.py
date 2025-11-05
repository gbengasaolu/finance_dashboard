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

# --- Load Data ---
df = pd.read_csv("Finance_data.csv")

# Clean basic fields
df.columns = df.columns.str.strip().str.replace(" ", "_")
df['Purpose'] = df['Purpose'].astype(str).str.title()
df['Investment_Avenues'] = df['Investment_Avenues'].astype(str)
df['Stock_Marktet'] = df['Stock_Marktet'].astype(str)
df['Expect'] = df['Expect'].astype(str)

{.sidebar}
{width="80%"}

🔍 Filters
Writing
Copy
ui.input_select(
"investment_filter",
"Investment Avenues (Yes/No):",
choices=sorted(df["Investment_Avenues"].dropna().unique().tolist()),
selected="Yes"
)
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
#
#
#
#
#
#
#
#
#
