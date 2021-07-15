# Extension Authoring

### [Index](index.md)

### Setup for Contributing
##### Work in Progress

If you are only interested in testing out an idea for an extension, without the intention of integrating it into the
end software, you can clone this main repository and jump to the [getting started](#Getting Started) section of this
page.

Before creating an extension for this framework, it is recommended that you first fork this repository.  To keep your
code organized, create a new branch for the extension you indend to work on, and work using your preferred workflow off
that branch.  After you have finished making your extension, update your fork to the newest version of this repository
and test it to ensure that it works as intended.  After you have finished testing, you can open up a pull request to
get your changes integrated into the main repository.

### Getting Started

Note: You will first need a clone of this repository on your computer.  See the
[setup up for contributing](#Setup for Contributing) section of this page for getting a clone of this repository.

To start authoring your extension, create a new python package in the `extensions` directory of this repo.  Your
folder structure should now resemble the following:

    .
    ├── ...
    ├── extensions
    │   ├── ...
    │   ├── <your-extension-name>
    │   │   └── __init__.py
    │   ├── ...
    │   └── __init__.py
    └── ...

When creating an extension, you will never need to modify any of the files outside your extension folder.  So for the
remainder of this page, all references to files or code will be local to that folder.  Ex. `__init__.py` refers to the
file with absolute path `<path-to-repo>/IntegratedBiometrics/extensions/<your-extension-name>/__init__.py`.

To get the framework to recognize your new folder as a valid extension, you will need to add a class definition to your
`__init__.py` file with the name `Extension`.  Moreover, you will need to specify that the parent of this class is the
class `ibs.IbsExt` - defined by the framework.  This can be achieved with the following code in your `__init__.py` file:

```python
import ibs


class Extension(ibs.IbsExt):
    pass
```

With the current code, the framework will recognize your extension as valid, but will crash when it tries to load it.
The reason for this is that the framwork will expect to find some predetermined method names in the `Extension` class
you define.  Minimally, you will need to define the following methods:

 - `__init__(self, options)`
 - `get_name()` (static method)
 - `startup_ref(self)`
 - `shutdown_ref(self)`

After defining these methods, your `__init__.py` file will look something like the following:

```python
import ibs


class Extension(ibs.IbsExt):
    def __init__(self, options):
        pass

    @staticmethod
    def get_name():
        pass

    def startup_ref(self):
        pass

    def shutdown_ref(self):
        pass
```

Before we go ahead and implement these methods, we first need to understand what they are for.  The `__init__` method
is used to create an instance of your `Extension` class for later use in launching the application.  For now, we will
ignore the exact use, and just call the parent's constructor will the following implementation:

```python
def __init__(self, options):
    super(Extension, self).__init__(options)
```

The `get_name` function is used by the framework to determine the name of you extension.  This will be used by the
framework in a number of ways, but what's important is to provide a descriptive name of your extension that can
comfortably fit on a single line.  The naming convention we intend to follow is a captial first letter of word
seperated by spaces.  For example:

```python
@staticmethod
def get_name():
    return "Pupil Size Estimation"
```

The `startup_ref` and `shutdown_ref` functions is where thing start to get more interesting.  Both of these methods
must return a function reference which will be used by the framework to start and stop you application.  The
implementation of the function references will be determined by you, but the signature and context in which they are
called is set by the framework.

The `startup_ref` method must return a reference to a function with a signature of `my_startup_function(api, widget)`.
You can change the name of the startup function to any name you prefer, but the signature must contain two arguments.
The first argument must be named `api`, and the second must be named `widget`.  If you alter the names of the arguments
it will most likely work, but it will not be guarenteed.

The `shutdown_ref` method must return a reference to a function with a signature of `my_shutdown_function()`.  Similar
to before, the name of the shutdown function can be changed to any name, but the function must have zero arguments.

Here is some sample code which fully implements the `Extension` class:

```python
import ibs


def my_startup_function(api, widget):
    print("Starting up my custom extension :)")


def my_shutdown_function():
    print("Shutting down :(")


class Extension(ibs.IbsExt):
    def __init__(self, options):
        super(Extension, self).__init__(options)

    @staticmethod
    def get_name():
        return "My New Extension"

    def startup_ref(self):
        return my_startup_function

    def shutdown_ref(self):
        return my_shutdown_function
```

With this extension definition in your `__init__.py` file, you have successfully created a working extension for the
Integrated Biometrics Framework!

### Implementing Startup and Shutdown

In the [getting started](#Getting Started) section of this page, you created your first working extension, but
unfortunately, it didn't seem to do much.  This is where the `startup` and `shutdown` functions are useful.  After the
user presses the `continue` button on the startup screen, a new thread of execution is launched for each extension that
is loaded.  Then the provided `startup` functions are called on that thread for each of the extensions.  This means
that you can use your `startup` function just as you would a normal `main` function in most languages.  For this
application, the `startup` function usually consists of a `while True` loop which continuously collects data and
measures the cognative load of the participant through some algorithm.  When the time comes for the application to close
via user interaction, external signals, etc. the provided `shutdown` functions are called for each of the extensions
from the main thread.  So to handle this, the following coding style is typically used:

```python
running = True


def startup(api, widget):
    while running:
        # Running the biometrics algorithm
        pass


def shutdown():
    global running
    running = False
```

Integrating this into the extension you created in the previous section, your `__init__.py` file becomes:

```python
import ibs

running = True


def startup(api, widget):
    while running:
        # Running the biometrics algorithm
        pass


def shutdown():
    global running
    running = False


class Extension(ibs.IbsExt):
    def __init__(self, options):
        super(Extension, self).__init__(options)

    @staticmethod
    def get_name():
        return "My New Extension"

    def startup_ref(self):
        return startup

    def shutdown_ref(self):
        return shutdown
```

As you write your extension, it will become useful to seperate out your extension configuration code ie. `Extension`
class from your biometrics algorithm.  A useful setup for this is uses the following file structure:

    .
    ├── ...
    ├── extensions
    │   ├── ...
    │   ├── <your-extension-name>
    │   │   ├── main.py
    │   │   └── __init__.py
    │   ├── ...
    │   └── __init__.py
    └── ...

Where your `startup` and `shutdown` functions are defined in your `main.py` file, while the `__init__.py` file is only
used for the `Extension` class as well as other framework specific information.  This will also help in testing your
extension independant of the framework since your `main.py` will be able to run without dependance on the framework api.

With this setup, your code would look like the following:

```python
# main.py
running = True


def startup(api, widget):
    while running:
        # Running the biometrics algorithm
        pass


def shutdown():
    global running
    running = False
```

```python
# __init__.py
import ibs

from . import main


class Extension(ibs.IbsExt):
    def __init__(self, options):
        super(Extension, self).__init__(options)

    @staticmethod
    def get_name():
        return "My New Extension"

    def startup_ref(self):
        return main.startup

    def shutdown_ref(self):
        return main.shutdown
```

### Startup Configurations

### Extension Graphics
