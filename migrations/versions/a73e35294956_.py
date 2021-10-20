"""empty message

Revision ID: a73e35294956
Revises: 1252a267da96
Create Date: 2020-10-09 11:26:50.066009

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a73e35294956"
down_revision = "1252a267da96"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "connection_ssh",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("connection_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=500), nullable=False),
        sa.Column("address", sa.String(length=500), nullable=False),
        sa.Column("port", sa.Integer(), nullable=True),
        sa.Column("username", sa.String(length=120), nullable=False),
        sa.Column("password", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(
            ["connection_id"],
            ["connection.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_connection_ssh_id"), "connection_ssh", ["id"], unique=False
    )
    op.add_column("task", sa.Column("source_ssh_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "task", "connection_ssh", ["source_ssh_id"], ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "task", type_="foreignkey")
    op.drop_column("task", "source_ssh_id")
    op.drop_index(op.f("ix_connection_ssh_id"), table_name="connection_ssh")
    op.drop_table("connection_ssh")
    # ### end Alembic commands ###
