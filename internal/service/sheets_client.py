from gspread import Client, Spreadsheet, service_account


class SheetsClient:
    def __init__(self, credentials_path: str):
        self._credentials_path = credentials_path

    def _init_client(self) -> Client:
        return service_account(filename=self._credentials_path)

    def get_table_by_url(self, client: Client, table_link) -> Spreadsheet:
        return client.open_by_url(table_link)

    def get_target(self, table: Spreadsheet, sheet_name: str, cell: str) -> (str | None):
        """
        Удаляет данные из заданного диапазона ячеек на указанном рабочем листе таблицы Google Sheets.

        :param table: Объект таблицы Google Sheets (Spreadsheet).
            :param sheet_name: Название листа в таблице.
            :param start_cell: Начальная ячейка диапазона (например, 'A1').
            :param end_cell: Конечная ячейка диапазона (например, 'B10').
            """
        worksheet = table.worksheet(sheet_name)
        val = worksheet.acell(cell).value
        return val

    def get_data(self, table_link: str, cell: str, sheet_name: str) -> (str | None):
        """Тестирование извлечения данных из таблицы Google Sheets."""
        op = "internal.service.sheets_client.get_data"

        client = self._init_client()
        table = self.get_table_by_url(client=client, table_link=table_link)
        data = self.get_target(table, sheet_name=sheet_name, cell=cell)

        print(op)
        return data
    
# print(123)
# sc = SheetsClient('internal/service/maxtgbottg-7720279c9ab8.json')
# res = sc.get_data(cell="B140", sheet_name="Структура - Парсер",
#                   table_link="https://docs.google.com/spreadsheets/d/19enXGBoOoWkfNakuCnEKLLibuyTbK15dncJpw71PLIE/edit?gid=1169725712#gid=1169725712")
# print(res)
# print(123)