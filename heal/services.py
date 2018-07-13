from .repos import member_repo

class MemberService(object):

    def modify(self, line_id, name, registered=None):
        member = member_repo.get_by_line_id(line_id)
        if not member:
            return

        member.display_name = name
        member.save()

    def is_registered(self, line_id):
        member = member_repo.get_by_line_id(line_id)
        return bool(member.display_name)

member_service = MemberService()