#!/usr/bin/env python3
"""Rebuild tabulations from frozen, manually authored decisions using stdlib only.
No literature codes, evidence judgments, or experiment partitions are inferred here.
Usage: python build_results.py
"""
from pathlib import Path
import csv, json, collections, hashlib
BASE=Path(__file__).resolve().parent
def read(name):return json.loads((BASE/name).read_text())
def write_csv(name,rows,fields=None):
    if fields is None: fields=list(rows[0]) if rows else []
    with (BASE/name).open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
def tokens(value):return {s.strip() for s in value.split(';') if s.strip() not in {'none found','UNRESOLVED',''}}
def content(r):
    m,a,e=r['modality'],r['affective_status'],r['effector_type']
    if m=='not applicable':return 'state (no content)'
    if 'UNRESOLVED' in (m,a):return 'UNRESOLVED'
    if m=='motor':return 'motor-conflict ('+e+')' if e in {'skeletal','autonomic'} else 'UNRESOLVED'
    if a=='interoceptive' or m=='interoceptive':return 'interoceptive'
    if a=='valenced':return 'valenced'
    if m=='visual' and a=='neutral':return 'neutral-visual'
    if m in {'auditory','tactile'} and a=='neutral':return 'neutral-nonvisual'
    return 'UNRESOLVED'
def main():
    s1=read('decisions_s1.json');s2=read('decisions_s2.json');parts=read('publication_partitions.json')
    s1fields=list(s1[0]);s2fields=[k for k in s2[0] if k!='samples_detail']
    write_csv('S1_coder2_AI.csv',s1,s1fields);write_csv('S2_coder2_AI.csv',s2,s2fields)
    write_csv('S2_publication_partition.csv',parts)
    write_csv('S2_samples_detail.csv',[dict(publication_id=r['publication_id'],experiment_id=r['experiment_id'],**s) for r in s2 for s in r['samples_detail']])
    codes=['EXPLICIT','INTERPRETED','NOT_LOCATED','NOT_APPLICABLE','UNRESOLVED']
    domains=list(dict.fromkeys(r['domain_id'] for r in s1)); accounts=list(dict.fromkeys(r['theory_id'] for r in s1))
    bydomain=[];bytheory=[]
    for field,values,target in [('domain_id',domains,bydomain),('theory_id',accounts,bytheory)]:
        for v in values:
            rr=[r for r in s1 if r[field]==v];cc=collections.Counter(r['code'] for r in rr)
            target.append({field:v,**{c:cc[c] for c in codes},'explicit_stated_null':sum(r['code']=='EXPLICIT' and r['polarity']=='stated_null' for r in rr),'n':len(rr)})
    write_csv('S1_counts_by_domain.csv',bydomain);write_csv('S1_counts_by_theory.csv',bytheory)
    flags=[dict(table='S1',key=r['theory_id']+':'+r['domain_id'],reason=r['adjudication_reason']) for r in s1 if r['flag_for_adjudication']]
    for r in s2:
        if r['flag_for_adjudication']:
            reason=' | '.join(x for x in [r['adjudication_reason'],r['contested_reason'],r['partition_note'] if r['partition_status']!='verified-main-text' else ''] if x)
            flags.append(dict(table='S2',key=r['experiment_id'],reason=reason))
    write_csv('adjudication_notes.csv',flags)
    derived=[]
    for r in s2:
        author=tokens(r['theory_attribution_by_authors']);later=tokens(r['theory_attribution_later'])
        cc=content(r);known=bool(author or later)
        strict=bool(author or (later and 'CONTEXT_NAMED' in r['later_attribution_evidence']))
        derived.append(dict(experiment_id=r['experiment_id'],publication_id=r['publication_id'],content_class_7way=cc,content_class_5way='motor-conflict' if cc.startswith('motor-conflict') else cc,theory_addressed_confirmed=known,theory_addressed_strict_confirmed=strict,by_authors_unresolved=r['theory_attribution_by_authors']=='UNRESOLVED',contested_inclusion=r['contested_inclusion'],evidence_status=r['evidence_status'],partition_status=r['partition_status']))
    write_csv('S2_derived.csv',derived)
    scenarios={
      'all_retained_rows':lambda r:True,
      'exclude_contested':lambda r:not r['contested_inclusion'],
      'theory_addressed_confirmed':lambda r:r['theory_addressed_confirmed'],
      'theory_addressed_confirmed_exclude_contested':lambda r:r['theory_addressed_confirmed'] and not r['contested_inclusion'],
      'strict_attribution_confirmed':lambda r:r['theory_addressed_strict_confirmed'],
      'strict_attribution_exclude_contested':lambda r:r['theory_addressed_strict_confirmed'] and not r['contested_inclusion'],
      'full_text_only':lambda r:r['evidence_status']=='full-text',
      'verified_partition_only':lambda r:r['partition_status']=='verified-main-text',
    }
    cats=['neutral-visual','neutral-nonvisual','motor-conflict (skeletal)','motor-conflict (autonomic)','valenced','interoceptive','state (no content)','UNRESOLVED']
    sensitivity=[]
    for name,pred in scenarios.items():
        rr=[r for r in derived if pred(r)]; cc=collections.Counter(r['content_class_7way'] for r in rr)
        sensitivity.append(dict(scenario=name,n_rows=len(rr),n_publications=len({r['publication_id'] for r in rr}),content_denominator=sum(cc[x] for x in cats if x not in {'state (no content)','UNRESOLVED'}),**{c:cc[c] for c in cats},by_authors_unresolved=sum(r['by_authors_unresolved'] for r in rr)))
    write_csv('s2_sensitivity.csv',sensitivity)
    summary={
      'coder':'independent AI coding, not an independent human rater',
      'codebook_hash':hashlib.sha256((BASE/'protocol/codebook_v2.md').read_bytes().rsplit(b'\n',2)[0]+b'\n').hexdigest(),
      'S1':{'n':len(s1),'codes':dict(collections.Counter(r['code'] for r in s1)),'provisional':sum(r['provisional'] for r in s1),'flagged':sum(r['flag_for_adjudication'] for r in s1),'explicit_stated_null':sum(r['code']=='EXPLICIT' and r['polarity']=='stated_null' for r in s1)},
      'S2':{'publications_audited':len(parts),'retained_rows':len(s2),'publications_with_rows':len({r['publication_id'] for r in s2}),'excluded_new_experiments_zero':['P35'],'abstract_only_rows':sum(r['evidence_status']=='abstract-only' for r in s2),'contested_rows':sum(r['contested_inclusion'] for r in s2),'ancillary_rows':sum(r['ancillary_experiment'] for r in s2),'partition_uncertain_rows':sum(r['partition_status']!='verified-main-text' for r in s2)},
      'intercoder_agreement':'NOT COMPUTED: coder 1 was not accessed',
      'column_typology':'NOT COMPUTED: S4 and pair judgments were not supplied',
      'sensitivity':sensitivity}
    (BASE/'results_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    matrix=[]
    short={'EXPLICIT':'E','INTERPRETED':'I','NOT_LOCATED':'N','NOT_APPLICABLE':'A','UNRESOLVED':'U'}
    for account in accounts:
        rr={r['domain_id']:r for r in s1 if r['theory_id']==account}
        matrix.append('| '+account+' | '+' | '.join(short[rr[d]['code']]+('0' if rr[d]['polarity']=='stated_null' else '') for d in domains)+' |')
    tab='| Теория | '+' | '.join(domains)+' |\n|---|'+'---|'*len(domains)+'\n'+'\n'.join(matrix)
    counts='\n'.join(f"| {c} | {summary['S1']['codes'].get(c,0)} |" for c in codes)
    sens='\n'.join(f"| {r['scenario']} | {r['n_rows']} | {r['content_denominator']} |" for r in sensitivity)
    report=f'''# Независимое кодирование пакета v3.4 — результаты ИИ

Дата завершения: 25 сентября 2026. Объект: кодбук v2.4, 12 теорий × 10 доменов, исходный список из 32 публикаций.

## Что выполнено

Заполнены **120 ячеек S1** и **54 строки S2**, соответствующие 31 публикации. Все 32 исходные публикации представлены в журнале разделения на эксперименты. P35 сохранена там с нулём новых экспериментов, поскольку это повторный анализ данных. Число 54 — результат текущего разделения, а не окончательно установленное число независимых экспериментов: часть единиц требует уточнения.

Это собственная разметка ИИ, выполненная по предоставленному пакету и опубликованным источникам. Она **не является разметкой независимого человека**. Файлы решений первого кодера, заполненные дополнения, рукопись с результатами и ответы рецензентам для этой работы не открывались. Сессия не была изолированной от прежнего контекста задачи, поэтому я не заявляю экспериментально обеспечленную слепоту. Описанные в пакете 70 частично и 50 полностью слепых ячеек относятся к указанному там человеку и не удостоверяют слепоту этой ИИ-разметки.

## S1: собственные решения

| Код | Ячеек |
|---|---:|
{counts}

В 3 ячейках EXPLICIT зафиксирован stated_null: FM–M8, SIT–M4c и PFT–M4c. Остальные EXPLICIT — положительные утверждения. NOT_LOCATED означает, что утверждение не найдено в указанном исследованном тексте; это не отрицательный результат эксперимента и не доказательство молчания всей теории.

{tab}

E — EXPLICIT; E0 — EXPLICIT stated_null; I — INTERPRETED; N — NOT_LOCATED; A — NOT_APPLICABLE; U — UNRESOLVED. Каждая ячейка имеет отдельное обоснование и ссылку в S1. Матрица показывает мои коды, а не согласие между кодерами.

Основные решения, влияющие на интерпретацию:

- **M5:** утверждения о телесности, гомеостазе или сердечных ответах не приравнены к прямому предсказанию об измеряемой общей корково-автономной согласованности. Прямых EXPLICIT по M5 в этой разметке нет.
- **M7:** сенсорная точность и само наличие высшего порядка не приравнены к точности метарепрезентации. Для AST, GNWT и HOSS использован ограниченный вывод из механизма; для PP и HOT подходящее прямое утверждение не найдено.
- **M4c:** функциональное исключение чисто автономного конфликта у SIT/PFT не означает, что телесные состояния нельзя чувствовать.
- **IIT–M3:** необязательность аффекта не превращена в утверждение об отсутствии эффекта валентности; оставлено UNRESOLVED.
- **PFT–M8:** ограничение нейронной реализации в аннотации ответа сопоставлено с нейронными утверждениями раннего текста; оставлено UNRESOLVED. Эта ячейка provisional, поскольку часть решающего основания доступна только в аннотации.

Всего provisional-ячеек S1: {summary['S1']['provisional']}; отмечено для обсуждения: {summary['S1']['flagged']}. Формальный provisional не отражает все ограничения: неполнота корпуса и спорность вывода записаны отдельно.

## S2: разделение и знаменатели

Аннотациями ограничены {summary['S2']['abstract_only_rows']} строк. В них одна строка публикации не означает доказанный единственный эксперимент. Контрольные и вспомогательные выборки учитываются отдельно; техники регистрации и условия одной выборки автоматически не размножают строки.

Пограничных строк: {summary['S2']['contested_rows']}. Они сохранены с причинами, а не молча исключены. Состояние без конкретного содержания (P36) и неразрешённая модальность не входят в знаменатель содержания. Показатели метакогниции не считаются автоматически показателями доступа.

| Сценарий | Строк | Знаменатель содержания |
|---|---:|---:|
{sens}

Полная разбивка на классы находится в `s2_sensitivity.csv`. `theory_addressed_confirmed` означает подтверждённую атрибуцию в прочитанном корпусе. Это не утверждение о полноте всех возможных поздних цитирований. `UNRESOLVED` не переименовывается в отсутствие атрибуции; его частота показана отдельно. Собственные предположения кодера о теории не добавлялись в основной знаменатель.

Ключевые случаи для согласования:

- P21: в доступной авторской версии Wilterson et al. есть Methods/Results для экспериментов 1–6; аннотация сформулирована как шесть плюс два. Сохранены шесть подтверждённых единиц, финальная версия требует сверки.
- P13: два основных визуальных дизайна и дополнительное слуховое наблюдение. Происхождение последнего требует уточнения, чтобы не посчитать опубликованные данные повторно.
- P20: два основных опыта, отдельно описанное первоначальное низкоконтрастное исследование; повторный анализ fMRI не создаёт новую строку. Для первоначального исследования не установлена численность.
- P22: три названных исследования плюс отдельные восемь судей сложности движений. Зрачковый рефлекторный контроль не содержит явного намерения управлять автономным эффектором; его модальность оставлена UNRESOLVED, а не автоматически отнесена к интероцепции.
- P35: повторный анализ вынесен из строк экспериментов, но остаётся в таблице публикаций для сопоставления разбиений.
- P01: атрибуция включает GNWT/IIT как основные проверяемые теории и HOT/RPT как прямо названные авторами следствия, что допускает правило I2.

## Источники, воспроизводимость и ограничения

Проверены DOI всех 75 уникальных источников через Crossref. Доступны 40 локально полученных полных текстов и одна полная авторская версия через веб-просмотр; ещё 31 источник доступен на уровне аннотации, три книжных/главных источника не прочитаны. Это доступность, а не заявление о сплошном прочтении каждой страницы: работа включала релевантные разделы, методы, результаты и поиск утверждений. Дополнительные материалы доступны не для каждой публикации. Сведения об уровне доступа и адресах находятся в `source_audit.csv`.

Кодбук сохранён без изменений; его штатный SHA-256: `6b2e7ad9df83b763c215eb79714fde83cf2a620eff8a9e3e95e80d3980ab8dcc`. В §4 есть противоречие относительно заполнения поздней атрибуции вторым кодером. Я выполнил повторённое конкретное требование README, §1 и основной инструкции §4: заполнил позднюю атрибуцию отдельно. Правила кодбука не редактировались.

Исходные исследовательские решения находятся в `decisions_s1.json` и `decisions_s2.json`. `build_results.py` создаёт CSV и сводки из этих решений; он не определяет смысл теорий автоматически. `validate_results.py` проверяет целостность сетки, допустимые значения, ссылки, разделение публикаций и знаменатели. Запуск: `python build_results.py`, затем `python validate_results.py`. Библиотеки вне стандартной поставки Python для этих двух скриптов не нужны.

Отдельные интервалы на каждую теорию не измерялись: чтение S1/S2 было перемежающимся. В журнале сохранены реальные доступные отметки этапов и пустые интервалы с объяснением для отдельных блоков. Человеческая трудоёмкость 6–10 и 2–3 часа не приписывается ИИ, ретроспективные минуты не придуманы.

κ, процент межкодерного согласия и итоговые классы «contested» по столбцам не вычислялись: нет независимого файла первого кодера и второго этапа S4/парных суждений. Опциональная S3 не заполнялась. Пакет пригоден для проверки и последующего сопоставления, но имеющиеся пробелы не следует скрывать при описании метода в статье.
'''
    (BASE/'RESULTS_RU.md').write_text(report,encoding='utf-8')
    print(json.dumps({'S1':summary['S1'],'S2':summary['S2'],'sensitivity':sensitivity},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
