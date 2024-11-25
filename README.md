# Конфигурационное управление

# Домашнее задание №4

**Вариант №2**

Разработать ассемблер и интерпретатор для учебной виртуальной машины (УВМ). Система команд УВМ представлена далее.

Для ассемблера необходимо разработать читаемое представление команд УВМ. Ассемблер принимает на вход файл с текстом исходной программы, путь к которой задается из командной строки.

Результатом работы ассемблера является бинарный файл в виде последовательности байт, путь к которому задается из командной строки.

Дополнительный ключ командной строки задает путь к файлу-логу, в котором хранятся ассемблированные инструкции в духе списков “ключ=значение”, как в приведенных далее тестах.

Интерпретатор принимает на вход бинарный файл, выполняет команды УВМ и сохраняет в файле-результате значения из диапазона памяти УВМ. Диапазон также указывается из командной строки.

Форматом для файла-лога и файла-результата является json.

Необходимо реализовать приведенные тесты для всех команд, а также написать и отладить тестовую программу.

**Загрузка константы**

| A | B | C |
|---|---|---|
| Биты 0—3 | Биты 4—30 | Биты 31—37 |
| 13 | Константа | Адрес |

Размер команды: 6 байт. Операнд: поле B. Результат: регистр по адресу, которым является поле C.

Тест (A=13, B=419, C=6):

0x3D, 0x1A, 0x00, 0x00, 0x03, 0x00


**Чтение значения из памяти**

| A | B | C |
|---|---|---|
| Биты 0—3 | Биты 4—10 | Биты 11—42 |
| 4 | Адрес | Адрес |

Размер команды: 6 байт. Операнд: значение в памяти по адресу, которым является поле C. Результат: регистр по адресу, которым является поле B.

Тест (A=4, B=88, C=763):

0x84, 0xDD, 0x17, 0x00, 0x00, 0x00


**Запись значения в память**

| A | B | C |
|---|---|---|
| Биты 0—3 | Биты 4—35 | Биты 36-42 |
| 2 | Адрес | Адрес |

Размер команды: 6 байт. Операнд: регистр по адресу, которым является поле C. Результат: значение в памяти по адресу, которым является поле B.

Тест (A=2, B=89, C=52):

0x92, 0x05, 0x00, 0x00, 0x40, 0x03


**Унарная операция: sqrt()**

| A | B | C |
|---|---|---|
| Биты 0—3 | Биты 4—10 | Биты 11—17 |
| 9 | Адрес | Адрес |

Размер команды: 6 байт. Операнд: регистр по адресу, которым является поле C. Результат: регистр по адресу, которым является поле B.

Тест (A=9, B=27, C=84):

0xB9, 0xA1, 0x02, 0x00, 0x00, 0x00

Тестовая программа: Выполнить поэлементно операцию sqrt() над вектором длины 7. Результат
записать в исходный вектор.
