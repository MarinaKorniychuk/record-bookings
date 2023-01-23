def update_google_spreadsheets(expenses_data):
    pass

# gc = pygsheets.authorize('secrets/desktop_client_secret.json')
# sh = gc.open('Расходы (все объекты) COPY')
# wk = sg.worksheet('title', 'Sheet1')
# wk.get_as_df()

# d = wk.get_as_df(has_header=False, start='A3', empty_value=None)
# # column_names = ['Отметка времени', 'Имя	Объекты (таблица)', 'Категория', 'Объект (Аренда)', 'Объект (ЖКХ/Интернет)', 'Сотрудник', 'Комментарий', 'Сумма', 'Загрузка чека', 'Внесено в таблицу']
# column_names = ['datetime', 'name', 'sheet', 'category', 'apartment/rent', 'apartment/internet', 'employee', 'comment', 'amount', 'receipt', 'recorded']
# d = d.set_axis(column_names, axis=1, copy=False)

# d[d.recorded.notnull()]
# d['recorded'] = d['recorded'].fillna(0)
# not_recordered = d[d.recorded.isin([0.0])]
# d[d.recorded == 0.0]

# int(an.value or 0) + 4
# cell.note = note
# empty note in None