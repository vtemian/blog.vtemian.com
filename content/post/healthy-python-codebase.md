---
title: "Healthy Python Codebase"
date: 2020-09-21T15:04:57+02:00
description: "Healthy Python Codebase"
keywords:
    - python
    - codebase
    - consistency
    - explicit is better than implicit
    - end-to-end testing python
    - integration testing python
    - unit testing python
    - python refactoring example
tags:
    - python
    - guide
    - refactoring
---

The code is a living entity. For the majority of the time, it stays in silence and it's doing its job, without complaining.
But, there are these creatures, humanoid, that from time to time, will change it. Will try to fix it, adapt, or
completely remove parts of it. Those creatures tend to conserve energy and they are using pattern recognition to do so.
They observe patterns and take fast and easy decisions based on those patterns.
Because of that, this code entity needs to be structured and behave in certain patterns.

## Consistency

Those patterns are grouped together in a collection called code style. Any change that doesn't follow the code style, 
introduces inconsistency, and should be treated as a systemic disease. Maybe is a little harsh, but any code change should 
avoid inconsistency. Even if the current code base has a "special" code style, even if some bad decisions were made, introducing
inconsistency is even worst. You'll have to maintain two or more styles, multiply the decisions and patterns, thus adding extra effort.

So, when reviewing any code, one should take into account the current code style. Following the current patterns and maintain
consistency is more valuable in the long run. If the current code base is not consistent, I suggest solving this issue first.
It should be an easy refactoring exercise and shouldn't impact the business logic.

Use formatting and linting tools and setup a CI pipeline that will run on every code change.
You can even run them as a pre-commit hook. Black for formatting and pylint / mypy for linting are the most popular tools.

From a behavioral point of view, make sure that the entities are doing what their name implies: fetch_users should return a list
of users or an empty list. It shouldn't compute anything or return false, true, int, or string. Be consistent with names
and obey components to respect their contract. If a component violets its contract, fail fast and visible. 
Don't be afraid to throw exceptions or stop the business logic. Failing fast and visible will help you catch bugs 
and solve inconsistency issues.

## Explicit is better than implicit

Python is magic and allows you to abuse it. Besides that, when designing certain components, make sure that those are well 
defined and their behavior is properly exposed and expected by their clients.

Avoid using generic components like Manager, Service, Data since they have a tendency of hiding complexity. 
Use specific and meaningful terminology for components that are responsible for doing just one thing. 
Favor small and well-defined logical units over complex ones (simple is better than complex).

Avoid implicit defaults and don't be afraid of exposing some implementation details:

```python
def compute_interval(start):
    return time.now() - start

def compute_interval(start, end=None):
    if end is None:
        end = time.now()

    return end - start
```

Leverage Python's functional tooling over in-place processing:

```python
def filter(items):
    items.sort()  # faster, in-place
    new_items = []

    for item in items:
        if item.get("property"):
            new_items.append(item)

    return new_items


def filter(items, filters=None):
     if not filters:
         filters = [lambda item: item.get("property")]

     return [item for item in sorted(items)  # slower, creates a new list
             all(filter(item) for filter in filters)]
 ```

Keep the levels of indirection small, avoid abusing metaclasses and complex OOP design:

```python
# abstractisation just for the sake of it adds more complexity than solves real issues
class RequestValidator:
    def __init__(self, request, validators=None):
         self.request = request
         self.validators = valiadtors or [
             lambda request: "foo" in request.POST.get("arg")
         ]

    def validate(self):
        return all([validator(self.request) for validator in self.validators])


if RequestValidator(request).validate():
    process()


# simple and concise, solves the issue is easy to read and to maintain
if "foo" in request.POST.get("arg", ""):
    process()
````

Avoid using classes as logical namespaces:

```python
class Refresh:
    @classmethod
    def create_token(cls):
        ...

    @classmethod
    def invalidate_token(cls, token):
        ...

    @classmethod
    def refresh_token(cls, token):
        ...
```

## Fail fast and visible

Breaking the production can be terrifying and sometimes, we tend to "hide" or "swallow" user-facing errors just to 
avoid showing weakness and to give our user a sense of shaky/unfinished product.

Having bugs and errors in your codebase is a natural thing. That's how software grows and evolves.
The catch is to see those bugs and errors as soon as possible and to fix them.
The scariest bugs always starts with This thing just doesn't work. It says nothing.

Avoid catching all exceptions. Instead, try to handle as many exception paths as possible.

```python
try:
    content = requests.get()
except Exception:
    pass


try:
    content = requests.get()
except ConnectTimeout:
    ...
except RequestException:
    ...
except RetryError:
    ...
```

Failing fast and visible allows you to identify the problem and fix it. But you'll need visibility over those exceptions. Just
failing fast may not be enough. An exception without a traceback may not be so useful to find the root cause.

[Sentry](https://sentry.io/) is the way to go. Other logging and monitoring tools will help as much:
[Datadog](https://www.datadoghq.com/), [Google Operations](https://cloud.google.com/products/operations), or
[NewRelic](https://newrelic.com/) are just a bunch of observability tools that will make your life easier.

## End-to-End > Integration > Unit tests

Testing is your safety net. It allows you a free state of mind in which changes can happen easily, without regression. In theory,
at least. Most of the time, we trust too much this safety net. A close to 100% code coverage doesn't really mean that your changes
are not breaking the current behavior. Some code paths can be purely understood and tested.

Multiple testing methodologies will create different safety nets. A really simple and fast to obtain is one using unit tests.
Testing small and well-contained pieces of logic is easy and fast. The downside comes when those pieces are interacting with other
parts and the interaction may be broke. Some assertions about those interactions can be tested using mocks, but those are our
interpretations and assertion about the behavior and not actual behavior. Avoid trusting only unit tests and mock only if
necessary. Mock data over behavior.

Instead of mocking behavior, use a production-ready setup and try to test multiple components together. This kind of testing can
be named integration tests. Use dependency injection over global services. The setup may cost you more than the setup for unit
tests, but in the end, it's closer to production behavior. Usually, a small integration test is more powerful than multiple unit
tests.

Even in integration, tested behavior is limited to the components tested. A wider testing methodology would be to test the entire
stack, a request lifecycle from client to server and back. This will cost you the most, but having just one simple e2e
(end-to-end) test can pay the bill big time. This type of test usually involves spawning a production-like environment, close to
production data.

Favor End-to-End tests over Integration tests. Favor Integration tests over Unit tests. Mock data over behavior.

## Deployable

Writing code is easy. But those written symbols are usually meant to run on different machines. They interact with other symbols,
alone, without your help. Even if may not be a big concern, deploying software is a big part of it. When writing code, starting
with the mindset that it should get deploy will help you with design decisions. Always start with deploying in mind. How should
data migration be handled? Does it involve downtime? Should I announce my users? How to deprecate API versions?

Beside actually releasing software, thinking about packaging and portability is also important. Dependencies should be locked and
build reproducible. A clear and consistent pipeline helps users use your software and allows developers to contribute, with
minimum pain. Don't be afraid to use helper scripts, Dockerfiles, Makefiles, or other tools to automate your job. Software is
always changing, so allow for this pipeline/procedure to be changing as well.

## Refactoring Example

Those were some small guidelines from my experience. In the end, a healthy codebase is a codebase that is easy to change.

Making a codebase healthy is not a one-time thing. Is a long and tedious process, with small incremental progress. Small
deployable changes are more sustainable, less invasive, and easier to understand.

```python
import requests

import os

from django.conf import settings
import time


def a(b):
    s = time.now()

    try:
        c = requests.get(b)
    except:
        return

    if time.now() - s > settings.TIME:
        return "it took too much"
    else:
        return c.content, c.status_code
```

```python
# Follow PEP-8 guidelines and sort imports.

import os
import time

import requests
from django.conf import settings
from requests.exceptions import RequestException


def validate_url(url: str) -> bool:
     if not url or not isinstance(url, str):
         return False

     rules = [
         lambda url: url.startswith("https://"),
         lambda url: settings.VALID_HOST in url,
         ...
     ]

     return not all([rule(url) for rule in rules])


# Naming should be meaningful and consistent.
def try_fetch(url: str) -> str: # Type-hinting allows tools like mypy to detect bugs.
    # Fail fast and visible.
    if not validate_url(url):
        raise ValueError(f"Invalid or missing url: {url}")

    start = time.now()

    # Avoid swallowing exceptions. If not possible, log them.
    response = response.get(url, raise_for_status=True)

    # Group conditions and their context 
    request_duration = time.now() - start
    if request_duration > settings.MAX_REQUEST_DURATION:
        # Add more context to errors.
        raise RuntimeError(f"Request duration excided maximum duration: {request_duration}.")

    # Check invalid usecases.
    if response.status_code != 200:
        raise RuntimeError(f"Service responded with {response.status_code} instead of 200.")

    return str(response.content) # Be consistent with returning type
```

Cheers 🍺!
