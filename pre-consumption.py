#!/usr/bin/env python

import os
import pikepdf


def is_pdf(file_path: str) -> bool:
    return os.path.splitext(file_path.lower())[1] == ".pdf"


def is_pdf_encrypted(file_path: str) -> bool:
    try:
        with pikepdf.open(file_path) as pdf:
            return pdf.is_encrypted
    except:
        return True


def pdf_has_attachments(file_path: str) -> bool:
    try:
        with pikepdf.open(file_path) as pdf:
            return len(pdf.attachments) > 0
    except:
        return False


def decrypt_pdf(in_file_path: str, pass_file_path: str) -> None:
    password = None
    print("Reading passwords from {}".format(pass_file_path))
    with open(pass_file_path, "r") as f:
        passwords = f.readlines()
    for idx, p in enumerate(passwords):
        password = p.strip()
        try:
            with pikepdf.open(in_file_path, password=password, allow_overwriting_input=True) as pdf:
                pdf.save(in_file_path, deterministic_id=True)
                print("{} overwritten. Decrypted with password #{}".format(in_file_path, idx + 1))
                break
        except pikepdf.PasswordError:
            print("Password #{} is not working".format(idx + 1))
            continue
    if password is None:
        print("Empty password file {}".format(pass_file_path))


def extract_pdf_attachments(in_file_path: str, out_path: str) -> None:
    with pikepdf.open(in_file_path) as pdf:
        ats = pdf.attachments
        for atm in ats:
            out_filename = ats.get(atm).filename
            if is_pdf(out_filename):
                out_file_path = os.path.join(out_path, out_filename)
                try:
                    with open(out_file_path, "wb") as wb:
                        wb.write(ats.get(atm).obj["/EF"]["/F"].read_bytes())
                        print("{} extracted from {}".format(out_file_path, in_file_path))
                except:
                    print("Error saving {} from {}".format(out_file_path, in_file_path))
                    continue
            else:
                print("Skipped non-pdf file {}".format(out_filename))


task_id = os.environ.get("TASK_ID")
document_working_path = os.environ.get("DOCUMENT_WORKING_PATH")
passwords_path = "/usr/src/paperless/scripts/passwords.txt"
consume_path = "/usr/src/paperless/consume/"

print("*** STARTING pre-consumption {} ***".format(task_id))
print(" ")

if document_working_path is None:
    print("No working path {}".format(document_working_path))
    exit(0)

if not is_pdf(document_working_path):
    print("{} is not a pdf".format(document_working_path))
    exit(0)

if is_pdf_encrypted(document_working_path):
    print("Decrypting {}".format(document_working_path))
    decrypt_pdf(document_working_path, passwords_path)
else:
    print("Not encrypted {}".format(document_working_path))

if pdf_has_attachments(document_working_path):
    print("Extracting attachments from {}".format(document_working_path))
    extract_pdf_attachments(document_working_path, consume_path)
else:
    print("No attachments in {}".format(document_working_path))

print(" ")
print("=== STOPPING pre-consumption {} ===".format(task_id))
