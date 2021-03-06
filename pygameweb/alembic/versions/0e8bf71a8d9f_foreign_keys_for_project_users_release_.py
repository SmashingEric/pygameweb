"""Foreign keys for Project.users Release.project Project.releases

Revision ID: 0e8bf71a8d9f
Revises: 71cf723fb7cb
Create Date: 2017-01-28 00:54:32.272610

"""

# revision identifiers, used by Alembic.
revision = '0e8bf71a8d9f'
down_revision = '71cf723fb7cb'
branch_labels = None
depends_on = None

from sqlalchemy import text
from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('groups', sa.Column('description', sa.String(length=80), nullable=True))

    # Some projects are marked with 0, which means they have not been claimed yet.
    # Mark them with the administrator user instead.
    op.execute('UPDATE project SET users_id=1 where users_id=0')

    # Need an anonymous user to assign projectcomments against.
    op.execute('UPDATE projectcomment set users_id=1 where users_id is NULL')

    # These projects have been deleted. So we remove the comments too.
    op.execute('DELETE from projectcomment where projectcomment.project_id not in (select id as pid from project)')

    # Remove any comments where the user does not exist anymore.
    op.execute('DELETE from projectcomment WHERE projectcomment.users_id not in (select id from users)')

    # Remove the releases where the projects do not exist.
    op.execute('DELETE from release WHERE release.project_id not in (select id from project)')

    # Remove the tags where the projects do not exist.
    op.execute('DELETE from tags WHERE tags.project_id not in (select id from project)')


    op.alter_column('project', 'users_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key('project_user_id_fkey', 'project', 'users', ['users_id'], ['id'])
    op.alter_column('projectcomment', 'project_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('projectcomment', 'users_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key('projectcomment_project_id_fkey', 'projectcomment', 'project', ['project_id'], ['id'])
    op.create_foreign_key('projectcomment_users_id_fkey', 'projectcomment', 'users', ['users_id'], ['id'])
    op.alter_column('release', 'project_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key('release_project_id_fkey', 'release', 'project', ['project_id'], ['id'])

    op.add_column('tags', sa.Column('id', sa.Integer()))


    # op.execute('ALTER table tags add column id integer')
    table_sql = text('SELECT id, project_id, value FROM tags')
    connection = op.get_bind()
    rows = connection.execute(table_sql)
    i = 1;
    for row in rows:
        sql = """UPDATE tags SET id=%s WHERE project_id=%s AND value='%s' """ % (i, row[1], row[2])
        op.execute(sql)
        i += 1


    op.alter_column('tags', 'id',
               existing_type=sa.INTEGER(),
               nullable=False)

    op.alter_column('tags', 'project_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key('tags_project_id_fkey', 'tags', 'project', ['project_id'], ['id'])


    op.add_column('users', sa.Column('confirmed_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('current_login_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('current_login_ip', sa.String(length=80), nullable=True))
    op.add_column('users', sa.Column('last_login_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('last_login_ip', sa.String(length=80), nullable=True))
    op.add_column('users', sa.Column('login_count', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('password', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password')
    op.drop_column('users', 'login_count')
    op.drop_column('users', 'last_login_ip')
    op.drop_column('users', 'last_login_at')
    op.drop_column('users', 'current_login_ip')
    op.drop_column('users', 'current_login_at')
    op.drop_column('users', 'confirmed_at')
    op.drop_constraint('tags_project_id_fkey', 'tags', type_='foreignkey')
    op.alter_column('tags', 'project_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('tags', 'id')
    op.drop_constraint('release_project_id_fkey', 'release', type_='foreignkey')
    op.alter_column('release', 'project_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('projectcomment_users_id_fkey', 'projectcomment', type_='foreignkey')
    op.drop_constraint('projectcomment_project_id_fkey', 'projectcomment', type_='foreignkey')
    op.alter_column('projectcomment', 'users_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('projectcomment', 'project_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('project_user_id_fkey', 'project', type_='foreignkey')
    op.alter_column('project', 'users_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('groups', 'description')
    # ### end Alembic commands ###
