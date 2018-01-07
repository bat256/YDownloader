import pytube,os,platform,random

class YDownloader():
    def __init__(self):
        self.lastP = 0

    def showProgressBar(self, stream, chunk, file_handle, bytes_remaining):
        nowP = int(100 - 100 * bytes_remaining / self.fileSize)
        if nowP != self.lastP:
            print(str(nowP) + "%")
            self.lastP = nowP
        
    def drawLogo(self):
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
        print("""
        ___                          _                    _             
/\_/\   /   \  ___  __      __ _ __  | |  ___    __ _   __| |  ___  _ __ 
\_ _/  / /\ / / _ \ \ \ /\ / /| '_ \ | | / _ \  / _` | / _` | / _ \| '__|
 / \  / /_// | (_) | \ V  V / | | | || || (_) || (_| || (_| ||  __/| |   
 \_/ /___,'   \___/   \_/\_/  |_| |_||_| \___/  \__,_| \__,_| \___||_| 
        """)


    def run(self):
        self.drawLogo()
        while True:
            youtubeLink = input("Введите ссылку для загрузки: ")
            try:
                video = pytube.YouTube(youtubeLink)
            except pytube.exceptions.RegexMatchError:
                print("")
                print("Ошибка: Вы ввели неправильную ссылку")
                input("")
                self.drawLogo()
            else:
                break

        video.register_on_progress_callback(self.showProgressBar)

        while True:
            self.drawLogo()
            print("Выбор потока: " + video.title)
            print("--------------------------------------------")
            iteratorVar = 0
            for stream in video.streams.all():
                iteratorVar = iteratorVar + 1
                print(str(iteratorVar) + ": " + str(stream))
            streamId = input("Выберите формат для загрузки: ")
            try:
                int(streamId)
            except ValueError:
                print("")
                print("Ошибка: Это не ID")
                input("")
            except IndexError:
                print("")
                print("Ошибка: ID вышел за 64 битное число")
                input("")
            else:
                break

        dStream = video.streams.all()[int(streamId) - 1]
        fileName = dStream.default_filename[0:dStream.default_filename.find(".")]
        fileExtension = dStream.default_filename[dStream.default_filename.find(".")::]
        iteratorVar = 0

        if os.path.exists(fileName + fileExtension) == True:
            fileName = fileName + " "
            iteratorVar = iteratorVar + 1
            tempfileName = fileName + str(iteratorVar)
            while True:
                if os.path.exists(tempfileName + fileExtension) == True:
                    iteratorVar = iteratorVar + 1
                    tempfileName = fileName + str(iteratorVar)
                else:
                    fileName = tempfileName
                    break


        self.drawLogo()
        print("Загрузка видео: " + video.title)
        self.fileSize = dStream.filesize
        dStream.download(filename=fileName)
        #self.drawLogo()
        print("Загрузка завершена!")
        input("")


try:
    YDownloader().run()
except Exception as e:
    print("")
    print("Произошла ошибка: " + str(e))
    input("")
    quit(1)
else:
    quit(0)