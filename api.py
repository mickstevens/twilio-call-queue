from flask import Flask, request
from twilio.twiml.voice_response import Dial, VoiceResponse, Gather
from calls import CallQueue
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

call_queue = CallQueue("support")
app = Flask(__name__)

AGENTS = {
    "+550000000000": "Ana",
    "+000000000001": "Miguel",
}


@app.route("/voice", methods=["GET", "POST"])
def voice():
    """Respond to incoming phone calls with a menu of options"""
    pprint(request.values)  # kept for debugging purposes
    resp = VoiceResponse()
    agent = AGENTS.get(request.values.get("Caller"))

    if "Digits" in request.values:
        choice = request.values["Digits"]

        if agent:
            if choice == "1":
                resp.say("You will get the next call.")
                dial = Dial()
                dial.queue(call_queue.name)
                resp.append(dial)
            else:
                resp.say("Sorry, I don't understand that choice.")
    else:
        queue_size = call_queue.size()
        if agent:
            gather = Gather(num_digits=1)
            gather.say(
                f"Hello, {agent}. There are {queue_size} callers in the queue, press 1 to answer the next call"
            )
            resp.append(gather)
        else:
            # customer
            resp.say(
                f"There are {queue_size} people ahead of you. An agent will talk to you soon."
            )

            # in case you want to play a message before
            # resp.play(
            #    'http://com.twilio.sounds.music.s3.amazonaws.com/MARKOVICHAMP-Borghestral.mp3'
            # )

            resp.enqueue(call_queue.name)
            # wait_url = 'http://demo.twilio.com/docs/voice.xml'

    # If the caller doesn't select an option, redirect them into a loop
    resp.redirect("/voice")
    return str(resp)
