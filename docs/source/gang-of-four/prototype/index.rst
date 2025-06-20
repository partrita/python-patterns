=======================
 프로토타입 패턴
=======================

*:doc:`/gang-of-four/index`의 "생성 패턴"*

.. admonition:: 결론

   프로토타입 패턴은 일급 함수와 클래스를 지원할 만큼
   강력한 언어에서는 필요하지 않습니다.

파이썬이 프로토타입 패턴에 대해 제공하는
좋은 대안이 얼마나 많은지 거의 당황스러울 정도입니다.

문제와 해결책이 간단하므로
이 글은 간략하게 작성될 것입니다.
문제를 정의하고,
몇 가지 파이썬다운 해결책을 나열한 다음,
Gang of Four가 더 까다로운 제약 조건 하에서
동일한 문제를 어떻게 해결했는지 연구하며 마무리할 것입니다.

문제점
-----------

프로토타입 패턴은
사용자 또는 다른 런타임 동적 요청 소스가
선택 메뉴에서 클래스를 선택할 때
호출자가 프레임워크에 인스턴스화할 클래스 메뉴를
제공할 수 있는 메커니즘을 제안합니다.

메뉴의 클래스 중 어느 것도 ``__init__()`` 인수가 필요하지 않다면
문제는 훨씬 간단해질 것입니다.

.. testcode::

   class Sharp(object):
       "♯ 기호."

   class Flat(object):
       "♭ 기호."

대신, 프로토타입 패턴은 인수가 필요한 클래스를
인스턴스화해야 할 때 사용됩니다.

.. testcode::

   class Note(object):
       "음표 1 ÷ `fraction` 마디 길이."
       def __init__(self, fraction):
           self.fraction = fraction

프로토타입 패턴이 해결하도록 설계된 것은
바로 이 상황, 즉 미리 지정된 인수 목록으로
인스턴스화해야 하는 클래스 메뉴를
프레임워크에 제공하는 것입니다.

파이썬다운 해결책
------------------

파이썬은 우리가 인스턴스화하려는 클래스와
해당 클래스를 인스턴스화하려는 인수를 프레임워크에 제공하기 위한
몇 가지 가능한 메커니즘을 제공합니다.

아래 예에서는 간단한 데이터 구조인
파이썬 딕셔너리로 클래스 메뉴를 제공하지만,
프레임워크가 메뉴 항목을 다른 데이터 구조로 제공하거나
일련의 ``register()`` 호출로 개별적으로 제공하기를 원하더라도
동일한 원칙이 적용됩니다.

한 가지 접근 방식은 클래스가 위치 인수만 필요하고
키워드 인수는 필요하지 않도록 설계하는 것입니다.
그러면 프레임워크는 인수를 간단한 튜플로 저장할 수 있으며,
이는 클래스 자체와 별도로 제공될 수 있습니다.
이는 호출 가능한 ``target=``을 전달할 ``args=(...)``와
별도로 요청하는 표준 라이브러리
`Thread <https://docs.python.org/3/library/threading.html#thread-objects>`_
클래스의 익숙한 접근 방식입니다.
메뉴 항목은 다음과 같을 수 있습니다.

.. testcode::

   menu = {
       'whole note': (Note, (1,)),
       'half note': (Note, (2,)),
       'quarter note': (Note, (4,)),
       'sharp': (Sharp, ()),
       'flat': (Flat, ()),
   }

또는 각 클래스와 인수가 동일한 튜플에 있을 수도 있습니다.

.. testcode::

   menu = {
       'whole note': (Note, 1),
       'half note': (Note, 2),
       'quarter note': (Note, 4),
       'sharp': (Sharp,),
       'flat': (Flat,),
   }

그러면 프레임워크는 ``tup[0](*tup[1:])``의
변형을 사용하여 각 호출 가능 객체를 호출합니다.

그러나 더 일반적인 경우 클래스는 위치 인수뿐만 아니라
키워드 인수도 필요할 수 있습니다.
이에 대한 응답으로, 인수가 필요한 클래스에 대해
람다 표현식을 사용하여 프레임워크에 간단한 호출 가능 객체를
제공하는 것으로 전환할 수 있습니다.

.. testcode::

   menu = {
       'whole note': lambda: Note(fraction=1),
       'half note': lambda: Note(fraction=2),
       'quarter note': lambda: Note(fraction=4),
       'sharp': Sharp,
       'flat': Flat,
   }

람다는 빠른 내부 검사를 지원하지 않지만 —
프레임워크나 디버거가 호출할 호출 가능 객체나
제공할 인수를 알기 위해 검사하기 쉽지 않습니다 —
프레임워크가 해야 할 일이 호출하는 것뿐이라면 잘 작동합니다.

또 다른 접근 방식은 각 항목에 대해
`partial <https://docs.python.org/3/library/functools.html#functools.partial>`_을
사용하는 것입니다.
이는 나중에 partial 자체가 호출될 때 제공될
위치 인수와 키워드 인수를 모두 사용하여
호출 가능 객체를 함께 패키징합니다.

.. testcode::

   from functools import partial

   # 설명을 위한 키워드 인수일 뿐입니다.
   # 이 경우 대신 ‘partial(Note, 1)’을 작성할 수 있습니다.

   menu = {
       'whole note': partial(Note, fraction=1),
       'half note': partial(Note, fraction=2),
       'quarter note': partial(Note, fraction=4),
       'sharp': Sharp,
       'flat': Flat,
   }

여기서 멈추겠지만, 더 많은 대안을 자유롭게 상상할 수 있습니다 —
예를 들어, 각 메뉴 항목에 대해 클래스, 튜플 및 딕셔너리
``(cls, args, kw)``를 제공하고
각 메뉴 항목이 선택될 때 프레임워크가 ``cls(*args, **kw)``를
호출하도록 할 수 있습니다.
파이썬에서 이 문제를 해결하기 위한 선택은 다양합니다.
왜냐하면 파이썬의 클래스와 함수는 일급 객체이므로
다른 객체와 마찬가지로 인수로 전달되고
데이터 구조에 저장될 수 있기 때문입니다.

구현
------------

그러나 Gang of Four는
파이썬 프로그래머가 누리는 것처럼 쉬운 환경을 누리지 못했습니다.
다형성과 메서드 호출만으로 무장한 그들은
실행 가능한 패턴을 만들기 위해 나섰습니다.

튜플이 없고 이를 인수 목록으로 적용할 수 없는 상황에서
각각 특정 인수 목록을 기억한 다음
새 객체를 요청받았을 때 해당 인수를 제공하는
팩토리 클래스가 필요할 것이라고 처음에는 상상할 수 있습니다.

.. testcode::

   # 프로토타입 패턴이 피하는 것:
   # 모든 클래스에 대해 하나의 팩토리가 필요한 것.

   class NoteFactory(object):
       def __init__(self, fraction):
           self.fraction = fraction

       def build(self):
           return Note(self.fraction)

   class SharpFactory(object):
       def build(self):
           return Sharp()

   class FlatFactory(object):
       def build(self):
           return Flat()

다행히 상황은 그렇게 암울하지 않습니다.
위의 팩토리 클래스를 다시 읽으면
각각이 우리가 만들고 싶은 대상 클래스와 비슷하다는 것을 알 수 있습니다 —
섬뜩할 정도로 비슷하고, 놀랍도록 비슷합니다!
``NoteFactory``는 ``Note`` 자체와 정확히 마찬가지로
``fraction`` 속성을 저장합니다.
팩토리 스택은 적어도 속성 목록에서는
우리가 인스턴스화하려는 클래스 스택처럼 보입니다.

이러한 대칭성은 각 클래스를 팩토리로 미러링하지 않고도
문제를 해결할 수 있는 방법을 제안합니다.
원래 객체 자체를 사용하여 인수를 저장하고
새 인스턴스를 제공하는 기능을 부여하면 어떨까요?

결과는 프로토타입 패턴입니다!
모든 팩토리 클래스가 사라집니다.
대신 각 인스턴스는 ``clone()`` 메서드를 얻고,
이 메서드에 응답하여 받은 것과 정확히 동일한 인수로
새 인스턴스를 빌드합니다.

.. testcode::

   # 프로토타입 패턴: 각 객체 인스턴스에
   # 자체 복사본을 빌드하는 방법을 가르칩니다.

   class Note(object):
       "음표 1 ÷ `fraction` 마디 길이."
       def __init__(self, fraction):
           self.fraction = fraction

       def clone(self):
           return Note(self.fraction)

   class Sharp(object):
       "♯ 기호."
       def clone(self):
           return Sharp()

   class Flat(object):
       "♭ 기호."
       def clone(self):
           return Flat()

이 예제를 더 복잡하게 만들 수도 있지만 —
예를 들어, 각 ``clone()`` 메서드는 서브클래스에서 메서드가 호출될 경우를 대비하여
클래스 이름을 하드 코딩하는 대신 ``type(self)``를 호출해야 합니다 —
이것은 적어도 패턴을 보여줍니다.
프로토타입 패턴은 파이썬 언어에서 사용할 수 있는
메커니즘만큼 편리하지는 않지만,
이 영리한 단순화 덕분에 Gang of Four는
지난 세기에 유행했던 일부 기능이 부족한 객체 지향 언어에서
매개변수화된 객체 생성을 훨씬 쉽게 수행할 수 있었습니다.
