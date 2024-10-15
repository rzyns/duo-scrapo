from genanki.model import Model
from ..Morf import VerbForms  # noqa: TID252
from . import AnkiTemplate, cond, dedent, end_cond, field, front, humanize_gender, humanize_number, humanize_person, humanize_tense
from attr import asdict


def humanize_col_name(col_name: str) -> str:
    match col_name.split("_"):
        case [(tense), (number), (person), (gender)]:
            return " ".join(
                [
                    humanize_person(person, number),
                    humanize_number(number),
                    humanize_tense(tense),
                    humanize_gender(gender),
                ]
            )
        case [(tense), (number), (person)]:
            return " ".join(
                [
                    humanize_person(person, number),
                    humanize_number(number),
                    f"({humanize_tense(tense)})",
                ]
            )
        case _:
            return col_name.capitalize()


class TplA(AnkiTemplate):
    pass


class TplB(AnkiTemplate):
    pass


def _make_conjugation_table() -> str:
    return dedent(f"""
        {cond("_is_imperfect")}
        <table>
            <tbody>
                <tr>
                    <th colspan="2" > &nbsp; </th>
                    <th colspan="5"> singular </th>
                    <th colspan="2"> plural </th>
                </tr>
                <tr>
                    <th> &nbsp; </th>
                    <th> <b>pers.</b> </th>
                    <th align="center"> <i>m1.</i> </th>
                    <th align="center"> <i>m2.</i> </th>
                    <th align="center"> <i>m3.</i> </th>
                    <th align="center"> <i>f.</i> </th>
                    <th align="center"> <i>n.</i> </th>
                    <th align="center"> personal&nbsp;<i>m.</i> </th>
                    <th align="center"> <i>f.</i>&nbsp;/&nbsp;<i>n.</i>&nbsp;/&nbsp;<i>non-personal</i> <i>m.</i> </th>
                </tr>
                <tr>
                    <th align="center"> bezokolicznik </th>
                    <td> &nbsp; </td>
                    <td colspan="8" align="center"> {field("bezokolicznik")} </td>
                </tr>
                <tr class="czas_teraźniejszy">
                    <th rowspan="3"> czas teraźniejszy </th>
                    <td> 1st </td>
                    <td colspan="5" align="center"> {field("teraz_sg_1p")} </td>
                    <td colspan="2" align="center"> {field("teraz_pl_1p")} </td>
                </tr>
                <tr class="czas_teraźniejszy">
                    <td> 2nd </td>
                    <td colspan="5" align="center"> {field("teraz_sg_2p")} </td>
                    <td colspan="2" align="center"> {field("teraz_pl_2p")} </td>
                </tr>
                <tr class="czas_teraźniejszy">
                    <td> 3rd </td>
                    <td colspan="5" align="center"> {field("teraz_sg_3p")} </td>
                    <td colspan="2" align="center"> {field("teraz_pl_3p")} </td>
                </tr>
                <tr class="czas_przeszły">
                    <th rowspan="3"> czas przeszły </th>
                    <td> 1st </td>
                    <td> {field("przeszły_sg_1p_m1")} </td>
                    <td> {field("przeszły_sg_1p_m2")} </td>
                    <td> {field("przeszły_sg_1p_m3")} </td>
                    <td> {field("przeszły_sg_1p_f")} </td>
                    <td> {field("przeszły_sg_1p_n")} </td>
                    <td> {field("przeszły_pl_1p_m1")} </td>
                    <td> {field("przeszły_pl_1p_r")} </td>
                </tr>
                <tr class="czas_przeszły">
                    <td> 2nd </td>
                    <td> {field("przeszły_sg_2p_m1")} </td>
                    <td> {field("przeszły_sg_2p_m2")} </td>
                    <td> {field("przeszły_sg_2p_m3")} </td>
                    <td> {field("przeszły_sg_2p_f")} </td>
                    <td> {field("przeszły_sg_2p_n")} </td>
                    <td> {field("przeszły_pl_3p_m1")} </td>
                    <td> {field("przeszły_pl_3p_r")} </td>
                </tr>
                <tr class="czas_przeszły">
                    <td> 3rd </td>
                    <td> {field("przeszły_sg_3p_m1")} </td>
                    <td> {field("przeszły_sg_3p_m2")} </td>
                    <td> {field("przeszły_sg_3p_m3")} </td>
                    <td> {field("przeszły_sg_3p_f")} </td>
                    <td> {field("przeszły_sg_3p_n")} </td>
                    <td> {field("przeszły_pl_3p_m1")} </td>
                    <td> {field("przeszły_pl_3p_r")} </td>
                </tr>
                <tr class="czas_przyszły">
                    <th rowspan="3"> czas przyszły </th>
                    <td> 1st </td>
                    <td> {field("przyszły_sg_1p_m1")}<sup>1</sup> </td>
                    <td> {field("przyszły_sg_1p_m2")}<sup>1</sup> </td>
                    <td> {field("przyszły_sg_1p_m3")}<sup>1</sup> </td>
                    <td> {field("przyszły_sg_1p_f")}<sup>1</sup> </td>
                    <td> {field("przyszły_sg_1p_n")}<sup>1</sup> </td>
                    <td> {field("przyszły_pl_1p_m1")}<sup>1</sup> </td>
                    <td> {field("przyszły_pl_1p_r")}<sup>1</sup> </td>
                </tr>
                <tr class="czas_przyszły">
                    <td> 2nd </td>
                    <td> {field("przyszły_sg_2p_m1")}<sup>1</sup> </td>
                    <td> {field("przyszły_sg_2p_m2")}<sup>1</sup> </td>
                    <td> {field("przyszły_sg_2p_m3")}<sup>1</sup> </td>
                    <td> {field("przyszły_sg_2p_f")}<sup>1</sup> </td>
                    <td> {field("przyszły_sg_2p_n")}<sup>1</sup> </td>
                    <td> {field("przyszły_pl_2p_m1")}<sup>1</sup> </td>
                    <td> {field("przyszły_pl_2p_r")}<sup>1</sup> </td>
                </tr>
                <tr class="czas_przyszły">
                    <td> 3rd </td>
                    <td> {field("przyszły_sg_3p_m1")}<sup>1</sup> </td>
                    <td> {field("przyszły_sg_3p_m2")}<sup>1</sup> </td>
                    <td> {field("przyszły_sg_3p_m3")}<sup>1</sup> </td>
                    <td> {field("przyszły_sg_3p_f")}<sup>1</sup> </td>
                    <td> {field("przyszły_sg_3p_n")}<sup>1</sup> </td>
                    <td> {field("przyszły_pl_3p_m1")}<sup>1</sup> </td>
                    <td> {field("przyszły_pl_3p_r")}<sup>1</sup> </td>
                </tr>
                <tr>
                    <td colspan="8" align="left"> <sup>1</sup> &nbsp; <i>or:</i> będę {field("bezokolicznik")}, będziesz {field("bezokolicznik")} etc.</td>
                </tr>
            </tbody>
        </table>
        {end_cond("_is_imperfect")}
    """)


def _make_template(col: str):
    match col:
        case "bezokolicznik":
            return TplA(
                name="Infinitive",
                qfmt=dedent(
                    f"""
                    {field("en")} (Infinitive)
                    """
                ),
                afmt=dedent(
                    f"""
                    {front()}
                    <hr id="answer">
                    {field('bezokolicznik')} ({field('aspekt')})
                    <hr id="conjugation">
                    {_make_conjugation_table()}
                    """
                ),
            )
        case _:
            return TplB(
                name=humanize_col_name(col),
                qfmt=dedent(
                    f"""
                    {cond(col)}
                        {field('bezokolicznik')} ({humanize_col_name(col)})
                        <p>{field(f"type:{col}")}</p>
                    {end_cond(col)}
                    """
                ),
                afmt=dedent(
                    f"""
                    {front()}

                    <hr id="answer">

                    <p class="field-{col}">
                        {field(col)}
                    </p>
                    <p class="field-en">
                        {field("en")}
                    </p>
                    <hr id="conjugation">
                    {_make_conjugation_table()}
                    """
                ),
            )


templates = [
    _make_template(col)
    for col in filter(
        lambda name: name not in {"en", "pl"},
        VerbForms.get_cols(),
    )
]

MODEL_ID_CZASOWNIKI = 2057651084

model = Model(
    model_id=MODEL_ID_CZASOWNIKI,
    name="Czasowniki",
    fields=[
        {"name": col}
        for col in ("en", "pl", *VerbForms.get_cols())
    ],
    templates=[
        asdict(a)
        for a in templates
    ],
    css=dedent("""
        table {
            font-size: .75rem;
            line-height: 1rem;
            margin-bottom: .5rem;
            margin-top: .5rem;
            width: 100%;
        }
        th { background-color: silver; }
        td { border: 1px solid black; }

    """)
)
