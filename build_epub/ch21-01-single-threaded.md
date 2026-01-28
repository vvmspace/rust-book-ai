## Однопоточный веб-сервер. Погнали! 🚀

Давайте-ка соберем что-нибудь рабочее. Начнем с простого: однопоточный веб-сервер. Никаких фреймворков. Только вы, Rust и голый TCP.

### Ликбез по протоколам 📚

- **TCP** (Transmission Control Protocol): низкоуровневая труба, по которой бегают байты. Она гарантирует, что байты добегут в правильном порядке.
- **HTTP** (Hypertext Transfer Protocol): язык, на котором общаются браузер и сервер поверх этой трубы.

Мы будем работать с *сырыми* данными. Хардкор.

### Слушаем эфир 🎧

Нам нужно открыть уши и слушать входящие соединения. В Rust для этого есть `std::net::TcpListener`.

Создаем проект:
```console
$ cargo new hello
$ cd hello
```

И пишем код, чтобы слушать порт `7878` (потому что это `rust` на клавиатуре телефона 😉).


**Листинг 21-1: Слушаем порт и радуемся входящим** *(src/main.rs)*


```rust,no_run
use std::net::TcpListener;

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        println!("Connection established!");
    }
}

```



Запускаем `cargo run` и идем в браузер по адресу `127.0.0.1:7878`. Браузер скажет "Ошибка соединения" (потому что мы ничего не ответили), но в консоли вы увидите: `Connection established!`.

Есть контакт!

### Читаем мысли (запрос) браузера 🔮

Теперь давайте узнаем, чего хочет клиент. Нам нужно прочитать данные из потока (`TcpStream`).


**Листинг 21-2: Читаем поток через BufReader** *(src/main.rs)*


```rust,no_run
use std::{
    io::{BufReader, prelude::*},
    net::{TcpListener, TcpStream},
};

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        handle_connection(stream);
    }
}

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let http_request: Vec<_> = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    println!("Request: {http_request:#?}");
}

```



Мы используем `BufReader` и его метод `lines()`. Мы читаем, пока не встретим пустую строку. Почему? Потому что HTTP-запрос заканчивается двойным переносом строки (`\r\n\r\n`).

Результат будет примерно такой:
```
Request: [
    "GET / HTTP/1.1",
    "Host: 127.0.0.1:7878",
    ...
]
```

Первая строка — самое важное. `GET / HTTP/1.1`. Метод, путь, версия.

### Пишем ответ ✍️

Клиент спросил — надо ответить. Формат ответа такой:
`HTTP-Version Status-Code Reason-Phrase CRLF headers CRLF message-body`

Например:
`HTTP/1.1 200 OK\r\n\r\n`

Давайте пошлем это клиенту.


**Листинг 21-3: Отправляем крошечный успешный ответ** *(src/main.rs)*


```rust,no_run
fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let http_request: Vec<_> = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    let response = "HTTP/1.1 200 OK\r\n\r\n";

    stream.write_all(response.as_bytes()).unwrap();
}

```



Теперь браузер покажет пустую белую страницу, а не ошибку. Прогресс!

### Возвращаем реальный HTML 📄

Давайте создадим файл `hello.html` в корне проекта (рядом с `src`, а не внутри).


**Листинг 21-4: hello.html** *(hello.html)*


```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Hello!</title>
  </head>
  <body>
    <h1>Hello!</h1>
    <p>Hi from Rust</p>
  </body>
</html>

```



И научим сервер читать его и отдавать.


**Листинг 21-5: Отправляем содержимое файла** *(src/main.rs)*


```rust,no_run
use std::{
    fs,
    io::{BufReader, prelude::*},
    net::{TcpListener, TcpStream},
};
// --snip--

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let http_request: Vec<_> = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    let status_line = "HTTP/1.1 200 OK";
    let contents = fs::read_to_string("hello.html").unwrap();
    let length = contents.len();

    let response =
        format!("{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}");

    stream.write_all(response.as_bytes()).unwrap();
}

```



Не забудьте заголовок `Content-Length`, чтобы браузер знал, сколько читать.

### Валидация и 404 🚫

Сейчас наш сервер отдает `hello.html` на любой запрос. Хоть `/foo`, хоть `/bar`.
Давайте будем вежливыми, но строгими. Если просят `/` -> держи `hello.html`. Если что-то другое -> 404.


**Листинг 21-6: Проверяем путь запроса** *(src/main.rs)*


```rust,no_run
// --snip--

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let request_line = buf_reader.lines().next().unwrap().unwrap();

    if request_line == "GET / HTTP/1.1" {
        let status_line = "HTTP/1.1 200 OK";
        let contents = fs::read_to_string("hello.html").unwrap();
        let length = contents.len();

        let response = format!(
            "{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}"
        );

        stream.write_all(response.as_bytes()).unwrap();
    } else {
        // some other request
    }
}

```



Если не совпало — отдаем `404.html`.


**Листинг 21-7: Обработка ошибки 404** *(src/main.rs)*


```rust,no_run
    // --snip--
    } else {
        let status_line = "HTTP/1.1 404 NOT FOUND";
        let contents = fs::read_to_string("404.html").unwrap();
        let length = contents.len();

        let response = format!(
            "{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}"
        );

        stream.write_all(response.as_bytes()).unwrap();
    }

```



### Рефакторинг: убираем дублирование 🧹

Код стал немного грязным. Много повторений. Давайте вынесем различия (статус и имя файла) в переменные.


**Листинг 21-9: Красивый и чистый код** *(src/main.rs)*


```rust,no_run
// --snip--

fn handle_connection(mut stream: TcpStream) {
    // --snip--

    let (status_line, filename) = if request_line == "GET / HTTP/1.1" {
        ("HTTP/1.1 200 OK", "hello.html")
    } else {
        ("HTTP/1.1 404 NOT FOUND", "404.html")
    };

    let contents = fs::read_to_string(filename).unwrap();
    let length = contents.len();

    let response =
        format!("{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}");

    stream.write_all(response.as_bytes()).unwrap();
}

```



Вот теперь у нас настоящий, (почти) взрослый веб-сервер на 40 строках Rust!
Единственная проблема — он однопоточный. Если кто-то "зависнет" при запросе, все остальные будут ждать.
Но это мы починим в следующей главе!

---

**Анекдот:**

> Клиент: GET /vodka HTTP/1.1
> Сервер: 402 Payment Required
> Клиент: GET /beer HTTP/1.1
> Сервер: 418 I'm a teapot
