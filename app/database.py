import logging
logger = logging.getLogger(__name__)
 
async def init_db():
    logger.info("✅ No database — printing transcripts to terminal only")