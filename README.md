API_hh
Три запускаемых файла с сохранением результатов в файлы: download_base.py - только скачивает вакансии (сокращенную и полную), сохраняет их в файлы not_full_vacancy.json и full_vacancy.json; test_json_file.py тестирует сохраненные download_base.py файлы и создает отчет в терминале; analysis_hh.py - выполнение домашнего задания, результат выводит в терминал и сохраняет в файл info_hh.txt, вакансии в формате json сохраняет в 2 файла, на примере download_base.py, в формате pandas в файл database_hh.csv.
Добавлет Бот Телеграм CurrControlBot
Стандартно запускается командой /start, есть описание /help. Эти команды можно запустить из меню. В остальном бот работает от голосовых команд. Его возможности на данное время: На фразу Включить/включи или засеки или поставь/поставить тайимер на 5 (7,10,20 и тд) секнд (минут) - бот возвращает сообщение, что засекает соответствующее время и через это время пришлет сообщение что пришло Время. На фразу сохранить/сохрани/записать/запиши/заметка и после этого слова надикторвать что-то боту, он пришлет сообщение с надиктовонным текстом. На фразу покажи/выведи/показать... время/часы бот выведет текущую дату и время. На фразу показать курс валют - получите ообщение с курсом доллора США и евро на сегодня. Курс валют получаем с cbr.ru
