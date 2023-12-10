
from config import TOKEN
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.update import Update
from typing import List

# Define the questions and answers
questions = [
    "I __ to bed before 1 am.",
    "She __ a husband. She is divorced.",
    "__ is it? - It's almost 5 pm.",
    "What's this? It's _ umbrella.",
    "Are you _ holiday here?",
    "_ you help me, please?",
    "Non mi conosci?",
    "He works very __?",
    "I hardly ever go dancing __.",
    "Does your mom have _ free time?",
    "I'm sorry, I didn't _ to hurt you.",
    "She spilled the tea to everyone. She knew it was a secret.\n\nNel momento in cui unisci queste due frasi in una, quale congiunzione utilizzi?",
    "I __ my friends tomorrow.",
    "I'm afraid I can't make it tonight because I'll be busy helping my family. If I _ so busy, I _.",
    "This movie is __ funny! I've watched it 5 times!",
    "She phoned to say they'd arrived safely, so that really put my mind _.",
    "We _ travel a lot when we were younger.",
    "We arranged to meet at 9.30, but he never _.",
    "He turned _ down.",
    "Hurry up! The movie _ by the time we get to the cinema.",
    "I didn’t like the album at first, but now it is really _ me.",
    "I don’t have a degree, so I didn’t get the job",
    "John was a very experienced manager, but he _ with time-keeping.",
    "- I wish we __ about it earlier.\n- Well, we didn't.",
    "_  the people I spoke to knew them."   
]

options = [
    ["don't never go","never go","am never going","ever go"],
    ["don't have","doesn't has","doesn't have","hasn't"],
    ["When","At what time","What time","Which time"],
    ["a","the","an","-"],
    ["at","on","in","during"],
    ["Are","May","Do","Can"],
    ["Have you known me?","Haven't you known me?","Do you know me?","Don't you know me?"],
    ["harder","hardly","difficult","hard"],
    ["nowadays","lately","today","soon"],
    ["the","many","much","a"],
    ["mean","hope","suppose","think"],
    ["Because","Once","While","Although"],
    ["am going to see","see","will see","am seeing"],
    ["wouldn't have been, had come","were not, would come","am not, would come","hadn't been, would have come"],
    ["such","a lot of","so","too"],
    ["down","to sleep","away","at rest"],
    ["didn't use to","didn't used to","didn't get used to","weren't used to"],
    ["made up","showed up","ended up","gave up"],
    ["the chance","the music","the job","the hat"],
    ["will probably have started","will probably be starting","has probably started","is probably starting"],
    ["breaking through","getting to","growing on","catching up"],
    ["If I have a degree, I would have gotten that job.","If I’d had a degree, I would get that job","If I had a degree, I would have gotten that job.","If I'd had a degree, I would have gotten that job."],
    ["collided","struggled","interfered","clash"],
    ["could think","thought","had thought","have thought"],
    ["None of","No one of","No of","Not a single of"]
]

answers = ["never go","doesn't have","What time","an","on","Can","Do you know me?","hard","lately","much","mean","Although","am going to see","were not, would come","so","at rest","didn't use to","showed up","the job","will probably have started","growing on","If I'd had a degree, I would have gotten that job.","struggled","had thought","None of"]

# Define the global variables
current_question = 0
score = 0

# Define the start function
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("Let's go 🚀", callback_data='1')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Hey there! Ready to find out how good your English is? Scegli le risposte che pensi siano giusti.\n\nQuesto quiz richiederà solo 5 minuti, clicca su «let’s go» per iniziare", reply_markup=reply_markup)

# Define the function to send a question
def send_question(update: Update, context: CallbackContext, question_num: int) -> None:
    global current_question
    current_question = question_num
    options_markup = create_options_markup(options[question_num - 1])
    if update.message:
        update.message.reply_text(f"Question {question_num}. {questions[question_num - 1]}", reply_markup=options_markup)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f" {question_num}. {questions[question_num - 1]}", reply_markup=options_markup)


# Define the function to create options markup
def create_options_markup(options_list: List[str]) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(option, callback_data=option)] for option in options_list]
    return InlineKeyboardMarkup(keyboard)

# Define the button handler function
def button(update: Update, context: CallbackContext) -> None:
    global score
    query = update.callback_query
    user_answer = query.data
    if user_answer == answers[current_question - 1]:
        score += 1
    if current_question < 25:
        send_question(update, context, current_question + 1)
    else:
        if score >= 0 and score <= 5:
            message = "Сongrats! 🎉 The test is over!\nYour level is - A1\n\nDalle tue risposte si nota che hai un grande potenziale! Per percorrere con sicurezza la strada verso il tuo inglese ideale, è importante costruire una solida base linguistica."
        elif score >= 6 and score <= 12:
            message = "Сongrats! 🎉 The test is over!\nYour level is - A2\n\nDai risultati, sembra che tu abbia già raggiunto il livello B1, ma non hai praticato la lingua per un pò. Non preoccuparti, l'inglese si può ricordare rapidamente!"
        elif score >= 13 and score <= 19:
            message = "Сongrats! 🎉 The test is over!\nYour level is - В1\n\nHai già molte conoscenze e ci sono ancora tanti argomenti interessanti da esplorare!\nPer progredire rapidamente e con fiducia nell'inglese, è importante sempre migliorare e praticare!"
        elif score >= 20 and score <= 25:
            message = "Сongrats! 🎉 The test is over!\nYour level is - В2\n\nRisultato eccellente! Hai già molte conoscenze, ma il plateau del livello intermedio può togliere tutta la motivazione allo studio, e quel desiderato C1 sembra sfuggente, vero?"
        
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

        if score >= 0 and score <= 25:
            second_message = "Ti regaliamo una LEZIONE GRATUITA con il nostro metodologo, durante la quale potrai:\n\n- Valutare il tuo livello di conoscenza della lingua e ottenere un piano individuale per migliorarlo 📈\n- Apprendere la tecnica per memorizzare le parole senza doverle imparare a memoria 🧠\n- Scoprire i corsi disponibili e scegliere quello che fa per te 🔥\n\nOccupati subito del tuo posto!👇🏼"
            button = InlineKeyboardButton("voglio la lezione gratuita!", url="https://calendly.com/way2speak")
            reply_markup = InlineKeyboardMarkup([[button]])
            context.bot.send_message(chat_id=update.effective_chat.id, text=second_message, reply_markup=reply_markup)

            #button = InlineKeyboardButton("voglio la lezione gratuita!", url="https://calendly.com/way2speak")
            #query.edit_message_text(text=second_message, reply_markup=InlineKeyboardMarkup([[button]]))



        

# Define the main function to start the bot
def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


