.. include:: beamerdefs.txt

=======================================
PyPy and CPython through execnet
=======================================

Mandelbrot demo (1)
-------------------

- Django application

- Mandelbrot fractal

  * fished randomly on the net :-)

- Run both on CPython and PyPy

  * django trunk!


Mandelbrot demo (2)
-------------------

- Works purely on PyPy

- Not always the case

  * missing extension modules (cpyext mitigates the problem)

  * libraries that rely on CPython details
    
  * ...

- clear performance-critical part


CPython and PyPy side by side
------------------------------

- CPython: runs the main application

- PyPy: subprocess, runs only the hotspots

- How do they communicate?

- execnet


Rendering (1)
---------------

|example<| Mandelbrot |>|
|small|
::

    def render(request):
        w = int(request.GET.get('w', 320))
        h = int(request.GET.get('h', 240))

        from py_mandel import mandelbrot
        img = mandelbrot(w, h)

        return HttpResponse(img, content_type="image/bmp")

|end_small|
|end_example|


Rendering (2)
-------------

|example<| Mandelbrot on PyPy |>|
|small|
::

    def pypy_render(request):
        w = int(request.GET.get('w', 320))
        h = int(request.GET.get('h', 240))

        channel = pypy.remote_exec("""
            from py_mandel import mandelbrot
            w, h = channel.receive()
            img = mandelbrot(w, h)
            channel.send(img)
        """)
        channel.send((w, h))
        img = channel.receive()

        return HttpResponse(img, content_type="image/bmp")

|end_small|
|end_example|

execnet setup
-------------

|example<| At startup |>|
|small|
::

    import execnet
    mygroup = execnet.Group()
    pypy = mygroup.makegateway("popen//python=pypy-c")
    pypy.remote_exec("""
        import sys
        import os
        os.chdir("mandelbrot")
        sys.path.insert(0, '')
    """)

|end_small|
|end_example|


Benchmarks
----------

.. image:: demo-graph.pdf
   :scale: 45
