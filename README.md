# self-portrait I

This project consists of two parts: a front-end interface made with Vue.js, and a back-end python webserver that generates the text messages using . I initially tried using [ml5.js](https://github.com/ml5js/ml5-library) to generate the messages on the front-end, but these were of rather low quality and were quite unreliable. That is why I decided to use the [textgenrnn](https://github.com/minimaxir/textgenrnn) python module together with [flask](https://github.com/pallets/flask) to create a simple API server that just returns one generated message every time it's called on the route /message.

## Back-end startup
```
python3 server/server.py
```

## Front-end setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

Concat all .txt logs into 1 big
```
ls *.txt | xargs -L 1 cat >> input.txt
```
