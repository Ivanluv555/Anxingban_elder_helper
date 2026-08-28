from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.sos.entity.SosRecordEntity import SosRecordEntity


class SosRepository:
    """SOS 数据访问层"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_profile(self, profile_id: int) -> list[SosRecordEntity]:
        """根据档案ID查询SOS记录列表"""
        return list(self.db.scalars(
            select(SosRecordEntity)
            .where(SosRecordEntity.profile_id == profile_id)
            .order_by(SosRecordEntity.id.desc())
        ).all())
    
    def find_all(self, limit: int = 100) -> list[SosRecordEntity]:
        """查询所有SOS记录"""
        return list(self.db.scalars(
            select(SosRecordEntity)
            .order_by(SosRecordEntity.id.desc())
            .limit(limit)
        ).all())
    
    def create(self, sos_record: SosRecordEntity) -> SosRecordEntity:
        """创建SOS记录"""
        self.db.add(sos_record)
        self.db.commit()
        self.db.refresh(sos_record)
        return sos_record
