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
        id_nummer = KBOBeco_object.get("ID-Nummer")
        uuid_nummer = KBOBeco_object.get("UUID-Nummer")
        gruppe = KBOBeco_object.get("Gruppe")
        baumaterialien = KBOBeco_object.get("BAUMATERIALIEN")
        id_nummer_entsorgung = KBOBeco_object.get("ID-Nummer Entsorgung")
        entsorgung = KBOBeco_object.get("Entsorgung")
        dichte_masse = KBOBeco_object.get("Dichte/Masse")
        bezug = KBOBeco_object.get("Bezug")
        ubp_total = KBOBeco_object.get("UBP Total")
        ubp_herstellung = KBOBeco_object.get("UBP Herstellung")
        ubp_entsorgung = KBOBeco_object.get("UBP Entsorgung")
        pe_gesamt_total = KBOBeco_object.get("PE gesamt, Total")
        pe_herstellung_total = KBOBeco_object.get("PE gesamt, Herstellung total")
        pe_herstellung_energetisch_genutzt = KBOBeco_object.get("PE gesamt, Herstellung energetisch genutzt")
        pe_herstellung_stofflich_genutzt = KBOBeco_object.get("PE gesamt, Herstellung stofflich genutzt")
        pe_entsorgung = KBOBeco_object.get("PE gesamt, Entsorgung")
        pe_erneuerbar_total = KBOBeco_object.get("PE erneuerbar, Total")
        pe_erneuerbar_herstellung_total = KBOBeco_object.get("PE erneuerbar, Herstellung total")
        pe_erneuerbar_herstellung_energetisch_genutzt = KBOBeco_object.get("PE erneuerbar, Herstellung energetisch genutzt")
        pe_erneuerbar_herstellung_stofflich_genutzt = KBOBeco_object.get("PE erneuerbar, Herstellung stofflich genutzt")
        pe_erneuerbar_entsorgung = KBOBeco_object.get("PE erneuerbar, Entsorgung")
        pe_nicht_erneuerbar_total = KBOBeco_object.get("PE nicht erneuerbar, Total")
        pe_nicht_erneuerbar_herstellung_total = KBOBeco_object.get("PE nicht erneuerbar, Herstellung total")
        pe_nicht_erneuerbar_herstellung_energetisch_genutzt = KBOBeco_object.get("PE nicht erneuerbar, Herstellung energetisch genutzt")
        pe_nicht_erneuerbar_herstellung_stofflich_genutzt = KBOBeco_object.get("PE nicht erneuerbar, Herstellung stofflich genutzt")
        pe_nicht_erneuerbar_entsorgung = KBOBeco_object.get("PE nicht erneuerbar, Entsorgung")
        gwp_total = KBOBeco_object.get("GWP Total")
        gwp_entsorgung = KBOBeco_object.get("GWP Entsorgung")
        gwp_herstellung = KBOBeco_object.get("GWP Herstellung")
        biogener_kohlenstoff = KBOBeco_object.get("Biogener Kohlenstoff")
        french_name = KBOBeco_object.get("French Name")


        # Initialize a default conversion dictionary
        conversion_value = {"to": Unit.KG, "value": 0.0, "error": "Not per kg"}

        # Check if dichte_masse is a valid float and not a dash ('-')
        if dichte_masse.replace('.', '', 1).isdigit() and dichte_masse != "-":
            conversion_value = {"to": Unit.KG, "value": float(dichte_masse) * declared_factor, "error": None}

        conversions = [conversion_value]


        epd = cls(
            id=KBOBeco_object.get("UUID-Nummer") or str(uuid.uuid4()),
            format_version=importlib.metadata.version("epdx"),
            name=baumaterialien,
            version="V4 - 2024",
            declared_unit=cls.convert_unit(declared_unit),
            valid_until=datetime(year=2025, month=12, day=22),
            published_date=datetime(year=2024, month=11, day=25),
            source=Source(name="KBOB", url="https://www.kbob.admin.ch/kbob/de/home/themen-leistungen/nachhaltiges-bauen/oekobilanzdaten_baubereich.html"),
            standard=Standard.EN15804A2,
            subtype="Generic",
            comment = f'{id_nummer}/{baumaterialien}',
            meta_data = {
                "ID-Nummer": id_nummer,
                "Material Group": gruppe,
                "UBP Total": ubp_total,
                "UBP Manufacturing": ubp_herstellung,
                "UBP Disposal": ubp_entsorgung,
                "Total PE": pe_gesamt_total,
                "Total Manufacturing PE": pe_herstellung_total,
                "Energy Utilized Manufacturing PE": pe_herstellung_energetisch_genutzt,
                "Material Utilized Manufacturing PE": pe_herstellung_stofflich_genutzt,
                "Disposal PE": pe_entsorgung,
                "Total Renewable PE": pe_erneuerbar_total,
                "Total Renewable Manufacturing PE": pe_erneuerbar_herstellung_total,
                "Energy Utilized Renewable Manufacturing PE": pe_erneuerbar_herstellung_energetisch_genutzt,
                "Material Utilized Renewable Manufacturing PE": pe_erneuerbar_herstellung_stofflich_genutzt,
                "Renewable Disposal PE": pe_erneuerbar_entsorgung,
                "Total Non-renewable PE": pe_nicht_erneuerbar_total,
                "Total Non-renewable Manufacturing PE": pe_nicht_erneuerbar_herstellung_total,
                "Energy Utilized Non-renewable Manufacturing PE": pe_nicht_erneuerbar_herstellung_energetisch_genutzt,
                "Material Utilized Non-renewable Manufacturing PE": pe_nicht_erneuerbar_herstellung_stofflich_genutzt,
                "Non-renewable Disposal PE": pe_nicht_erneuerbar_entsorgung,
                "GWP Total": gwp_total,
                "GWP Disposal": gwp_entsorgung,
                "GWP Manufacturing": gwp_herstellung,
                "Biogenic Carbon": biogener_kohlenstoff
            },
            reference_service_life=60,
            location="CH",
            conversions = [conversion_value],
            penre={
                "a1a3": cls.convert_penre(
                    KBOBeco_object.get("PE nicht erneuerbar, Herstellung total"),
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
                "c1": cls.convert_penre(
                    KBOBeco_object.get("PE nicht erneuerbar, Entsorgung"),
                    declared_factor
                ),
                "c2": None,
                "c3": None,
                "c4": None,
                "d":  None,
            },
            pere={
                "a1a3": cls.convert_pere(
                    KBOBeco_object.get("PE erneuerbar, Herstellung total"),
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
                "c1": cls.convert_penre(
                    KBOBeco_object.get("PE erneuerbar, Entsorgung"),
                    declared_factor
                ),
                "c2": None,
                "c3": None,
                "c4": None,
                "d":  None,
            },
            pert={
                "a1a3": cls.convert_pert(
                    KBOBeco_object.get("PE gesamt, Total"),
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
                    KBOBeco_object.get("GWP Herstellung"),
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
                "c1": cls.convert_penre(
                    KBOBeco_object.get("GWP Entsorgung"),
                    declared_factor
                ),
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
    (out_path / f"{epd.id}.json").write_text(epd.json())

#help(EPD)
#print(dir(EPD))


if __name__ == "__main__":
    p = Path("C:\\Users\\LouisTrümpler\\Documents\\GitHub\\KBOB_EPDx\\src\\Oekobilanzdaten_ Baubereich_Donne_ecobilans_construction_2009-1-2022_v4_0_clean.csv")
    out = Path(__file__).parent.parent / "KBOB"
    main(p, out)
