import asyncio

async def f():
    print('f() func')

async def g():  # async нужен для того чтобы сделать из синхронной функции асинхронную
    print("g() func")
    await asyncio.sleep(5)
    print('g() func2')

async def main():
    main_loop.create_task(g())     # создает задачу main() и g() одновременно, мы создаем две задачи и в нашем случае мы запускаем функцию main
    await f()                      # и он сначала создает отдельный таск g() который выполняется уже сам по себе, но потом сразу переходит
                                   # на вызов функции f() из за чего функция g() не успевает закончится из за блокирующей sleep, и в данном случае
                                   # мы можем использовать функцию run.forever() которая как раз таки помогает в таких случаях чтобы в программах не было так сказать недосказанности.


main_loop = asyncio.get_event_loop()
main_loop.run_until_complete(main())
# main_loop.run_until_complete(g())
# main_loop.run_until_complete(f()) # запускает задачу ф и он будет работать пока ф не закончится
main_loop.run_forever()              # блокирующая задача для циклов и она сделает так что цикл будет работать бесконечно