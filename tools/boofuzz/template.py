from boofuzz import *

def main():
    session = Session(
        target=Target(
            connection=SocketConnection("192.168.101.186", 7510, proto='tcp')
        ),
    )

    s_initialize(name="Request")
    with s_block("Request-Line"):
        s_static("GET")
        s_static(" ")
        s_static("/topology/home")
        s_static(" ")
        s_static('HTTP/1.1')
        s_static("\r\n")

    with s_block("Host-Line"):
        s_static("Host: ")
        # s_delim(" ", name='space-3')
        s_string("192.168.101.186", name='ip')
        s_static(":")
        s_string('7510', name='port')
        s_static("\r\n", name="Host-Line-CRLF")

    with s_block("User-Agent"):
        s_static("User-Agent")
        s_static(": ")
        s_static("Mozilla/5.0")
        s_static("\r\n")
        s_static("\r\n", "Request-CRLF")

    session.connect(s_get("Request"))

    session.fuzz()


if __name__ == "__main__":
    main()

