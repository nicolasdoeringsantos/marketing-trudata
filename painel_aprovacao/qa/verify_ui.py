"""Regressões do estúdio editorial. Requer Playwright, Chrome e Edge instalados.
Execute com o servidor em localhost:8080: python painel_aprovacao/qa/verify_ui.py
API de status e WhatsApp são interceptados; nenhuma publicação é enviada.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
import csv
import io
import json
import zipfile
import xml.etree.ElementTree as ET

OUT = Path(__file__).parent
BASE = 'http://127.0.0.1:8080'


def run():
    report = []
    with sync_playwright() as pw:
        for channel in ['chrome', 'msedge']:
            browser = pw.chromium.launch(channel=channel, headless=True)
            context = browser.new_context(viewport={'width': 1366, 'height': 1000},
                                          permissions=['clipboard-read', 'clipboard-write'])
            shared = {}
            def api(route):
                if route.request.method == 'POST':
                    item = route.request.post_data_json
                    shared[item['id']] = item['status']
                    route.fulfill(json={'sucesso': True})
                else:
                    route.fulfill(json=shared)
            context.route('**/api/status', api)
            context.route('https://wa.me/**', lambda route: route.fulfill(body='WhatsApp mock'))
            page = context.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(BASE + '/index.html')
            expect(page.locator('.post')).to_have_count(22)
            expect(page.locator('#storage-note')).to_contain_text('compartilhados')
            for name in ['index', 'calendario']:
                page.goto(BASE + '/' + name + '.html')
                page.evaluate('document.fonts.ready')
                for width in [1366, 1920, 768]:
                    page.set_viewport_size({'width': width, 'height': 1000})
                    page.screenshot(animations="disabled", path=str(OUT / f'{name}-{channel}-{width}.png'))
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                    assert not page.locator('body').inner_text().count('undefined')
                    assert '[object Object]' not in page.locator('body').inner_text()
                page.set_viewport_size({'width': 1366, 'height': 1000})
            page.goto(BASE + '/index.html')
            page.locator('[data-status="aprovado"]').first.click()
            expect(page.locator('#toast')).to_have_text('Aprovado')
            expect(page.locator('#stats .stat').nth(1).locator('strong')).to_have_text('1')
            expect(page.locator('.post').first.locator('.badge')).to_have_text('Aprovado')
            assert shared['post-contadores-real'] == 'aprovado'
            page.reload()
            expect(page.locator('.post').first.locator('.badge')).to_have_text('Aprovado')
            page.locator('[data-filter="aprovado"]').click()
            expect(page.locator('.post')).to_have_count(1)
            page.locator('[data-status="publicado"]').click()
            expect(page.locator('.empty')).to_be_visible()
            page.locator('[data-reset]').click()
            page.locator('[data-status="ajuste"]').first.click()
            expect(page.locator('.post').first.locator('.badge')).to_have_text('Em ajuste')
            page.locator('#search').fill('texto-que-nao-existe')
            expect(page.locator('.empty')).to_be_visible()
            page.locator('[data-reset]').click()
            page.locator('#channel').select_option('Instagram')
            expect(page.locator('.post')).to_have_count(18)
            trigger = page.locator('.image-button').first
            trigger.focus()
            page.keyboard.press('Enter')
            expect(page.locator('dialog')).to_be_visible()
            for _ in range(15):
                page.keyboard.press('Tab')
                assert page.evaluate('document.activeElement.closest("dialog") !== null')
            page.locator('[data-copy-post]').click()
            expect(page.locator('#toast')).to_have_text('Copiado')
            assert len(page.evaluate('navigator.clipboard.readText()')) > 30
            page.keyboard.press('Escape')
            expect(trigger).to_be_focused()
            page.goto(BASE + '/calendario.html')
            total = 0
            for month in ['09', '10', '11', '12']:
                page.locator('#month').select_option(month)
                total += page.locator('.day[data-day]').count()
                assert page.locator('#calendar-grid > *').count() % 7 == 0
            assert total == 108
            page.locator('#month').select_option('09')
            page.locator('#segment').select_option('Farmácia')
            assert 0 < page.locator('.day[data-day]').count() < 16
            page.locator('#search').fill('inexistente-xyz')
            expect(page.locator('#calendar-empty')).to_be_visible()
            expect(page.locator('[data-export="csv"]')).to_be_disabled()
            page.locator('#clear-filters').click()
            expect(page.locator('.day[data-day]')).to_have_count(16)
            page.locator('#pillar').select_option('Fiscal e contabilidade')
            assert 0 < page.locator('.day[data-day]').count() < 16
            page.locator('#clear-filters').click()
            page.locator('[data-day="2"]').click()
            expect(page.locator('.story')).to_have_count(3)
            page.locator('[data-poll]').first.click()
            expect(page.locator('[data-poll]').first).to_have_attribute('aria-pressed', 'true')
            page.locator('#day-status').select_option('aprovado')
            expect(page.locator('#progress-label')).to_contain_text('1 de 108')
            with page.expect_download() as downloaded:
                page.locator('[data-package]').click()
            text = Path(downloaded.value.path()).read_text(encoding='utf-8')
            assert all(s in text for s in ['Tela 1', 'Tela 2', 'Tela 3', '17/09/2026'])
            with page.expect_popup() as popup:
                page.locator('[data-whatsapp]').click()
            assert popup.value.url.startswith('https://wa.me/')
            popup.value.close()
            page.keyboard.press('Escape')
            page.reload()
            expect(page.locator('#progress-label')).to_contain_text('1 de 108')
            page.locator('[data-day="7"]').click()
            expect(page.locator('.feed-details')).to_be_visible()
            page.locator('[data-copy-feed]').click()
            expect(page.locator('#toast')).to_have_text('Copiado')
            page.screenshot(animations="disabled", path=str(OUT / f'detalhe-{channel}.png'))
            page.keyboard.press('Escape')
            for filetype in ['csv', 'xlsx', 'notion', 'md']:
                with page.expect_download() as downloaded:
                    page.locator('[data-export="'+filetype+'"]').click()
                data = Path(downloaded.value.path()).read_bytes()
                if filetype == 'xlsx':
                    with zipfile.ZipFile(io.BytesIO(data)) as z:
                        assert z.testzip() is None
                        sheet = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
                        assert len(sheet.findall('.//{*}row')) == 17
                        assert len(sheet.findall('.//{*}row')[0]) == 13
                elif filetype in ['csv', 'notion']:
                    rows = list(csv.reader(io.StringIO(data.decode('utf-8-sig'))))
                    assert len(rows) == 17 and len(rows[0]) == 13
                else:
                    assert data.decode('utf-8').count('# ') == 16
            page.locator('#preview-feed').click()
            expect(page.locator('.feed-tile')).to_have_count(9)
            page.locator('.feed-mosaic img').evaluate_all('(images) => Promise.all(images.map(image => image.decode()))')
            page.screenshot(animations="disabled", path=str(OUT / f'feed-{channel}.png'))
            tile = page.locator('button.feed-tile').first
            box = tile.bounding_box()
            assert abs(box['width']-box['height']) < 1
            tile.click()
            expect(page.locator('.story')).to_have_count(3)
            page.keyboard.press('Escape')
            assert not errors, errors
            report.append({'browser': channel, 'widths': [768,1366,1920], 'posts':22,
                           'days':total,'exports':['csv','xlsx','notion','md','txt'],
                           'page_errors':errors,'result':'passed'})
            # Falha de armazenamento deve informar o problema sem mudar o status.
            page.goto(BASE + '/index.html')
            page.evaluate("() => { Storage.prototype.setItem = () => { throw new Error('QuotaExceededError'); }; }")
            before = page.locator('.post').nth(1).locator('.badge').inner_text()
            page.locator('.post').nth(1).locator('[data-status="aprovado"]').click()
            expect(page.locator('#error')).to_contain_text('não conseguiu salvar')
            assert page.locator('.post').nth(1).locator('.badge').inner_text() == before
            browser.close()
    (OUT/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    run()
