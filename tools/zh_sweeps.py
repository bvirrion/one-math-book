#!/usr/bin/env python3
"""Sweeps over an installed zh year (parts/<year>/zh and solutions/zh), against the English twin.

    python3 draft/zh-sweeps.py <year> [--fix]

Reports (and with --fix, repairs the safe classes):
  quotes      ``…'' around Chinese text -> “…”                       (fix)
  fwdigit     full-width digits -> ASCII                             (fix)
  dash        ' --- ' in a Chinese line -> '——' (mainland dash)                    (fix)
  tabcr       a space between a Chinese character and \\\\                    (fix)
  emphspace   a space between Chinese and a Chinese \\emph/\\omterm/\\textbf   (fix)
  dupbreak    the same Han character ending one line and opening the next (的\n的)   (report)
  short       a prose line far shorter than its English twin: a dropped clause      (report)
  nounref     a noun or 第 before \\cref, which prints its own noun                  (report)
  latinname   a capitalised Latin word of 4+ letters in visible prose (a name left untranslated) (report)
After --fix, every file's math spans, labels and braces are compared with English again (id_apply censuses).
"""
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent  # tools/ -> repo
sys.path.insert(0, str(REPO / 'tools'))
import id_apply as A  # noqa: E402

HAN = '㐀-䶿一-鿿'
QUOTES = re.compile(rf"``((?:(?!'').)*[{HAN}](?:(?!'').)*)''")
NOUNREF = re.compile(r'(?:定理|命题|引理|推论|定义|例题|例|注|练习|问题|方法|记号|章|第)[\s~]*\\[cC]ref\{')
LATIN = re.compile(r'(?<![\\A-Za-z{])[A-Z][a-z]{3,}')
MASK = re.compile(r'\$[^$]*\$|\\[A-Za-z]+(?:\[[^\]]*\])?(?:\{[^{}]*\})?|%.*')


def pairs(year):
    base = REPO / 'parts' / year
    for kind in ('', 'solutions/'):
        for t in sorted((base / f'{kind}zh').glob('[0-9][0-9]-*.tex')):
            yield base / kind / t.name, t


ROMAN = 'VIII|VII|III|II|IV|IX|VI|V|I|X'
CN = {'I': '一', 'II': '二', 'III': '三', 'IV': '四', 'V': '五', 'VI': '六', 'VII': '七', 'VIII': '八', 'IX': '九', 'X': '十'}
PARTREF = re.compile(rf'第 ?({ROMAN})(?: ?(--|–|—|至|、) ?({ROMAN}))? ?部分')


def main():
    year, fix = sys.argv[1], '--fix' in sys.argv
    counts = {}
    for en_p, zh_p in pairs(year):
        en = A.unwrap_omterm(en_p.read_text(encoding='utf-8')).split('\n')
        orig = zh_p.read_text(encoding='utf-8')
        # inside an index key `！` is no sub-entry mark (the pack's punctuation pass made 25 of them, Books 2-3)
        zh_text = re.sub(r'\\index\{(?:[^{}]|\{[^{}]*\})*\}', lambda m: m.group(0).replace('！', '!'), orig)
        if zh_text != orig:
            counts['indexbang'] = counts.get('indexbang', 0) + zh_text.count('!') - orig.count('!')
        zh = zh_text.split('\n')
        rel = f'{zh_p.parent.parent.name}/{zh_p.parent.name}/{zh_p.name}' if 'solutions' in str(zh_p) else f'zh/{zh_p.name}'
        out = list(zh)
        inmath, state = [], False   # does line i open inside an inline formula begun on an earlier line?
        for l in zh:
            inmath.append(state)
            body = re.sub(r'(?<!\\)%.*', '', l).replace('\\$', '')
            if len(re.findall(r'\$', body.replace('$$', ''))) % 2:
                state = not state
        for i, l in enumerate(zh):
            if l.lstrip().startswith('%'):
                continue
            nl = QUOTES.sub(r'“\1”', l)
            nl = re.sub('[０-９]', lambda m: chr(ord(m.group(0)) - 0xfee0), nl)
            # a problem's parts in Chinese numerals, as most files write them: 第 III 部分 -> 第三部分 (Book 3 close)
            if re.search(f'[{HAN}]', nl):  # `Part III --- 占优根`, `（Part I 与 Part III）` left by the model
                nl = re.sub(rf'(?:(?<=[{HAN}（]) )?\bParts? ({ROMAN})(?: ?(--|–|—|至|、) ?({ROMAN}))?\b(?: (?=[{HAN}]))?',
                            lambda m: '第' + CN[m.group(1)] + ({'、': '、'}.get(m.group(2), '至') + CN[m.group(3)]
                                                             if m.group(3) else '') + '部分', nl)
            nl = PARTREF.sub(lambda m: '第' + CN[m.group(1)] + ({'、': '、'}.get(m.group(2), '至') + CN[m.group(3)]
                                                               if m.group(3) else '') + '部分', nl)
            # a typed space between Chinese and a Chinese \emph/\omterm/\textbf, either side (就 \emph{退位})
            nl = re.sub(rf'(?<=[{HAN}，。：；、）”]) (?=\\(?:emph|omterm\{{[^{{}}]*\}}|textbf)\{{[{HAN}])', '', nl)
            nl = re.sub(rf'(?<=[{HAN}]\}})((?:\\index\{{[^{{}}]*\}})?) (?=[{HAN}（，。])', r'\1', nl)
            # xeCJK + tabular: a Chinese character right before a row end is "Improper alphabetic constant" (Book 2, g12)
            nl = re.sub(rf'(?<=[{HAN}])\\\\', r' \\\\', nl)
            if re.search(f'[{HAN}、，。：；（）]', nl) and '---' in nl and nl.strip() != '---':   # mainland dash: —— with no spaces
                lead = '$' if inmath[i] else ''
                # a formula left open at the end of the line (it runs on) is math too: `(?<!\\)\$[^$]*$`
                parts = re.split(r'(\$[^$]*\$|(?<!\\)\$[^$]*$|(?<!\\)%.*)', lead + nl)
                nl = ''.join(q if i % 2 else re.sub(r'(?:\\ |[ \t])*---[ \t]*', '——', q)
                             for i, q in enumerate(parts))
                if lead:
                    nl = nl[1:]
            if nl != l:
                counts['quotes/fwdigit'] = counts.get('quotes/fwdigit', 0) + 1
                out[i] = nl
            if NOUNREF.search(l):
                counts['nounref'] = counts.get('nounref', 0) + 1
                print(f'nounref   {rel}:{i + 1}: {l.strip()[:90]}')
            if i + 1 < len(zh):
                a, b = l.rstrip(), zh[i + 1].lstrip()
                if a and b and re.match(f'[{HAN}]', a[-1]) and a[-1] == b[0] and a[-1] not in '一二三四五六七八九十':
                    counts['dupbreak'] = counts.get('dupbreak', 0) + 1
                    print(f'dupbreak  {rel}:{i + 1}: …{a[-12:]} | {b[:12]}…')
            if i < len(en):
                ev = re.sub(r'\s+', ' ', MASK.sub(' ', en[i])).strip()
                zv = re.sub(r'\s+', ' ', MASK.sub(' ', l)).strip()
                if len(ev) >= 70 and re.search(f'[{HAN}]', zv) and len(zv) < 0.12 * len(ev):
                    counts['short'] = counts.get('short', 0) + 1
                    print(f'short     {rel}:{i + 1}: {len(zv)}/{len(ev)} {l.strip()[:70]}')
                for m in LATIN.finditer(MASK.sub(' ', l)):
                    if re.search(f'[{HAN}]', l) and m.group(0) not in ('One', 'Math', 'Book', 'Course', 'Creative', 'Commons'):
                        counts['latinname'] = counts.get('latinname', 0) + 1
                        print(f'latinname {rel}:{i + 1}: {m.group(0)}')
        if fix and '\n'.join(out) != orig:
            new = '\n'.join(out)
            en_text = '\n'.join(en)
            for name in ('label_seq', 'env_seq', 'solution_seq', 'math_spans', 'index_count'):
                def norm(v):  # a space inside math (\$0 = \$ -> \$0 =\$) and \\allowbreak are the coordinator's own fixes
                    return [re.sub(r'\s+', '', str(x)) for x in v] if isinstance(v, list) else v
                # against the Chinese before the fix: a translated \emph inside a display (b1 ch. 15) is not the sweep's doing
                if norm(getattr(A, name)(A.unwrap_omterm(orig).replace('\\allowbreak', ''))) != norm(getattr(A, name)(A.unwrap_omterm(new).replace('\\allowbreak', ''))):
                    print(f'REFUSED   {rel}: the fix would change {name}')
                    break
            else:
                zh_p.write_text(new, encoding='utf-8')
    print('SUMMARY', year, counts)


if __name__ == '__main__':
    main()
