
import readline

class ChiekuiCliBufferCompleter(object):
    def __init__(self, commands):
        self.commands = commands
        self.current_candidates = []
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            origline = readline.get_line_buffer()
            begin = readline.get_begidx()
            end = readline.get_endidx()
            being_completed = origline[begin:end]
            words = origline.split()

            if not words:
                self.current_candidates = sorted(self.commands.keys())
            else:
                try:
                    if begin == 0:
                        candidates = self.commands.keys()
                    else:
                        first = words[0]
                        candidates = self.commands[first]

                    if being_completed:
                        self.current_candidates = [
                            w for w in candidates if w.startswith(being_completed)
                        ]
                    else:
                        self.current_candidates = candidates




                    nw = []
                    for w in words:
                        try:
                            nw.append(w.split('=')[0] + '=')
                        except:
                            pass
                    self.current_candidates = list(filter(lambda c: not c in nw, self.current_candidates))

                    self.current_candidates = list(filter(lambda c: not c in words, self.current_candidates))

                except (KeyError, IndexError) as err:
                    print('completion error: %s'.format(err))
                    self.current_candidates = []

        try:
            response = self.current_candidates[state]
        except IndexError:
            response = None
        return response

