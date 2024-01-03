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


        epd = cls(
            id=KBOBeco_object.get("UUID-Nummer") or str(uuid.uuid4()),
            format_version=importlib.metadata.version("epdx"),
            name=KBOBeco_object.get("BAUMATERIALIEN"),
            version="version 4 - 2024",
            declared_unit=cls.convert_unit(declared_unit),
            valid_until=datetime(year=2025, month=12, day=22),
            published_date=datetime(year=2024, month=11, day=25),
            source=Source(name="KBOB", uuid=KBOBeco_object.get("UUID-Nummer")),
            standard=Standard.EN15804A1,
            subtype="Generic",
            reference_service_life=None,
            location="CH",

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
    def convert_unit(unit: str) -> Unit:
        match unit:
            case "STK":
                return Unit.PCS
            case "M":
                return Unit.M
            case "M2":
                return Unit.M2
            case "M3":
                return Unit.M3
            case "KG":
                return Unit.KG
            case "L":
                return Unit.L
            case _:
                return Unit.UNKNOWN


    @staticmethod
    def convert_gwp(gwp: str, declared_factor: float) -> float | None:
        return None if gwp in ["-", ""] else float(gwp) / declared_factor



def main(path: Path, out_path: Path):
    reader = csv.DictReader(io.StringIO(path.read_text()))

    for row in reader:
        parse_row(row, out_path)


def parse_row(row: dict, out_path: Path):
    epd = EPDx.from_dict(row)
    (out_path / f"{epd.id}.json").write_text(epd.json(ensure_ascii=False, indent=2))


if __name__ == "__main__":
    p = Path("C:\\Users\\LouisTrümpler\\Documents\\GitHub\\KBOB_EPDx\\src\\KBOB.csv")
    out = Path(__file__).parent.parent / "KBOB"
    main(p, out)
