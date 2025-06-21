=============
플라이웨이트 패턴
=============

*:doc:`/gang-of-four/index`의 "구조 패턴"*

.. admonition:: 결론

   플라이웨이트 객체는 파이썬에 매우 적합하여
   언어 자체가 식별자, 일부 정수, 부울 참 및 거짓과 같은
   널리 사용되는 값에 대해 이 패턴을 사용합니다.

.. TODO "싱글톤"과 혼동된다는 점을 언급하십시오.
   모호성 제거 섹션이 작성되면

플라이웨이트 패턴의 완벽한 예는
파이썬 |intern|_ 함수입니다.
파이썬 2에서는 내장 함수였지만
파이썬 3에서는 |sys|_ 모듈로 이동했습니다.
문자열을 전달하면 정확히 동일한 문자열을 반환합니다.
장점은 공간을 절약한다는 것입니다.
``'xyzzy'``와 같은 특정 값에 대해 얼마나 많은 다른 문자열 객체를 전달하든
매번 동일한 ``'xyzzy'`` 객체를 반환합니다.

파이썬 내부에서 메모리를 절약하는 데 사용됩니다.
파이썬이 프로그램을 구문 분석할 때
``range``와 같은 지정된 식별자를 여러 번 만날 가능성이 높습니다.
각각을 별도의 문자열 객체로 저장하는 대신
``intern()``을 사용하여 코드의 모든 ``range`` 언급이
모두를 나타내는 단일 문자열 객체를 메모리에서 공유할 수 있도록 합니다.

두 가지 다른 방식으로 문자열 ``'python'``을 계산하여
(지정된 파이썬 구현이 실제로 두 개의 다른 문자열을 제공할 가능성이 높도록)
해당 동작을 확인하고 intern 함수에 전달할 수 있습니다.

.. |intern| replace:: ``intern()``
.. _intern: https://docs.python.org/3/library/sys.html#sys.intern

.. |sys| replace:: ``sys``
.. _sys: https://docs.python.org/3/library/sys.html

::

>>> from sys import intern  # 파이썬 2에서는 필요하지 않음
>>> a = intern('py' + 'thon')
>>> b = intern('PYTHON'.lower())
>>> a
'python'
>>> b
'python'
>>> a is b
True

문자열은 플라이웨이트 객체의 세 가지 주요 속성을 모두 가지고 있기 때문에
플라이웨이트 패턴의 자연스러운 후보입니다.

* 파이썬 문자열은 불변이므로 공유하기에 안전합니다.
  그렇지 않으면 문자열의 문자 중 하나를 변경하기로 결정한 루틴이
  다른 모든 사람과 공유되는 단일 복사본에 영향을 미칩니다.

* 파이썬 문자열은 사용 방법에 대한 컨텍스트를 전달하지 않습니다.
  사용 중인 목록, 사전 또는 기타 객체에 대한 참조를
  유지해야 하는 경우 각 문자열은 한 번에 하나의 컨텍스트에서만
  사용할 수 있습니다.

* 문자열은 객체 ID가 아닌 값으로 중요합니다.
  ``is`` 키워드 대신 ``==``로 비교합니다.
  잘 작성된 파이썬 프로그램은 한 곳에서 디렉터리 이름으로 사용되고
  다른 곳에서 사용자 이름으로 사용되는 문자열 ``"brandon"``이
  동일한 객체인지 아니면 두 개의 다른 객체인지조차 알아차리지 못합니다.

갱 오브 포는 "대부분의 객체 상태를 외부화할 수 있다"고 요구할 때
이러한 동일한 요구 사항을 약간 다르게 설명합니다.
그들은 "외부" 및 "내부" 상태라고 부르는 것의 혼합인 객체로 시작한다고 상상합니다.

    a1 = Glyph(width=6, ascent=9, descent=3, x=32, y=8)
    a2 = Glyph(width=6, ascent=9, descent=3, x=8, y=60)

서체와 크기가 주어지면 지정된 문자의 각 발생(예: 문자 *M*)은
동일한 너비, 기준선 위의 동일한 상승 및
그 아래의 동일한 하강을 갖습니다.
갱 오브 포는 이러한 속성을 문자 *M*이 되는 것의 "내부"라고 부릅니다.
그러나 페이지의 각 *M*은 다른 ``x`` 및 ``y`` 좌표를 갖습니다.
해당 상태는 "외부"이며 문자의 발생마다 다릅니다.

내부 및 외부 상태가 혼합된 객체가 주어지면
갱 오브 포는 두 종류의 상태를 분리하기 위해 리팩터링하여
플라이웨이트에 도달합니다.

    a = Glyph(width=6, ascent=9, descent=3)
    a1 = DrawnGlyph(glyph=a, x=32, y=8)
    a2 = DrawnGlyph(glyph=a, x=8, y=60)

플라이웨이트 패턴으로 인한 공간 절약이 상당할 뿐만 아니라,
`플라이웨이트를 소개하는 1990년 원본 논문 <https://www.researchgate.net/profile/Mark_Linton2/publication/220877079_Glyphs_flyweight_objects_for_user_interfaces/links/58adbb6345851503be91e1dc/Glyphs-flyweight-objects-for-user-interfaces.pdf?origin=publication_detail>`_에서는
패턴을 사용하여 작성된 문서 편집기의 코드가
상당히 단순하다는 것을 발견했습니다.

팩토리 또는 생성자
==========

갱 오브 포는 플라이웨이트 모음을 관리하기 위해 |intern|과 같은
팩토리 함수를 사용하는 것만 상상했지만,
파이썬은 종종 대신 클래스의 생성자로 논리를 이동합니다.

파이썬에서 가장 간단한 예는 ``bool`` 타입입니다.
정확히 두 개의 인스턴스가 있습니다.
내장 이름 ``True`` 및 ``False``를 통해 액세스할 수 있지만,
진실성 또는 거짓성을 테스트할 객체가 전달될 때
클래스에서도 반환됩니다.

::

>>> bool(0)
False
>>> bool('')
False
>>> bool(12)
True

또 다른 예는 정수입니다.
구현 세부 정보로서 파이썬의 기본 C 언어 버전은
-5부터 256까지의 정수를 플라이웨이트로 처리합니다.
이러한 정수는 인터프리터가 시작될 때 미리 생성되며,
해당 값을 가진 정수가 필요할 때 반환됩니다.
다른 정수 값을 계산하면 각 계산에서 고유한 객체가 생성됩니다.

::

>>> 1 + 4 is 2 + 3
True
>>> 100 + 400 is 200 + 300
False

빈 문자열 및 빈 튜플과 같이 매우 일반적인 불변 객체에 대해
표준 라이브러리에 숨겨진 몇 가지 다른 플라이웨이트가 있습니다.

::

>>> str() is ''
True
>>> tuple([]) is ()
True

인터프리터가 미리 빌드한 모든 객체가
플라이웨이트로 인정되는 것은 아니라는 점에 유의하십시오.
예를 들어 ``None`` 객체는 인정되지 않습니다.
클래스가 진정한 플라이웨이트가 되려면 둘 이상의 인스턴스가 필요하지만,
``None``은 ``NoneType``의 유일한 인스턴스입니다.

구현
==

가장 간단한 플라이웨이트는 미리 할당됩니다.
학점 할당 시스템은 학점 자체에 대해
플라이웨이트를 사용할 수 있습니다.

.. testcode::

   _grades = [letter + suffix
              for letter in 'ABCD'
              for suffix in ('+', '', '-')] + ['F']

   def compute_grade(percent):
       percent = max(59, min(99, percent))
       return _grades[(99 - percent) * 3 // 10]

   print(compute_grade(55))
   print(compute_grade(89))
   print(compute_grade(90))

.. testoutput::

    F
    B+
    A-

플라이웨이트 모집단을 동적으로 빌드해야 하는 팩토리는
더 복잡합니다.
플라이웨이트를 등록하고 나중에 다시 찾을 수 있는
동적 데이터 구조가 필요합니다.
일반적으로 사전을 선택합니다.

.. testcode::

   _strings = {}

   def my_intern(string):
       s = _strings.setdefault(string, string)
       return s

   a1 = my_intern('A')
   b1 = my_intern('B')
   a2 = my_intern('A')

   print(a1 is b1)
   print(a1 is a2)

.. testoutput::

   False
   True

동적으로 할당된 플라이웨이트의 한 가지 위험은
가능한 값의 수가 매우 많고
호출자가 프로그램 런타임 동안 많은 고유한 값을 요청할 수 있는 경우
결국 메모리가 고갈될 가능성입니다.
이러한 경우 ``weakref`` 모듈의 |WeakValueDictionary|를 사용하는 것을
고려할 수 있습니다.

.. |WeakValueDictionary| replace:: ``WeakValueDictionary``
.. _WeakValueDictionary: https://docs.python.org/3/library/weakref.html#weakref.WeakValueDictionary

약한 참조는 위에서 주어진 간단한 예에서는 작동하지 않습니다.
왜냐하면 ``my_intern``은 각 인턴된 문자열을
값뿐만 아니라 해당 키로도 사용하기 때문입니다.
그러나 인덱스가 단순한 값이고
키가 더 복잡한 객체 인스턴스인 더 일반적인 경우에는
잘 작동해야 합니다.

갱 오브 포는 플라이웨이트 패턴을 팩토리 함수를 사용하는 것으로 정의하지만,
파이썬은 또 다른 가능성을 제공합니다.
클래스는 ``bool()`` 및 ``int()``와 마찬가지로
생성자에서 바로 패턴을 구현할 수 있습니다.
위의 예제를 클래스로 다시 작성하고 —
예를 들어 미리 빌드하는 대신 주문형으로 객체를 할당하면 —
다음과 같은 결과가 생성됩니다.

.. testcode::

   class Grade(object):
       _instances = {}

       def __new__(cls, percent):
           percent = max(50, min(99, percent))
           letter = 'FDCBA'[(percent - 50) // 10]
           self = cls._instances.get(letter)
           if self is None:
               self = cls._instances[letter] = object.__new__(Grade)
               self.letter = letter
           return self

       def __repr__(self):
           return 'Grade {!r}'.format(self.letter)

   print(Grade(55), Grade(85), Grade(95), Grade(100))
   print(len(Grade._instances))    # 인스턴스 수
   print(Grade(95) is Grade(100))  # 'A'를 두 번 더 요청
   print(len(Grade._instances))    # 숫자가 동일하게 유지되었습니까?

.. testoutput::

    Grade 'F' Grade 'B' Grade 'A' Grade 'A'
    3
    True
    3

*A*에 대한 ``Grade`` 객체가 생성되면
이에 대한 모든 추가 요청은 동일한 객체를 받습니다.
인스턴스 사전은 계속 증가하지 않습니다.

``__new__()``가 기존 객체를 반환할 수 있는 이러한 클래스에서는
``__init__()``을 정의하지 않는다는 점에 유의하십시오.
이는 파이썬이 항상 ``__new__()``에서 반환된 객체에서
``__init__()``을 호출하기 때문입니다
(객체가 클래스 자체의 인스턴스인 한).
이는 새 플라이웨이트 객체를 처음 반환할 때는 유용하지만,
이미 초기화된 객체를 반환하는 후속 경우에는 중복됩니다.
따라서 대신 ``__new__()`` 중간에 초기화 작업을 수행합니다.

               self.letter = letter

.. TODO 싱글톤과 동일한 이유로 여기에 언급하십시오. 작성되면

``__new__()`` 내부에 플라이웨이트 패턴 팩토리를 숨기는 가능성을
설명했지만, 동작이 철자와 일치하지 않는 코드를 생성하므로
권장하지 않습니다.
파이썬 프로그래머가 ``Grade(95)``를 보면
``__new__()``가 재정의되었다는 비밀을 알고 있고
코드를 읽을 때 항상 해당 사실을 기억하지 않는 한,
모든 결과와 함께 "새 객체 인스턴스"라고 생각할 것입니다.

전통적인 플라이웨이트 패턴 팩토리 함수는
"이 코드는 새 객체를 빌드하고 있습니다"와 같은 가정을 유발할 가능성이 적으며,
어쨌든 구현하고 디버깅하기가 더 간단합니다.
