======================
 반복자 패턴
======================

*:doc:`/gang-of-four/index`의 "행동 패턴"*

.. admonition:: 결론

   파이썬은 프로그래밍 언어에 사용 가능한 가장 근본적인 수준에서
   반복자 패턴을 지원합니다:
   파이썬 구문에 내장되어 있습니다.

   그러나 객체 기반 반복자 패턴뿐만 아니라
   자체 레거시 반복 프로토콜도 지원하기 위해,
   파이썬은 실제 반복 객체 프로토콜을
   한 쌍의 던더 메서드로 격하시킵니다.
   이를 직접 호출하는 대신,
   프로그래머는 한 쌍의 내장 함수를 통해
   반복을 호출해야 합니다.

가장 표현력이 낮은 컴퓨터 언어는
데이터 구조의 내부 작동을 숨기려는 시도를 하지 않습니다.
이러한 언어에서는
배열의 모든 요소를 방문하려면
정수 인덱스를 직접 생성해야 합니다.

이러한 언어의 코드는 프로그래머의 의도를 설명하는
높은 수준을 유지하기 위해 애씁니다.
대신 각 생각의 흐름은
낮은 수준의 데이터 구조 세부 정보로 중단됩니다.
코드가 반복 메커니즘을 추상화할 수 없으면
읽기가 더 어려워집니다.
동일한 반복 세부 정보가 반복적으로 반복되어야 하므로
오류가 발생하기 쉽습니다.
그리고 데이터 구조를 순회하는 방식을 변경하려면
해당 데이터 구조가 반복되는 코드의 모든 위치를 찾아 변경해야 합니다.

해결책은 캡슐화입니다.
반복자 패턴은
데이터 구조를 순회하는 방법에 대한 세부 정보가
외부에서는 데이터 구조가 설계된 방식의 내부를 노출하지 않고
단순히 항목을 차례로 생성하는 "반복자" 객체로
이동되어야 한다고 제안합니다.

"for" 루프를 사용한 반복
=============================

파이썬의 ``for`` 루프는
반복자 패턴을 너무 철저하게 추상화하여
대부분의 파이썬 프로그래머는
그것이 표면 아래에서 실행하는 객체 디자인 패턴을
인식조차 하지 못합니다.
``for`` 루프는 반복 할당을 수행하며,
반복하는 시퀀스의 각 항목에 대해
들여쓰기된 코드 블록을 한 번 실행합니다.

.. testcode::

   some_primes = [2, 3, 5]
   for prime in some_primes:
       print(prime)

.. testoutput::

   2
   3
   5

위의 루프는 ``prime = 2``, ``prime = 3``, ``prime = 5``의
세 가지 할당문을 수행했으며,
각 할당 후 들여쓰기된 코드 블록을 실행했습니다.
블록에는 루프를 일찍 종료하는 C 스타일 루프 제어문 ``break``와
루프의 맨 위로 다시 건너뛰는 ``continue``가 포함될 수 있습니다.

.. TODO 루프 작성 가이드를 작성하고 여기에 링크합니다.

``for``는 반복 할당문이므로
파이썬의 일반적인 ``=`` 할당 연산자와 동일한 유연성을 갖습니다.
쉼표로 구분된 여러 이름을 나열하여
단일 이름에 할당하는 것에서 전체 튜플을 언패킹하는 것으로
업그레이드할 수 있습니다.
이렇게 하면 별도의 언패킹 단계를 건너뛸 수 있습니다.

.. testcode::

   elements = [('H', 1.008), ('He', 4.003), ('Li', 6.94)]

   # "tup"과 같은 단일 이름으로 제한되지 않습니다...
   for tup in elements:
       symbol, weight = tup
       print(symbol, weight)

   # ...대신 "for" 문 안에서 바로 언패킹합니다.
   for symbol, weight in elements:
       print(symbol, weight)

.. testoutput::
   :hide:

   H 1.008
   He 4.003
   Li 6.94
   H 1.008
   He 4.003
   Li 6.94

잘 알려진 바와 같이, 이것은 파이썬 딕셔너리의 ``item()`` 메서드와 결합되어
각 루프의 맨 위에서 키 조회를 하는 비용 없이
각 딕셔너리 키와 값을 쉽게 방문할 수 있습니다.

.. testcode::

   d = {'H': 1.008, 'He': 4.003, 'Li': 6.94}

   # 그럴 필요가 없습니다...
   for symbol in d.keys():
       weight = d[symbol]
       print(symbol, weight)

   # ...대신 간단히 다음을 수행할 수 있습니다.
   for symbol, weight in d.items():
       print(symbol, weight)

.. testoutput::
   :hide:

   H 1.008
   He 4.003
   Li 6.94
   H 1.008
   He 4.003
   Li 6.94

``for`` 루프는 매우 훌륭한 간결성과 표현력을 결합하여
파이썬은 이를 독립 실행형 문으로 지원할 뿐만 아니라
네 가지 다른 표현식에 통합했습니다 —
인라인 루프에서 직접 리스트, 세트, 딕셔너리 및
제너레이터를 빌드하는 파이썬의 유명한 "컴프리헨션"입니다.

.. testcode::

   [symbol for symbol, weight in d.items() if weight > 5]
   {symbol for symbol, weight in d.items() if weight > 5}
   {symbol: weight for symbol, weight in d.items() if weight > 5}
   list(symbol for symbol, weight in d.items() if weight > 5)

표현식 내에서 ``for`` 문 구문을 재사용하기로 한 파이썬의 결정 —
인라인 반복을 위한 별도의 특수 목적 구문을 고안하는 수고를 덜었습니다 —
언어를 더 간단하고 배우기 쉽고 기억하기 쉽게 만듭니다.

패턴: 반복 가능 객체와 반복자
==========================================

이제 ``for`` 루프 뒤로 물러나
그것을 구동하는 디자인 패턴에 대해 알아봅시다.
전통적인 반복자 패턴에는 세 가지 종류의 객체가 포함됩니다.

첫째, *컨테이너* 객체가 있습니다.

둘째, 컨테이너의 내부 로직을 통해
여러 *항목* 객체를 모으고 구성할 수 있습니다.

마지막으로 패턴의 핵심이 있습니다.
컨테이너가 항목을 단계별로 실행하기 위한 고유한 메서드 호출을 고안하는 대신 —
이렇게 하면 프로그래머가 모든 컨테이너에 대해 다른 접근 방식을 배워야 합니다 —
다른 모든 종류의 컨테이너의 반복자와
정확히 동일한 인터페이스를 구현하는
일반 *반복자* 객체를 통해 항목에 순차적으로 액세스할 수 있도록 합니다.

파이썬은 ``for`` 루프 뒤로 물러나
직접 반복 레버를 당길 수 있는 한 쌍의 내장 함수를 제공합니다.

* ``iter()``는 컨테이너 객체를 인수로 받아
  새 반복자 객체를 빌드하고 반환하도록 요청합니다.
  전달한 인수가 실제로 컨테이너가 아니면
  ``TypeError``가 발생합니다: ``object is not iterable``.

* ``next()``는 반복자를 인수로 받아
  호출될 때마다 컨테이너에서 다음 항목을 반환합니다.
  컨테이너에 더 이상 반환할 객체가 없으면
  예외 ``StopIteration``이 발생합니다.

이전 섹션의 첫 번째 ``for`` 루프를 수동으로 다시 실행하려면
``iter()``를 한 번 호출한 다음 ``next()``를 네 번 호출합니다.

>>> it = iter(some_primes)
>>> it
<list_iterator object at 0x7f072ffdb518>
>>> print(next(it))
2
>>> print(next(it))
3
>>> print(next(it))
5
>>> print(next(it))
Traceback (most recent call last):
  ...
StopIteration

이것들은 정확히 파이썬의 ``for`` 루프가 수행한 작업입니다.
물론 실제 ``for`` 루프는
여기서 했던 것처럼 정확한 수의 ``next()`` 호출을 하드 코딩하지 않습니다 —
대신 ``for``는 다음과 같은 ``while`` 루프와 유사하게 구현됩니다.

.. testcode::

   it = iter(some_primes)
   while True:
       try:
           prime = next(it)
       except StopIteration:
           break
       else:
           print(prime)

.. testoutput::

   2
   3
   5

반복자 패턴을 처음 배웠을 때의 첫 번째 질문은 다음과 같습니다.
왜 반복자가 컨테이너와 별개의 객체여야 할까요?
왜 각 컨테이너가 다음에 생성할 객체를 알려주는
카운터를 내부에 단순히 포함할 수 없을까요?

답은 한 번에 하나의 ``for`` 루프만
컨테이너를 반복하는 한 단일 내부 카운터가 작동한다는 것입니다.
그러나 여러 ``for`` 루프가
동시에 동일한 컨테이너에서 작동하는 경우가 많습니다.
예를 들어, 두 동전 던지기의 모든 조합을 생성하기 위해
프로그래머는 중첩 루프를 작성할 수 있습니다.

.. testcode::

   sides = ['heads', 'tails']
   for coin1 in sides:
       for coin2 in sides:
           print(coin1, coin2)

.. testoutput::

    heads heads
    heads tails
    tails heads
    tails tails

파이썬 리스트 객체 ``sides``가
단일 내부 카운터만 사용하여 반복을 지원하려고 했다면,
내부 ``for`` 루프가 모든 항목을 사용하고
외부 ``for`` 루프에는 방문할 추가 항목이 남지 않았을 것입니다.
대신 ``iter()``를 호출할 때마다 별도의 반복자가 제공됩니다.

>>> it1 = iter(sides)
>>> it2 = iter(sides)
>>> it1
<list_iterator object at 0x7fa8b8b292b0>
>>> it2
<list_iterator object at 0x7fa8b8b29400>
>>> it1 is it2
False

중첩 루프뿐만 아니라 여러 제어 스레드 —
운영 체제 스레드이든 코루틴이든 —
객체가 동시에 여러 ``for`` 루프에 의해 작동될 수 있는
많은 상황을 제공하므로,
이러한 각 ``for`` 루프는 서로를 방해하지 않도록
자체 반복자가 필요합니다.

변형: 자체 반복자인 객체
=============================================

일반적인 파이썬 컨테이너(리스트, 세트 또는 딕셔너리 등)를
``iter()``에 전달할 때마다
컨테이너의 항목을 처음부터 다시 방문하기 시작하는
새로운 반복자 객체를 받습니다.

그러나 일부 파이썬 객체는 다른 동작을 보입니다.

파이썬 파일 객체가 좋은 예입니다.
``for`` 루프를 사용하여 반복할 때 편리하게 텍스트 줄을 생성합니다.
그러나 리스트나 딕셔너리와 달리
새 ``for`` 루프로 순회할 때 첫 번째 줄부터 다시 시작하지 않습니다.
대신 파일에서 이전 위치를 기억하고
이전에 중단한 위치에서 줄을 계속 생성합니다.

파일이 중단된 지점에서 다시 시작한다는 사실을 사용하여
파일을 단계별로 반복할 수 있습니다.
여러 섹션으로 구성된 파일 형식의 간단한 예는
전통적인 UNIX 메일박스 파일입니다.

.. literalinclude:: email.txt

이 파일은 각 섹션이 다른 규칙으로 구분되므로
세 단계로 구문 분석해야 합니다.
단어 ``From``으로 시작하는 초기 "봉투 줄"은
항상 단일 독립 실행형 줄입니다.
헤더가 뒤따르며,
콜론으로 구분된 이름과 값의 연속으로 구성되며
단일 빈 줄로 끝납니다.
본문이 마지막에 오고
다음 봉투 ``From`` 줄 또는 파일 끝에서 끝납니다.
다음은 ``for`` 루프만 사용하여 메일박스 파일에서
첫 번째 메시지를 구문 분석하는 방법입니다.

.. testsetup::

   import os
   os.chdir('gang-of-four/iterator')

.. testcode::

   def parse_email(f):
       for line in f:
           envelope = line
           break
       headers = {}
       for line in f:
           if line == '\n':
               break
           name, value = line.split(':', 1)
           headers[name.strip()] = value.lstrip().rstrip('\n')
       body = []
       for line in f:
           if line.startswith('From'):
               break
           body.append(line)
       return envelope, headers, body

이 편리한 패턴 —
파일의 각 섹션을 자체 ``for`` 루프로 처리하고
섹션 처리가 완료되면 ``break``를 수행합니다 —
다른 루프를 시작할 때마다
파일 객체가 중단된 지점에서 바로 읽기를 계속하기 때문에 가능합니다.

.. testcode::

   with open('email.txt') as f:
       envelope, headers, body = parse_email(f)

   print(headers['To'])
   print(len(body), 'lines')

.. testoutput::

   Mary Smith <mary@example.net>
   2 lines

파일 객체는 일반적인 반복을 어떻게 방해하고
한 ``for`` 루프와 다음 루프 사이의 상태를 유지할까요?

``for`` 루프 뒤로 물러나 ``iter()``를 직접 호출하고
결과를 검사하여 답을 볼 수 있습니다.

>>> f = open('email.txt')
>>> f
<_io.TextIOWrapper name='email.txt' mode='r' encoding='UTF-8'>
>>> it1 = iter(f)
>>> it1
<_io.TextIOWrapper name='email.txt' mode='r' encoding='UTF-8'>
>>> it2 = iter(f)
>>> it2
<_io.TextIOWrapper name='email.txt' mode='r' encoding='UTF-8'>
>>> it1 is it2 is f
True

파일 객체는 기술적인 세부 사항을 활용하고 있습니다.
``iter()``가 반복자를 반환해야 한다는 규칙은
반복자가 반복 가능한 객체 자체가 될 수 없다고 말하지 않습니다!
파일에서 다음 줄을 반환해야 하는 줄을 추적하기 위해
별도의 반복자 객체를 만드는 대신,
파일 자체가 자체 반복자 역할을 하며
단일 연속적인 줄 시리즈를 생성하여
가능한 여러 소비자 중 ``next()``를 먼저 호출하는 소비자에게
사용 가능한 다음 줄을 전달합니다.

파일 객체의 경우,
반복 가능 객체와 반복자를 단일 객체로 통합하기로 한 결정은
기본 운영 체제의 동작에 의해 주도됩니다.
결국 모든 종류의 파일이 되감기 및 빨리 감기를 지원하는 것은 아닙니다 —
예를 들어 Unix 터미널과 파이프는 지원하지 않습니다 —
따라서 파이썬 파일 객체는 단순히 운영 체제가
현재 줄을 추적하도록 하고 자체적으로 되감기를 시도하지 않습니다.

그러나 파일뿐만 아니라 다른 종류의 객체에 대해서도
여러 단계로 반복하는 기능을 원한다면 어떻게 해야 할까요?

예를 들어, ``parse_email()``에 일반적인 줄 목록을 전달하면 어떻게 될까요?
그러면 루틴이 중단됩니다 — 두 번째와 세 번째 ``for`` 루프가
이전 루프가 중단된 지점에서 계속하는 대신
목록의 처음부터 다시 시작하기 때문입니다.
다른 문제 중에서도
이렇게 하면 함수가 이메일 본문을 찾지 못하게 됩니다.

.. testcode::

   with open('email.txt') as f:
       lines = list(f)

   envelope, headers, body = parse_email(lines)
   print(headers['To'])
   print(len(body), 'lines')

.. testoutput::

   Mary Smith <mary@example.net>
   0 lines

파이썬 리스트와 같은 표준 컨테이너에 대한
점진적인 반복을 어떻게 지원할 수 있을까요?

답은 전통적인 반복자 패턴에 대한 또 다른 확장입니다.
파이썬에서는 반복자가 ``iter()``에 전달되면 자신을 반환합니다!
즉, 반복자 자체를 ``for`` 루프에 전달할 수 있으며,
``next()``를 사용한 수동 단일 단계와
``for`` 루프를 사용한 자동 반복 사이를
원할 때마다 전환하는 프로그램을 작성할 수 있습니다.

.. testcode::

   it = iter(some_primes)
   print(next(it))
   for prime in it:
       print(prime)
       break
   print(next(it))

.. testoutput::

   2
   3
   5

위의 코드는 ``iter()``로 직접 요청한 단일 반복자만 처리하므로,
수동 ``next()`` 호출과 ``for()`` 루프 모두
기본 목록의 3개 항목을 통해 동일한 반복자를 진행시키고 있습니다.
``for`` 루프는 반복자 객체 ``it``이
반복자를 요청받았을 때 자신을 반환하기 때문에 작동합니다.

>>> it
<list_iterator object at 0x7f4fdce6c5f8>
>>> iter(it)
<list_iterator object at 0x7f4fdce6c5f8>
>>> iter(it) is it
True

따라서 기본 목록을 전달하는 대신
이미 생성한 반복자를 전달하면
파이썬 목록과 함께 ``parse_email()`` 루틴을 성공적으로 사용할 수 있습니다.
이렇게 변경하면 루틴은 열린 파일에서 원래 그랬던 것처럼
목록에서도 성공적으로 실행됩니다.

.. testcode::

   with open('email.txt') as f:
       lines = list(f)

   it = iter(lines)
   envelope, headers, body = parse_email(it)
   print(headers['To'])
   print(len(body), 'lines')

.. testoutput::

   Mary Smith <mary@example.net>
   2 lines

``parse_email()``과 같은 루틴을 실제로 구현하는 경우,
호출자에게 반복자를 전달하도록 기억하게 하는 것보다
컨테이너를 전달하고 ``iter()``를 직접 호출하는 것이 좋습니다.

반복 가능 객체 및 반복자 구현
=====================================

클래스가 반복자 패턴을 구현하고
파이썬의 기본 반복 메커니즘인
``for``, ``iter()`` 및 ``next()``에 연결하려면 어떻게 해야 할까요?

* 컨테이너는 반복자 객체를 반환하는 ``__iter__()`` 메서드를 제공해야 합니다.
  이 메서드를 지원하면 컨테이너가 *반복 가능 객체*가 됩니다.

* 각 반복자는 컨테이너에서 호출될 때마다 다음 항목을 반환하는
  ``__next__()`` 메서드(이전 파이썬 2 코드에서는 던더 없는 ``next()`` 철자)를
  제공해야 합니다.
  더 이상 항목이 없으면 ``StopIteration``을 발생시켜야 합니다.

* 이전 섹션에서 배운 특수한 경우를 기억하십시오 —
  일부 사용자는 기본 컨테이너를 전달하는 대신
  반복자를 ``for`` 루프에 전달합니다.
  이 경우를 처리하기 위해 각 반복자는 단순히 자신을 반환하는
  ``__iter__()`` 메서드도 제공해야 합니다.

자체 간단한 반복자를 구현하여
이러한 모든 요구 사항이 함께 작동하는 것을 볼 수 있습니다!

``__next__()``에 의해 생성된 항목이
컨테이너 내부에 영구 값으로 저장되거나
``__next__()``가 호출될 때까지 존재해야 한다는 요구 사항은 없습니다.
이를 통해 컨테이너에 스토리지를 구현하지 않고도
매우 간단한 반복자 패턴 예제를 제공할 수 있습니다.

.. testcode::

   class OddNumbers(object):
       "An iterable object."

       def __init__(self, maximum):
           self.maximum = maximum

       def __iter__(self):
           return OddIterator(self)

   class OddIterator(object):
       "An iterator."

       def __init__(self, container):
           self.container = container
           self.n = -1

       def __next__(self):
           self.n += 2
           if self.n > self.container.maximum:
               raise StopIteration
           return self.n

       def __iter__(self):
           return self

이러한 세 가지 간단한 메서드(컨테이너 객체용 하나,
반복자용 두 개)를 사용하면
``OddNumbers`` 컨테이너는 이제
파이썬의 풍부한 반복 생태계에 대한 전체 멤버십을 받을 수 있습니다.
``for`` 루프와 원활하게 작동합니다.

.. testcode::

   numbers = OddNumbers(7)

   for n in numbers:
       print(n)

.. testoutput::

   1
   3
   5
   7

그리고 ``iter()`` 및 ``next()`` 내장 함수와도 작동합니다.

.. testcode::

   it = iter(OddNumbers(5))
   print(next(it))
   print(next(it))

.. testoutput::

   1
   3

그리고 컴프리헨션과도 춤을 출 수 있습니다!

.. testcode::

   print(list(numbers))
   print(set(n for n in numbers if n > 4))

.. testoutput::

    [1, 3, 5, 7]
    {5, 7}

세 가지 간단한 메서드만 있으면
파이썬의 구문 수준 반복 지원에 액세스할 수 있습니다.

파이썬의 추가 간접 수준
===================================

그러나 한 가지 질문이 있습니다.
왜 파이썬에는 ``iter()``와 ``next()``가 있을까요?

프로그래밍 언어의 더 넓은 세계에서
표준 반복 패턴에는 내장 함수가 포함되지 않습니다.
대신 패턴은 객체 동작에 대해 직접 이야기합니다.
컨테이너는 하나의 메서드를 구현해야 하고,
반복 가능 객체는 다른 메서드를 구현해야 합니다.
왜 파이썬은 단순히 메서드 이름 자체를 지정하고
사용자가 잘 알려진 ``obj.method()`` 표기법을 사용하여
직접 호출하도록 하지 않았을까요?

그 이유는 파이썬이 지원해야 할 레거시 반복 메커니즘이 있었기 때문입니다.

원래 파이썬의 ``for`` 루프는
파이썬 리스트 및 튜플과 같이 정수 인덱싱된 컨테이너만 지원했습니다.
기본 작업은 다음과 같습니다.

>>> some_primes[0]
2
>>> some_primes[1]
3
>>> some_primes[2]
5
>>> some_primes[3]
Traceback (most recent call last):
  ...
IndexError: list index out of range

원래 파이썬 ``for`` 루프에 완료되었음을 알린 것은
마지막 ``IndexError``였습니다.
딕셔너리와 같이 순차적 정수 인덱스로 항상 주소 지정할 수 없는
컨테이너를 반복하려면
먼저 키, 값 또는 항목의 ``list``를 요청한 다음
정수 인덱싱된 리스트 객체를 반복해야 했습니다 —
정수 인덱스가 ``for`` 루프가 이해하는 전부였기 때문입니다.

`PEP-234 <https://www.python.org/dev/peps/pep-0234/>`_가
파이썬 2.2에 반복자 패턴을 통합할 때가 되었을 때
문제가 있었습니다.
``for`` 루프가 이제 주어진 컨테이너에서 ``__iter__()``를 호출하기 시작하면
프로그래머가 수년에 걸쳐 빌드한 모든 간단한 컨테이너에
무슨 일이 일어날까요 —
정수 인덱스를 받아들이고 반복 가능하다고 믿었던 컨테이너 말입니다.

다행히도 컴퓨터 과학의 모든 문제는
또 다른 간접 수준으로 해결할 수 있습니다!\ `¹ <https://en.wikipedia.org/wiki/Indirection>`_

파이썬은 사용자와 언어가 두 가지 반복 패턴을 특징으로 한다는
불행한 사실 사이에 한 쌍의 내장 함수를 삽입하기로 결정했습니다 —
하나는 레거시이고 다른 하나는 객체 기반 반복자 패턴 자체입니다.
PEP는 다음과 같이 규정했습니다.

* ``for`` 루프는 이제 반복자 패턴을 선호합니다.
  컨테이너가 ``__iter__()``를 제공하면
  ``for`` 루프는 반환된 반복자를 사용합니다.

* 이전 컨테이너를 지원하기 위해
  ``for``는 ``__getitem__()`` 메서드를 찾는 것으로 대체되고,
  존재하는 경우 정수 0, 1, 2, …를 전달하여 항목을 받고
  ``IndexError``를 받을 때까지 계속합니다.

* 모든 프로그래머가 이 신중하게 만들어진 대체 방법을
  직접 구현할 필요 없이 이 메커니즘을 파이썬 프로그래머에게 노출하기 위해
  ``iter()``가 도입되었습니다.
  이를 통해 프로그래머는 기본 작업인
  "반복 가능 객체에서 반복자 만들기"에 액세스할 수 있으며,
  그렇지 않으면 ``for`` 루프 자체에서만 기본적으로 사용할 수 있었습니다.

* 마지막으로, 반복자 패턴의 양쪽 절반(컨테이너 절반뿐만 아니라)이
  대칭적으로 내장 함수로 처리되도록
  나중에 파이썬 버전에 ``next()``가 추가되었습니다.

그 과정에서 그들은 또한 ``iter()``에
하나가 아닌 두 개의 인수를 전달하는 것과 관련된
모호한 편의 기능을 추가했습니다.
고전적인 반복자 패턴 자체와는 관련이 없으므로
궁금하다면 ``iter()``에 대한
`표준 라이브러리 설명서 <https://docs.python.org/3/library/functions.html#iter>`_에서
읽어보고 직접 실험해 보시기 바랍니다.

.. testcleanup::

   os.chdir('../..')
