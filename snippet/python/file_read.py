import logging

def txtRead(filePath, encodeType = 'utf-8'):
    listLine = []
    try:
        file = open(filePath, 'r', encoding= encodeType)

        while True:
            line = file.readline()
            if not line:
                break

            listLine.append(line)

        file.close()

    except Exception as e:
        logging.info(str(e))

    finally:
        return listLine