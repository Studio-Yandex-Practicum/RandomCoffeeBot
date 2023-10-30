"""test

Revision ID: cebca1c19787
Revises: ae30bf2db609
Create Date: 2023-10-26 22:56:39.340776

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "cebca1c19787"
down_revision = "ae30bf2db609"
branch_labels = None
depends_on = None

old_options = (
    "ONGOING",
    "SUCCESSFUL",
    "UNSUCCESSFUL",
)
new_options = ("ONGOING", "CLOSED")

old_type = sa.Enum(*old_options, name="matchstatusenum")
new_type = sa.Enum(*new_options, name="matchstatusenum")
tmp_type = sa.Enum(*new_options, name="_matchstatusenum")


def upgrade():
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        "ALTER TABLE usersmatch ALTER COLUMN status TYPE _matchstatusenum" " USING status::text::_matchstatusenum"
    )
    old_type.drop(op.get_bind(), checkfirst=False)
    new_type.create(op.get_bind(), checkfirst=False)
    op.execute("ALTER TABLE usersmatch ALTER COLUMN status TYPE matchstatusenum" " USING status::text::matchstatusenum")
    tmp_type.drop(op.get_bind(), checkfirst=False)


def downgrade():
    tmp_type.create(op.get_bind(), checkfirst=False)
    op.execute(
        "ALTER TABLE usersmatch ALTER COLUMN status TYPE _matchstatusenum" " USING status::text::_matchstatusenum"
    )
    new_type.drop(op.get_bind(), checkfirst=False)
    old_type.create(op.get_bind(), checkfirst=False)
    op.execute("ALTER TABLE usersmatch ALTER COLUMN status TYPE matchstatusenum" " USING status::text::matchstatusenum")
    tmp_type.drop(op.get_bind(), checkfirst=False)
