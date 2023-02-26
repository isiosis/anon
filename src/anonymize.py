#!/usr/bin/env python3

import sys
import os
import json
import argparse


def load_rules(rule_file):
    try:
        with open(rule_file) as data_file:
            try:
                data = json.load(data_file)
                return data
            except json.JSONDecodeError:
                return None
            except IOError:
                return None
    except FileNotFoundError:
        return None


def anonymized_file(resume_file):
    original_dir = os.path.dirname(resume_file)
    original_base = os.path.basename(resume_file)
    anonymized_base = 'anonymized_' + original_base

    return os.path.join(original_dir, anonymized_base)


def apply_rules(rules, resume_file):
    identifiable_resume = None
    anonymized_resume = None
    try:
        identifiable_resume = open(resume_file, 'r')
        anonymized_resume = open(anonymized_file(resume_file), 'w+')

        for line in identifiable_resume:
            anonymized_line = line
            for rule in rules:
                for identifier, anonymizer in rule.items():
                    anonymized_line = anonymized_line.replace(
                        identifier, anonymizer)
            anonymized_resume.write(anonymized_line)

    except OSError as ose:
        print(ose)
        return False

    finally:
        if identifiable_resume is not None:  # would be better to check if it had this method
            identifiable_resume.close()
        if anonymized_resume is not None:
            anonymized_resume.close()

    return True


def verify_args(args):
    for arg in args:
        try:
            f = open(arg, 'r')
            f.close()
        except OSError:
            return False

    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", '--rulesfile', help='the JSON rulesfile to import', default='rules.json')
    parser.add_argument('-i', '--input', nargs='+',
                        help='the names of the resumes to anonymize', dest='inputs', required=True)
    args = parser.parse_args()

    filenames = args.inputs
    if verify_args(filenames) is not True:
        print("one of the arguments is not a valid file")

    rules = load_rules(args.rulesfile)
    if rules is not None:
        print("loaded rules:\n" + json.dumps(rules, indent=4, sort_keys=True))
        for filename in filenames:
            status = apply_rules(rules, filename)
            if status is True:
                print("rules applied; result written to " +
                      anonymized_file(filename))
            else:
                print("some problem occurred while trying to produce " +
                      anonymized_file(filename))
    else:
        print("I could not parse the rules data; is it a real, openable file containing valid JSON?")
        sys.exit(1)


if __name__ == '__main__':
    main()
