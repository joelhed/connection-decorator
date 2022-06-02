# connection-decorator

This library provides a decorator that makes sure that if a decorated function is called, it has access to a database connection.
If the decorated function calls another decorated function, it uses the same connection, making sure that there is only one connection in a given call tree where the parent is a decorated function.
