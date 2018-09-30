#配置log
logger=logging.getLogger()
formatter=logging.Formatter('%(asctime)s %(levelname)-8s:     %(message)s')
console_handler=logging.StreamHandler(sys.stdout)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)