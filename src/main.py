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

        declared_factor = float(KBOBeco_object.get("Bezug"))
        declared_unit = 1
        KBOBeco_id = KBOBeco_object.get("UUID-Nummer")

        epd = cls(
            id=cls.convert_lcabyg_id(KBOBeco_id),
            format_version=importlib.metadata.version("epdx"),
            name=KBOBeco_object.get("BAUMATERIALIEN"),
            version="version 4 - 2024",
            declared_unit=cls.convert_unit(declared_unit),
            valid_until=datetime(year=2025, month=12, day=22),
            published_date=datetime(year=2024, month=11, day=25),
            source="KBOB",
            standard=Standard.EN15804A1,
            subtype=cls.convert_subtype(KBOBeco_object.get("Data type")),
            comment=KBOBeco_id,
            reference_service_life=None,
            location="CH",
            conversions=[
                {"to": Unit.KG,
                 "value": float(KBOBeco_object.get("Masse")) * declared_factor}
            ],
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
                "c3": cls.convert_gwp(KBOBeco_object.get("Global Opvarmning, modul C3"), declared_factor),
                "c4": cls.convert_gwp(KBOBeco_object.get("Global Opvarmning, modul C4"), declared_factor),
                "d": cls.convert_gwp(KBOBeco_object.get("Global Opvarmning, modul D"), declared_factor),
            },
        )
        return epd

    @staticmethod
    def convert_lcabyg_id(bpst_id: str) -> str:
        _map = json.loads(Path("C:\\Users\\LouisTrümpler\\Documents\\GitHub\\KBOB_EPDx\\src\\lcabyg_tabel7_map.json").read_text())
        return _map.get(bpst_id, str(uuid.uuid4()))

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
    def convert_subtype(subtype: str) -> SubType:
        _map = {
            "Generisk data": SubType.Generic,
            "Branche data": SubType.Industry,
        }
        return _map.get(subtype)

    @staticmethod
    def convert_gwp(gwp: str, declared_factor: float) -> float | None:
        if gwp == "-":
            return None
        else:
            return float(gwp) / declared_factor


def main(path: Path, out_path: Path):
    reader = csv.DictReader(io.StringIO(path.read_text()))

    for row in reader:
        parse_row(row, out_path)


def parse_row(row: dict, out_path: Path):
    if row.get("Sorterings ID").startswith("#S"):
        return
    epd = EPDx.from_dict(row)

    (out_path / f"{epd.id}.json").write_text(epd.json(ensure_ascii=False, indent=2))


if __name__ == "__main__":
    p = Path("C:\\Users\\LouisTrümpler\\Documents\\GitHub\\KBOB_EPDx\\src\\KBOB.csv")
    out = Path(__file__).parent.parent / "KBOB"
    main(p, out)
