import schedule, time, json, os, dotenv
from whatsapp_api_client_python import API


dotenv.load_dotenv()


greenAPI = API.GreenApi(os.getenv("ID_INSTANCE"), os.getenv("API_TOKEN_INSTANCE"))


class Group:

    def __init__(self, name, groupID, time, place, placeLink):
        self.name = name
        self.groupID = groupID
        self.time = time
        self.place = place
        self.placeLink = placeLink

    def sendMessage(self, message):
        return greenAPI.sending.sendMessage(self.groupID, message)

    def notify(self):
        message = f"""🚀 Вас приветствует Клиент-сервис Роботек!

                    Напоминаем Вам, что завтра пройдет занятие по робототехнике 🥳
                    Расписание: { self.time }
                    Адрес: { self.place }
                    { self.placeLink }

                    Мы готовимся к интересному и продуктивному уроку!
                    ⏰ Ценим ваше и наше время: начнем точно по расписанию.

                    🎒 Что взять с собой?
                    - Сменную обувь
                    - Перекус
                    - Бутылочку воды

                    Спасибо, что Вы с нами! 🚀🌟"""
        self.sendMessage(message)
        print(f"Group {self.name} was been successfully notified!")


def sendMessageToGroup(groupID, message):
    return greenAPI.sending.sendMessage(groupID, message)


def getGroupsList():
    groups = list()
    with open("groups.json", encoding="utf-8") as groupsJSON:
        for group in json.loads(groupsJSON.read()):
            groups.append(
                Group(
                    group["name"],
                    group["groupID"],
                    group["time"],
                    group["place"],
                    group["placeLink"],
                )
            )

    return groups


def sendReminders():
    groups = getGroupsList()
    for group in groups:
        group.notify()


schedule.every().friday.at("11:00").do(sendReminders)

while True:
    schedule.run_pending()
    time.sleep(1)
