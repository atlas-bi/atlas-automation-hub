"""empty message

Revision ID: a68731ea75d6
Revises: 3daa9bdf0b76
Create Date: 2020-12-04 13:31:10.992663

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a68731ea75d6"
down_revision = "3daa9bdf0b76"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.add_column("task", sa.Column("next_run", sa.DateTime(), nullable=True))
    op.create_index(op.f("ix_task_next_run"), "task", ["next_run"], unique=False)

    # these are auto added by postgres, but added to this file so they will not be added again.
    op.create_index(
        op.f("ix_connection_database_type_id"),
        "connection_database",
        ["type_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_task_destination_file_type_id"),
        "task",
        ["destination_file_type_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_task_processing_type_id"), "task", ["processing_type_id"], unique=False
    )
    op.create_index(
        op.f("ix_task_source_query_type_id"),
        "task",
        ["source_query_type_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_task_source_type_id"), "task", ["source_type_id"], unique=False
    )
    op.create_index(op.f("ix_task_status_id"), "task", ["status_id"], unique=False)


# ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_task_status_id"), table_name="task")
    op.drop_index(op.f("ix_task_source_type_id"), table_name="task")
    op.drop_index(op.f("ix_task_source_query_type_id"), table_name="task")
    op.drop_index(op.f("ix_task_processing_type_id"), table_name="task")
    op.drop_index(op.f("ix_task_next_run"), table_name="task")
    op.drop_index(op.f("ix_task_destination_file_type_id"), table_name="task")
    op.drop_column("task", "next_run")
    op.drop_index(
        op.f("ix_connection_database_type_id"), table_name="connection_database"
    )
    # ### end Alembic commands ###
