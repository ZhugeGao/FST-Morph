# !/usr/bin/python3
import sys


class FST:
    """ A class representing finite state transducer.
    """

    def __init__(self, att_file=None):
        self._reset()
        if att_file:
            self.read_att(att_file)

    def _reset(self):
        self.transitions = dict()
        self.start_state = None
        self.accepting = set()
        self._input_alphabet = set()
        self._output_alphabet = set()

    def read_att(self, filename):
        """
        Read an FST from a AT&T-formatted text file. The file column number should be either one or four.

        """
        with open(filename, 'rt') as att_file:
            for index, line in enumerate(att_file):
                line = line.strip().split()
                length = len(line)
                # don't know if the format part would work...
                assert (length == 4 or length == 1), "Incorrect number of columns at line {}!".format(index + 1)
                if index == 0:  # first line
                    self.start_state = line[0]
                # for line with only one column
                if length == 1:  # add accepting states
                    self.accepting.add(line[0])
                    continue
                # for other column
                source_state = line[0]
                input_symbol = line[2]

                target_state = line[1]
                output_symbol = line[3]

                transition_key = (source_state, input_symbol)
                # maybe I need to give a vatiable name for the target_state output_symbol tuple

                if transition_key in self.transitions.keys():
                    self.transitions[transition_key].append((target_state, output_symbol))
                    self._output_alphabet.add(output_symbol)
                else:
                    self.transitions[transition_key] = list()
                    self.transitions[transition_key].append((target_state, output_symbol))
                    self._input_alphabet.add(input_symbol)
                    self._output_alphabet.add(output_symbol)

    def transduce(self, s):
        """ Return a list of outputs for the given input 's'.
        """
        assert(s), "Empty input string!"#didn't do a empty string check

        symbol_list = list(s)
        token_list = list()
        while symbol_list:
            input_symbol = symbol_list[0]
            if input_symbol == "<" or input_symbol == "@":
                multi_symbol = input_symbol
                next_index = 1
                stop_symbol = self._get_stop_symbol(input_symbol)
                while next_index in range(len(symbol_list)):  # what if out of range and next symbol not found?
                    multi_symbol += symbol_list[next_index]
                    if symbol_list[next_index] != stop_symbol:
                        next_index += 1
                    else:
                        break
                token_list.append(multi_symbol)
                symbol_list = symbol_list[len(multi_symbol):]
            else:
                token_list.append(input_symbol)
                symbol_list = symbol_list[1:]

        input_length = len(token_list)

        agenda = list()
        token_readed = 0
        current_state = self.start_state
        current_output = ""
        agenda.append((token_readed, current_state, current_output))

        output_list = list()

        while agenda:
            token_readed, current_state, current_output = agenda.pop()
            if (current_state, "@0@") in self.transitions.keys():
                for next_transduction in self.transitions[(current_state, "@0@")]:
                    next_state = next_transduction[0]
                    next_output = next_transduction[1]
                    agenda.append((token_readed, next_state, current_output + next_output))

            if token_readed < input_length:
                if (current_state, token_list[token_readed]) in self.transitions.keys():
                    for next_transduction in self.transitions[
                        (current_state, token_list[token_readed])]:
                        next_state = next_transduction[0]
                        next_output = next_transduction[1]
                        agenda.append((token_readed + 1, next_state, current_output + next_output))
            elif token_readed == input_length:

                if current_state in self.accepting:
                    # here transform eplisilon into empty string
                    current_output = current_output.replace("@0@", "")
                    output_list.append(current_output)

        return output_list

    def _get_stop_symbol(self, input_symbol):
        # if input is < we use >
        # if input is @ we use @
        if input_symbol == "<":
            return ">"
        elif input_symbol == "@":
            return "@"

    def invert(self):
        """ Invert the FST.
        """
        transitions_copy = self.transitions.copy()
        self.transitions.clear()#should have kept this, instead of use a temp_dict
        for i, (source_input, target_output) in enumerate(transitions_copy.items()):
            source = source_input[0]
            new_output = source_input[1]
            for transition in target_output:
                new_input = transition[1]
                invert_key = (source, new_input)

                target = transition[0]#access the wrong thing in the last attempt
                invert_transition = (target, new_output)
                if invert_key in self.transitions.keys():
                    if invert_transition not in self.transitions[invert_key]:
                        self.transitions[invert_key].append(invert_transition)
                else:
                    self.transitions[invert_key] = list()
                    self.transitions[invert_key].append(invert_transition)


if __name__ == '__main__':
    action = sys.argv[0]
    fst_file = sys.argv[1]
    input_file = sys.argv[2]
    fst = FST()
    fst.read_att(fst_file)

    with open(input_file, 'rt') as f:
        for line in f:
            if action == "analyze":
                fst.invert()
                print(fst.transduce(line.strip()))
            if action == "generate":
                print(fst.transduce(line.strip()))


