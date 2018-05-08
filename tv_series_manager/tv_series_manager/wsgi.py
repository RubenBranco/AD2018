from .series_manager import application
import ssl

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('../server.crt', '../server.key')
    application.run(ssl_context=context)
