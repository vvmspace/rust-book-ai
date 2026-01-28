## Изящное завершение и уборка мусора 🧹

**Стоп машина!**

Код в Листинге 21-20 обрабатывает запросы асинхронно через пул потоков, как мы и хотели. Всё круто? А вот и нет. Мы получаем предупреждения про поля `workers`, `id` и `thread`, которые мы не используем напрямую. Это как грязная посуда в раковине — намек на то, что мы за собой не убираем. Если сейчас остановить сервер через <kbd>ctrl</kbd>-<kbd>C</kbd>, это будет равносильно выдергиванию вилки из розетки. Все потоки вырубятся мгновенно, даже если они прямо сейчас обрабатывают чей-то важный запрос. Грубо. Очень грубо.

### А как надо? 🤔

Нам нужно научить наш `ThreadPool` хорошим манерам. Мы реализуем трейт `Drop` для пула, чтобы он вызывал `join` для каждого потока. Это даст им возможность закончить свои дела перед выходом. Но этого мало! Нам нужно еще как-то сказать потокам: "Эй, горшочек, не вари! Больше заказов не принимаем!".

Чтобы увидеть это в действии, мы заставим наш сервер обработать всего два запроса, а потом красиво уйти в закат.

Обратите внимание: вся эта магия не касается того, *как* выполняются замыкания. Это чисто инфраструктурная уборка.

### Реализация `Drop` для `ThreadPool`

Начнем с `Drop`. Когда пул выходит из области видимости (droрается), все потоки должны собраться (join). Вот первая попытка (Листинг 21-22), которая... спойлер: **не сработает**.


**Листинг 21-22: Попытка джойнить потоки при дропе пула** *(src/lib.rs)*


```rust,ignore,does_not_compile
impl Drop for ThreadPool {
    fn drop(&mut self) {
        for worker in &mut self.workers {
            println!("Shutting down worker {}", worker.id);

            worker.thread.join().unwrap();
        }
    }
}

```



Мы тут пытаемся пройтись по `workers`. Вроде логично использовать `&mut`, так как `self` изменяемый. Но загвоздка в том, что `join` забирает владение потоком! А у нас только изменяемая ссылка. Rust не даст нам просто так "украсть" поток из `Worker`, который им владеет.

Ошибка компилятора будет кричать на нас:

```console
$ cargo check
    Checking hello v0.1.0 (file:///projects/hello)
error[E0507]: cannot move out of `worker.thread` which is behind a mutable reference
  --> src/lib.rs:52:13
   |
52 |             worker.thread.join().unwrap();
   |             ^^^^^^^^^^^^^ ------ `worker.thread` moved due to this method call
   |             |
   |             move occurs because `worker.thread` has type `JoinHandle<()>`, which does not implement the `Copy` trait
   |
note: `JoinHandle::<T>::join` takes ownership of the receiver `self`, which moves `worker.thread`
  --> /rustc/1159e78c4747b02ef996e55082b704c09b970588/library/std/src/thread/mod.rs:1921:17

For more information about this error, try `rustc --explain E0507`.
error: could not compile `hello` (lib) due to 1 previous error

```

**Что делать?**

Нужно вытащить поток из `Worker`. Вспомним трюк с `Option`. Если бы `Worker` хранил `Option<thread::JoinHandle<()>>`, мы могли бы использовать метод `take`. Это как вынуть конфету из обертки (`Some`) и оставить пустую бумажку (`None`).

Но ждать! `Option` придется проверять везде, где мы обращаемся к потоку. А ведь поток *всегда* должен быть там, пока воркер жив. Заворачивать всё в `Option` только ради деструктора — как носить каску круглосуточно только потому, что раз в год на стройку заходишь.

Есть способ лучше: `Vec::drain`. Этот метод высасывает элементы из вектора, оставляя его пустым. Как пылесос.

Обновляем `Drop` в `ThreadPool`:

 *(src/lib.rs)*


```rust
impl Drop for ThreadPool {
    fn drop(&mut self) {
        for worker in self.workers.drain(..) {
            println!("Shutting down worker {}", worker.id);

            worker.thread.join().unwrap();
        }
    }
}

```



Теперь компилятор счастлив. Заметьте, мы не обрабатываем панику в `join`. Если тут что-то упадет, то упадет всё. Для учебного примера - сойдет, для продакшена - ну, вы поняли (лучше так не делать).

### Сигнализируем потокам: "Отбой!" 📢

Код компилируется, но... не работает как надо. Мы вызываем `join`, но потоки-то крутятся в бесконечном цикле `loop`! Главный поток будет вечно ждать, пока воркеры закончат, а воркеры будут вечно ждать новую работу. Тупик.

Нам нужно разорвать этот порочный круг.

План такой:

1.  Явно дропаем `sender` (отправитель задач) в `ThreadPool`. Это закроет канал.
2.  Когда канал закрыт, `recv()` в воркерах вернет ошибку.
3.  Воркеры ловят ошибку и выходят из цикла.

В `ThreadPool`: нам все-таки придется завернуть `sender` в `Option`, чтобы можно было его забрать (`take`) и дропнуть.


**Листинг 21-23: Явно дропаем sender перед ожиданием потоков** *(src/lib.rs)*


```rust,noplayground,not_desired_behavior
pub struct ThreadPool {
    workers: Vec<Worker>,
    sender: Option<mpsc::Sender<Job>>,
}
// --snip--
impl ThreadPool {
    pub fn new(size: usize) -> ThreadPool {
        // --snip--

        ThreadPool {
            workers,
            sender: Some(sender),
        }
    }

    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);

        self.sender.as_ref().unwrap().send(job).unwrap();
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        drop(self.sender.take());

        for worker in self.workers.drain(..) {
            println!("Shutting down worker {}", worker.id);

            worker.thread.join().unwrap();
        }
    }
}

```



А теперь обновляем воркера, чтобы он понимал: "Ага, канал закрыт, значит, пора домой".


**Листинг 21-24: Выходим из цикла, если recv вернул ошибку** *(src/lib.rs)*


```rust,noplayground
impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        let thread = thread::spawn(move || {
            loop {
                let message = receiver.lock().unwrap().recv();

                match message {
                    Ok(job) => {
                        println!("Worker {id} got a job; executing.");

                        job();
                    }
                    Err(_) => {
                        println!("Worker {id} disconnected; shutting down.");
                        break;
                    }
                }
            }
        });

        Worker { id, thread }
    }
}

```



Чтобы проверить, ограничим `main` двумя запросами:


**Листинг 21-25: Сервер выключается после двух запросов** *(src/main.rs)*


```rust,ignore
fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    let pool = ThreadPool::new(4);

    for stream in listener.incoming().take(2) {
        let stream = stream.unwrap();

        pool.execute(|| {
            handle_connection(stream);
        });
    }

    println!("Shutting down.");
}

```



Запускаем `cargo run`. Делаем три запроса.

1. Ок.
2. Ок.
3. Ошибка (сервер лег спать).

Вывод будет примерно такой:

```console
$ cargo run
   ...
Worker 0 got a job; executing.
Shutting down.
Shutting down worker 0
Worker 3 got a job; executing.
Worker 1 disconnected; shutting down.
...
```

Смотрите, какая красота! Мы:

1.  Перестали принимать задачи.
2.  Дождались, пока текущие задачи доделаются.
3.  Аккуратно выключили свет.

Магия! 🎩

Поздравляю! У нас есть веб-сервер с пулом потоков и корректным завершением.

### Полный код для потомков

 *(src/main.rs)*


```rust,ignore
use hello::ThreadPool;
use std::{
    fs,
    io::{BufReader, prelude::*},
    net::{TcpListener, TcpStream},
    thread,
    time::Duration,
};

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    let pool = ThreadPool::new(4);

    for stream in listener.incoming().take(2) {
        let stream = stream.unwrap();

        pool.execute(|| {
            handle_connection(stream);
        });
    }

    println!("Shutting down.");
}

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let request_line = buf_reader.lines().next().unwrap().unwrap();

    let (status_line, filename) = match &request_line[..] {
        "GET / HTTP/1.1" => ("HTTP/1.1 200 OK", "hello.html"),
        "GET /sleep HTTP/1.1" => {
            thread::sleep(Duration::from_secs(5));
            ("HTTP/1.1 200 OK", "hello.html")
        }
        _ => ("HTTP/1.1 404 NOT FOUND", "404.html"),
    };

    let contents = fs::read_to_string(filename).unwrap();
    let length = contents.len();

    let response =
        format!("{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}");

    stream.write_all(response.as_bytes()).unwrap();
}

```



 *(src/lib.rs)*


```rust,noplayground
use std::{
    sync::{Arc, Mutex, mpsc},
    thread,
};

pub struct ThreadPool {
    workers: Vec<Worker>,
    sender: Option<mpsc::Sender<Job>>,
}

type Job = Box<dyn FnOnce() + Send + 'static>;

impl ThreadPool {
    /// Create a new ThreadPool.
    ///
    /// The size is the number of threads in the pool.
    ///
    /// # Panics
    ///
    /// The `new` function will panic if the size is zero.
    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let (sender, receiver) = mpsc::channel();

        let receiver = Arc::new(Mutex::new(receiver));

        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id, Arc::clone(&receiver)));
        }

        ThreadPool {
            workers,
            sender: Some(sender),
        }
    }

    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);

        self.sender.as_ref().unwrap().send(job).unwrap();
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        drop(self.sender.take());

        for worker in &mut self.workers {
            println!("Shutting down worker {}", worker.id);

            if let Some(thread) = worker.thread.take() {
                thread.join().unwrap();
            }
        }
    }
}

struct Worker {
    id: usize,
    thread: Option<thread::JoinHandle<()>>,
}

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        let thread = thread::spawn(move || {
            loop {
                let message = receiver.lock().unwrap().recv();

                match message {
                    Ok(job) => {
                        println!("Worker {id} got a job; executing.");

                        job();
                    }
                    Err(_) => {
                        println!("Worker {id} disconnected; shutting down.");
                        break;
                    }
                }
            }
        });

        Worker {
            id,
            thread: Some(thread),
        }
    }
}

```



### И это всё?

Ну, почти. Если есть желание прокачаться дальше:

- Добавьте документацию.
- Напишите тесты.
- Сделайте обработку ошибок надежнее (без `unwrap`).
- Попробуйте использовать готовый крейт для пула потоков и сравните ощущения.

## Итоги 🏁

**Вы сделали это!** 🎉

Вы дочитали книгу до конца! Это был долгий путь. Вы пришли сюда новичком, а уходите с почетным званием Rustacean. Вы готовы писать свои проекты, помогать другим и менять мир к лучшему (с памятью, безопасной от гонок данных).

Помните: Rust-сообщество — это семья. Если застрянете (а вы застрянете, это нормально) — вам всегда помогут.

Вперёд, к вершинам! 🚀

---

**Прощальная шутка:**

> Бесконечный цикл заходит в бар. Бармен спрашивает: «Чего желаете?»
> Цикл: «Пива!»
> Бармен: «Чего желаете?»
> Цикл: «Пива!»
> ...
> Тут заходит Graceful Shutdown, выдергивает шнур из розетки и говорит: "Лавочка закрыта, всем спать!"
