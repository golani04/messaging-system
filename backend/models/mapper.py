from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from backend import db


recipients = db.Table(
    "UserMessages",
    Column("m_id", Integer, ForeignKey("Messages.id")),
    Column("r_id", Integer, ForeignKey("Users.id"), index=True),
    UniqueConstraint("m_id", "r_id", name="uc_mr_ids"),
)
