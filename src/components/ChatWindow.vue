<template>
  <div id="phone">
    <header>
      <img src="../assets/profile.png" alt="Profile Picture">
      <span>Dani&euml;l 2</span>
    </header>
    <section id="scroll">
      <div id="messages-window" v-if="messages.length>0">
        <span :class="'message ' + (message.user_id==1 ? 'ours' : 'theirs')"
                v-for="(message,index) in messages" :key="index">{{message.content}}</span>
        <span class="message typing-indicator" v-if="this.state==2">
          <span></span>
          <span></span>
          <span></span>
        </span>
      </div>
      <div class="emptyState" v-else>
        <h1>Chat with me.</h1>
        <p>
          I am a machine learning model trained on the <b>59353</b> messages send by Dani&euml;l on WhatsApp over the past <b>five years.</b>
        </p>
        <p>
          The data on which this model is trained encompasses everything from my darkest secrets to my deepest crushes.
        </p>
        <p>
          Have fun!
        </p>
        <p>
          With love,<br/>
            <b>Original Dani&euml;l</b>
        <br/>
        </p>
      </div>
    </section>
    <footer>
          <input focus id="input" :placeholder="placeholder"  :disabled="this.state==2||this.state==1" type="text" v-model="newMessageContent" v-on:keyup.enter="addMessage"/>
    </footer>

    <!-- The sound effects triggered by js -->
    <audio hidden id="message_receive" volume="0.1">
      <source src="message_receive.mp3" type="audio/mpeg">
    </audio>
    <audio hidden id="message_send" volume="0.1">
      <source src="message_send.mp3" type="audio/mpeg">
    </audio>

  </div>
</template>

<script>
import axios from 'axios'

// Define the different states of the bot
// as constanst for readability
const NOT_TYPING = 0
const RECEIVED = 1
const TYPING = 2

export default {
  name: 'ChatWindow',
  mounted(){
   document.getElementById("input").focus();

   // Use the speechSynthesis API to speak the messages out loud
   this.speachSynth = window.speechSynthesis;

   // Getting the list of available voices is an async process
   if (speechSynthesis.onvoiceschanged !== undefined) {
     speechSynthesis.onvoiceschanged = () =>{
       this.synthVoices = this.speachSynth.getVoices();
     }
   }

   // Since this work is shown at an exhibition, it includes a function to
   // reset the state of the app when people aren't interacting with it for some time
   // Every second it checks if the limit is reached
   window.setInterval(()=>{
     this.inactivityTimer++;
     if(this.inactivityTimer>=this.inactivtyLimit){
       this.reset();
       // Pick a random idle message and speak it out loud to grab attention
       this.speak(this.idleMessages[Math.floor(Math.random()*this.idleMessages.length)],0);
     }
   }, 1000);

   // When the app is being interacted with, reset the timer
   document.onkeypress = () =>{
     this.inactivityTimer = 0;
   }

  },
  data() {
    return{
      newMessageContent: '',
      messages: [],
      state: NOT_TYPING,
      placeholder:'Type something and press ENTER to send',
      inactivityTimer:0,
      inactivtyLimit:120, // Amount of s that the app will wait until it resets itself,
      serverURI:'http://127.0.0.1:5000', // URI of the back-end that supplies messages
      idleMessages: ['Ik voel me eenzaam.','Hallo, waarom praat niemand tegen mij','Mag ik wat aandacht alsjeblieft'],
    }
  },
  methods: {
    // This function uses the SpeechSynthesis API to speak text
    speak(text = '',voice = 0){
      if (this.speachSynth.speaking) {
          return;
      }else{
        let utterThis = new SpeechSynthesisUtterance(text);
        utterThis.voice = this.synthVoices[voice];
        this.speachSynth.speak(utterThis);
      }
    },
    // Resets the chat window to its original state
    reset:function(){
      this.newMessageContent = ''
      this.messages = []
      this.state = NOT_TYPING
      this.inactivityTimer = 0;
      this.placeholder = 'Type something and press ENTER to send'
    },
    // Adds a message typed by the user to the chat window
    addMessage: function() {
      if(this.newMessageContent.length<1)
      return

      this.messages.push({user_id: 1, content: this.newMessageContent});

      // Play send sound and let the text be spoken
      document.querySelector('#message_send').play()
      this.speak(this.newMessageContent,10);

      this.newMessageContent = '';

      this.state = RECEIVED
      this.placeholder = 'Waiting for response...'

      axios.get(this.serverURI+'/message').then((response) =>{

          let reply = response.data.message

          setTimeout(()=>{
            this.state = TYPING
            let typingTime = 900 + reply.length*10

            setTimeout(()=>{
              document.querySelector('#message_receive').play()
              this.messages.push({user_id: 2, content: reply});

              this.state = NOT_TYPING
              this.placeholder = 'Type something and press ENTER to send'
              this.inactivityTimer = 0;

              setTimeout(() => {
                this.speak(reply,0);
              }, 400);

            }, typingTime);

          }, 600);

        })
        .catch(function (error) {
          console.error(error);
        })

      }
  },
  updated(){
    // Everytime a new message is added, scroll to the bottom so it is in view
    // And refocus the input so a mouse isn't needed
    var scrollElement = document.getElementById("scroll");
    scrollElement.scrollTop = scrollElement.scrollHeight;
    document.getElementById("input").focus();
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#phone{
  max-width: 375px;
  border-radius: 15px;
  margin: 0 auto;
  height: 652px;
  box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
  position: relative;
  overflow:hidden;
  background: #fff;
  display: flex;
  flex-flow: column;
}

header,footer{
	background: rgba(250, 250, 250, 1);
  backdrop-filter:blur(10px);
}

header{
  position: absolute;
  height: 75px;
  width: 100%;
  border-bottom: 1px solid #EBEAEB;
  text-align: center;
  box-sizing: border-box;
  border-radius: 15px 15px 0 0;
  font-size: 0.9em;
}

header img{
    background: #f2f2f2;
    width: 40px;
    height: 40px;
    border-radius: 20px;
    margin: 5px auto;
    display: block;
}

footer{
  position: absolute;
  bottom: 0;
  width: 100%;
  box-sizing: border-box;
  border:none;
  border-top: 1px solid #EBEAEB;
  outline: none;
  margin: 0;
  border-radius: 0 0 15px 15px;
  box-sizing: border-box;
  padding: 7px;
}

input{
  border-radius: 15px;
  height: 30px;
  border: 1px solid #EBEAEB;
  width: 100%;
  box-sizing: border-box;
  outline: none;
  padding: 20px;
}

::scrollbar {
    display: none;
}

#scroll{
    overflow:scroll;
    scroll-behavior: smooth;
}

#messages-window {
  flex: 1 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items:flex-start;
  padding: 80px 20px;
}

.message {
  background: #EBEAEB;
  color:#000;
  padding:8px 12px;
  margin-bottom:8px;
  border-radius:16px;
  max-width:70%;
}

.ours {
  background:#0076FF;
  color:#fff;
  align-self:flex-end;
}

/* TYPING ANIMATION
   Inspired by Joseph Fusco
   https://codepen.io/fusco/pen/XbpaYv
*/
.typing-indicator {
  padding: 12px;
  -webkit-animation: 2s bulge infinite ease-out;
          animation: 2s bulge infinite ease-out;
}
.typing-indicator span {
  height: 10px;
  width: 10px;
  float: left;
  margin: 0 1px;
  background-color: #9E9EA1;
  display: block;
  border-radius: 50%;
  opacity: 0.4;
}

.typing-indicator span:nth-of-type(1) {
  -webkit-animation: 1s blink infinite 0.3333s;
          animation: 1s blink infinite 0.3333s;
}
.typing-indicator span:nth-of-type(2) {
  -webkit-animation: 1s blink infinite 0.6666s;
          animation: 1s blink infinite 0.6666s;
}
.typing-indicator span:nth-of-type(3) {
  -webkit-animation: 1s blink infinite 0.9999s;
          animation: 1s blink infinite 0.9999s;
}

@-webkit-keyframes blink {
  50% {
    opacity: 1;
  }
}

@keyframes blink {
  50% {
    opacity: 1;
  }
}

@-webkit-keyframes bulge {
  50% {
    -webkit-transform: scale(1.05);
            transform: scale(1.05);
  }
}
@keyframes bulge {
  50% {
    -webkit-transform: scale(1.05);
            transform: scale(1.05);
  }
}
</style>
