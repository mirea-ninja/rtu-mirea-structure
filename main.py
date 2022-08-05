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
        .replace("\\textnumero", "&numero;")


def add_code_sources_to_md_file(md_file, tex_source, headers_level):
    md_file.new_header(headers_level, "Plain text:")
    md_file.new_line(text_fenced_code_block(from_tex_to_text(tex_source)))
    md_file.new_header(headers_level, "TeX:")
    md_file.new_line(tex_fenced_code_block(tex_source))
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

    md_file.new_header(2, "Институты")
    for institute in rtu_mirea_structure.institutes:
        md_file.new_line(f"* [{from_tex_to_html(institute.name)}](./institutes/{institute.short_name}.md)")

    md_file.new_header(1, "Источники")
    md_file.new_line("* [Структура РТУ МИРЭА](https://www.mirea.ru/about/the-structure-of-the-university/)")
    md_file.new_line("* [ГОСТ 8.417-81](https://docs.cntd.ru/document/1200005371)")
    md_file.new_line("* [Википедия. Неразрывный пробел](https://ru.wikipedia.org/wiki/Неразрывный_пробел)")
    md_file.new_line("* [А.&nbsp;Лебедев «Ководство. § 97. Тире, минус и дефис, или Черты русской типографики»]" +
                     "(https://www.artlebedev.ru/kovodstvo/sections/97/)")
    md_file.new_line("* [А.&nbsp;Лебедев «Ководство. § 158. Короткое тире»]" +
                     "(https://www.artlebedev.ru/kovodstvo/sections/158/)")

    md_file.create_md_file()


def generate_institute_md_file(institute_structure):
    md_file = MdUtils(file_name=f"./institutes/{institute_structure.short_name}.md")

    md_file.new_header(1, from_tex_to_html(institute_structure.name))

    md_file.new_header(2, "Название")
    add_code_sources_to_md_file(md_file, institute_structure.name, 3)
    md_file.new_header(2, "Короткое название")
    add_code_sources_to_md_file(md_file, institute_structure.short_name, 3)

    md_file.new_header(2, "Структура института")
    for department in institute_structure.departments:
        md_file.new_header(3, from_tex_to_html(department[0].upper() + department[1:]))
        add_code_sources_to_md_file(md_file, department, 4)

    md_file.create_md_file()


def main():
    rtu_mirea_structure = json.loads(open("rtu-mirea-structure.json").read(),
                                     object_hook=lambda d: SimpleNamespace(**d))

    generate_university_md_file(rtu_mirea_structure)
    for institute in rtu_mirea_structure.institutes:
        generate_institute_md_file(institute)


if __name__ == '__main__':
    main()
