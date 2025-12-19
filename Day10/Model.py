import re

class Joltage_Requirements:
    def __init__(self, input) -> None:
        self.Joltage = [int(i) for i in re.findall("{(.*?)}", input)[0].split(",")]

class Wiring_Schematics:
    def __init__(self, input) -> None:
        self.Wiring = [[int(j) for j in i.split(",")] for i in re.findall(r" \((.*?)\)", input)]

class Light_Diagram:
    def __init__(self, input) -> None:
        self.Diagram = re.findall(r"\[(.*?)\]", input)[0]

class Machine:
    def __init__(self, input: str) -> None:
        self.__LightDiagram   = Light_Diagram(input)
        self.__Wiring         = Wiring_Schematics(input)
        self.__Joltage        = Joltage_Requirements(input)

        #: Getters
        self.Wiring = self.__Wiring.Wiring
        self.Joltage= self.__Joltage.Joltage
        self.Lights = self.__LightDiagram.Diagram
        self.ButtonsCount = len(self.__Joltage.Joltage)