import json
from pathlib import Path
from collections import defaultdict
from types import SimpleNamespace
from mdutils import MdUtils

EDUCATIONAL_AND_SCIENTIFIC_STRUCTURAL_DIVISIONS_DIRECTORY_NAME = (
    "educational_and_scientific_structural_divisions"
)
BRANCHES_DIRECTORY_NAME = "branches"


def fenced_code_block(code, lang):
    return f"""```{lang}\n{code}\n```"""


def tex_fenced_code_block(code):
    return fenced_code_block(code, "tex")


def html_fenced_code_block(code):
    return fenced_code_block(code, "html")


def text_fenced_code_block(code):
    return fenced_code_block(code, "text")


def from_tex_to_text(tex_source):
    return (
        tex_source.replace("~", " ")
        .replace("---", "—")
        .replace("--", "–")
        .replace("<<", "«")
        .replace(">>", "»")
        .replace("‘‘", "“")
        .replace("‘‘", "“")
        .replace("’’", "”")
        .replace("\\textnumero", "№")
    )


def from_tex_to_html(tex_source):
    return (
        tex_source.replace("~", "&nbsp;")
        .replace("---", "&mdash;")
        .replace("--", "&#8211;")
        .replace("<<", "&laquo;")
        .replace(">>", "&raquo;")
        .replace("‘‘", "“")
        .replace("’’", "”")
        .replace("\\textnumero", "&numero;")
    )


def from_tex_to_tex_with_dirtytalk(tex_source):
    return (
        tex_source.replace("<<", "\\say{")
        .replace(">>", "}")
        .replace("„", "\\say{")
        .replace("“", "}")
        .replace("‘‘", "\\say{")
        .replace("’’", "}")
    )


def add_code_sources_to_md_file(md_file, tex_source):
    code = {
        "plain text": from_tex_to_text(tex_source),
        "TeX": tex_source,
        "TeX with dirtytalk package": from_tex_to_tex_with_dirtytalk(tex_source),
        "HTML": from_tex_to_html(tex_source),
    }

    grouped_code = defaultdict(list)
    for language, code_source in sorted(code.items(), key=lambda t: t[0].lower()):
        grouped_code[code_source].append(language)

    for code_source, languages in grouped_code.items():
        md_file.new_list(languages)
        if languages[0] == "plain text":
            code_block = text_fenced_code_block(code_source)
        elif languages[0] in ("TeX", "TeX with dirtytalk package"):
            code_block = tex_fenced_code_block(code_source)
        elif languages[0] == "HTML":
            code_block = html_fenced_code_block(code_source)
        else:
            code_block = fenced_code_block(code_source, "")
        md_file.new_paragraph(code_block)

        md_file.new_paragraph("---")


def generate_university_md_file(rtu_mirea_structure, path: Path):
    path.mkdir(parents=True, exist_ok=True)

    md_file = MdUtils(file_name=str(Path(path, "README.md")))

    md_file.new_header(1, "Университет")

    md_file.new_header(2, "Полное название")
    add_code_sources_to_md_file(md_file, rtu_mirea_structure.full_name)
    md_file.new_header(2, "Короткое название")
    add_code_sources_to_md_file(md_file, rtu_mirea_structure.short_name)

    md_file.new_header(2, "Учебно-научные структурные подразделения")
    md_file.new_list(
        map(
            lambda division: md_file.new_reference_link(
                str(
                    Path(
                        EDUCATIONAL_AND_SCIENTIFIC_STRUCTURAL_DIVISIONS_DIRECTORY_NAME,
                        f"{from_tex_to_text(division.short_name).replace(' ', '%20')}.md",
                    )
                ),
                from_tex_to_html(division.full_name),
            ),
            rtu_mirea_structure.educational_and_scientific_structural_divisions,
        )
    )

    md_file.new_header(2, "Филиалы")
    md_file.new_list(
        map(
            lambda branch: md_file.new_reference_link(
                str(
                    Path(
                        BRANCHES_DIRECTORY_NAME,
                        f"{from_tex_to_text(branch.short_name).replace(' ', '%20')}.md",
                    )
                ),
                from_tex_to_html(branch.short_name),
            ),
            rtu_mirea_structure.branches,
        )
    )

    md_file.new_header(1, "Источники")
    sources = {
        "Структура РТУ МИРЭА": "https://www.mirea.ru/about/the-structure-of-the-university/",
        "ГОСТ 8.417-2002": "https://ru.wikisource.org/wiki/ГОСТ_8.417‒2002",
        "Википедия. Неразрывный пробел": "https://ru.wikipedia.org/wiki/Неразрывный_пробел",
        "А.&nbsp;Лебедев «Ководство. §&nbsp;97. Тире, минус и&nbsp;дефис, или Черты русской типографики": "https://www.artlebedev.ru/kovodstvo/sections/97/",
        "А.&nbsp;Лебедев «Ководство. §&nbsp;158. Короткое тире»": "https://www.artlebedev.ru/kovodstvo/sections/158/",
    }
    md_file.new_list(
        list(map(lambda key: md_file.new_reference_link(sources[key], key), sources))
    )

    md_file.create_md_file()


def generate_division_or_brench_files(structure, md_file):
    md_file.new_header(2, "Полное название")
    add_code_sources_to_md_file(md_file, structure.full_name)
    md_file.new_header(2, "Короткое название")
    add_code_sources_to_md_file(md_file, structure.short_name)

    if len(structure.departments) > 0:
        md_file.new_header(2, "Структура")
        for department in structure.departments:
            md_file.new_header(
                3, from_tex_to_html(department[0].upper() + department[1:])
            )
            add_code_sources_to_md_file(md_file, department)

    md_file.create_md_file()


def generate_education_and_scientific_structural_divisions_md_file(
    division_structure, path: Path
):
    path = Path(path, EDUCATIONAL_AND_SCIENTIFIC_STRUCTURAL_DIVISIONS_DIRECTORY_NAME)
    path.mkdir(parents=True, exist_ok=True)

    md_file = MdUtils(
        file_name=str(
            Path(path, f"{from_tex_to_text(division_structure.short_name)}.md")
        )
    )

    md_file.new_header(1, from_tex_to_html(division_structure.full_name))

    generate_division_or_brench_files(division_structure, md_file)


def generate_branches_md_file(branch_structure, path: Path):
    path = Path(path, BRANCHES_DIRECTORY_NAME)
    path.mkdir(parents=True, exist_ok=True)

    md_file = MdUtils(
        file_name=str(Path(path, f"{from_tex_to_text(branch_structure.short_name)}.md"))
    )

    md_file.new_header(
        1,
        from_tex_to_html(
            branch_structure.short_name[0].upper() + branch_structure.short_name[1:]
        ),
    )

    generate_division_or_brench_files(branch_structure, md_file)


def generate_laguage_specific_structure(rtu_mirea_structure, lang: str):
    rtu_mirea_structure_lang = getattr(rtu_mirea_structure, lang)
    path = Path(lang)

    generate_university_md_file(rtu_mirea_structure_lang, path)
    for (
        division
    ) in rtu_mirea_structure_lang.educational_and_scientific_structural_divisions:
        generate_education_and_scientific_structural_divisions_md_file(division, path)
    for branch in rtu_mirea_structure_lang.branches:
        generate_branches_md_file(branch, path)


def main():
    rtu_mirea_structure = json.loads(
        open("rtu-mirea-structure.json").read(),
        object_hook=lambda d: SimpleNamespace(**d),
    )

    for lang in rtu_mirea_structure.__dict__.keys():
        generate_laguage_specific_structure(rtu_mirea_structure, lang)

    with open("ru_RU/README.md", "r") as rm_ru_file:
        rm_file = MdUtils(file_name="README.md")

        rm_file.new_paragraph(
            rm_file.new_reference_link("en_US/README.md", "English names")
        )
        rm_file.new_paragraph(
            rm_ru_file.read()
            .replace(
                EDUCATIONAL_AND_SCIENTIFIC_STRUCTURAL_DIVISIONS_DIRECTORY_NAME,
                str(
                    Path(
                        "ru_RU",
                        EDUCATIONAL_AND_SCIENTIFIC_STRUCTURAL_DIVISIONS_DIRECTORY_NAME,
                    )
                ),
            )
            .replace(
                BRANCHES_DIRECTORY_NAME, str(Path("ru_RU", BRANCHES_DIRECTORY_NAME))
            )
        )
        rm_file.create_md_file()


if __name__ == "__main__":
    main()
