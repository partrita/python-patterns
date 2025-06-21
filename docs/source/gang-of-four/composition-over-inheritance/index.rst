============================================
 상속보다 컴포지션 원칙
============================================

*:doc:`/gang-of-four/index`의 원칙*

.. TODO 아래에 파이썬의 장점을 언급하여
   여기 경고에서 한 약속을 이행하십시오.

.. admonition:: 결론

   다른 프로그래밍 언어와 마찬가지로 파이썬에서도
   이 위대한 원칙은 소프트웨어 아키텍트가
   객체 지향에서 벗어나
   대신 객체 기반 프로그래밍의
   더 간단한 관행을 즐기도록 권장합니다.

이것은 :doc:`/gang-of-four/index`가 맨 처음 "소개" 장에서 제시한
두 번째 원칙입니다.
이 원칙은 매우 중요하여 다음과 같이 들여쓰기하고 기울임꼴로 표시합니다.

    *클래스 상속보다 객체 컴포지션을 선호하십시오.*

단일 디자인 문제를 가지고 이 원칙이
몇 가지 고전적인 갱 오브 포 디자인 패턴을 통해
어떻게 작동하는지 살펴보겠습니다.
각 디자인 패턴은 상속에 얽매이지 않는 간단한 클래스를 조립하여
우아한 런타임 솔루션을 만듭니다.

문제: 서브클래스 폭발
-------------------------------

디자인 전략으로서 상속의 결정적인 약점은
클래스가 종종 여러 다른 디자인 축을 따라 동시에 특수화되어야 한다는 것입니다.
이는 갱 오브 포가 브리지 장에서 "클래스의 확산"이라고 부르는 것과
데코레이터 장에서 "모든 조합을 지원하기 위한 서브클래스의 폭발"이라고 부르는 것으로 이어집니다.

파이썬의 `logging 모듈 <https://docs.python.org/3/library/logging.html>`_은
표준 라이브러리 자체에서 상속보다 컴포지션 원칙을 따르는 모듈의 좋은 예이므로
로깅을 예로 사용하겠습니다.
개발자가 새 대상으로 로그 메시지를 보내야 함에 따라
점차 서브클래스를 얻은 기본 로깅 클래스를 상상해 보십시오.

.. testcode::

    import sys
    import syslog

    # 초기 클래스.

    class Logger(object):
        def __init__(self, file):
            self.file = file

        def log(self, message):
            self.file.write(message + '\n')
            self.file.flush()

    # 메시지를 다른 곳으로 보내는 두 개의 추가 클래스.

    class SocketLogger(Logger):
        def __init__(self, sock):
            self.sock = sock

        def log(self, message):
            self.sock.sendall((message + '\n').encode('ascii'))

    class SyslogLogger(Logger):
        def __init__(self, priority):
            self.priority = priority

        def log(self, message):
            syslog.syslog(self.priority, message)

이 첫 번째 디자인 축에 다른 축이 합류하면 문제가 발생합니다.
이제 로그 메시지를 필터링해야 한다고 상상해 보십시오 —
일부 사용자는 "Error"라는 단어가 포함된 메시지만 보고 싶어하고,
개발자는 ``Logger``의 새 서브클래스로 응답합니다.

.. testcode::

    # 새로운 디자인 방향: 메시지 필터링.

    class FilteredLogger(Logger):
        def __init__(self, pattern, file):
            self.pattern = pattern
            super().__init__(file)

        def log(self, message):
            if self.pattern in message:
                super().log(message)

    # 작동합니다.

    f = FilteredLogger('Error', sys.stdout)
    f.log('Ignored: this is not important')
    f.log('Error: but you want to see this')

.. testoutput::

    Error: but you want to see this

이제 함정이 놓였고, 애플리케이션이 메시지를 필터링해야 하지만
파일 대신 소켓에 써야 하는 순간에 터질 것입니다.
기존 클래스 중 어느 것도 해당 사례를 다루지 않습니다.
개발자가 서브클래싱을 계속 진행하여
두 클래스의 기능을 결합한 ``FilteredSocketLogger``를 만들면
서브클래스 폭발이 진행 중입니다.

프로그래머는 운이 좋아서 더 이상 조합이 필요하지 않을 수도 있습니다.
그러나 일반적인 경우 애플리케이션은 3×2=6개의 클래스로 끝납니다.

    Logger            FilteredLogger
    SocketLogger      FilteredSocketLogger
    SyslogLogger      FilteredSyslogLogger

*m*과 *n*이 모두 계속 증가하면 총 클래스 수는 기하급수적으로 증가합니다.
이것이 갱 오브 포가 피하고 싶어하는 "클래스의 확산"과
"서브클래스의 폭발"입니다.

해결책은 메시지 필터링과 메시지 로깅을 모두 담당하는 클래스가
너무 복잡하다는 것을 인식하는 것입니다.
최신 객체 지향 관행에서는
"단일 책임 원칙"을 위반했다고 비난받을 것입니다.

그러나 메시지 필터링과 메시지 출력이라는 두 가지 기능을
다른 클래스에 어떻게 분배할 수 있을까요?

해결책 #1: 어댑터 패턴
--------------------------------

.. TODO 작성되면 어댑터 페이지에 링크

한 가지 해결책은 어댑터 패턴입니다.
원래 로거 클래스를 개선할 필요가 없다고 결정하는 것입니다.
왜냐하면 메시지를 출력하는 모든 메커니즘을
로거가 예상하는 파일 객체처럼 보이도록 래핑할 수 있기 때문입니다.

1. 따라서 원래 ``Logger``를 유지합니다.
2. 그리고 ``FilteredLogger``도 유지합니다.
3. 그러나 대상별 서브클래스를 만드는 대신
   각 대상을 파일의 동작에 맞게 조정하고
   어댑터를 ``Logger``의 출력 파일로 전달합니다.

다음은 다른 두 출력 각각에 대한 어댑터입니다.

.. testcode::

    import socket

    class FileLikeSocket:
        def __init__(self, sock):
            self.sock = sock

        def write(self, message_and_newline):
            self.sock.sendall(message_and_newline.encode('ascii'))

        def flush(self):
            pass

    class FileLikeSyslog:
        def __init__(self, priority):
            self.priority = priority

        def write(self, message_and_newline):
            message = message_and_newline.rstrip('\n')
            syslog.syslog(self.priority, message)

        def flush(self):
            pass

파이썬은 덕 타이핑을 권장하므로
어댑터의 유일한 책임은 올바른 메서드를 제공하는 것입니다 —
예를 들어 우리 어댑터는 래핑하는 클래스나
모방하는 ``file`` 타입에서 상속받을 필요가 없습니다.
또한 실제 파일이 제공하는 12개 이상의 메서드 전체를
다시 구현할 의무도 없습니다.
오리가 꽥꽥거리는 소리만 필요하다면 걸을 수 있다는 것이 중요하지 않듯이,
우리 어댑터는 ``Logger``가 실제로 사용하는
두 가지 파일 메서드만 구현하면 됩니다.

따라서 서브클래스 폭발을 피할 수 있습니다!
로거 객체와 어댑터 객체는
추가 클래스를 만들 필요 없이
런타임에 자유롭게 혼합하고 일치시킬 수 있습니다.

.. testcode::

    sock1, sock2 = socket.socketpair()

    fs = FileLikeSocket(sock1)
    logger = FilteredLogger('Error', fs)
    logger.log('Warning: message number one')
    logger.log('Error: message number two')

    print('The socket received: %r' % sock2.recv(512))

.. testoutput::

    The socket received: b'Error: message number two\n'

위에서 ``FileLikeSocket`` 클래스를 작성한 것은
예시를 위해서일 뿐이라는 점에 유의하십시오 —
실제로는 해당 어댑터가 파이썬 표준 라이브러리에 내장되어 있습니다.
소켓의 |makefile|_ 메서드를 호출하기만 하면
소켓을 파일처럼 보이게 만드는 완전한 어댑터를 받을 수 있습니다.

.. |makefile| replace:: ``makefile()``
.. _makefile: https://docs.python.org/3/library/socket.html#socket.socket.makefile

해결책 #2: 브리지 패턴
-------------------------------

.. TODO 작성되면 브리지 패턴에 링크

브리지 패턴은 클래스의 동작을
호출자가 보는 외부 "추상화" 객체와
내부에 래핑된 "구현" 객체로 분할합니다.
필터링은 "추상화" 클래스에 속하고
출력은 "구현" 클래스에 속한다는
(아마도 약간 임의적인) 결정을 내리면
로깅 예제에 브리지 패턴을 적용할 수 있습니다.

.. TODO s/write/output?

어댑터 사례와 마찬가지로
별도의 클래스 계층이 이제 쓰기를 관리합니다.
그러나 출력 클래스를 파이썬 ``file`` 객체의 인터페이스와 일치하도록
왜곡해야 하는 대신 —
로거에서 줄 바꿈을 추가하고
어댑터에서 다시 제거해야 하는 어색한 기동이 필요했습니다 —
이제 래핑된 클래스의 인터페이스를 직접 정의할 수 있습니다.

따라서 내부 "구현" 객체가 줄 바꿈이 추가될 필요 없이
원시 메시지를 받도록 설계하고,
인터페이스를 단일 메서드 ``emit()``으로 줄여서
일반적으로 아무 작업도 하지 않는 ``flush()`` 메서드를
지원할 필요가 없도록 합시다.

.. testcode::

    # 호출자가 보게 될 "추상화".

    class Logger(object):
        def __init__(self, handler):
            self.handler = handler

        def log(self, message):
            self.handler.emit(message)

    class FilteredLogger(Logger):
        def __init__(self, pattern, handler):
            self.pattern = pattern
            super().__init__(handler)

        def log(self, message):
            if self.pattern in message:
                super().log(message)

    # 이면의 "구현".

    class FileHandler:
        def __init__(self, file):
            self.file = file

        def emit(self, message):
            self.file.write(message + '\n')
            self.file.flush()

    class SocketHandler:
        def __init__(self, sock):
            self.sock = sock

        def emit(self, message):
            self.sock.sendall((message + '\n').encode('ascii'))

    class SyslogHandler:
        def __init__(self, priority):
            self.priority = priority

        def emit(self, message):
            syslog.syslog(self.priority, message)

추상화 객체와 구현 객체는
이제 런타임에 자유롭게 결합할 수 있습니다.

.. testcode::

    handler = FileHandler(sys.stdout)
    logger = FilteredLogger('Error', handler)

    logger.log('Ignored: this will not be logged')
    logger.log('Error: this is important')

.. testoutput::

    Error: this is important

이것은 어댑터보다 더 많은 대칭성을 제공합니다.
파일 출력이 ``Logger``에 기본적으로 제공되지만
파일이 아닌 출력에는 추가 클래스가 필요한 대신,
이제 항상 추상화와 구현을 구성하여
작동하는 로거가 빌드됩니다.

다시 한번, 두 종류의 클래스가 런타임에 함께 구성되므로
어느 클래스도 확장할 필요 없이
서브클래스 폭발을 피할 수 있습니다.

해결책 #3: 데코레이터 패턴
----------------------------------

동일한 로그에 두 가지 다른 필터를 적용하려면 어떻게 해야 할까요?
위의 해결책 중 어느 것도 여러 필터를 지원하지 않습니다 —
예를 들어, 하나는 우선순위로 필터링하고 다른 하나는 키워드와 일치시킵니다.

이전 섹션에서 정의된 필터를 다시 살펴보십시오.
두 개의 필터를 쌓을 수 없는 이유는
제공하는 인터페이스와 래핑하는 인터페이스 사이에
비대칭성이 있기 때문입니다.
``log()`` 메서드를 제공하지만
핸들러의 ``emit()`` 메서드를 호출합니다.
한 필터를 다른 필터로 래핑하면 외부 필터가
내부 필터의 ``emit()``을 호출하려고 할 때 ``AttributeError``가 발생합니다.

대신 필터와 핸들러가 동일한 인터페이스를 제공하도록 전환하여
모두 ``log()`` 메서드를 제공하도록 하면
데코레이터 패턴에 도달하게 됩니다.

.. testcode::

    # 모든 로거는 실제 출력을 수행합니다.

    class FileLogger:
        def __init__(self, file):
            self.file = file

        def log(self, message):
            self.file.write(message + '\n')
            self.file.flush()

    class SocketLogger:
        def __init__(self, sock):
            self.sock = sock

        def log(self, message):
            self.sock.sendall((message + '\n').encode('ascii'))

    class SyslogLogger:
        def __init__(self, priority):
            self.priority = priority

        def log(self, message):
            syslog.syslog(self.priority, message)

    # 필터는 제공하는 것과 동일한 메서드를 호출합니다.

    class LogFilter:
        def __init__(self, pattern, logger):
            self.pattern = pattern
            self.logger = logger

        def log(self, message):
            if self.pattern in message:
                self.logger.log(message)

처음으로 필터링 코드가 특정 로거 클래스 외부로 이동했습니다.
대신 이제 원하는 모든 로거 주위에 래핑할 수 있는
독립 실행형 기능이 되었습니다.

처음 두 가지 해결책과 마찬가지로
특별한 결합 클래스를 빌드하지 않고도
런타임에 필터링을 출력과 결합할 수 있습니다.

.. testcode::

    log1 = FileLogger(sys.stdout)
    log2 = LogFilter('Error', log1)

    log1.log('Noisy: this logger always produces output')

    log2.log('Ignored: this will be filtered out')
    log2.log('Error: this is important and gets printed')

.. testoutput::

    Noisy: this logger always produces output
    Error: this is important and gets printed

그리고 데코레이터 클래스는 대칭적이므로 —
래핑하는 것과 정확히 동일한 인터페이스를 제공합니다 —
이제 동일한 로그 위에 여러 다른 필터를 쌓을 수 있습니다!

.. testcode::

    log3 = LogFilter('severe', log2)

    log3.log('Error: this is bad, but not that bad')
    log3.log('Error: this is pretty severe')

.. testoutput::

    Error: this is pretty severe

그러나 이 디자인의 대칭성이 깨지는 한 곳에 유의하십시오.
필터는 쌓을 수 있지만
출력 루틴은 결합하거나 쌓을 수 없습니다.
로그 메시지는 여전히 하나의 출력에만 쓸 수 있습니다.

해결책 #4: 갱 오브 포 패턴을 넘어서
---------------------------------------------

파이썬의 로깅 모듈은 훨씬 더 많은 유연성을 원했습니다.
여러 필터를 지원할 뿐만 아니라
단일 로그 메시지 스트림에 대한 여러 출력을 지원합니다.
다른 언어의 로깅 모듈 디자인을 기반으로 —
주요 영감에 대해서는 `PEP 282 <https://www.python.org/dev/peps/pep-0282/>`_의
"영향" 섹션을 참조하십시오 —
파이썬 로깅 모듈은 자체 상속보다 컴포지션 패턴을 구현합니다.

1. 호출자가 상호 작용하는 ``Logger`` 클래스는
   자체적으로 필터링이나 출력을 구현하지 않습니다.
   대신 필터 목록과 핸들러 목록을 유지합니다.

2. 각 로그 메시지에 대해
   로거는 각 필터를 호출합니다.
   필터 중 하나라도 거부하면 메시지가 삭제됩니다.

3. 모든 필터에서 수락된 각 로그 메시지에 대해
   로거는 출력 핸들러를 반복하고
   각 핸들러에게 메시지를 ``emit()``하도록 요청합니다.

또는 적어도 그것이 아이디어의 핵심입니다.
표준 라이브러리의 로깅은 실제로 더 복잡합니다.
예를 들어, 각 핸들러는 로거에 나열된 필터 외에
자체 필터 목록을 가질 수 있습니다.
그리고 각 핸들러는 또한 ``INFO`` 또는 ``WARN``과 같은
최소 메시지 "수준"을 지정하며,
혼란스럽게도 이는 핸들러 자체나
핸들러의 필터 중 어느 것도 적용하지 않고
대신 로거가 핸들러를 반복하는 곳 깊숙이 묻혀 있는
``if`` 문에 의해 적용됩니다.
따라서 전체 디자인은 약간 엉망입니다.

그러나 표준 라이브러리 로거의 기본 통찰력 —
로거의 메시지는 여러 필터 *및* 여러 출력을 받을 자격이 있을 수 있다는 것 —
을 사용하여 필터 클래스와 핸들러 클래스를 완전히 분리할 수 있습니다.

.. testcode::

    # 이제 로거는 하나뿐입니다.

    class Logger:
        def __init__(self, filters, handlers):
            self.filters = filters
            self.handlers = handlers

        def log(self, message):
            if all(f.match(message) for f in self.filters):
                for h in self.handlers:
                    h.emit(message)

    # 필터는 이제 문자열에 대해서만 알고 있습니다!

    class TextFilter:
        def __init__(self, pattern):
            self.pattern = pattern

        def match(self, text):
            return self.pattern in text

    # 핸들러는 이전 해결책의 "로거"처럼 보입니다.

    class FileHandler:
        def __init__(self, file):
            self.file = file

        def emit(self, message):
            self.file.write(message + '\n')
            self.file.flush()

    class SocketHandler:
        def __init__(self, sock):
            self.sock = sock

        def emit(self, message):
            self.sock.sendall((message + '\n').encode('ascii'))

    class SyslogHandler:
        def __init__(self, priority):
            self.priority = priority

        def emit(self, message):
            syslog.syslog(self.priority, message)

이 최종 디자인 전환에서만
필터가 마땅히 받아야 할 단순함으로 빛을 발한다는 점에 유의하십시오.
처음으로 문자열만 받고 판정만 반환합니다.
이전의 모든 디자인은
로깅 클래스 자체 내부에 필터링을 숨기거나
단순히 판정을 내리는 것 이상의 추가 의무를
필터에 지웠습니다.

사실, "log"라는 단어는 필터 클래스의 이름에서 완전히 사라졌으며,
매우 중요한 이유가 있습니다.
더 이상 로깅에 특정한 것이 없기 때문입니다!
``TextFilter``는 이제 문자열과 관련된 모든 컨텍스트에서
완전히 재사용할 수 있습니다.
마지막으로 로깅이라는 특정 개념에서 분리되어
테스트하고 유지 관리하기가 더 쉬워질 것입니다.

다시 한번, 문제에 대한 모든 상속보다 컴포지션 해결책과 마찬가지로
클래스는 상속 없이 런타임에 구성됩니다.

.. testcode::

    f = TextFilter('Error')
    h = FileHandler(sys.stdout)
    logger = Logger([f], [h])

    logger.log('Ignored: this will not be logged')
    logger.log('Error: this is important')

.. testoutput::

    Error: this is important

여기에는 중요한 교훈이 있습니다.
상속보다 컴포지션과 같은 디자인 원칙은
결국 어댑터나 데코레이터와 같은 개별 패턴보다
더 중요합니다.
항상 원칙을 따르십시오.
그러나 항상 공식 목록에서 패턴을 선택하도록
제한받는다고 느끼지 마십시오.
우리가 지금 도달한 디자인은
이전 디자인보다 유연하고 유지 관리가 더 쉽습니다.
비록 이전 디자인은 공식적인 갱 오브 포 패턴을 기반으로 했지만
이 최종 디자인은 그렇지 않습니다.
때로는 문제에 완벽하게 맞는 기존 디자인 패턴을 찾을 수 있지만 —
그렇지 않다면 디자인을 넘어서면 디자인이 더 강력해질 수 있습니다.

.. TODO Facade가 작성되면 클라이언트가 필터와 핸들러를
   메서드 뒤에 숨기는 대신 직접 빌드하도록 허용했기 때문에
   Facade가 아니라는 점에 유의하십시오. (아니면 빌더 패턴이
   언급하기에 적절한 패턴일까요? 흠.)

회피: "if" 문
----------------------

위의 코드가 많은 독자를 놀라게 했을 것이라고 생각합니다.
일반적인 파이썬 프로그래머에게는
클래스를 많이 사용하는 것이 완전히 부자연스러워 보일 수 있습니다 —
1980년대의 오래된 아이디어를 현대 파이썬과 관련 있어 보이게 하려는
어색한 연습처럼 말입니다.

새로운 디자인 요구 사항이 나타나면
일반적인 파이썬 프로그래머는
정말로 새 클래스를 작성할까요?
아니요!
"복잡한 것보다 간단한 것이 낫다."
``if`` 문으로도 충분한데
왜 클래스를 추가해야 할까요?
단일 로거 클래스는 점차 조건문을 추가하여
이전 예제와 동일한 모든 경우를 처리할 수 있습니다.

.. testcode::

    # "if" 문으로서의 각 새로운 기능.

    class Logger:
        def __init__(self, pattern=None, file=None, sock=None, priority=None):
            self.pattern = pattern
            self.file = file
            self.sock = sock
            self.priority = priority

        def log(self, message):
            if self.pattern is not None:
                if self.pattern not in message:
                    return
            if self.file is not None:
                self.file.write(message + '\n')
                self.file.flush()
            if self.sock is not None:
                self.sock.sendall((message + '\n').encode('ascii'))
            if self.priority is not None:
                syslog.syslog(self.priority, message)

    # 잘 작동합니다.

    logger = Logger(pattern='Error', file=sys.stdout)

    logger.log('Warning: not that important')
    logger.log('Error: this is important')

.. testoutput::

    Error: this is important

실제 애플리케이션에서 접했던
더 일반적인 파이썬 디자인 관행으로
이 예를 인식할 수 있습니다.

``if`` 문 접근 방식이 전혀 이점이 없는 것은 아닙니다.
이 클래스의 전체 가능한 동작 범위는
코드를 위에서 아래로 한 번 읽는 것만으로 파악할 수 있습니다.
매개변수 목록은 장황해 보일 수 있지만,
파이썬의 선택적 키워드 인수 덕분에
클래스에 대한 대부분의 호출은 네 가지 인수를 모두 제공할 필요가 없습니다.

(이 클래스는 파일 하나와 소켓 하나만 처리할 수 있다는 것은 사실이지만,
가독성을 위해 단순화한 것입니다.
``file`` 및 ``socket`` 매개변수를
``files`` 및 ``sockets``라는 목록으로 쉽게 전환할 수 있습니다.)

모든 파이썬 프로그래머가 ``if``를 빨리 배우지만
클래스를 이해하는 데 훨씬 더 오래 걸릴 수 있다는 점을 감안할 때,
기능을 작동시키는 가장 간단한 메커니즘에
코드가 의존하는 것이 분명한 승리처럼 보일 수 있습니다.
그러나 상속보다 컴포지션을 회피함으로써 잃어버린 것을 명시적으로 만들어
그 유혹의 균형을 맞춰 봅시다.

.. TODO 여기서 "지역성"이라는 단어와 다른 단어를 찾고 있었던 것 같습니다.

1. **지역성.**
   ``if`` 문을 사용하도록 코드를 재구성하는 것이
   가독성에 대한 무조건적인 승리는 아니었습니다.
   특정 기능(예: 소켓에 쓰는 지원)을 개선하거나 디버깅하는 임무를 맡은 경우
   해당 코드를 한 곳에서 모두 읽을 수 없다는 것을 알게 될 것입니다.
   해당 단일 기능 뒤의 코드는
   초기화자의 매개변수 목록, 초기화자의 코드 및
   ``log()`` 메서드 자체 사이에 흩어져 있습니다.

2. **삭제 가능성.**
   좋은 디자인의 과소평가된 속성은
   기능 삭제를 쉽게 만든다는 것입니다.
   아마도 크고 성숙한 파이썬 애플리케이션의 베테랑만이
   프로젝트 상태에 대한 코드 삭제의 중요성을
   충분히 인식할 것입니다.
   클래스 기반 솔루션의 경우,
   애플리케이션이 더 이상 필요하지 않으면
   ``SocketHandler`` 클래스와 해당 단위 테스트를 제거하여
   소켓에 로깅과 같은 기능을 간단히 삭제할 수 있습니다.
   반대로 ``if`` 문의 숲에서 소켓 기능을 삭제하는 것은
   인접 코드를 손상시키지 않도록 주의해야 할 뿐만 아니라
   초기화자에서 ``socket`` 매개변수를 어떻게 해야 하는지에 대한
   어색한 질문을 제기합니다.
   제거할 수 있습니까?
   위치 매개변수 목록을 일관되게 유지해야 하는 경우에는 그렇지 않습니다 —
   매개변수를 유지해야 하지만
   사용되면 예외를 발생시켜야 합니다.

3. **죽은 코드 분석.**
   이전 요점과 관련된 것은
   상속보다 컴포지션을 사용할 때
   죽은 코드 분석기가 코드베이스에서 ``SocketHandler``의 마지막 사용이
   사라지는 시점을 간단히 감지할 수 있다는 사실입니다.
   그러나 죽은 코드 분석은 종종
   "이제 소켓 출력과 관련된 모든 속성과 ``if`` 문을 제거할 수 있습니다.
   왜냐하면 초기화자에 대한 남아 있는 호출 중
   ``socket``에 대해 ``None`` 이외의 것을 전달하는 것이 없기 때문입니다."와 같은
   결정을 내리는 데 무력합니다.

4. **테스팅.**
   테스트가 제공하는 코드 상태에 대한 가장 강력한 신호 중 하나는
   테스트 중인 줄에 도달하기 전에
   얼마나 많은 관련 없는 코드가 실행되어야 하는지입니다.
   테스트가 단순히 ``SocketHandler`` 인스턴스를 시작하고,
   라이브 소켓을 전달하고, 메시지를 ``emit()``하도록 요청할 수 있다면
   소켓에 로깅과 같은 기능을 테스트하는 것은 쉽습니다.
   기능과 관련된 코드 외에는 코드가 실행되지 않습니다.
   그러나 ``if`` 문의 숲에서 소켓 로깅을 테스트하면
   최소 3배의 코드 줄이 실행됩니다.
   여러 기능의 올바른 조합으로 로거를 설정해야 하는 것은
   그중 하나만 테스트하기 위한 것이며,
   이 작은 예에서는 사소해 보일 수 있지만
   시스템이 커짐에 따라 중요해지는 중요한 경고 신호입니다.

5. **효율성.**
   가독성과 유지 관리성이 일반적으로 더 중요한 문제이므로
   이 점을 의도적으로 마지막에 배치합니다.
   그러나 ``if`` 문의 숲에 대한 디자인 문제는
   접근 방식의 비효율성으로도 나타납니다.
   단일 파일에 대한 간단한 필터링되지 않은 로그를 원하더라도
   모든 단일 메시지는 활성화했을 수 있는 모든 가능한 기능에 대해
   ``if`` 문을 실행해야 합니다.
   반대로 컴포지션 기술은
   함께 구성한 기능에 대해서만 코드를 실행합니다.

이러한 모든 이유로 ``if`` 문 숲의 명백한 단순성은
소프트웨어 디자인 관점에서 볼 때 대체로 환상이라고 제안합니다.
로거를 위에서 아래로 단일 코드 조각으로 읽을 수 있는 능력은
코드베이스의 크기에 따라 급격히 증가할
몇 가지 다른 종류의 개념적 비용을 치르게 됩니다.

회피: 다중 상속
---------------------------

일부 파이썬 프로젝트는 파이썬 언어의 논란이 많은 기능인
다중 상속을 통해 원칙을 회피하려는 유혹 때문에
상속보다 컴포지션을 실천하는 데 미치지 못합니다.

``FilteredLogger``와 ``SocketLogger``가
기본 ``Logger`` 클래스의 두 가지 다른 서브클래스였던
처음 시작한 예제 코드로 돌아가 봅시다.
단일 상속만 지원하는 언어에서는
``FilteredSocketLogger``가 ``SocketLogger`` 또는 ``FilteredLogger``에서
상속하도록 선택해야 하며,
그런 다음 다른 클래스의 코드를 복제해야 합니다.

그러나 파이썬은 다중 상속을 지원하므로
새 ``FilteredSocketLogger``는 ``SocketLogger``와 ``FilteredLogger``를
모두 기본 클래스로 나열하고 둘 다에서 상속할 수 있습니다.

.. testcode::

    # 원래 예제의 기본 클래스와 서브클래스.

    class Logger(object):
        def __init__(self, file):
            self.file = file

        def log(self, message):
            self.file.write(message + '\n')
            self.file.flush()

    class SocketLogger(Logger):
        def __init__(self, sock):
            self.sock = sock

        def log(self, message):
            self.sock.sendall((message + '\n').encode('ascii'))

    class FilteredLogger(Logger):
        def __init__(self, pattern, file):
            self.pattern = pattern
            super().__init__(file)

        def log(self, message):
            if self.pattern in message:
                super().log(message)

    # 다중 상속을 통해 파생된 클래스.

    class FilteredSocketLogger(FilteredLogger, SocketLogger):
        def __init__(self, pattern, sock):
            FilteredLogger.__init__(self, pattern, None)
            SocketLogger.__init__(self, sock)

    # 잘 작동합니다.

    logger = FilteredSocketLogger('Error', sock1)
    logger.log('Warning: not that important')
    logger.log('Error: this is important')

    print('The socket received: %r' % sock2.recv(512))

.. testoutput::

    The socket received: b'Error: this is important\n'

이것은 데코레이터 패턴 해결책과 몇 가지 놀라운 유사점을 가지고 있습니다.
두 경우 모두:

* 각 종류의 출력에 대한 로거 클래스가 있습니다.
  (파일을 직접 쓰고 파일이 아닌 것은 어댑터를 통해 쓰는
  어댑터의 비대칭성과는 대조적입니다.)

* ``message``는 호출자가 제공한 정확한 값을 유지합니다.
  (줄 바꿈을 추가하여 파일별 값으로 바꾸는
  어댑터의 습관과는 대조적입니다.)

* 필터와 로거는 둘 다 동일한 메서드 ``log()``를 구현한다는 점에서
  대칭적입니다.
  (데코레이터 이외의 다른 해결책은
  한 메서드를 제공하는 필터 클래스와
  다른 메서드를 제공하는 출력 클래스를 가졌습니다.)

* 필터는 자체적으로 출력을 생성하려고 시도하지 않지만,
  메시지가 필터링을 통과하면
  출력 작업을 다른 코드에 위임합니다.

이전 데코레이터 해결책과의 이러한 밀접한 유사성은
상속보다 컴포지션과 다중 상속 간의
매우 날카로운 비교를 위해 이 새 코드와 비교할 수 있음을 의미합니다.
질문을 통해 초점을 더욱 선명하게 해 봅시다.

*로거와 필터 모두에 대한 철저한 단위 테스트가 있는 경우
함께 작동할 것이라고 얼마나 확신합니까?*

1. 데코레이터 예제의 성공은
   각 클래스의 공개 동작에만 의존합니다.
   ``LogFilter``는 ``log()`` 메서드를 제공하고
   이 메서드는 래핑하는 객체에서 ``log()``를 호출합니다.
   (테스트는 작은 가짜 로거를 사용하여 간단히 확인할 수 있습니다.)
   그리고 각 로거는 작동하는 ``log()`` 메서드를 제공합니다.
   단위 테스트가 이러한 두 가지 공개 동작을 확인하는 한,
   단위 테스트를 실패하지 않고는 컴포지션을 깰 수 없습니다.

   반대로 다중 상속은
   해당 클래스를 단순히 인스턴스화하는 것만으로는 확인할 수 없는
   동작에 의존합니다.
   ``FilteredLogger``의 공개 동작은
   파일을 필터링하고 쓰는 ``log()`` 메서드를 제공하는 것입니다.
   그러나 다중 상속은 해당 공개 동작에만 의존하는 것이 아니라
   해당 동작이 내부적으로 구현되는 방식에 의존합니다.
   메서드가 ``super()``를 사용하여 기본 클래스에 위임하는 경우
   다중 상속이 작동하지만,
   메서드가 파일에 자체 ``write()``를 수행하는 경우에는 작동하지 않습니다.
   어떤 구현이든 단위 테스트를 만족시킬지라도 말입니다.

   따라서 테스트 스위트는 단위 테스트를 넘어서
   클래스에 대한 실제 다중 상속을 수행하거나 —
   또는 ``log()``가 ``super().log()``를 호출하는지 확인하기 위해 몽키 패치를 수행해야 합니다 —
   미래 개발자가 코드를 작업할 때
   다중 상속이 계속 작동하도록 보장합니다.

2. 다중 상속은 새 ``__init__()`` 메서드를 도입했습니다.
   왜냐하면 어느 기본 클래스의 ``__init__()`` 메서드도
   결합된 필터와 로거에 대한 충분한 인수를 받지 않기 때문입니다.
   해당 새 코드를 테스트해야 하므로
   모든 새 서브클래스에 대해 최소한 하나의 테스트가 필요합니다.

   모든 서브클래스에 대한 새 ``__init__()``를 피하기 위해
   ``*args``를 받고 ``super().__init__()``에 전달하는 것과 같은
   계획을 세우고 싶을 수 있습니다.
   (이 접근 방식을 추구한다면
   고전적인 에세이 "\ `파이썬의 Super는 해롭다고 간주됨
   <https://fuhm.net/super-harmful/>`_ "을 검토하십시오.
   이 에세이는 ``**kw``만 실제로 안전하다고 주장합니다.)
   이러한 계획의 문제점은 가독성을 해친다는 것입니다 —
   더 이상 ``__init__()`` 메서드가 어떤 인수를 사용하는지
   매개변수 목록을 읽는 것만으로는 알 수 없습니다.
   그리고 유형 검사 도구는
   더 이상 정확성을 보장할 수 없습니다.

   그러나 각 파생 클래스에 자체 ``__init__()``를 제공하든
   함께 연결하도록 설계하든,
   원래 ``FilteredLogger`` 및 ``SocketLogger``의 단위 테스트는
   결합될 때 클래스가 올바르게 초기화된다는 것을
   자체적으로 보장할 수 없습니다.

   반대로 데코레이터의 디자인은 초기화자를
   행복하고 엄격하게 직교적으로 남겨둡니다.
   필터는 ``pattern``을 받고,
   로거는 ``sock``을 받으며,
   두 가지 사이에 가능한 충돌은 없습니다.

3. 마지막으로, 두 클래스가 자체적으로는 잘 작동하지만
   다중 상속을 통해 클래스가 결합될 때
   충돌할 동일한 이름의 클래스 또는 인스턴스 속성을 가질 수 있습니다.

   예, 여기의 작은 예는
   충돌 가능성이 너무 작아서 걱정할 필요가 없어 보입니다 —
   그러나 이러한 예는 실제 애플리케이션에서 작성할 수 있는
   훨씬 더 복잡한 클래스를 대신하는 것일 뿐이라는 것을 기억하십시오.

   프로그래머가 각 클래스의 인스턴스에서 ``dir()``을 실행하고
   공통 속성을 확인하여 충돌을 방지하기 위한 테스트를 작성하든,
   가능한 모든 서브클래스에 대한 통합 테스트를 작성하든,
   두 개의 개별 클래스에 대한 원래 단위 테스트는
   다중 상속을 통해 깔끔하게 결합될 수 있다는 것을
   다시 한번 보장하지 못할 것입니다.

이러한 이유 중 어느 하나라도,
두 기본 클래스의 단위 테스트는
다중 상속을 통해 결합하는 능력이 깨지더라도
계속해서 녹색으로 유지될 수 있습니다.
이는 갱 오브 포의
"모든 조합을 지원하기 위한 서브클래스의 폭발"이
테스트에도 영향을 미칠 것임을 의미합니다.
애플리케이션에서 *m* × *n* 기본 클래스의 모든 조합을 테스트해야만
애플리케이션이 런타임에 이러한 클래스를 안전하게 사용할 수 있습니다.

단위 테스트의 보증을 깨는 것 외에도
다중 상속에는 최소 세 가지 추가 책임이 따릅니다.

4. 데코레이터의 경우 성찰이 간단합니다.
   단순히 ``print(my_filter.logger)``를 하거나 디버거에서 해당 속성을 보면
   어떤 종류의 출력 로거가 연결되어 있는지 알 수 있습니다.
   그러나 다중 상속의 경우
   클래스 자체의 메타데이터를 검사해야만
   어떤 필터와 로거가 결합되었는지 알 수 있습니다 —
   ``__mro__``를 읽거나 객체에 일련의 ``isinstance()`` 테스트를 수행합니다.

5. 데코레이터의 경우
   필터와 로거의 라이브 조합을 가져와
   런타임에 ``.logger`` 속성에 할당하여
   다른 로거로 교체하는 것이 간단합니다 —
   예를 들어 사용자가 방금 애플리케이션 인터페이스에서
   기본 설정을 전환했기 때문입니다.
   그러나 다중 상속의 경우 동일한 작업을 수행하려면
   객체의 클래스를 덮어쓰는 훨씬 더 불쾌한 기동이 필요합니다.
   런타임에 객체의 클래스를 변경하는 것은
   파이썬과 같은 동적 언어에서는 불가능하지 않지만,
   일반적으로 소프트웨어 디자인이 잘못되었다는 증상으로 간주됩니다.

6. 마지막으로, 다중 상속은 프로그래머가
   기본 클래스를 올바르게 정렬하는 데 도움이 되는
   기본 제공 메커니즘을 제공하지 않습니다.
   ``FilteredSocketLogger``는 기본 클래스가 바뀌면
   소켓에 성공적으로 쓰지 못하며,
   수십 개의 스택 오버플로 질문이 증명하듯이
   파이썬 프로그래머는 타사 기본 클래스를
   올바른 순서로 배치하는 데 영구적인 어려움을 겪습니다.
   반대로 데코레이터 패턴은
   클래스가 구성되는 방식을 명확하게 만듭니다.
   필터의 ``__init__()``는 ``logger`` 객체를 원하지만,
   로거의 ``__init__()``는 ``filter``를 요청하지 않습니다.

따라서 다중 상속은 단일 이점을 추가하지 않고
여러 가지 책임을 발생시킵니다.
적어도 이 예에서는 상속으로 디자인 문제를 해결하는 것이
컴포지션 기반 디자인보다 엄격하게 나쁩니다.

회피: 믹스인
-------------

이전 섹션의 ``FilteredSocketLogger``는
두 기본 클래스 모두에 대한 인수를 받아야 했기 때문에
자체 사용자 지정 ``__init__()`` 메서드가 필요했습니다.
그러나 이 책임은 피할 수 있다는 것이 밝혀졌습니다.
물론 서브클래스에 추가 데이터가 필요하지 않은 경우에는
문제가 발생하지 않습니다.
그러나 추가 데이터가 필요한 클래스라도
다른 수단으로 데이터를 전달받을 수 있습니다.

클래스 자체에서 ``pattern``에 대한 기본값을 제공하고
호출자가 초기화와 별도로 속성을 직접 사용자 지정하도록 초대하면
``FilteredLogger``를 다중 상속에 더 친화적으로 만들 수 있습니다.

.. testcode::

    # 초기화 중에 "pattern"을 받지 마십시오.

    class FilteredLogger(Logger):
        pattern = ''

        def log(self, message):
            if self.pattern in message:
                super().log(message)

    # 다중 상속이 이제 더 간단해졌습니다.

    class FilteredSocketLogger(FilteredLogger, SocketLogger):
        pass  # 이 서브클래스에는 추가 코드가 필요하지 않습니다!

    # 호출자는 "pattern"을 직접 설정할 수 있습니다.

    logger = FilteredSocketLogger(sock1)
    logger.pattern = 'Error'

    # 잘 작동합니다.

    logger.log('Warning: not that important')
    logger.log('Error: this is important')

    print('The socket received: %r' % sock2.recv(512))

.. testoutput::

    The socket received: b'Error: this is important\n'

``FilteredLogger``를 기본 클래스의 초기화 기동과
직교적인 초기화 기동으로 전환했으므로,
직교성이라는 아이디어를 논리적 결론까지 밀어붙이지 않겠습니까?
``FilteredLogger``를 다중 상속이 결합할 클래스 계층 구조
외부에 완전히 존재하는 "믹스인"으로 변환할 수 있습니다.

.. testcode::

    # 믹스인으로 만들어 필터를 단순화합니다.

    class FilterMixin:  # 기본 클래스 없음!
        pattern = ''

        def log(self, message):
            if self.pattern in message:
                super().log(message)

    # 다중 상속은 위와 동일하게 보입니다.

    class FilteredLogger(FilterMixin, FileLogger):
        pass  # 다시 한번, 서브클래스에는 추가 코드가 필요하지 않습니다.

    # 잘 작동합니다.

    logger = FilteredLogger(sys.stdout)
    logger.pattern = 'Error'
    logger.log('Warning: not that important')
    logger.log('Error: this is important')

.. testoutput::

    Error: this is important

믹스인은 지난 섹션에서 보았던 필터링된 서브클래스보다
개념적으로 더 간단합니다.
메서드 확인 순서를 복잡하게 만들 수 있는 기본 클래스가 없으므로
``super()``는 항상 ``class`` 문에 나열된
다음 기본 클래스를 호출합니다.

믹스인은 또한 동등한 서브클래스보다 테스트 스토리가 더 간단합니다.
``FilteredLogger``는 독립 실행형으로 실행하고
다른 클래스와 결합하는 테스트가 모두 필요하지만,
``FilterMixin``은 로거와 결합하는 테스트만 필요합니다.
믹스인은 자체적으로 불완전하므로
독립 실행형으로 실행하는 테스트는 작성할 수도 없습니다.

.. TODO 다른 계층 구조로 들어가기 때문에 원할 수도 있습니다.

그러나 다중 상속의 다른 모든 책임은 여전히 적용됩니다.
따라서 믹스인 패턴은 다중 상속의
가독성과 개념적 단순성을 향상시키지만,
문제에 대한 완전한 해결책은 아닙니다.

.. TODO 템플릿 메서드가 작성되면 간단한 부울 필터 메서드를 작성하여
   다중 상속으로 전환했을 때 잃어버린 재사용 가능성을
   되찾을 수 있다는 점을 지적하십시오.

회피: 동적으로 클래스 빌드
-----------------------------------

이전 두 섹션에서 보았듯이
전통적인 다중 상속이나 믹스인 모두
"모든 조합을 지원하기 위한 서브클래스의 폭발"이라는
갱 오브 포의 문제를 해결하지 못합니다 —
단지 두 클래스를 결합해야 할 때 코드 중복을 피할 뿐입니다.

다중 상속은 여전히 일반적인 경우
각각 다음과 같이 보이는 *m* × *n* 클래스 문의
"클래스 확산"을 필요로 합니다.

.. testcode::

    class FilteredSocketLogger(FilteredLogger, SocketLogger):
        ...

그러나 파이썬은 해결 방법을 제공한다는 것이 밝혀졌습니다.

애플리케이션이 구성 파일을 읽어
사용해야 할 로그 필터와 로그 대상을 학습한다고 상상해 보십시오.
이 파일의 내용은 런타임까지 알 수 없습니다.
미리 가능한 모든 *m* × *n* 클래스를 빌드하고
올바른 클래스를 선택하는 대신,
기다렸다가 파이썬이 ``class`` 문뿐만 아니라
런타임에 동적으로 새 클래스를 만드는
내장 ``type()`` 함수도 지원한다는 사실을 활용할 수 있습니다.

.. testsetup::

    class PatternFilteredLog:
        def __init__(self, ellipsis):
            pass
    class SeverityFilteredLog: pass
    class FileLog: pass
    class SocketLog: pass
    class SyslogLog: pass

    from io import StringIO
    def open(filename):
        return StringIO('pattern file')

.. testcode::

    # 2개의 필터링된 로거와 3개의 출력 로거를 상상해 보십시오.

    filters = {
        'pattern': PatternFilteredLog,
        'severity': SeverityFilteredLog,
    }
    outputs = {
        'file': FileLog,
        'socket': SocketLog,
        'syslog': SyslogLog,
    }

    # 결합하려는 두 클래스를 선택합니다.

    with open('config') as f:
        filter_name, output_name = f.read().split()

    filter_cls = filters[filter_name]
    output_cls = outputs[output_name]

    # 새 파생 클래스를 빌드합니다 (!)

    name = filter_name.title() + output_name.title() + 'Log'
    cls = type(name, (filter_cls, output_cls), {})

    # 평소와 같이 호출하여 인스턴스를 생성합니다.

    logger = cls(...)

``type()``에 전달된 클래스 튜플은 ``class`` 문의 기본 클래스 시리즈와 동일한 의미를 갖습니다. 위의 ``type()`` 호출은 필터링된 로거와 출력 로거 모두에서 다중 상속을 통해 새 클래스를 만듭니다.

.. TODO 특별한 초기화 논리가 필요하지 않은 경우에만 작동합니다.

묻기 전에: 예, ``class`` 문을 일반 텍스트로 빌드한 다음 |eval|에 전달하는 것도 작동합니다.

.. |eval| replace:: ``eval()``
.. _eval: https://docs.python.org/3/library/functions.html#eval

그러나 즉석에서 클래스를 빌드하는 것은 심각한 책임을 수반합니다.

* 가독성이 저하됩니다.
  위의 코드 조각을 읽는 사람은
  ``cls``의 인스턴스가 어떤 종류의 객체인지 확인하기 위해
  추가 작업을 수행해야 합니다.
  또한 많은 파이썬 프로그래머는
  ``type()``에 익숙하지 않으므로
  설명서를 멈추고 고민해야 합니다.
  클래스를 동적으로 정의할 수 있다는 새로운 개념에 어려움을 겪는다면
  여전히 혼란스러울 수 있습니다.

* ``PatternFilteredFileLog``와 같이 생성된 클래스가
  예외 또는 오류 메시지에 명명되면
  개발자는 해당 클래스 이름을 코드로 검색할 때
  아무것도 나오지 않는다는 사실을 발견하고 불행해할 것입니다.
  클래스를 찾을 수조차 없을 때 디버깅이 더 어려워집니다.
  코드베이스에서 ``type()`` 호출을 검색하고
  어떤 호출이 클래스를 생성했는지 확인하는 데
  상당한 시간이 소요될 수 있습니다.
  때로는 개발자가 각 메서드를 잘못된 인수로 호출하고
  결과 추적의 줄 번호를 사용하여
  기본 클래스를 추적해야 합니다.

* 일반적으로 런타임에 동적으로 생성된 클래스의 경우
  유형 성찰이 실패합니다.
  편집기의 "클래스로 이동" 바로 가기는
  디버거에서 ``PatternFilteredFileLog``의 인스턴스를 강조 표시할 때
  이동할 곳이 없습니다.
  그리고 `mypy <https://github.com/python/mypy>`_ 및
  `pyre-check <https://github.com/facebook/pyre-check>`_와 같은
  유형 검사 엔진은 생성된 클래스에 대해
  일반 파이썬 클래스에 대해 제공할 수 있는 강력한 보호 기능을
  제공하지 않을 가능성이 높습니다.

* 아름다운 Jupyter Notebook 기능 ``%autoreload``는
  라이브 파이썬 인터프리터에서 수정된 소스 코드를
  감지하고 다시 로드하는 거의 초자연적인 능력을 가지고 있습니다.
  그러나 예를 들어 `matplotlib이 런타임에 빌드하는
  <https://github.com/matplotlib/matplotlib/blob/54b426397c0e7567edaee4f7f77036c2b8569573/lib/matplotlib/axes/_subplots.py#L180>`_
  다중 상속 클래스에 의해 좌절됩니다.
  ``subplot_class_factory()`` 내부의 ``type()`` 호출을 통해 말입니다.

책임을 고려하면, 이미 결함이 있는 다중 상속 메커니즘을 구출하기 위한 최후의 수단으로 런타임 클래스 생성을 사용하려는 시도는
객체의 동작이 여러 독립적인 축에 걸쳐 다양해야 할 때 상속보다 컴포지션을 회피하는 전체 프로젝트의 *귀류법*으로 간주됩니다.
