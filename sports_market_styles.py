BACKGROUND_COLOR = "#fafafa"

def apply_plotly_style(fig):
    fig.update_layout(
        title={
            "text": "North American Sports Teams by City<br>"
            "<sup>City coordinates &copy; OpenStreetMap contributors</sup>",
            "x": 0.5,
        },
        font=dict(family="serif"),
        paper_bgcolor=BACKGROUND_COLOR,
        plot_bgcolor=BACKGROUND_COLOR,
    )
    return fig
                
