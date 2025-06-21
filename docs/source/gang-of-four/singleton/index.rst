=========
싱글턴 패턴
=========

*:doc:`/gang-of-four/index`의 "생성 패턴"*

.. admonition:: 결론

   파이썬 프로그래머는 :doc:`/gang-of-four/index`에 설명된 싱글턴 패턴을
   거의 구현하지 않습니다. 이 싱글턴 클래스는 일반적인 인스턴스화를 금지하고
   대신 싱글턴 인스턴스를 반환하는 클래스 메서드를 제공합니다.
   파이썬은 더 우아하며, 클래스가 일반적인 인스턴스화 구문을 계속 지원하도록 하면서
   싱글턴 인스턴스를 반환하는 사용자 정의 ``__new__()`` 메서드를 정의할 수 있도록 합니다.
   하지만 디자인이 싱글턴 객체에 대한 전역 액세스를 제공하도록 강제하는 경우,
   훨씬 더 파이썬다운 접근 방식은 대신 :doc:`/python/module-globals/index`를 사용하는 것입니다.

모호성 제거
======

파이썬은 객체 지향 디자인 패턴 커뮤니티에서
"싱글턴 패턴"이 정의되기 전부터 이미 *싱글턴*이라는 용어를 사용하고 있었습니다.
따라서 파이썬에서 "싱글턴"의 여러 의미를 구별하는 것부터 시작하겠습니다.

1. 길이가 1인 튜플을 *싱글턴*이라고 합니다.
   이 정의는 일부 프로그래머에게는 놀랍겠지만,
   수학에서 싱글턴의 원래 정의를 반영합니다.
   즉, 정확히 하나의 요소를 포함하는 집합입니다.
   파이썬 자습서 자체는 `데이터 구조
   <https://docs.python.org/3/tutorial/datastructures.html>`_ 장에서
   하나의 요소로 구성된 튜플을 "싱글턴"이라고 부르면서 이 정의를 초보자에게 소개하며,
   이 단어는 파이썬 설명서의 나머지 부분에서도 계속해서 그러한 의미로 사용됩니다.
   `확장 및 임베딩 <https://docs.python.org/3/extending/extending.html#calling-python-functions-from-c>`_
   가이드에서
   "하나의 인수로 파이썬 함수를 호출하려면 ...
   싱글턴 튜플을 전달하십시오."라고 말할 때,
   이는 정확히 하나의 항목을 포함하는 튜플을 의미합니다.

2. 파이썬에서 모듈은 "싱글턴"입니다.
   왜냐하면 ``import``는 각 모듈의 단일 복사본만 생성하기 때문입니다.
   동일한 이름의 후속 가져오기는 계속해서 동일한 모듈 객체를 반환합니다.
   예를 들어, 파이썬/C API 참조 설명서의
   `모듈 객체 <https://docs.python.org/3/c-api/module.html>`_ 장에서
   "단일 단계 초기화는 싱글턴 모듈을 생성합니다."라고 주장할 때,
   "싱글턴 모듈"이란 단 하나의 객체만 생성되는 모듈을 의미합니다.

3. "싱글턴"은 :doc:`/python/module-globals/index`를 통해
   전역 이름이 할당된 클래스 인스턴스입니다.
   예를 들어, 공식 파이썬 프로그래밍 FAQ는
   `“모듈 간에 전역 변수를 공유하려면 어떻게 해야 합니까?”
   <https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules>`_라는
   질문에 대해 파이썬에서는
   "모듈을 사용하는 것이 싱글턴 디자인을 구현하는 기초이기도 합니다."라고 답합니다.
   왜냐하면 모듈의 전역 네임스페이스는 상수(FAQ의 예는 여러 모듈간에 공유되는 ``x = 0``)뿐만 아니라
   변경 가능한 클래스 인스턴스도 저장할 수 있기 때문입니다.

4. :doc:`/gang-of-four/flyweight/index`의 예인
   개별 플라이웨이트 객체는 종종 파이썬 프로그래머에 의해
   "싱글턴" 객체라고 불립니다.
   예를 들어, 표준 라이브러리의 ``itertoolsmodule.c`` 내부 주석은
   "CPython의 빈 튜플은 싱글턴입니다."라고 주장합니다.
   이는 파이썬 인터프리터가 단일 빈 튜플 객체만 생성하며,
   길이가 0인 시퀀스가 전달될 때마다 ``tuple()``이 이 객체를
   계속해서 반환한다는 의미입니다.
   ``marshal.c``의 주석도 유사하게
   "빈 frozenset 싱글턴"을 참조합니다.
   그러나 이러한 싱글턴 객체 중 어느 것도 Gang of Four의 싱글턴 패턴의 예는 아닙니다.
   왜냐하면 어느 객체도 해당 클래스의 유일한 인스턴스가 아니기 때문입니다.
   ``tuple``은 빈 튜플 외에 다른 튜플을 만들 수 있도록 하며,
   ``frozenset``은 다른 고정된 세트를 만들 수 있도록 합니다.
   마찬가지로 ``True``와 ``False`` 객체는 한 쌍의 플라이웨이트이며,
   어느 것도 ``bool``의 유일한 인스턴스가 아니므로 싱글턴 패턴의 예가 아닙니다.

5. 마지막으로, 파이썬 프로그래머는 드물게
   객체를 "싱글턴"이라고 부를 때 실제로 "싱글턴 패턴"을 의미합니다.
   즉, 클래스가 호출될 때마다 해당 클래스에서 반환되는 유일한 객체입니다.

파이썬 2 표준 라이브러리에는 싱글턴 패턴의 예가 포함되어 있지 않았습니다.
``None`` 및 ``Ellipsis``와 같은 싱글턴 객체를 제공했지만,
언어는 ``__builtin__`` 모듈에 이름을 지정하여
더 파이썬다운 :doc:`전역 객체 패턴 </python/module-globals/index>`을 통해
액세스를 제공했습니다.
그러나 해당 클래스는 호출할 수 없었습니다.

::

    >>> type(None)
    <type 'NoneType'>
    >>> NoneType = type(None)
    >>> NoneType()
    TypeError: cannot create 'NoneType' instances
    >>> type(Ellipsis)()
    TypeError: cannot create 'ellipsis' instances

그러나 파이썬 3에서는 클래스가 싱글턴 패턴을 사용하도록 업그레이드되었습니다.

::

>>> NoneType = type(None)
>>> print(NoneType())
None
>>> type(Ellipsis)()
Ellipsis

이렇게 하면 항상 ``None``을 반환하는 빠른 호출 가능 객체가 필요한
프로그래머의 삶이 더 쉬워지지만, 그러한 경우는 드뭅니다.
대부분의 파이썬 프로젝트에서 이러한 클래스는 호출되지 않으며
이점은 순전히 이론적인 것으로 남아 있습니다.
파이썬 프로그래머가 ``None`` 객체가 필요할 때
:doc:`/python/module-globals/index`를 사용하고 단순히 이름을 입력합니다.

Gang of Four의 구현
===============

Gang of Four가 대상으로 삼았던 C++ 언어는
객체 생성에 다음과 같은 고유한 구문을 부과했습니다.

::

    # "new" 키워드가 있는 언어에서의
    # 객체 생성.

    log = new Logger()

``new``라고 표시된 C++ 줄은 항상 새 클래스 인스턴스를 생성하며,
싱글턴을 반환하지 않습니다.
이러한 특수 구문이 있는 경우,
싱글턴 객체를 제공하기 위한 옵션은 무엇이었을까요?

1. Gang of Four는 쉬운 방법을 택하지 않고
   :doc:`/python/module-globals/index`를 사용하지 않았습니다.
   왜냐하면 초기 버전의 C++ 언어에서는 잘 작동하지 않았기 때문입니다.
   거기서는 전역 이름이 모두 단일 혼잡한 전역 네임스페이스를 공유했으므로,
   다른 라이브러리의 이름이 충돌하는 것을 방지하기 위해
   정교한 명명 규칙이 필요했습니다.
   Gang은 클래스와 해당 싱글턴 인스턴스를 모두
   혼잡한 전역 네임스페이스에 추가하는 것은 과도하다고 판단했습니다.
   그리고 C++ 프로그래머는 전역 객체가 초기화되는 순서를
   제어할 수 없었으므로,
   어떤 전역 객체도 다른 전역 객체를 호출할 수 있다고 의존할 수 없었습니다.
   따라서 전역 객체 초기화의 책임은 종종 클라이언트 코드에 있었습니다.

2. C++에서 ``new``의 의미를 재정의할 방법이 없었으므로,
   모든 클라이언트가 동일한 객체를 받도록 하려면
   대체 구문이 필요했습니다.
   그러나 클래스 생성자를 ``protected`` 또는 ``private``으로 표시하여
   클라이언트 코드가 ``new``를 호출하는 것을 컴파일 시간 오류로 만드는 것은
   적어도 가능했습니다.

3. 그래서 Gang of Four는 클래스의 싱글턴 객체를 반환하는
   클래스 메서드로 전환했습니다.
   전역 함수와 달리 클래스 메서드는 전역 네임스페이스에
   또 다른 이름을 추가하는 것을 피했으며,
   정적 메서드와 달리 싱글턴인 서브클래스도 지원할 수 있었습니다.

파이썬 코드는 그들의 접근 방식을 어떻게 보여줄 수 있을까요?
파이썬에는 ``new``, ``protected`` 및 ``private``의 복잡성이 없습니다.
대안은 ``__init__()``에서 예외를 발생시켜
일반적인 객체 인스턴스화를 불가능하게 만드는 것입니다.
그런 다음 클래스 메서드는 던더 메서드 트릭을 사용하여
예외를 트리거하지 않고 객체를 생성할 수 있습니다.

.. testcode::

    # Gang of Four의 원래 싱글턴 패턴이
    # 파이썬에서 어떻게 보일 수 있는지 보여줍니다.

    class Logger(object):
        _instance = None

        def __init__(self):
            raise RuntimeError('대신 instance()를 호출하십시오.')

        @classmethod
        def instance(cls):
            if cls._instance is None:
                print('새 인스턴스 생성 중')
                cls._instance = cls.__new__(cls)
                # 여기에 초기화를 넣으십시오.
            return cls._instance

.. testcode::
   :hide:

   def fake_repr(self):
       return '<Logger object at 0x7f0ff5e7c080>'

   Logger.__repr__ = fake_repr

이렇게 하면 클라이언트가 클래스를 호출하여
새 인스턴스를 만드는 것을 성공적으로 방지합니다.

.. testcode::

    log = Logger()

.. testoutput::

    Traceback (most recent call last):
      ...
    RuntimeError: 대신 instance()를 호출하십시오.

대신 호출자는 ``instance()`` 클래스 메서드를 사용하도록 지시받으며,
이 메서드는 객체를 생성하고 반환합니다.

.. testcode::

    log1 = Logger.instance()
    print(log1)

.. testoutput::

    새 인스턴스 생성 중
    <Logger object at 0x7f0ff5e7c080>

후속 ``instance()`` 호출은 초기화 단계를 반복하지 않고
싱글턴을 반환합니다("새 인스턴스 생성 중"이 다시 인쇄되지 않는다는 사실에서 알 수 있듯이).
이는 Gang of Four가 의도한 대로 정확하게 작동합니다.

.. testcode::

    log2 = Logger.instance()
    print(log2)
    print('동일한 객체입니까?', log1 is log2)

.. testoutput::

    <Logger object at 0x7f0ff5e7c080>
    동일한 객체입니까? True

파이썬에서 원래 Gang of Four 클래스 메서드를 구현하기 위해
상상할 수 있는 더 복잡한 체계가 있지만,
위의 예가 가능한 한 최소한의 마법으로 원래 체계를
가장 잘 보여준다고 생각합니다.
Gang of Four의 패턴은 어쨌든 파이썬에 적합하지 않으므로,
더 이상 반복하려는 유혹을 참고
대신 파이썬에서 패턴이 가장 잘 지원되는 방법으로 넘어가겠습니다.

더 파이썬다운 구현
==========

어떤 의미에서 파이썬은 싱글턴 패턴에 대해 C++보다 더 잘 준비되어 시작했습니다.
왜냐하면 파이썬에는 새 객체를 강제로 생성하는 ``new`` 키워드가 없기 때문입니다.
대신 객체는 호출 가능 객체를 호출하여 생성되며,
이는 호출 가능 객체가 실제로 수행하는 작업에 대한 구문적 제한을 부과하지 않습니다.

::

    log = Logger()

작성자가 클래스 호출을 제어할 수 있도록 하기 위해
파이썬 2.4는 싱글턴 패턴 및 :doc:`/gang-of-four/flyweight/index`와 같은
대체 생성 패턴을 지원하기 위해 ``__new__()`` 던더 메서드를 추가했습니다.

웹에는 ``__new__()``를 특징으로 하는 싱글턴 패턴 레시피가 가득하며,
각각은 메서드의 가장 큰 단점, 즉 반환되는 객체가 새롭든 아니든
항상 반환 값에서 ``__init__()``이 호출된다는 사실을 해결하기 위한
다소 복잡한 메커니즘을 제안합니다.
내 예제를 간단하게 만들기 위해 ``__init__()`` 메서드를 정의하지 않고
따라서 해결할 필요가 없도록 하겠습니다.

.. testcode::

    # 싱글턴 패턴의 간단한 구현

    class Logger(object):
        _instance = None

        def __new__(cls):
            if cls._instance is None:
                print('객체 생성 중')
                cls._instance = super(Logger, cls).__new__(cls)
                # 여기에 초기화를 넣으십시오.
            return cls._instance

.. testcode::
   :hide:

   def fake_repr(self):
       return '<Logger object at 0x7fa8e9cf7f60>'

   Logger.__repr__ = fake_repr

객체는 클래스에 대한 첫 번째 호출에서 생성됩니다.

.. testcode::

    log1 = Logger()
    print(log1)

.. testoutput::

    객체 생성 중
    <Logger object at 0x7fa8e9cf7f60>

그러나 두 번째 호출은 동일한 인스턴스를 반환합니다.
"객체 생성 중" 메시지는 인쇄되지 않으며 다른 객체도 반환되지 않습니다.

.. testcode::

    log2 = Logger()
    print(log2)
    print('동일한 객체입니까?', log1 is log2)

.. testoutput::

    <Logger object at 0x7fa8e9cf7f60>
    동일한 객체입니까? True

위의 예는 일반적인 경우에 ``cls._instance`` 속성 조회를
두 번 수행하는 비용을 감수하면서 단순성을 선택합니다.
그러한 낭비에 몸서리치는 프로그래머를 위해
결과를 물론 이름에 할당하고 반환 문에서 재사용할 수 있습니다.
그리고 더 빠른 바이트 코드를 생성할 수 있는 다양한 다른 개선 사항을 상상할 수 있습니다.
그러나 아무리 정교하게 조정하더라도
위의 패턴은 일반적인 클래스 인스턴스화처럼 보이는 것 뒤에
싱글턴 객체를 숨기는 모든 파이썬 클래스의 기초입니다.

결론
==

Gang of Four의 원래 싱글턴 패턴은 ``new``, ``private`` 및 ``protected``와 같은
개념이 없는 파이썬과 같은 언어에는 적합하지 않지만,
``__new__()`` 위에 빌드될 때 패턴을 무시하기는 쉽지 않습니다 —
결국 싱글턴은 ``__new__()`` 던더 메서드가 도입된 이유 중 하나였습니다!

그러나 파이썬의 싱글턴 패턴에는 몇 가지 단점이 있습니다.

첫 번째 반론은 싱글턴 패턴의 구현이
많은 파이썬 프로그래머에게 읽기 어렵다는 것입니다.
대안인 :doc:`전역 객체 패턴 </python/module-globals/index>`은
읽기 쉽습니다. 단순히 익숙한 할당문이며 모듈의 최상위 수준에 배치됩니다.
그러나 ``__new__()`` 메서드를 처음 읽는 파이썬 프로그래머는
무슨 일이 일어나고 있는지 이해하기 위해 문서를 찾아봐야 할 것입니다.

두 번째 반론은 싱글턴 패턴이 ``Logger()``와 같은 클래스 호출을
독자에게 오해하게 만든다는 것입니다.
디자이너가 클래스 이름에 "싱글턴" 또는 다른 힌트를 넣지 않았고
독자가 힌트를 이해할 만큼 디자인 패턴을 잘 알지 못한다면,
코드는 새 인스턴스가 생성되어 반환되는 것처럼 읽힐 것입니다.

세 번째 반론은 싱글턴 패턴이 :doc:`/python/module-globals/index`가
그렇지 않은 디자인 약속을 강요한다는 것입니다.
전역 객체를 제공하면 프로그래머는 여전히 클래스의 다른 인스턴스를
자유롭게 만들 수 있습니다. 이는 특히 테스트에 유용하며,
공유 객체를 알려진 양호한 상태로 재설정할 필요 없이
각각 완전히 별개의 객체를 테스트할 수 있도록 합니다.
그러나 싱글턴 패턴은 추가 인스턴스를 불가능하게 만듭니다.
(호출자가 몽키 패치에 기꺼이 참여하거나,
``__new__()``의 논리를 전복시키기 위해 ``_instance``를 일시적으로 수정하거나,
메서드를 대체하는 서브클래스를 만들지 않는 한 말입니다.
그러나 해결해야 할 패턴은 일반적으로 피해야 할 패턴입니다.)

그렇다면 왜 파이썬에서 싱글턴 패턴을 사용해야 할까요?

패턴이 정말로 필요한 한 가지 상황은
새로운 요구 사항으로 인해 이제 단일 인스턴스로 가장 잘 작동하는
기존 클래스일 것입니다.
모든 클라이언트 코드를 마이그레이션하여 클래스를 직접 호출하는 것을 중단하고
전역 객체를 사용하기 시작하는 것이 불가능하다면,
싱글턴 패턴은 이전 구문을 유지하면서 싱글턴으로 전환하는
자연스러운 접근 방식이 될 것입니다.

그러나 그렇지 않으면 `공식 파이썬 FAQ
<https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules>`_의
조언을 따르고 :doc:`/python/module-globals/index`를 사용하는 것이 좋습니다.

.. See also

   Lib/pydoc_data/topics.py
   Doc/library/marshal.rst:46:singletons :const:`None`, and :exc:`StopIteration` can also be
   Doc/c-api/module.rst:258:singletons: if the *sys.modules* entry is removed and the module is re-imported,
   Doc/library/enum.rst:1026:The most interesting thing about Enum members is that they are singletons.
