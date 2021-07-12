# Integrated Biometrics Overview

### Purpose

This repository contains the python code nessisary to run the biometrics software required by the Human Systems Lab to
perform their studies on cognitive load.  Since metrics are measured using a number of independant agorithms, a
framework is needed for integrating these algorithms into a single deployable application.  This is what the Integrated
Biometrics framework aims to achieve.

### Structure

The framework is an extendable core set of features built on PyQt5.  Each extension mostly acts as an independant
application with a set api defined by the framework.  Extensions are dynamically loaded by the framework at runtime and
are entirely isolated from each other as there are no assumtions made about the existance of any extension ahead of
time.

On application startup, all extensions are loaded, and presented to the user.  The user then selects the individual
extensions to load.  Once the relevent extensions are selected, the framework starts each of the extensions with their
cooresponding configurations.  Each extension defines a startup and shutdown function at load time.  The startup
functions acts as a 'main' function for the extension as each recieve their own thread of execution.  On application
shutdown, each extensions' shutdown function is called serially from the main thread (asyncronously from the
extension's perspective).

In extensions, the retrieval and serialization of data is handled by calling an API which the framework provides to
each extension at startup.  This ensures a stable system for accessing shared resources such as web camera frames and
any recorded audio.  Furthermore, this also ensures that data is serialized in a form which will be both efficient and
easy to work with for the later analysis needed.

To access screen space and provide interaction with the user, an extension can define a PyQt5 widget which will be
shown to the user throughout the application lifetime.  The extension will have full control over this widget
throughout the lifetime of the application and can set hints for the positioning of the widget relative to others
during application startup.

### Further Reading

- [Extension Authoring](extension_authoring.md)
- [Layout System](layout_system.md)

### [Index](index.md)
