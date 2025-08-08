# app/infrastructure/sql/state_saver.py
from typing import Optional
from app.infrastructure.sql.setupDB import SessionLocal, execute_try
from app.domain.model.stateStorage import StateStorage
from app.domain.model.state import State

class StateSaver:
    @staticmethod
    def get_by_session(session_id: int) -> Optional[StateStorage]:
        def _get():
            db = SessionLocal()
            try:
                return db.query(StateStorage).filter(StateStorage.session_id == session_id).first()
            finally:
                db.close()
        return execute_try(_get)

    @staticmethod
    def save_state(state: State) -> StateStorage:
        def _save():
            db = SessionLocal()
            try:
                db_state = StateStorage(**state.model_dump(exclude_none=True))
                db.add(db_state)
                db.commit()
                db.refresh(db_state)
                return db_state
            except Exception as e:
                db.rollback()
                raise e
            finally:
                db.close()
        return execute_try(_save)

    @staticmethod
    def update_state(session_id: int, state: State) -> Optional[StateStorage]:
        def _update():
            db = SessionLocal()
            try:
                db_state = db.query(StateStorage).filter(StateStorage.session_id == session_id).first()
                if not db_state:
                    return None
                for key, value in state.model_dump(exclude_none=True).items():
                    setattr(db_state, key, value)
                db.commit()
                db.refresh(db_state)
                return db_state
            except Exception as e:
                db.rollback()
                raise e
            finally:
                db.close()
        return execute_try(_update)

    @staticmethod
    def delete_state(session_id: int) -> bool:
        def _delete():
            db = SessionLocal()
            try:
                rows = db.query(StateStorage).filter(StateStorage.session_id == session_id).delete()
                db.commit()
                return rows > 0
            except Exception as e:
                db.rollback()
                raise e
            finally:
                db.close()
        return execute_try(_delete)
