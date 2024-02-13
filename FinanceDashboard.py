# Financial Dashbaord
# Grant Cates

import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


# Load data
filepath = "https://docs.google.com/spreadsheets/d/19lnPnb9urWtuC_X-0_n9Oi9KwhO9USZ-ljJKVsSvcrs/export?format=csv"
df = pd.read_csv(filepath)

# Convert "Date" to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Data Manipulation
df2 = df
columns_to_delete = [
    "Dow Jones (^DJI)",
    "Nasdaq (^IXIC)",
    "S&P500 (^GSPC)",
    "NYSE Composite (^NYA)",
    "Russell 2000 (^RUT)",
    "DAX Index (^GDAXI)",
    "FTSE 100 (^FTSE)",
    "Hang Seng Index (^HSI)",
    "Treasury Yield 5 Years (^FVX)",
    "Treasury Bill 13 Week (^IRX)",
    "Treasury Yield 10 Years (^TNX)",
    "Treasury Yield 30 Years (^TYX)",
]
f_df2 = df2.drop(columns=columns_to_delete)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div(
    [
        html.H1("Stock Market Dashboard"),
        html.H2("By: Grant Cates", style={"fontSize": 20}),
        dcc.Dropdown(
            id="stock_dropdown",
            options=[{"label": stock, "value": stock} for stock in df.columns[1:]],
            value="Dow Jones (^DJI)",
            style={"width": "50%"},
        ),
        dcc.RangeSlider(
            id="date_slider",
            min=df["Date"].min().year,
            max=df["Date"].max().year,
            step=1,
            marks={
                str(year): str(year)
                for year in range(df["Date"].min().year, df["Date"].max().year + 1, 5)
            },
            value=[df["Date"].min().year, df["Date"].max().year],
        ),
        dcc.RadioItems(
            id="chart_type_radio",
            options=[
                {"label": "Line Chart", "value": "line"},
                {"label": "Scatter Plot", "value": "scatter"},
            ],
            value="line",
            labelStyle={"display": "block"},
        ),
        dcc.Checklist(
            id="log_scale_checklist",
            options=[{"label": "Logarithmic Scale", "value": "log_scale"}],
            value=[],
        ),
        dcc.Graph(id="stock_chart", figure={}),
        html.Div(id="surprise_message"),
        dcc.Graph(id="chart1"),
        dcc.Graph(id="chart2"),
        dcc.Graph(id="chart3"),
    ]
)


# Callbacks to update charts based on user input
@app.callback(
    [
        Output("stock_chart", "figure"),
        Output("surprise_message", "children"),
        Output("chart1", "figure"),
        Output("chart2", "figure"),
        Output("chart3", "figure"),
    ],
    [
        Input("stock_dropdown", "value"),
        Input("date_slider", "value"),
        Input("log_scale_checklist", "value"),
        Input("chart_type_radio", "value"),
    ],
)
def update_charts(
    selected_stock,
    selected_dates,
    log_scale,
    selected_chart_type,
):
    filtered_df = df[
        (df["Date"].dt.year >= selected_dates[0])
        & (df["Date"].dt.year <= selected_dates[1])
    ]

    # Create main chart
    if selected_chart_type == "line":
        chart = px.line(
            filtered_df,
            x="Date",
            y=selected_stock,
            title=f"{selected_stock} over Time",
            log_y=log_scale,
        )
    elif selected_chart_type == "scatter":
        chart = px.scatter(
            filtered_df,
            x="Date",
            y=selected_stock,
            title=f"{selected_stock} over Time",
            log_y=log_scale,
        )
    elif selected_chart_type == "bar":
        chart = px.bar(
            filtered_df,
            x="Date",
            y=selected_stock,
            title=f"{selected_stock} over Time",
            log_y=log_scale,
        )
    else:
        chart = px.line(
            filtered_df,
            x="Date",
            y=selected_stock,
            title=f"{selected_stock} over Time",
            log_y=log_scale,
        )

    chart1 = px.line(
        df,
        x="Date",
        y=f"Treasury Bill 13 Week (^IRX)",
        title="Treasury Bill 13 Week (^IRX)",
        log_y=log_scale,
    )

    chart2 = px.line(
        df,
        x="Date",
        y=f"Treasury Yield 5 Years (^FVX)",
        title="Treasury Yield 5 Years (^FVX)",
        log_y=log_scale,
    )

    chart3 = px.line(
        df,
        x="Date",
        y=["Treasury Yield 10 Years (^TNX)", "Treasury Yield 30 Years (^TYX)"],
        title="Combined Treasury Yield (10 Years and 30 Years)",
    )

    # Easter Egg
    surprise_message = None
    if selected_stock == "S&P500 (^GSPC)":
        surprise_message = html.Div(
            dbc.Alert(
                "Surprise! You chose the stock that you should buy like RIGHT NOW!",
                color="success",
                is_open=True,
                style={"background-color": "green", "color": "white"},
            )
        )

    return chart, surprise_message, chart1, chart2, chart3


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
