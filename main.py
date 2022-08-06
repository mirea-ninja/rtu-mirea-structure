import json
from types import SimpleNamespace
from mdutils import MdUtils


def fenced_code_block(code, lang):
    return f"""```{lang}\n{code}\n```"""


def tex_fenced_code_block(code):
    return fenced_code_block(code, "tex")


def html_fenced_code_block(code):
    return fenced_code_block(code, "html")


def text_fenced_code_block(code):
    return fenced_code_block(code, "text")


def from_tex_to_text(tex_source):
    return tex_source \
        .replace("~", " ") \
        .replace("---", "—") \
        .replace("--", "–") \
        .replace("<<", "«") \
        .replace(">>", "»") \
        .replace("\\textnumero", "№")


def from_tex_to_html(tex_source):
    return tex_source \
        .replace("~", "&nbsp;") \
        .replace("---", "&mdash;") \
        .replace("--", "&#8211;") \
        .replace("<<", "&laquo;") \
        .replace(">>", "&raquo;") \
        .replace("„", "&#132;") \
        .replace("“", "&#147;") \
        .replace("\\textnumero", "&numero;")


def from_tex_to_tex_with_dirtytalk(tex_source):
    return tex_source \
        .replace("<<", "\\say{") \
        .replace(">>", "}") \
        .replace("„", "\\say{") \
        .replace("“", "}")


def add_code_sources_to_md_file(md_file, tex_source, headers_level):
    md_file.new_header(headers_level, "Plain text:")
    md_file.new_line(text_fenced_code_block(from_tex_to_text(tex_source)))

    md_file.new_header(headers_level, "TeX:")
    md_file.new_line(tex_fenced_code_block(tex_source))

    md_file.new_header(headers_level, "TeX with dirtytalk package:")
    md_file.new_line(tex_fenced_code_block(from_tex_to_tex_with_dirtytalk(tex_source)))

    md_file.new_header(headers_level, "HTML:")
    md_file.new_line(html_fenced_code_block(from_tex_to_html(tex_source)))


def generate_university_md_file(rtu_mirea_structure):
    md_file = MdUtils(file_name="readme.md")

    md_file.new_header(1, "Университет")

    md_file.new_header(2, "Название")
    add_code_sources_to_md_file(md_file, rtu_mirea_structure.name, 3)
    md_file.new_header(2, "Короткое название")
    add_code_sources_to_md_file(md_file, rtu_mirea_structure.short_name, 3)
    md_file.new_header(2, "Полное название")
    add_code_sources_to_md_file(md_file, rtu_mirea_structure.full_name, 3)

    md_file.new_header(2, "Учебно-научные структурные подразделения")
    for division in rtu_mirea_structure.educational_and_scientific_structural_divisions:
        md_file.new_line(f"* [{from_tex_to_html(division.name)}](./educational_" +
                         f"and_scientific_structural_divisions/{from_tex_to_text(division.short_name)}.md)")

    md_file.new_header(2, "Филиалы")
    for branch in rtu_mirea_structure.branches:
        md_file.new_line(f"* [{from_tex_to_html(branch.short_name)}]" +
                         f"(./branches/{from_tex_to_text(branch.short_name).replace(' ', '%20')}.md)")

    md_file.new_header(1, "Источники")
    sources = {
        "Структура РТУ МИРЭА": "https://www.mirea.ru/about/the-structure-of-the-university/",
        "ГОСТ 8.417-81": "https://docs.cntd.ru/document/1200005371",
        "Википедия. Неразрывный пробел": "https://ru.wikipedia.org/wiki/Неразрывный_пробел",
        "А.&nbsp;Лебедев «Ководство. §&nbsp;97. Тире, минус и&nbsp;дефис, или Черты русской типографики":
            "https://www.artlebedev.ru/kovodstvo/sections/97/",
        "А.&nbsp;Лебедев «Ководство. §&nbsp;158. Короткое тире»": "https://www.artlebedev.ru/kovodstvo/sections/158/"
    }
    for name, link in sources.items():
        md_file.new_line(f"* {md_file.new_reference_link(link, name)}")

    md_file.create_md_file()


def generate_education_and_scientific_structural_divisions_md_file(division_structure):
    md_file = MdUtils(file_name="./educational_and_scientific_structural_divisions/" +
                                f"{from_tex_to_text(division_structure.short_name)}.md")

    md_file.new_header(1, from_tex_to_html(division_structure.name))

    md_file.new_header(2, "Название")
    add_code_sources_to_md_file(md_file, division_structure.name, 3)
    md_file.new_header(2, "Короткое название")
    add_code_sources_to_md_file(md_file, division_structure.short_name, 3)

    if len(division_structure.departments) > 0:
        md_file.new_header(2, "Структура")
        for department in division_structure.departments:
            md_file.new_header(3, from_tex_to_html(department[0].upper() + department[1:]))
            add_code_sources_to_md_file(md_file, department, 4)

    md_file.create_md_file()


def generate_branches_md_file(branch_structure):
    md_file = MdUtils(file_name=f"./branches/{from_tex_to_text(branch_structure.short_name)}.md")

    md_file.new_header(1, from_tex_to_html(branch_structure.short_name[0].upper() + branch_structure.short_name[1:]))

    md_file.new_header(2, "Полное название")
    add_code_sources_to_md_file(md_file, branch_structure.full_name, 3)
    md_file.new_header(2, "Короткое название")
    add_code_sources_to_md_file(md_file, branch_structure.short_name, 3)

    md_file.new_header(2, "Структура")
    for department in branch_structure.departments:
        md_file.new_header(3, from_tex_to_html(department[0].upper() + department[1:]))
        add_code_sources_to_md_file(md_file, department, 4)

    md_file.create_md_file()


def main():
    rtu_mirea_structure = json.loads(open("rtu-mirea-structure.json").read(),
                                     object_hook=lambda d: SimpleNamespace(**d))

    generate_university_md_file(rtu_mirea_structure)
    for division in rtu_mirea_structure.educational_and_scientific_structural_divisions:
        generate_education_and_scientific_structural_divisions_md_file(division)

    for branch in rtu_mirea_structure.branches:
        generate_branches_md_file(branch)


if __name__ == '__main__':
    main()
