import re



def process_rhs(rhs: str):
    pass

def parse_line(line: str):
    production_rule = r'([^=]+)\s*=\s*([^;]+);'
    lhs, pre_processed_rhs = re.match(production_rule, line).groups()




