import plotly.graph_objects as go


AMBER = "#D9A441"
AMBER_LIGHT = "#E7BF67"
SLATE = "#778292"
GRID = "#29303A"
TEXT = "#C9D0DA"
MUTED = "#99A3B1"


# ---------------------------------------------------------
# Shared chart styling
# ---------------------------------------------------------

def apply_chart_layout(
    figure: go.Figure,
    *,
    height: int = 410,
) -> go.Figure:

    figure.update_layout(
        height=height,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color=TEXT,
            size=12,
        ),
        hoverlabel=dict(
            bgcolor="#171C24",
            bordercolor="#343B47",
            font=dict(
                color="#F0F2F5",
            ),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
    )

    figure.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor=GRID,
        tickfont=dict(
            color=MUTED,
        ),
    )

    figure.update_yaxes(
        gridcolor=GRID,
        zeroline=False,
        tickfont=dict(
            color=MUTED,
        ),
    )

    return figure


# ---------------------------------------------------------
# Field Overview
# ---------------------------------------------------------

def make_field_production_figure(
    history,
):
    field_monthly = (
        history.groupby(
            "DATE",
            as_index=False,
        )
        .agg(
            oil_volume=(
                "oil_volume",
                "sum",
            ),
            represented_wells=(
                "NPD_WELL_BORE_NAME",
                "nunique",
            ),
        )
    )

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=field_monthly["DATE"],
            y=field_monthly["oil_volume"],
            customdata=field_monthly[
                ["represented_wells"]
            ],
            mode="lines",
            name="Core producer oil",
            line=dict(
                color=AMBER,
                width=2.4,
            ),
            fill="tozeroy",
            fillcolor="rgba(217, 164, 65, 0.08)",
            hovertemplate=(
                "<b>%{x|%b %Y}</b><br>"
                "Oil volume: %{y:,.0f}<br>"
                "Represented wells: %{customdata[0]}"
                "<extra></extra>"
            ),
        )
    )

    figure.update_yaxes(
        title="Monthly oil volume"
    )

    return apply_chart_layout(
        figure,
        height=430,
    )


def make_latest_vs_recent_figure(
    monitoring,
):
    plot_data = monitoring.copy()

    if "display_well_name" in plot_data.columns:
        plot_data["well_label"] = (
            plot_data["display_well_name"]
            .fillna(
                plot_data[
                    "NPD_WELL_BORE_NAME"
                ]
            )
        )
    else:
        plot_data["well_label"] = (
            plot_data[
                "NPD_WELL_BORE_NAME"
            ]
        )

    figure = go.Figure()

    figure.add_trace(
        go.Bar(
            x=plot_data["well_label"],
            y=plot_data["oil_volume"],
            name="Latest oil",
            marker_color=AMBER,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Latest oil: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    figure.add_trace(
        go.Bar(
            x=plot_data["well_label"],
            y=plot_data[
                "recent_3_observation_mean_oil"
            ],
            name="Recent 3-observation mean",
            marker_color=SLATE,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Recent mean: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    figure.update_layout(
        barmode="group",
    )

    figure.update_yaxes(
        title="Oil volume"
    )

    return apply_chart_layout(
        figure,
        height=390,
    )


# ---------------------------------------------------------
# Well Monitor
# ---------------------------------------------------------

def make_well_oil_history_figure(
    well_history,
):
    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=well_history["DATE"],
            y=well_history["oil_volume"],
            mode="lines+markers",
            name="Monthly oil",
            line=dict(
                color=AMBER,
                width=2.4,
            ),
            marker=dict(
                size=5,
            ),
            hovertemplate=(
                "<b>%{x|%b %Y}</b><br>"
                "Oil volume: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    figure.add_trace(
        go.Scatter(
            x=well_history["DATE"],
            y=well_history[
                "oil_volume_recent_mean_3"
            ],
            mode="lines",
            name="Recent 3-observation mean",
            line=dict(
                color=SLATE,
                width=2,
                dash="dash",
            ),
            hovertemplate=(
                "<b>%{x|%b %Y}</b><br>"
                "Recent mean: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    figure.update_yaxes(
        title="Oil volume"
    )

    return apply_chart_layout(
        figure,
        height=440,
    )


def make_well_intensity_figure(
    well_history,
):
    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=well_history["DATE"],
            y=well_history[
                "oil_per_on_stream_hour"
            ],
            mode="lines+markers",
            name="Oil intensity",
            line=dict(
                color=AMBER_LIGHT,
                width=2.2,
            ),
            marker=dict(
                size=5,
            ),
            connectgaps=False,
            hovertemplate=(
                "<b>%{x|%b %Y}</b><br>"
                "Oil per on-stream hour: "
                "%{y:,.2f}"
                "<extra></extra>"
            ),
        )
    )

    figure.update_yaxes(
        title="Oil per on-stream hour"
    )

    return apply_chart_layout(
        figure,
        height=360,
    )


def make_well_water_cut_figure(
    well_history,
):
    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=well_history["DATE"],
            y=well_history[
                "water_cut_pct"
            ],
            mode="lines+markers",
            name="Water cut",
            line=dict(
                color=AMBER,
                width=2.2,
            ),
            marker=dict(
                size=5,
            ),
            connectgaps=False,
            hovertemplate=(
                "<b>%{x|%b %Y}</b><br>"
                "Water cut: %{y:.1f}%"
                "<extra></extra>"
            ),
        )
    )

    figure.update_yaxes(
        title="Water cut (%)",
        range=[0, 100],
    )

    return apply_chart_layout(
        figure,
        height=360,
    )


def make_well_onstream_figure(
    well_history,
):
    figure = go.Figure()

    zero_months = well_history.loc[
        well_history[
            "on_stream_hours"
        ].eq(0)
    ].copy()

    figure.add_trace(
        go.Bar(
            x=well_history["DATE"],
            y=well_history[
                "on_stream_hours"
            ],
            name="On-stream hours",
            marker_color=SLATE,
            hovertemplate=(
                "<b>%{x|%b %Y}</b><br>"
                "On-stream hours: %{y:,.1f}"
                "<extra></extra>"
            ),
        )
    )

    if not zero_months.empty:
        figure.add_trace(
            go.Scatter(
                x=zero_months["DATE"],
                y=zero_months[
                    "on_stream_hours"
                ],
                mode="markers",
                name="Recorded zero on-stream",
                marker=dict(
                    color=AMBER,
                    size=11,
                    symbol="x",
                ),
                cliponaxis=False,
                hovertemplate=(
                    "<b>%{x|%b %Y}</b><br>"
                    "On-stream hours: 0.0<br>"
                    "Recorded zero-hour month"
                    "<extra></extra>"
                ),
            )
        )

    figure.update_yaxes(
        title="On-stream hours",
        rangemode="tozero",
    )

    return apply_chart_layout(
        figure,
        height=350,
    )


# ---------------------------------------------------------
# Forecast Analysis
# ---------------------------------------------------------

def make_forecast_event_figure(
    well_history,
    forecast_row,
):
    origin_date = forecast_row["DATE"]
    target_date = forecast_row["target_month"]

    current_oil = forecast_row[
        "oil_volume"
    ]

    actual_target = forecast_row[
        "target_next_month_oil_volume"
    ]

    persistence_prediction = forecast_row[
        "persistence_prediction"
    ]

    ridge_prediction = forecast_row[
        "ridge_prediction"
    ]

    figure = go.Figure()

    figure.add_trace(
        go.Scatter(
            x=well_history["DATE"],
            y=well_history["oil_volume"],
            mode="lines",
            name="Historical oil",
            line=dict(
                color=SLATE,
                width=2,
            ),
            hovertemplate=(
                "<b>%{x|%b %Y}</b><br>"
                "Oil volume: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    figure.add_trace(
        go.Scatter(
            x=[origin_date],
            y=[current_oil],
            mode="markers",
            name="Forecast origin",
            marker=dict(
                color=AMBER,
                size=13,
                symbol="circle",
                line=dict(
                    color="#F4D38A",
                    width=2,
                ),
            ),
            hovertemplate=(
                "<b>Forecast origin</b><br>"
                "%{x|%b %Y}<br>"
                "Current oil: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    figure.add_trace(
        go.Scatter(
            x=[target_date],
            y=[actual_target],
            mode="markers",
            name="Observed target",
            marker=dict(
                color="#E8EAED",
                size=14,
                symbol="diamond",
            ),
            hovertemplate=(
                "<b>Observed target</b><br>"
                "%{x|%b %Y}<br>"
                "Oil volume: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    figure.add_trace(
        go.Scatter(
            x=[target_date],
            y=[persistence_prediction],
            mode="markers",
            name="Persistence",
            marker=dict(
                color=SLATE,
                size=13,
                symbol="square",
            ),
            hovertemplate=(
                "<b>Persistence forecast</b><br>"
                "%{x|%b %Y}<br>"
                "Forecast: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    figure.add_trace(
        go.Scatter(
            x=[target_date],
            y=[ridge_prediction],
            mode="markers",
            name="Ridge",
            marker=dict(
                color=AMBER_LIGHT,
                size=13,
                symbol="triangle-up",
            ),
            hovertemplate=(
                "<b>Ridge forecast</b><br>"
                "%{x|%b %Y}<br>"
                "Forecast: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    figure.add_vline(
        x=origin_date.to_pydatetime(),
        line_width=1,
        line_dash="dot",
        line_color=AMBER,
    )

    figure.update_yaxes(
        title="Oil volume"
    )

    return apply_chart_layout(
        figure,
        height=470,
    )


def make_forecast_error_figure(
    forecast_row,
):
    persistence_error = forecast_row[
        "persistence_absolute_error"
    ]

    ridge_error = forecast_row[
        "ridge_absolute_error"
    ]

    figure = go.Figure()

    figure.add_trace(
        go.Bar(
            x=[
                "Persistence",
                "Ridge",
            ],
            y=[
                persistence_error,
                ridge_error,
            ],
            marker_color=[
                SLATE,
                AMBER,
            ],
            text=[
                f"{persistence_error:,.0f}",
                f"{ridge_error:,.0f}",
            ],
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Absolute error: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    figure.update_layout(
        showlegend=False,
    )

    figure.update_yaxes(
        title="Absolute forecast error"
    )

    return apply_chart_layout(
        figure,
        height=330,
    )


# ---------------------------------------------------------
# Model Reliability
# ---------------------------------------------------------

def make_well_wape_comparison_figure(
    monitoring,
):
    plot_data = monitoring.copy()

    plot_data = plot_data.sort_values(
        "persistence_WAPE_pct"
    )

    figure = go.Figure()

    figure.add_trace(
        go.Bar(
            y=plot_data[
                "display_well_name"
            ],
            x=plot_data[
                "persistence_WAPE_pct"
            ],
            name="Persistence",
            orientation="h",
            marker_color=SLATE,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Persistence WAPE: %{x:.1f}%"
                "<extra></extra>"
            ),
        )
    )

    figure.add_trace(
        go.Bar(
            y=plot_data[
                "display_well_name"
            ],
            x=plot_data[
                "ridge_WAPE_pct"
            ],
            name="Ridge",
            orientation="h",
            marker_color=AMBER,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Ridge WAPE: %{x:.1f}%"
                "<extra></extra>"
            ),
        )
    )

    figure.update_layout(
        barmode="group",
    )

    figure.update_xaxes(
        title="WAPE (%)"
    )

    return apply_chart_layout(
        figure,
        height=410,
    )


def make_negative_forecast_incidence_figure(
    monitoring,
):
    plot_data = monitoring.copy()

    figure = go.Figure()

    figure.add_trace(
        go.Bar(
            x=plot_data[
                "display_well_name"
            ],
            y=plot_data[
                "negative_ridge_forecast_pct"
            ],
            marker_color=AMBER,
            text=plot_data[
                "negative_ridge_forecasts"
            ].astype(int),
            texttemplate="%{text}",
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Negative forecasts: %{text}<br>"
                "Incidence: %{y:.1f}%"
                "<extra></extra>"
            ),
        )
    )

    figure.update_layout(
        showlegend=False,
    )

    figure.update_yaxes(
        title="Negative Ridge forecasts (%)",
        rangemode="tozero",
    )

    return apply_chart_layout(
        figure,
        height=370,
    )