import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)


@contextmanager
def session_scope(session_factory, dryrun=False):
    """Provide a transactional scope around a series of operations."""
    session = session_factory()
    try:
        yield session
        if dryrun:
            logger.info('would add %i new objects, modify %i and delete %i',
                  len(session.new), len(session.dirty), len(session.deleted))
        else:
            session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
