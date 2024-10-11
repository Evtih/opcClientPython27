# chcp 65001
# -*- coding: utf-8 -*-
import OpenOPC
import sys
import codecs
from datetime import datetime

# Устанавливаем кодировку для stdout
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

def formatTimestamp(timestamp):
    """Форматирует временную метку в формате дд.мм.гггг чч:мм:сс."""
    if isinstance(timestamp, str):  # Проверяем, если timestamp - строка
        try:
            dt = datetime.strptime(timestamp, "%m/%d/%y %H:%M:%S")  # Парсим строку в объект datetime
            return dt.strftime("%d.%m.%Y %H:%M:%S")  # Форматируем в нужный вид
        except ValueError:
            return timestamp  # Если не удалось распарсить, возвращаем оригинал
    return timestamp  # Если timestamp не строка, возвращаем оригинал

def main():
    opc = OpenOPC.client()
    
    # Получаем список серверов
    servers = opc.servers('192.168.0.102')
    print(u"Доступные серверы:")
    print(servers)  # Вывод списка серверов на новой строке
    
    opc.connect('OPCServer.WinCC.1', '192.168.0.102')
    
    info = opc.info()
    print(u"\nИнформация о сервере:")
    for item in info:
        # Форматируем время в нужный вид
        if item[0] in ['Start Time', 'Current Time']:
            formattedTime = formatTimestamp(item[1])
            print(u"{:<20}: {}".format(item[0], formattedTime))
        else:
            print(u"{:<20}: {}".format(item[0], item[1]))

    # Читаем значение
    tag = 'FIR1_121_PV_act'
    value, quality, timestamp = opc.read(tag)  # Предполагается, что read возвращает 3 значения
    
    # Форматируем временную метку
    formattedTimestamp = formatTimestamp(timestamp)

    # Вывод результата
    print(u"\nТег                  | Значение | Качество | Временная метка")
    print(u"----------------------------------------------------------------")
    print(u"{:<20} | {:<8} | {:<8} | {}".format(tag, value, quality, formattedTimestamp))
    
    opc.close()

if __name__ == "__main__":
    main()
