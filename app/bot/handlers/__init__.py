# from app.bot.handlers
# from app.bot.handlers
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from starthandler import start
# from app.utils.callback import download
# from app.bot.handlers.general.handlerFromUrl import fromurl, send_file
# from app.utils.states.linkDownload import LinkState
# from app.bot.handlers.general.handlerHelp import help

router = Router(name=__name__)

@router.message.register(start, CommandStart())
@router.message.register(F.data == "start_create_post")
# # router.message.register(help, Command("help"))

# router.message.register(upload, Command("upload"))
# router.message.register(upload, F.text == "Upload the file")
# router.message.register(upload_file, Upload.filename)
# router.message.register(file_accepted, Upload.file)

# # router.callback_query.register(download, lambda x: x.data=="download")
# router.message.register(inline, Command("download"))
# router.message.register(inline, F.text == "Download the file")
# router.callback_query.register(download)
