import string
from typing import Set, Tuple, Dict, List
import numpy as np

class CFG:
    def __init__(self, terminal_symbols: Set[str], nonterminal_symbols: Set[str], productions: List[Tuple[str, List[str]]]):
        self.terminal_symbols = terminal_symbols
        self.nonterminal_symbols = nonterminal_symbols
        self.productions = productions
        self.all_symbols = self.terminal_symbols.union(self.nonterminal_symbols)
        self.validate()

    def validate(self):
        # Check no overlap between terminal and nonterminal symbols
        assert len(self.terminal_symbols.intersection(self.nonterminal_symbols)) == 0, "Terminal and nonterminal symbols must be disjoint"
        # Check that all productions are valid
        for production in self.productions:
            assert production[0] in self.nonterminal_symbols, f"Production {production} has invalid left hand side"
            for symbol in production[1]:
                assert symbol in self.all_symbols, f"Production {production} has invalid right hand side"

    def get_productions_for_symbol(self, symbol: str) -> List[Tuple[str, List[str]]]:
        assert symbol in self.all_symbols, f"Symbol {symbol} is not a valid symbol"
        return [production for production in self.productions if production[0] == symbol]
    
    def generate(self, symbol: str, max_length: int = 100, sampling_strategy: str = "uniform", sampling_params: Dict = {}) -> str:
        assert symbol in self.nonterminal_symbols, f"Symbol {symbol} is not a nonterminal symbol"
        assert sampling_strategy in ["uniform", "weighted"], "Sampling strategy must be either 'uniform' or 'weighted'"
        assert max_length > 0, "Max length must be positive"
        if max_length == 1:
            return symbol
        generated_string = symbol
        current_symbol = symbol
        for _ in range(max_length - 1):
            productions = self.get_productions_for_symbol(current_symbol)
            if len(productions) == 0:
                break
            if sampling_strategy == "uniform":
                production_idx = np.random.choice(list(range(len(productions))))
                production = productions[production_idx]
                possible_outputs = production[1]
                sampled_output = np.random.choice(possible_outputs)
            generated_string += " " + " ".join(sampled_output)
            current_symbol = sampled_output
            if current_symbol in self.terminal_symbols:
                break
        return generated_string

    def __str__(self):
        return f"CFG({self.terminal_symbols}, {self.nonterminal_symbols}, {self.productions})"
    
    def __repr__(self):
        return str(self)
    
    def __eq__(self, other):
        return self.terminal_symbols == other.terminal_symbols and self.nonterminal_symbols == other.nonterminal_symbols and self.productions == other.productions
    
    def __hash__(self):
        return hash((self.terminal_symbols, self.nonterminal_symbols, self.productions))
    
    def is_terminal(self, symbol: str) -> bool:
        return symbol in self.terminal_symbols
    
    def is_nonterminal(self, symbol: str) -> bool:
        return symbol in self.nonterminal_symbols
    
    def is_valid_production(self, production: Tuple[str, str]) -> bool:
        return production in self.productions
    
    def is_valid_string(self, string: str) -> bool:
        # Check that all symbols are valid
        for symbol in string.split():
            if symbol not in self.all_symbols:
                return False
        # Check that all productions are valid
        for i in range(len(string.split()) - 1):
            if not self.is_valid_production((string.split()[i], string.split()[i + 1])):
                return False
        return True

if __name__ == "__main__":
    production_rules = []
    all_ascii_characters = list(string.ascii_lowercase + string.ascii_uppercase)
    all_ascii_characters_without_a = all_ascii_characters.copy()
    all_ascii_characters_without_a.remove("a")
    for char in all_ascii_characters_without_a:
        production_rules.append((char, list(all_ascii_characters)))
    CFG = CFG(
        set('a'),
        set(all_ascii_characters_without_a),
        production_rules
    )
    print(CFG.generate("S", max_length=10))
    

    