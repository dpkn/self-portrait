<template>
  <div id="app">
    <ChatWindow/>

  </div>
</template>

<script>
import ChatWindow from './components/ChatWindow.vue'

export default {
  name: 'app',
  components: {
    ChatWindow
  }
}
</script>

<style>
html, body, #app {
  font-family: 'SF UI Text', 'San Francisco Text', Roboto, -apple-system, sans-serif;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  background: #f9f9f9;
  top:0;
  left:0;
}
h1{
  max-width:500px;
  margin: 30px auto;
  text-align: center;
  font-size:2em;
}
#info{
  max-width: 400px;
  position: fixed;
  top:225px;
  right:80px;
}
#info h1{
  text-align: left;
  margin-bottom: 0;
}
</style>
