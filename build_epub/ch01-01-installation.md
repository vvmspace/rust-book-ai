# Установка

Первым делом — самолеты. Точнее, установка Rust.
Мы будем использовать `rustup` — это как швейцарский нож для управления версиями Rust.

### Linux / macOS

Открываем терминал и копипастим эту магическую строку:

```console
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```

Скрипт спросит пароль (возможно) и сделает всё красиво. Если увидите:
`Rust is installed now. Great!`
Значит, вы великолепны.

Вам также понадобится линкер (обычно он есть в GCC или Clang).

- macOS: `xcode-select --install`
- Linux: `sudo apt install build-essential` (ну или что там у вас в дистрибутиве).

### Windows

Идем на [https://www.rust-lang.org/tools/install](https://www.rust-lang.org/tools/install), качаем `rustup-init.exe`.
В процессе он может попросить поставить Visual Studio C++ Build Tools. Не сопротивляйтесь, это нужно для линкера.

### Проверка связи

```console
$ rustc --version
rustc 1.xx.x (hash date)
```

Если видите версию — поздравляю, вы теперь (потенциальный) Растоман!

### Обновление и Удаление

- Обновить: `rustup update`
- Удалить (зачем?!): `rustup self uninstall`

---

**Анекдот:**

> — Ты зачем удалил Rust?  
> — Место на диске кончилось.  
> — А `target` папку почистить не пробовал?  
> — ... (звук удара головой о клавиатуру)
