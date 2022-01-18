import dataclasses
import re
import sys
from typing import List


@dataclasses.dataclass()
class Header:
    name: str
    level: int

    @property
    def slug(self):
        text = self.name.replace(' ', '-')
        # single chars that are removed
        text = re.sub(r'[`~!@#$%^&*()+=<>?,./:;"\'|{}\[\]\\–—]', '', text)
        # CJK punctuations that are removed
        text = re.sub(r'[　。？！，、；：“”【】（）〔〕［］﹃﹄“”‘’﹁﹂—…－～《》〈〉「」]', '', text)
        return text


class TOCMaker:
    def __init__(
            self,
            *,
            max_depth=6,
            link_prefix='',
            indentation_size=2,
            list_bullets=('-', '*', '+', '-'),
            header_class=Header,
    ):
        self.max_depth = max_depth
        self.link_prefix = link_prefix
        self.indentation_size = indentation_size
        self.list_bullets = list_bullets
        self.header_class = header_class

    def make(self, text):
        headers = self._collect_headers(text)
        return self._make_toc(headers)

    def make_from_file(self, fp):
        return self.make(fp.read())

    def _collect_headers(self, text):
        headers = []

        code_blocks = 0
        for line in text.splitlines():
            line = line.strip()
            code_blocks += line.count('```') % 2
            if code_blocks % 2 == 0 and line.startswith('#'):
                header = self._parse_header_from_line(line)
                if header.level <= self.max_depth:
                    headers.append(self._parse_header_from_line(line))

        return headers

    def _make_toc(self, headers: List[Header]):
        toc = []
        for header in headers:
            indentation = ' ' * ((header.level - 1) * self.indentation_size)
            bullet = self._get_bullet(header.level)
            toc.append(f'{indentation}{bullet} [{header.name}]({self.link_prefix}#{header.slug})')
        return '\n'.join(toc)

    def _get_bullet(self, level):
        if level > len(self.list_bullets):
            return self.list_bullets[-1]
        return self.list_bullets[level - 1]

    def _parse_header_from_line(self, line):
        level = 0
        name = ''
        for char in line:
            if char == '#':
                level += 1
            else:
                name = line[level + 1:].strip()
                break

        return self.header_class(
            name=name,
            level=level
        )


def paste_after(delimiter, content, text):
    result = []
    for line in text.splitlines():
        if line.strip() != delimiter:
            result.append(line)
        else:
            result.append(f'{delimiter}\n')
            result.append(f'{content}\n')
            return '\n'.join(result)

    raise ValueError(f"Can't find delimiter '{delimiter}'")


if __name__ == '__main__':
    with open('questions.md') as fp:
        maker = TOCMaker(link_prefix='questions.md/')
        toc = maker.make_from_file(fp)

    with open('README.md', 'r') as fp:
        original = fp.read()
        changed = paste_after('<!-- toc -->', toc, original)

    if '--check' in sys.argv:
        if original != changed:
            print('Error')
            sys.exit(1)
    else:
        with open('README.md', 'w') as fp:
            fp.write(changed)

    print('Done')
