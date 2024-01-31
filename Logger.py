import logging

logging.basicConfig(filename="file.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')

# Creating an object
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# object = logger
# object.debug("Harmless debug Message1")
# logger.info("Just an information")
# logger.warning("Its a Warning")
# logger.error("Did you try to divide by zero")
# logger.critical("Internet is down")
 
# # Create a custom logger
# logger = logging.getLogger(__name__)
 
# # Set the level of this logger. This could be DEBUG, INFO, WARNING, ERROR, or CRITICAL
# logger.setLevel(logging.DEBUG)
 
# # Create handlersa
# c_handler = logging.StreamHandler()
# f_handler = logging.FileHandler('file.log')
# c_handler.setLevel(logging.WARNING)
# f_handler.setLevel(logging.ERROR)
 
# # Create formatters and add it to handlers
# c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
# f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# c_handler.setFormatter(c_format)
# f_handler.setFormatter(f_format)
 
# # Add handlers to the logger
# logger.addHandler(c_handler)
# logger.addHandler(f_handler)
