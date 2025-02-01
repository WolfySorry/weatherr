import asyncio

async def f():
    while True:
        print('f() func')
        await asyncio.sleep(1) # если бы у нас не было этой функции то функция main бы постоянно вызывала эту функцию и времени на выполнения функции g()
                               # не было бы так как наша функция бесконечна, но так как мы добавили функцию слип, у нас появился маленькое окошко в 1 секунду
                               # в течении которой even_loop может перейти на другую задачу и начать выполнять ее

async def g():
    while True:
        print("g() func")
        await asyncio.sleep(1)

async def main():
    main_loop.create_task(g())
    await f()


main_loop = asyncio.get_event_loop()
main_loop.run_until_complete(main())
# main_loop.run_until_complete(g())
# main_loop.run_until_complete(f())
main_loop.run_forever()