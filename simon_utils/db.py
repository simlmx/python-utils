import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)


try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
except ImportError:
    pass

def init_session(url, verbose=False):
    engine = create_engine(url, echo=verbose)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


@contextmanager
def session_scope(url, dryrun=False):
    """Provide a transactional scope around a series of operations."""
    session = init_session(url)
    try:
        yield session
        if dryrun:
            logger.info('would add %i new objects, modify %i and delete %i',
                  len(session.new), len(session.dirty), len(session.deleted))
            # session.rollback()
        else:
            session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

