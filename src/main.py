from parsers.s3_parser import parse_s3_command
from parsers.ec2_parser import parse_ec2_command

def parse_aws_cli_command(command):
    if command.startswith("aws s3"):
        return parse_s3_command(command)
    elif command.startswith("aws ec2"):
        return parse_ec2_command(command)
    else:
        return "Command not supported yet."

# Example usage
if __name__ == "__main__":
    command_input = "aws s3 ls"
    print(parse_aws_cli_command(command_input))
