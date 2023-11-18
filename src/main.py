#!/usr/bin/env python3
import sys
import os
import argparse
from parsers.s3_parser import parse_s3_command
from parsers.ec2_parser import parse_ec2_command

def parse_aws_cli_command(command, language):
    if language == "py" or language == "python":
        if command.startswith("aws s3"):
            return parse_s3_command(command)
        elif command.startswith("aws ec2"):
            return parse_ec2_command(command)
        else:
            return "Command not supported yet."
    else:
        return f"Language '{language}' not supported yet."

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Claudr: AWS CLI to Code Translator')
    parser.add_argument('language', nargs='?', default=os.getenv('CLAUDR_DEFAULT_LANGUAGE', 'python'))
    parser.add_argument('command', nargs='+')
    args = parser.parse_args()

    command_input = " ".join(args.command)
    print(parse_aws_cli_command(command_input, args.language))