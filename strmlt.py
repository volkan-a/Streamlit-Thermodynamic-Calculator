import streamlit as st
from utility import Utility
from pandas import DataFrame
import numpy as np
from ProcessStream import PropertyPair


def plot_ts(fluid: str) -> DataFrame:
    Tmin = Utility.get_single_prop("Tmin", "T", 100, "P", 100, fluid)
    Tmax = Utility.get_single_prop("Tcrit", "T", 100, "P", 100, fluid)
    T1 = np.linspace(Tmin, Tmax, 101)
    T2 = np.linspace(Tmax, Tmin, 101)
    s1 = [Utility.get_single_prop("S", "T", T, "Q", 0.0, fluid) for T in T1]
    s2 = [Utility.get_single_prop("S", "T", T, "Q", 1.0, fluid) for T in T2]
    data = DataFrame({"T": np.concatenate((T1, T2)), "s": np.concatenate((s1, s2))})
    return data


def get_formatted_results(stream_results) -> DataFrame:
    return DataFrame(
        {
            "Property": [
                "Temperature",
                "Pressure",
                "Density",
                "Specific enthalpy",
                "Specific entropy",
                "Vapour fraction",
            ],
            "Value": stream_results.values(),
            "Units": ["K", "Pa", "kg/m3", "J/kg", "J/kg.K", "-"],
        }
    )


property_pairs = {
    "Temperature & pressure": {
        "pair": PropertyPair.TP,
        "cp name": ["T", "P"],
        "name": ["Temperature", "Pressure"],
    },
    "Temperature & vapour fraction": {
        "pair": PropertyPair.TQ,
        "cp name": ["T", "Q"],
        "name": ["Temperature", "Vapour fraction"],
    },
    "Pressure & specific enthalpy": {
        "pair": PropertyPair.PH,
        "cp name": ["P", "H"],
        "name": ["Pressure", "Specific enthalpy"],
    },
    "Pressure & specific entropy": {
        "pair": PropertyPair.PS,
        "cp name": ["P", "S"],
        "name": ["Pressure", "Specific entropy"],
    },
    "Pressure & vapour fraction": {
        "pair": PropertyPair.PQ,
        "cp name": ["P", "Q"],
        "name": ["Pressure", "Vapour fraction"],
    },
}

stream_results = None

st.title("**Thermodynamic Property Calculator**")

with st.expander("Calculator"):
    col1, col2 = st.columns(2)
    with col1:
        fluid_name = st.selectbox(
            "Select your fluid",
            ("Water", "R134a", "R507A", "Methane", "Butane", "n-Propane"),
        )
        fluid = {fluid_name: 1.0}
        property_pair = st.selectbox("Select property pair", property_pairs)
        val1 = st.number_input(
            f"{property_pairs[property_pair]['name'][0]} value in SI units"
        )
        val2 = st.number_input(
            f"{property_pairs[property_pair]['name'][1]} value in SI units"
        )
        if st.button("Calculate"):
            try:
                stream_results = Utility.get_all_props(
                    property_pairs[property_pair]["cp name"][0],
                    val1,
                    property_pairs[property_pair]["cp name"][1],
                    val2,
                    fluid,
                )
            except ValueError:
                with col2:
                    st.error("Error on calculation, check your inputs.")
    with col2:
        with st.container():
            if stream_results is not None:
                st.table(get_formatted_results(stream_results))
with st.expander("About"):
    st.markdown(
        """
        # Hello world
        Please use freely

        vakkaya@gmail.com
    """
    )

    # st.table(
    #     pd.DataFrame(
    #         {
    #             "Property": [
    #                 "Temperature",
    #                 "Pressure",
    #                 "Density",
    #                 "Specific enthalpy",
    #                 "Specific entropy",
    #                 "Vapour fraction",
    #             ],
    #             "Value": props.values(),
    #             "Units": ["K", "Pa", "kg/m3", "J/kg", "J/kg.K", "-"],
    #         }
    #     )
    # )


# with col3:
#     graph = graphviz.Digraph()
#     graph.
#     graph.node("well", "Well", {"shape": "box"})
#     graph.node("valve1", "Valve 1", {"shape": "triangle"})
#     graph.edge("Well", "valve1")
#     graph.edge("valve1", "seperator1")
#     graph.edge("seperator1", "turbine1")
#     graph.edge("seperator1", "valve2")
#     graph.edge("valve2", "seperator2")
#     graph.edge("turbine1", "mixer")
#     graph.edge("seperator2", "mixer")

#     st.graphviz_chart(graph)
