import io
from datetime import datetime, timedelta
from typing import List, Dict, Any
import xlsxwriter

from app.core.config import settings
from app.core.yandex_client import YandexDiskClient


async def format_time_delta(time: timedelta) -> str:
    """Форматирует объект timedelta в человекочитаемую строку"""
    days = time.days
    hours = time.seconds // 3600
    minutes = (time.seconds % 3600) // 60

    if days > 0:
        return f'{days} дн. {hours} ч.'
    else:
        return f'{hours} ч. {minutes} мин.'


async def create_simple_report(
    projects: list,
    yandex_client: YandexDiskClient
) -> str:
    now_date_time = datetime.now().strftime(settings.report_format)
    filename = f'Отчет_{now_date_time}'.replace(
        ':', '-').replace(' ', '_').replace('/', '-')

    upload_url, file_path = await yandex_client.create_excel_file(filename)

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('Отчет')

    title_format = workbook.add_format({'bold': True})
    header_format = workbook.add_format({
        'bold': True,
        'bg_color': '#D7E4BC',
        'border': 1
    })
    cell_format = workbook.add_format({'border': 1})

    worksheet.write(0, 0, f'Отчёт от {now_date_time}', title_format)

    headers = ['Название проекта', 'Время сбора', 'Описание']
    worksheet.write_row(1, 0, headers, header_format)

    row = 2
    for project in projects:
        time_diff = project.close_date - project.create_date
        time_str = await format_time_delta(time_diff)

        worksheet.write(row, 0, project.name, cell_format)
        worksheet.write(row, 1, time_str, cell_format)
        worksheet.write(row, 2, project.description, cell_format)
        row += 1

    worksheet.write(row, 0, f'Итого проектов: {len(projects)}', title_format)

    worksheet.set_column(0, 0, 30)
    worksheet.set_column(1, 1, 20)
    worksheet.set_column(2, 2, 50)

    workbook.close()

    output.seek(0)

    await yandex_client.upload_file(upload_url, output.read())

    public_url = await yandex_client.publish_file(file_path)

    return public_url
