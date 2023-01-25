# EvoGuessAI

Компонент EvoGuessAI предназначен для поиска декомпозиционных множеств и оценки сложности для вариантов задач булевой выполнимости. Поиск декомпозиционных множеств осуществляется посредством оптимизации специальной псевдобулевой "black-box" функции, которая оценивает сложность декомпозиции в соответствии используемому методу декомпозиции и рассматриваемому множеству. Для оптимизации значения таких функций используются метаэвристические алгоритмы, в частности, эволюционные.

## Установка

```shell script
git clone git@github.com:ctlab/evoguess-ai.git
cd evoguess-ai
pip install -r requirements.txt
```

Чтобы использовать EvoGuessAI в MPI режиме, также необходимо установить:

```shell script
pip install -r requirements-mpi.txt
```

### Запуск в MPI режиме

Компонент EvoGuessAI может быть запущен в MPI режиме следующим образом:

```shell script
mpiexec -n <workers> -perhost <perhost> python3 -m mpi4py.futures main.py
```

где **perhost** - это число рабочих процессов MPI на одной ноде, и **workers** - это общее число рабочих процессов MPI на всех выделенных нодах.

## При поддержке

Разработка поддерживается исследовательским центром «Сильный искусственный интеллект в промышленности» Университета ИТМО.

<img src='https://gitlab.actcognitive.org/itmo-sai-code/organ/-/raw/main/docs/AIM-Strong_Sign_Norm-01_Colors.svg' width='200'>

## Документация

Документация компонента доступна [здесь](https://evoguess-ai.readthedocs.io/) и включает в себя инструкцию по установке и руководство по использованию.
