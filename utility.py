from CoolProp.CoolProp import PropsSI
from pandas import DataFrame


class Utility:
    @staticmethod
    def get_single_prop(
        p: str, p1: str, v1: float, p2: str, v2: float, fluid: str
    ) -> float:
        return PropsSI(p, p1, v1, p2, v2, fluid)

    @staticmethod
    def get_ts_data(fluid: str) -> DataFrame:
        # will be implemented
        return DataFrame({"T": [], "s": []})

    @staticmethod
    def normalize_fluids(fluid: dict[str, float]) -> dict[str, float]:
        normalized_fluid = {}
        total_mass = 0.0
        for d in fluid.keys():
            total_mass += fluid[d]
        for d in fluid.keys():
            normalized_fluid[d] = fluid[d] / total_mass
        return normalized_fluid

    @staticmethod
    def get_all_props(
        p1: str, v1: float, p2: str, v2: float, fluid: dict[str, float]
    ) -> dict[str, float]:
        fld = ""
        for d in fluid.keys():
            fld += f"{d}[{fluid[d]}]&"
        fld = fld[:-1]
        return {
            "T": PropsSI("T", p1, v1, p2, v2, fld),
            "P": PropsSI("P", p1, v1, p2, v2, fld),
            "D": PropsSI("D", p1, v1, p2, v2, fld),
            "h": PropsSI("H", p1, v1, p2, v2, fld),
            "s": PropsSI("S", p1, v1, p2, v2, fld),
            "q": PropsSI("Q", p1, v1, p2, v2, fld),
        }
