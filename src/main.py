import csv
import io
import json
import uuid
from datetime import datetime
from pathlib import Path
import importlib.metadata
from epdx.pydantic import EPD, Standard, SubType, Unit, Source

class EPDx(EPD):

    @classmethod
    def from_dict(cls, KBOBeco_object: dict):
        """Convert a row from the KBOB eco data csv to an EPDx object"""

        declared_factor = 1
        declared_unit = KBOBeco_object.get("Bezug")
        french_name = KBOBeco_object.get("MATERIAUX")
        biogen_c = KBOBeco_object.get("Biogener Kohlenstoff")

        epd = cls(
            id=KBOBeco_object.get("UUID-Nummer") or str(uuid.uuid4()),
            format_version=importlib.metadata.version("epdx"),
            name=KBOBeco_object.get("BAUMATERIALIEN"),
                        version="version 4 - 2024",
            declared_unit=cls.convert_unit(declared_unit),
            valid_until=datetime(year=2025, month=12, day=22),
            published_date=datetime(year=2024, month=11, day=25),
            source=Source(name="KBOB", url="https://www.kbob.admin.ch/kbob/de/home/themen-leistungen/nachhaltiges-bauen/oekobilanzdaten_baubereich.html"),
            standard=Standard.EN15804A2,
            subtype="Generic",
            comment=str(french_name),
            reference_service_life=60,
            location="CH",
            penre={
                "a1a3": cls.convert_penre(
                    KBOBeco_object.get("Primärenergie nicht erneuerbar (kWh oil-eq)"),
                    declared_factor
                ),
                "a4": None,
                "a5": None,
                "b1": None,
                "b2": None,
                "b3": None,
                "b4": None,
                "b5": None,
                "b6": None,
                "b7": None,
                "c1": None,
                "c2": None,
                "c3": None,
                "c4": None,
                "d":  None,
            },
            pere={
                "a1a3": cls.convert_pere(
                    KBOBeco_object.get("Primärenergie erneuerbar (kWh oil-eq)"),
                    declared_factor
                ),
                "a4": None,
                "a5": None,
                "b1": None,
                "b2": None,
                "b3": None,
                "b4": None,
                "b5": None,
                "b6": None,
                "b7": None,
                "c1": None,
                "c2": None,
                "c3": None,
                "c4": None,
                "d":  None,
            },
            pert={
                "a1a3": cls.convert_pert(
                    KBOBeco_object.get("Primärenergie"),
                    declared_factor
                ),
                "a4": None,
                "a5": None,
                "b1": None,
                "b2": None,
                "b3": None,
                "b4": None,
                "b5": None,
                "b6": None,
                "b7": None,
                "c1": None,
                "c2": None,
                "c3": None,
                "c4": None,
                "d":  None,
            },
            gwp={
                "a1a3": cls.convert_gwp(
                    KBOBeco_object.get("Treibhausgasemissionen (kg CO2-eq)"),
                    declared_factor
                ),
                "a4": None,
                "a5": None,
                "b1": None,
                "b2": None,
                "b3": None,
                "b4": None,
                "b5": None,
                "b6": None,
                "b7": None,
                "c1": None,
                "c2": None,
                "c3": None,
                "c4": None,
                "d":  None,
            },
        )
        return epd



    @staticmethod
    def convert_gwp(gwp: str, declared_factor: float) -> float | None:
        try:
            return float(gwp) / declared_factor if gwp and gwp not in ["-", ""] else None
        except ValueError:
            return None

    @staticmethod
    def convert_pert(pert: str, declared_factor: float) -> float | None:
        try:
            return float(pert) / declared_factor if pert and pert not in ["-", ""] else None
        except ValueError:
            return None


    @staticmethod
    def convert_penre(penre: str, declared_factor: float) -> float | None:
        try:
            return float(penre) / declared_factor if penre and penre not in ["-", ""] else None
        except ValueError:
            return None

    @staticmethod
    def convert_pere(pere: str, declared_factor: float) -> float | None:
        try:
            return float(pere) / declared_factor if pere and pere not in ["-", ""] else None
        except ValueError:
            return None

    @staticmethod
    def convert_unit(unit: str) -> Unit:
        if unit == "STK":
            return Unit.PCS
        elif unit == "m":
            return Unit.M
        elif unit == "m2":
            return Unit.M2
        elif unit == "m3":
            return Unit.M3
        elif unit == "kg":
            return Unit.KG
        elif unit == "l":
            return Unit.L
        else:
            return Unit.UNKNOWN



def main(path: Path, out_path: Path):
    with path.open('r', encoding='utf-8-sig') as file:  # Handle potential BOM
        reader = csv.DictReader(file, delimiter=',')  # Specify the correct delimiter if not a comma
        for row in reader:
            parse_row(row, out_path)



def parse_row(row: dict, out_path: Path):
    epd = EPDx.from_dict(row)
    (out_path / f"{epd.id}.json").write_text(epd.json(ensure_ascii=False, indent=2))


if __name__ == "__main__":
    p = Path("C:\\Users\\LouisTrümpler\\Documents\\GitHub\\KBOB_EPDx\\src\\KBOB.csv")
    out = Path(__file__).parent.parent / "KBOB"
    main(p, out)
