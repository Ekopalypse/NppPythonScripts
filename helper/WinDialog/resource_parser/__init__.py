from dataclasses import dataclass
from ..win_helper import (
    WindowStyle as WS,
    ExtendedWindowStyles as WS_EX,
    DialogBoxStyles as DS
)
from ..controls.button import BS
from ..controls.static import SS
from ..controls.edit import ES
from ..controls.listbox import LBS
from ..controls.syslistview32 import LVS, LVS_EX
from ..controls.combobox import CBS, CBES_EX
from ..controls.msctls_progress32 import PBS
from ..controls.msctls_statusbar32 import SBARS
from ..controls.msctls_updown32 import UDS


STYLE_MAP = {
    'WS': WS,
    'WS_EX': WS_EX,
    'DS': DS,
    'BS': BS,
    'SS': SS,
    'ES': ES,
    'LBS': LBS,
    'LVS': LVS,
    'LVS_EX': LVS_EX,
    'CBS': CBS,
    'CBES_EX': CBES_EX,
    'PBS': PBS,
    'SBARS': SBARS,
    'UDS': UDS,
}

@dataclass
class FONT:
    pointsize: int = None
    typeface: str = None
    weight: int = None
    italic: int = None
    charset: int = None

    def __init__(self, line):
        not_set = [None] * 5
        pointsize, typeface, weight, italic, charset, *_ = [x.strip() for x in line.split(',')] + not_set
        self.pointsize = int(pointsize) if pointsize else 0
        self.typeface = typeface.strip('"')
        self.weight = int(weight) if weight else 0
        self.italic = int(italic) if italic else 0
        self.charset = int(charset) if charset else 0


@dataclass
class ControlStatement:
    # ('', '1', 'EDIT', ['ES_LEFT', 'WS_CHILD', 'WS_VISIBLE', 'WS_BORDER', 'WS_TABSTOP'], 6, 5, 240, 14),
    title: str = ''
    id_ : int = None
    control_class: str = ''
    style: int = None
    position: (int, int) = None
    size: (int, int) = None
    ex_style: int = 0
    name: str = None

    def __init__(self, line):
        if '//' in line:
            line, name = line.split('//')
            self.name = name.strip()
        self.title, self.id_, control_class, style, x, y, width, height, *ex_style = [x.strip().strip('"') for x in line.split(',')]
        self.control_class = control_class.lower()
        self.style = _get_style_value([x.strip() for x in style.split('|')])
        self.position = (int(x), int(y))
        self.size = int(width), int(height)
        self.ex_style = _get_extended_style_value(ex_style)


@dataclass
class DialogExResource:
    styles: int = None
    ex_styles: int = 0
    title: str = ''
    size: (int, int) = (300, 400)
    position: (int, int) = (0, 0)
    font: FONT = None
    controls: list[ControlStatement] = None
    def __post_init__(self):
        if self.controls is None:
            self.controls = []

# TODO: needs to be revised if VS generated rc files are considered.
def parser(rc_code):
    dlg = DialogExResource()
    for line_ in rc_code.splitlines():
        line = line_.strip()
        if line.startswith('CONTROL'):
            dlg.controls.append(ControlStatement(line.replace('CONTROL', '')))
        elif line.startswith('STYLE'):
            dlg.styles = _get_style_value([x.strip() for x in line.replace('STYLE', '').split('|')])
        elif line.startswith('EXSTYLE'):
            dlg.ex_styles = _get_extended_style_value([x.strip() for x in line.replace('EXSTYLE', '').split('|')])
        elif line.startswith('CAPTION'):
            dlg.title = line.replace('CAPTION', '').strip().strip('"')
        elif line.startswith('FONT'):
            dlg.font = FONT(line.replace('FONT', ''))
        else:
            if 'DIALOGEX' in line:
                pos = line.find('DIALOGEX',0)
                x, y, width, height, *rest = [x.strip() for x in line[pos+8:].split(',')]
                dlg.position = (int(x), int(y))
                dlg.size = (int(width), int(height))
            else:
                continue
    return dlg

def _get_extended_style_value(styles):
    value = 0
    for style in styles:
        klass, _, member = style.partition('_EX_')
        klass += '_EX'
        if klass in STYLE_MAP:
            value += STYLE_MAP[klass].__members__.get(member, 0)
    return value

def _get_style_value(styles):
    value = 0
    for style in styles:
        klass, _, member = style.partition('_')
        if klass in STYLE_MAP:
            value += STYLE_MAP[klass].__members__.get(member, 0)
    return value