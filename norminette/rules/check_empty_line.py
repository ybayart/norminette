from rules import Rule
from scope import *



class CheckEmptyLine(Rule):
    def __init__(self):
        super().__init__()
        self.depends_on = []

    def run(self, context):
        i = 0
        if len(context.history) == 1 and context.history[-1] == "IsEmptyLine":
            context.new_error("EMPTY_LINE_FILE_START", context.peek_token(i))
            return False, 0
        if context.scope.name != "GlobalScope" and context.history[-1] != "IsBlockStart":
            if context.history[-1] != "IsVarDeclaration" and context.scope.vdeclarations_allowed == True:
                context.scope.vdeclarations_allowed = False
                if context.history[-1] != "IsEmptyLine":
                    context.new_error("NL_AFTER_VAR_DECL", context.peek_token(i))
                    return True, i
        if context.history[-1] != "IsEmptyLine":
            return False, 0
        if context.check_token(i, "NEWLINE") is False:
            context.new_error("SPACE_EMPTY_LINE", context.peek_token(i))
        if context.history[-2] == "IsEmptyLine":
            context.new_error("CONSECUTIVE_NEWLINES", context.peek_token(i))
        if context.history[-2] != "IsVarDeclaration" and context.scope.name != "GlobalScope":
            context.new_error("EMPTY_LINE_FUNCTION", context.peek_token(i))
        if context.peek_token(i + 1) is None:
            context.new_error("EMPTY_LINE_EOF", context.peek_token(i))
        #allowed
        # -> newline in between functions or declarations
        # -> newline in function between declaration and the rest

        return False, 0