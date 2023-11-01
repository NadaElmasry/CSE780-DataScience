from shiny import ui, App
from shinywidgets import output_widget, render_widget
import plotly.express as px
import plotly.graph_objs as go
import options as op
import pandas as pd
employment_df = pd.read_csv("Employment_by_prov_occ.csv")
app_ui = ui.page_fluid(
    ui.div(
        ui.input_select("geo", label="Province",choices= op.GEO),
        ui.input_select("occ", label="Occupation",choices= op.NOC),
        class_="d-flex gap-3"
        ),
        output_widget("my_widget")
        )
def server(input, output, session):
    @output
    @render_widget
    def my_widget():
        if input.geo() == 'ALL':
            occ_prov = employment_df[employment_df["National Occupational Classification (NOC)"]==input.occ()]
            fig = px.line(occ_prov, x="REF_DATE", y="VALUE", color="GEO")
            fig.update_layout(xaxis_title = "Reference Date", yaxis_title = "Number of Employed Persons", 
            title = f"Employment for {input.occ()} for all provinces",title_x=0.5)
            fig.update_traces(textposition="bottom right")
        else:
            occ_prov = employment_df[(employment_df["GEO"]==input.geo()) &
            (employment_df["National Occupational Classification (NOC)"]==input.occ())]
            fig = px.line(occ_prov, x="REF_DATE", y="VALUE", color="GEO")
            fig.update_layout(xaxis_title = "Reference Date", yaxis_title = "Number of Employed Persons", 
            title = f"Employment for {input.occ()} in {input.geo()}"
            ,title_x=0.5)
            fig.update_traces(textposition="bottom right")
        return fig
app = App(app_ui, server)