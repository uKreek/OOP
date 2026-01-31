from log_classes import (
    LogLevel,
    SimpleLogFilter,
    ReLogFilter,
    LevelFilter,
    ConsoleHandler,
    SocketHandler,
    FileHandler,
    SyslogHandler,
    FtpHandler,
    Formatter,
    Logger
)

print("===== DEMO FILTERS =====")

simple_filter = SimpleLogFilter("problem")
text1 = "this is epic"
text2 = "Houston, we have a problem"
print(f'\n>>> pattern = "problem"')
print(f'"{text1}": {simple_filter.match(LogLevel.INFO, text1)}')
print(f'"{text2}": {simple_filter.match(LogLevel.INFO, text2)}')

re_filter = ReLogFilter(r"\d+")
text3 = "error 500"
text4 = "Rick-roll error"
print(f'\n>>> re_pattern = any number')
print(f'"{text3}": {re_filter.match(LogLevel.INFO, text3)}')
print(f'"{text4}": {re_filter.match(LogLevel.INFO, text4)}')

level_filter = LevelFilter(LogLevel.WARN)
print('\n>>> level = WARN')
print(f'info text: {level_filter.match(LogLevel.INFO, text1)}')
print(f'warn text: {level_filter.match(LogLevel.ERROR, text2)}')


print("\n===== DEMO HANDLERS =====")

print('\n>>> console_handler')
console_handler = ConsoleHandler()
console_handler.handle(LogLevel.INFO, "This message wrote in console")

file_handler = FileHandler("demo_log.txt")
file_handler.handle(LogLevel.INFO, "text1")

print('\n>>> syslog_handler')
syslog_handler = SyslogHandler("Pinterest")
syslog_handler.handle(LogLevel.INFO, "Syslog simulation")

socket_handler = SocketHandler('127.0.0.1', 0000)
socket_handler.handle(LogLevel.INFO, "Socket simulation")

print('\n>>> ftp_handler')
ftp_handler = FtpHandler("ftp.reddit.com", "Kreek")
ftp_handler.handle(LogLevel.INFO, "User signed in")


print("\n===== DEMO FORMATTER =====")

formatter = Formatter('%Y.%m.%d %H:%M:%S')
formatted_text = formatter.format(LogLevel.INFO, text1)
print(formatted_text)


print("\n===== DEMO LOGGER =====")

filters = [
    LevelFilter(LogLevel.INFO)
]

handlers = [
    ConsoleHandler(),
    FileHandler("logger_output.txt")
]

formatters = [
    Formatter('%d.%m.%Y %H:%M:%S')
]

logger = Logger(filters, handlers, formatters)

logger.log_info(text1)
logger.log_warn(text2)
logger.log_error("fatality")
