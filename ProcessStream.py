from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from enum import Enum
from utility import Utility


class PropertyPair(Enum):
    TP = 1
    TQ = 2
    PH = 3
    PS = 4
    PQ = 5


class StreamInput(BaseModel):
    name: str = Field(default="new stream")
    id: UUID = Field(default_factory=uuid4)
    m: float = Field(default=1.0)
    fluid: dict[str, float] = Field(default={"Water": 1.0})
    property_pair: PropertyPair = Field(default=PropertyPair.TP)
    value1: float = Field(default=298.15)
    value2: float = Field(default=101325.0)


class StreamResult(BaseModel):
    name: str
    id: UUID
    fluid: dict[str, float]
    m: float
    T: float
    P: float
    D: float
    h: float
    s: float
    q: float


class ProcessStream:
    def __init__(self, input: StreamInput):
        self.input = input
        self.isCalculated = False
        self.__calculate__()

    def get_results(self) -> None | StreamResult:
        if self.isCalculated is False:
            return None
        return self.results

    def __calculate__(self):
        match self.input.property_pair:
            case PropertyPair.TP:
                prop1 = "T"
                prop2 = "P"
            case PropertyPair.TQ:
                prop1 = "T"
                prop2 = "Q"
            case PropertyPair.PH:
                prop1 = "P"
                prop2 = "H"
            case PropertyPair.PS:
                prop1 = "P"
                prop2 = "S"
            case PropertyPair.PQ:
                prop1 = "P"
                prop2 = "Q"
            case _:
                prop1 = "T"
                prop2 = "P"
        res = Utility.get_all_props(
            prop1, self.input.value1, prop2, self.input.value2, self.input.fluid
        )
        self.result = StreamResult(
            name=self.input.name,
            id=self.input.id,
            fluid=self.input.fluid,
            m=self.input.m,
            T=res["T"],
            P=res["P"],
            D=res["D"],
            h=res["h"],
            s=res["s"],
            q=res["q"],
        )
        self.isCalculated = True
